"""
Passo 10 — Pipeline de Carga
Lê o CSV do Oscar AMPAS e popula o banco PostgreSQL.

Ordem de inserção:
  1. edicao, categoria, filme, vencedor  (tabelas de domínio, sem FKs)
  2. premio                              (tabela central, com FKs)

Executar no terminal:
  python 02_carga_dados.py
"""

from pathlib import Path
import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary", "pandas", "-q"])

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


US_STATES = {
    'Al', 'Ak', 'Az', 'Ar', 'Ca', 'Co', 'Ct', 'De', 'Fl', 'Ga',
    'Hi', 'Id', 'Il', 'In', 'Ia', 'Ks', 'Ky', 'La', 'Me', 'Md',
    'Ma', 'Mi', 'Mn', 'Ms', 'Mo', 'Mt', 'Ne', 'Nv', 'Nh', 'Nj',
    'Nm', 'Ny', 'Nc', 'Nd', 'Oh', 'Ok', 'Or', 'Pa', 'Ri', 'Sc',
    'Sd', 'Tn', 'Tx', 'Ut', 'Vt', 'Va', 'Wa', 'Wv', 'Wi', 'Wy',
    'Dc'
}


# =============================================================
# Configuração
# =============================================================

CSV_PATH = Path('world_ampas_oscar_winner_demographics.csv')

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


def extrair_pais(birthplace: str):
    if not isinstance(birthplace, str):
        return None
    partes = [p.strip() for p in birthplace.split(',')]
    if len(partes) == 1:
        return 'United States'
    elif len(partes) == 2:
        if partes[-1] in US_STATES:
            return 'United States'
        else:
            return partes[-1]
    else:
        return partes[-1]


# =============================================================
# Leitura e limpeza do CSV
# =============================================================

print("Lendo CSV...")
df = pd.read_csv(CSV_PATH)

# Tratar "Na" em sexual_orientation como None
df['sexual_orientation'] = df['sexual_orientation'].replace('Na', None)

# Atomizar CEP
print(df.columns)
df['pais'] = df['birthplace'].apply(extrair_pais)

# Valores únicos
filmes = df['movie'].dropna().unique()
paises = df['pais'].dropna().unique()
anos = sorted(df['year_edition'].unique())
categorias = df['category'].dropna().unique()
etnias = df['race_ethnicity'].dropna().unique()
orientacoes_sexuais = df['sexual_orientation'].dropna().unique()
religioes = df['religion'].dropna().unique()
vencedores = df.drop_duplicates(subset='name')[
    ['name', 'birth_year', 'birth_date', 'pais',
        'race_ethnicity', 'religion', 'sexual_orientation']
]

print(f"  {len(df)} linhas carregadas")

# =============================================================
# Conexão
# =============================================================

conn = psycopg2.connect(**DB)
cur  = conn.cursor()
print("Conectado ao PostgreSQL (banco: oscar)\n")

try:
    with conn:
        # ---------------------------------------------------------
        # 1. edicao
        # ---------------------------------------------------------

        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO edicao (ano) VALUES %s ON CONFLICT DO NOTHING",
                [(int(a),) for a in anos]
            )

            cur.execute("SELECT ano, id_edicao FROM edicao")
            edicao_id = {row[0]: row[1] for row in cur.fetchall()}
            print(f"edicao    : {len(edicao_id)} registros")

        # ---------------------------------------------------------
        # 2. categoria
        # ---------------------------------------------------------
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO categoria (nome) VALUES %s ON CONFLICT DO NOTHING",
                [(str(c),) for c in categorias]
            )

            cur.execute("SELECT nome, id_categoria FROM categoria")
            categoria_id = {row[0]: row[1] for row in cur.fetchall()}
            print(f"categoria : {len(categoria_id)} registros")

        # ---------------------------------------------------------
        # 3. filme
        # ---------------------------------------------------------
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO filme (titulo) VALUES %s ON CONFLICT DO NOTHING",
                [(str(f),) for f in filmes]
            )

            cur.execute("SELECT titulo, id_filme FROM filme")
            filme_id = {row[0]: row[1] for row in cur.fetchall()}
            print(f"filme     : {len(filme_id)} registros")

        # Etnias
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO etnia (nome_etnia) VALUES %s ON CONFLICT DO NOTHING",
                [(str(e),) for e in etnias]
            )

            cur.execute("SELECT nome_etnia FROM etnia")
            count = len(cur.fetchall())
            print(f"etnia     : {count} registros")

        # Países
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO pais (nome_pais) VALUES %s ON CONFLICT DO NOTHING",
                [(str(p),) for p in paises]
            )

            cur.execute("SELECT nome_pais FROM pais")
            count = len(cur.fetchall())
            print(f"pais     : {count} registros")

        # Orientações sexuais
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO orient_sexual (nome_orient_sexual) VALUES %s ON CONFLICT DO NOTHING",
                [(str(o),) for o in orientacoes_sexuais]
            )

            cur.execute("SELECT nome_orient_sexual FROM orient_sexual")
            count = len(cur.fetchall())
            print(f"orient_sexual     : {count} registros")

        # Religiões
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO religiao (nome_religiao) VALUES %s ON CONFLICT DO NOTHING",
                [(str(r),) for r in religioes]
            )

            cur.execute("SELECT nome_religiao FROM religiao")
            count = len(cur.fetchall())
            print(f"religiao     : {count} registros")

        # ---------------------------------------------------------
        # 4. vencedor  (deduplicado por nome)
        # ---------------------------------------------------------

        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO vencedor (nome, ano_nascimento, pais_nascimento, nome_etnia, nome_religiao, nome_orient_sexual)
                VALUES %s ON CONFLICT DO NOTHING
                """,
                [
                    (
                        row['name'],
                        nulo(row['birth_year']),
                        nulo(row['pais']),
                        row['race_ethnicity'],
                        nulo(row['religion']),
                        nulo(row['sexual_orientation']),
                    )
                    for _, row in vencedores.iterrows()
                ]
            )

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

        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO premio (id_vencedor, id_filme, id_categoria, id_edicao)
                VALUES %s
                """,
                linhas
            )
            print(f"premio    : {len(linhas)} registros\n")

        print("Carga concluida com sucesso!")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    raise e

finally:
    conn.close()
