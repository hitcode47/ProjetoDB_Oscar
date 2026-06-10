"""
Passo 10 — Pipeline de Carga
Lê o CSV do Oscar AMPAS e popula o banco PostgreSQL.

Ordem de inserção:
  1. edicao, categoria, filme, vencedor  (tabelas de domínio, sem FKs)
  2. premio                              (tabela central, com FKs)

Executar no terminal:
  python 02_carga_dados.py
"""

import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary", "pandas", "-q"])

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# =============================================================
# Configuração
# =============================================================

CSV_PATH = r'C:\Users\bruno\OneDrive\Área de Trabalho\Projetos\projetoFinalDB\world_ampas_oscar_winner_demographics.csv'

DB = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "oscar",
    "user":     "postgres",
    "password": "brasil123",
}

# =============================================================
# Utilitário
# =============================================================

def nulo(val):
    """Converte NaN/NaT do pandas para None (NULL no banco)."""
    try:
        if pd.isna(val):
            return None
    except (TypeError, ValueError):
        pass
    return val

# =============================================================
# Leitura e limpeza do CSV
# =============================================================

print("Lendo CSV...")
df = pd.read_csv(CSV_PATH)

# Tratar "Na" em sexual_orientation como None
df['sexual_orientation'] = df['sexual_orientation'].replace('Na', None)

# Converter birth_date para datetime
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')

print(f"  {len(df)} linhas carregadas")

# =============================================================
# Conexão
# =============================================================

conn = psycopg2.connect(**DB)
cur  = conn.cursor()
print("Conectado ao PostgreSQL (banco: oscar)\n")

try:
    # ---------------------------------------------------------
    # 1. edicao
    # ---------------------------------------------------------
    anos = sorted(df['year_edition'].unique())
    execute_values(
        cur,
        "INSERT INTO edicao (ano) VALUES %s ON CONFLICT DO NOTHING",
        [(int(a),) for a in anos]
    )
    conn.commit()

    cur.execute("SELECT ano, id_edicao FROM edicao")
    edicao_id = {row[0]: row[1] for row in cur.fetchall()}
    print(f"edicao    : {len(edicao_id)} registros")

    # ---------------------------------------------------------
    # 2. categoria
    # ---------------------------------------------------------
    categorias = df['category'].dropna().unique()
    execute_values(
        cur,
        "INSERT INTO categoria (nome) VALUES %s ON CONFLICT DO NOTHING",
        [(str(c),) for c in categorias]
    )
    conn.commit()

    cur.execute("SELECT nome, id_categoria FROM categoria")
    categoria_id = {row[0]: row[1] for row in cur.fetchall()}
    print(f"categoria : {len(categoria_id)} registros")

    # ---------------------------------------------------------
    # 3. filme
    # ---------------------------------------------------------
    filmes = df['movie'].dropna().unique()
    execute_values(
        cur,
        "INSERT INTO filme (titulo) VALUES %s ON CONFLICT DO NOTHING",
        [(str(f),) for f in filmes]
    )
    conn.commit()

    cur.execute("SELECT titulo, id_filme FROM filme")
    filme_id = {row[0]: row[1] for row in cur.fetchall()}
    print(f"filme     : {len(filme_id)} registros")

    # ---------------------------------------------------------
    # 4. vencedor  (deduplicado por nome)
    # ---------------------------------------------------------
    vencedores = df.drop_duplicates(subset='name')[
        ['name', 'birth_year', 'birth_date', 'birthplace', 'race_ethnicity', 'religion', 'sexual_orientation']
    ]

    execute_values(
        cur,
        """
        INSERT INTO vencedor (nome, ano_nascimento, data_nascimento, local_nascimento, etnia, religiao, orient_sexual)
        VALUES %s ON CONFLICT DO NOTHING
        """,
        [
            (
                row['name'],
                nulo(row['birth_year']),
                nulo(row['birth_date']),
                nulo(row['birthplace']),
                row['race_ethnicity'],
                nulo(row['religion']),
                nulo(row['sexual_orientation']),
            )
            for _, row in vencedores.iterrows()
        ]
    )
    conn.commit()

    cur.execute("SELECT nome, id_vencedor FROM vencedor")
    vencedor_id = {row[0]: row[1] for row in cur.fetchall()}
    print(f"vencedor  : {len(vencedor_id)} registros")

    # ---------------------------------------------------------
    # 5. premio
    # ---------------------------------------------------------
    print("\nMontando linhas de premio...")
    linhas = []
    for _, r in df.iterrows():
        linhas.append((
            vencedor_id[r['name']],
            filme_id[r['movie']],
            categoria_id[r['category']],
            edicao_id[int(r['year_edition'])],
        ))

    execute_values(
        cur,
        """
        INSERT INTO premio (id_vencedor, id_filme, id_categoria, id_edicao)
        VALUES %s
        """,
        linhas
    )
    conn.commit()
    print(f"premio    : {len(linhas)} registros\n")

    print("Carga concluida com sucesso!")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    raise

finally:
    cur.close()
    conn.close()
