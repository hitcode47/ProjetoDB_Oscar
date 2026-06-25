"""
Setup do banco — Oscar AMPAS
Executa uma única vez após subir o container com:  docker compose up -d

  python setup.py

Pré-requisitos:
  - Docker Desktop instalado e rodando
  - Python 3 com pip
"""

from pathlib import Path
import psycopg2
import sys
import time

# ── Caminhos ─────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
DDL = ROOT / "01_ddl_criar_tabelas.sql"

DB = dict(host="localhost", port=5432, dbname="oscar",
          user="postgres", password="brasil123")

# ── Aguarda o PostgreSQL inicializar ─────────────────────────────────
print("Aguardando PostgreSQL inicializar", end="", flush=True)
for _ in range(30):
    try:
        conn = psycopg2.connect(**DB)
        conn.close()
        print(" OK")
        break
    except psycopg2.OperationalError:
        print(".", end="", flush=True)
        time.sleep(2)
else:
    print("\nERRO: PostgreSQL não respondeu em 60 s.")
    print("Verifique se o container está rodando:  docker compose up -d")
    sys.exit(1)

# ── DDL ──────────────────────────────────────────────────────────────
print("\nCriando tabelas...")
conn = psycopg2.connect(**DB)
cur = conn.cursor()
cur.execute(DDL.read_text(encoding="utf-8"))
conn.commit()
cur.close()
conn.close()
print("      Tabelas criadas.")

print("\nSetup concluído! Banco oscar pronto para uso.")
