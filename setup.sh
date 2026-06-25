python -m venv .venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
docker-compose up -d
python Documentacao/Etapa3_SQL/02_ddl_setup.py
python Documentacao/Etapa3_SQL/03_carga_dados.py
