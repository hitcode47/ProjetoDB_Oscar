# Projeto de Banco de Dados - Normalização e Análise Exploratória de Dados do Oscar

## Setup inicial

É preciso ter o [Docker](https://docs.docker.com/get-started/get-docker/) instalado. O projeto foi rodado com [Python](https://www.python.org/downloads/) na versão 3.14. Além disso, é necessário o [Jupyter](https://jupyter.org/install) para rodar os relatórios de análise de dados.

### Ambiente virtual (opcional)

É fortemente recomendado criar um ambiente virtual para rodar o projeto:

```bash
python -m venv .venv/
source .venv/bin/activate     # se você estiver no Linux/Max; ou
source .venv/Scripts/activate # no windows
```

### Dependências Python

Depois, instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### PostgreSQL

Por fim, habilite o container do PostgreSQL com o Docker. Certifique-se de que o Docker está rodando.

```bash
docker-compose up -d
```

## DDL

Para criar as tabelas no banco, a partir da raiz do projeto, rode:

```bash
python Documentacao/Etapa3_SQL/02_ddl_setup.py
```

## Populando o banco

Para popular as tabelas, rode

```bash
python Documentacao/Etapa3_SQL/03_carga_dados.py
```

Com isso, o banco está pronto para análise exploratória.

## Análise exploratória de dados (EDA)

Se ainda não o tiver feito, inicie o jupyter notebook 
```bash
jupyter notebook
```

Depois, abra o notebook localizado em `Etapa04_EDA/06_visualizacoes.ipynb` para ver e executar os resultados e os gráficos obtidos.
