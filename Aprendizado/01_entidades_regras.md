# Entidades, Relacionamentos e Regras de Integridade

## Dataset
Oscar AMPAS — Winner Demographics (1927–2014)
415 linhas, 10 colunas

## Entidades identificadas

| Entidade | Atributos principais | Origem no CSV |
|---|---|---|
| VENCEDOR | id (PK), nome, ano_nascimento, data_nascimento, local_nascimento, etnia, religiao, orient_sexual | name, birth_year, birth_date, birthplace, race_ethnicity, religion, sexual_orientation |
| FILME | id (PK), titulo | movie |
| CATEGORIA | id (PK), nome | category |
| EDICAO | id (PK), ano | year_edition |
| PREMIO | id (PK), id_vencedor FK, id_filme FK, id_categoria FK, id_edicao FK | linha inteira |

## Decisões de modelagem

- **birthplace como texto livre:** cidade, estado e país aparecem misturados sem padrão. Separar causaria mais ruído do que valor — fica como varchar em VENCEDOR.
- **CATEGORIA como tabela própria:** apenas 5 valores fixos, mas criar tabela garante integridade referencial e evita erros de digitação.
- **religion e orient_sexual nullable:** religion tem 62% de ausência estrutural (dado não coletado para todos). orient_sexual tinha string "Na" — tratada como NULL na carga.
- **PREMIO como entidade central:** resolve a relação entre as 4 dimensões. Cada linha do CSV é exatamente um PREMIO.

## Relacionamentos

- PREMIO pertence a VENCEDOR (N:1) — um vencedor pode ter vários prêmios
- PREMIO é para FILME (N:1) — um filme pode receber vários prêmios
- PREMIO pertence a CATEGORIA (N:1) — uma categoria tem um vencedor por edição
- PREMIO pertence a EDICAO (N:1) — uma edição entrega 5 prêmios

## Regras de integridade

| Regra | Tipo | Descrição |
|---|---|---|
| PKs únicas e não nulas | Chave | Toda tabela |
| FKs referenciam registros existentes | Referencial | Toda FK em PREMIO |
| nome NOT NULL em todas as tabelas | Entidade | Identificador textual obrigatório |
| ano ≥ 1927 em EDICAO | Domínio | Início do Oscar |
| (id_vencedor, id_categoria, id_edicao) únicos | Negócio | Uma pessoa não ganha a mesma categoria duas vezes na mesma edição |

## Conceitos aplicados

- **Entidade associativa (PREMIO):** entidade que resolve uma relação complexa entre 4 outras entidades, carregando as FKs como atributos
- **Tabela de domínio (CATEGORIA):** tabela com valores fixos que funciona como enum controlado pelo banco
- **NULL estrutural:** ausência de dado por limitação histórica de coleta, não por erro
