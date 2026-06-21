---
output:
  html_document: default
  pdf_document: default
---
# Relatório — Projeto Final de Banco de Dados
**Disciplina:** Banco de Dados — DCC/UFMG  
**Professor:** Pedro H. Barros  
**Dataset:** Oscar AMPAS — Winner Demographics (1927–2014)

---

## 1. Introdução

Este projeto implementa o ciclo completo de um banco de dados relacional sobre os vencedores do Oscar (Academy Awards), premiação anual da Academia de Artes e Ciências Cinematográficas dos Estados Unidos (AMPAS). O dataset contém informações demográficas de vencedores de cinco categorias principais entre 1927 e 2014, permitindo análises sobre representatividade étnica, longevidade de carreira e domínio artístico ao longo de quase nove décadas de cinema.

As etapas de um projeto de banco de dados desenvolvidas partem do projeto conceitual Entidade-Relacionamento, que é depois convertido num modelo Relacional e testado sobre as premissas das 3 formas normais. Os modelos projetados são então implementados em SQL por meio da Data Definition language (DDL) e a base de dados resultante é populada com o arquivo csv. Antes de se executar as análises e consultas SQL, um tratamento é feito, seguido da análise exploratópria dos dados.

### Motivação
O Oscar é a premiação cinematográfica mais influente do mundo. Analisar o perfil dos vencedores ao longo do tempo revela padrões históricos de diversidade — ou ausência dela — na indústria do cinema.

---

## 2. Dataset

A base de dados utilizada, "World Oscar AMPAS winner demographics", contém dados a respeito das categorias: Melhor Atriz, Melhor Ator, Melhor Diretor, Melhor Ator Coadjuvante, Melhor Atriz Coadjuvante, para as edições da premiação que ocorreram entre 1927 e 2014. Os atributos do dataset e a relação das variáveis presentes está mostrada na tabela a seguir:

| Atributo | Valor |
|---|---|
| Fonte | FiveThirtyEight / AMPAS |
| Arquivo | `world_ampas_oscar_winner_demographics.csv` |
| Linhas | 415 |
| Colunas | 10 |
| Período | 1927 a 2014 |

### Colunas originais

| Coluna | Tipo | Descrição |
|---|---|---|
| name | texto | Nome do vencedor |
| birth_year | inteiro | Ano de nascimento |
| birth_date | data | Data de nascimento |
| birthplace | texto | Local de nascimento (texto livre) |
| race_ethnicity | texto | Etnia (6 valores: White, Black, Hispanic, Asian, Multiracial, Middle Eastern) |
| religion | texto | Religião — 62% ausente |
| sexual_orientation | texto | Orientação sexual — "Na" tratado como NULL |
| year_edition | inteiro | Ano da cerimônia |
| category | texto | Categoria do Oscar (5 categorias: Melhor Atriz, Melhor Ator, Melhor Diretor, Melhor Ator Coadjuvante, Melhor Atriz Coadjuvante) |
| movie | texto | Filme premiado |

### Tratamento de dados ausentes
Foram realizadas os seguintes tratamentos na base original importada:

- `religion`: 62% de ausência estrutural — dado não coletado para todos os vencedores históricos. Tratado como `NULL`.
- `sexual_orientation`: string `"Na"` convertida para `NULL` na carga.
- `birth_date`: 1 registro ausente; `birth_year` mantido para não perder informação.

---

## 3. Modelo Entidade-Relacionamento

### Entidades

| Entidade | Atributos | Chave |
|---|---|---|
| VENCEDOR | nome, ano_nascimento, data_nascimento, local_nascimento, etnia, religiao, orient_sexual | id_vencedor |
| FILME | titulo | id_filme |
| CATEGORIA | nome | id_categoria |
| EDICAO | ano | id_edicao |
| PREMIO | id_vencedor, id_filme, id_categoria, id_edicao | id_premio |

### Relacionamentos

O projeto para o banco de dados considerou a criação de `PREMIO`, que é uma **entidade associativa** que conecta as quatro demais entidades. `PREMIO` permite que VENCEDOR, FILME, EDICAO e CATEGORIA se relacionem diretamente, de forma que caracterizem uma entrada na base de dados, ou seja, cada `PREMIO` corresponde a uma das categorias do Oscar em determinada edição, da qual houve um vencedor por causa de determinado filme.

Nessa estruturação, é obrigatório que cada uma dessas 4 entidades possuam uma respectiva entrada nas demais 3 que se associem a ela, caracterizando uma participação total. A entidade associativa caracteriza um relacionamento M:N.


### Diagrama ER

O diagrama a seguir representa o esquemático da modelagem apresentada anteriormente, com as entidades, relacionamentos representados pela notação clássica.

![](Etapa1_ModeloER/OSCAR_ER.png)


### Restrições de integridade de domínio

**VENCEDOR**

`id_vencedor` (Chave):
- Tipo: Numérico Inteiro (ex: INT).
- Restrição: Único, NOT NULL

`nome`:
- Tipo: Texto.
- Restrição: NOT NULL.

`ano_nascimento`:
- Tipo: Numérico Inteiro.
- Restrição: Positivo, pode aceitar nulos (NULL).

`data_nascimento`:
- Tipo: Data.
- Restrição: Formato padrão de data (YYYY-MM-DD). Pode aceitar nulos (NULL).

`local_nascimento`:
- Tipo: Texto.
- Restrição: Texto livre, pode aceitar nulos (NULL).

`etnia`:
- Tipo: Texto.
- Restrição: Pode aceitar nulos (NULL).

`religiao`:
- Tipo: Texto.
- Restrição: Pode aceitar nulos (NULL).

`orient_sexual`:
- Tipo: Texto.
- Restrição: Aceita nulos (NULL). Valores identificados como "Na" no sistema de origem devem ser convertidos e tratados formalmente como NULL no banco de dados.

**FILME**

`id_filme` (Chave):
- Tipo: Numérico Inteiro.
- Restrição: Único, NOT NULL.

`titulo`:
- Tipo: Texto.

**CATEGORIA**

`id_categoria` (Chave):
- Tipo: Numérico Inteiro.
- Restrição: Único, NOT NULL.

`nome`:
- Tipo: Texto.
- Restrição: NOT NULL.

**EDICAO**

`id_edicao` (Chave):
- Tipo: Numérico Inteiro.
- Restrição: Único, NOT NULL.

`ano`:
- Tipo: Numérico Inteiro.
- Restrição: O ano deve ser maior ou igual a 1927 (ano inicial da premiação no dataset).

**PREMIO**

`id_premio` (Chave):
- Tipo: Numérico Inteiro.
- Restrição: Único, NOT NULL.

`id_vencedor`:
- Tipo: Numérico Inteiro.

`id_filme`:
- Tipo: Numérico Inteiro.

`id_categoria`:
- Tipo: Numérico Inteiro.

`id_edicao`:
- Tipo: Numérico Inteiro.

---

## 4. Modelo Relacional

A modelagem Entidade-Relacionamento anterior permitiu uma abordagem bem direta para a modelagem Relacional, cada entidade se tornou 1 tabela relação, a entidade associativa formou uma tabela associativa da relação M:N, constituindo-se das chaves primárias de cada uma das outras relações como chaves estrangeiras.

```
vencedor(id_vencedor PK, nome, ano_nascimento, data_nascimento,
         local_nascimento, etnia, religiao, orient_sexual)

filme(id_filme PK, titulo)

categoria(id_categoria PK, nome)

edicao(id_edicao PK, ano)

premio(id_premio PK,
       id_vencedor FK → vencedor,
       id_filme    FK → filme,
       id_categoria FK → categoria,
       id_edicao   FK → edicao)
```

### Normalização

**1FN:** todos os valores são atômicos. `local_nascimento` é texto livre, mas atômico por linha.

**2FN:** todas as tabelas têm chave primária simples — dependências parciais são impossíveis.

**3FN:** único caso analisado foi `ano_nascimento` vs `data_nascimento` em VENCEDOR. Optou-se por manter ambos pois há 1 registro com `birth_year` mas sem `birth_date` completa — eliminar a coluna causaria perda real de informação. Não há dependências transitivas nas demais tabelas.

---

## 5. Implementação Física

A carga dos dados do csv foi feita em script python, enquanto a definição das tabelas do esquema relacional (DDL) e a validação dos dados e  foi feita em SQL.

### Banco de dados
- **SGBD:** PostgreSQL 16 (via Docker)
- **Container:** `oscar-db`
- **Banco:** `oscar`

### Constraints implementadas

| Constraint | Tipo | Tabela |
|---|---|---|
| `id_*` únicos e não nulos | Chave primária | Todas |
| `nome` NOT NULL | Entidade | vencedor, filme, categoria |
| `ano >= 1927` | Domínio | edicao |
| FKs referenciam registros existentes | Referencial | premio |
| `(id_vencedor, id_categoria, id_edicao)` único | Negócio | premio |

### Índices criados
```sql
CREATE INDEX idx_premio_vencedor  ON premio(id_vencedor);
CREATE INDEX idx_premio_filme     ON premio(id_filme);
CREATE INDEX idx_premio_categoria ON premio(id_categoria);
CREATE INDEX idx_premio_edicao    ON premio(id_edicao);
```

---

## 6. Carga dos Dados

Pipeline em Python (`Etapa3_SQL/02_carga_dados.py`) usando `psycopg2`.

**Ordem de inserção:**
1. `edicao` — 87 cerimônias
2. `categoria` — 5 categorias
3. `filme` — 335 títulos únicos
4. `vencedor` — 348 pessoas únicas (deduplicadas por nome)
5. `premio` — 415 registros (um por linha do CSV)

**Validação pós-carga:**
- Zero registros órfãos em todas as FKs
- Nenhuma duplicata na constraint `uq_premio`
- NULLs distribuídos como esperado (`religion`: 219, `orient_sexual`: 10)

---

## 7. Análise Exploratória

### P1 — Filmes com múltiplas vitórias na mesma edição
*It Happened One Night* (1935), *Gone with the Wind* (1940) e *Going My Way* (1945) foram os únicos a vencer 3 categorias em uma mesma cerimônia. 60 filmes no total venceram 2 ou mais categorias.

### P2 — Diversidade étnica por década
Até os anos 1970, a proporção de vencedores não-brancos foi praticamente zero. A partir dos anos 2000, subiu para cerca de 19%, ainda longe de representar a diversidade da população americana.

### P3 — Idade dos vencedores
Atrizes vencem mais jovens (média 37 anos) enquanto atores coadjuvantes vencem mais velhos (média 51). A mais jovem foi Tatum O'Neal com 11 anos (1974); o mais velho foi Christopher Plummer com 83 anos (2012).

### P4 — Intervalo entre vitórias
Helen Hayes esperou 39 anos entre seu primeiro (1932) e segundo Oscar (1971), o maior intervalo registrado. Katharine Hepburn também esperou 34 anos (1934–1968).

### P5 — Primeira vitória não-branca por categoria
| Categoria | Vencedor | Etnia | Ano |
|---|---|---|---|
| Best Supporting Actress | Hattie McDaniel | Black | 1940 |
| Best Actor | Jose Ferrer | Hispanic | 1951 |
| Best Supporting Actor | Anthony Quinn | Hispanic | 1953 |
| Best Actress | Halle Berry | Multiracial | 2002 |
| Best Director | Ang Lee | Asian | 2006 |

---

## 8. Conclusão

O projeto implementou com sucesso todas as etapas do ciclo de vida de um banco de dados relacional: modelagem ER, mapeamento relacional, normalização até 3FN, implementação DDL com restrições de integridade, pipeline de carga e análise exploratória via SQL e visualizações.

Os dados revelam que a Academia de Artes e Ciências Cinematográficas demorou décadas para reconhecer artistas não-brancos, com a primeira vitória não-branca em Best Director ocorrendo apenas em 2006 — quase 80 anos após a primeira cerimônia.

---

## Arquivos do Projeto

```
Documentacao/
├── Etapa0_Exploracao/01_exploracao.ipynb
├── Etapa1_ModeloER/diagrama_er.dbml
├── Etapa3_SQL/
│   ├── 01_ddl_criar_tabelas.sql
│   ├── 02_carga_dados.py
│   └── 03_validacao_carga.sql
└── Etapa4_EDA/
    ├── 04_perguntas_investigativas.md
    ├── 05_consultas_sql.sql
    └── 06_visualizacoes.ipynb

Aprendizado/
├── 00_rota_do_projeto.md
├── 01_entidades_regras.md
└── 02_modelo_relacional_normalizacao.md
```
