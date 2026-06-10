# Modelo Relacional e Normalização

## Mapeamento ER → Relacional

| Regra | Aplicação no projeto |
|---|---|
| Entidade → Tabela | vencedor, filme, categoria, edicao, premio |
| Atributo → Coluna com tipo | id_*, nome, ano, data, varchar, etc. |
| Chave primária → PK | id_* em cada tabela |
| Relacionamento 1:N → FK | id_vencedor, id_filme, id_categoria, id_edicao em premio |
| Entidade associativa → Tabela com múltiplas FKs | premio centraliza os 4 relacionamentos |

## Esquema Relacional Final

```
vencedor(
  id_vencedor PK,
  nome,
  ano_nascimento,
  data_nascimento,     -- nullable (1 ausente)
  local_nascimento,    -- texto livre
  etnia,
  religiao,            -- nullable (62% ausente)
  orient_sexual        -- nullable ("Na" tratado como NULL)
)

filme(id_filme PK, titulo)

categoria(id_categoria PK, nome)

edicao(id_edicao PK, ano)

premio(
  id_premio PK,
  id_vencedor FK → vencedor,
  id_filme    FK → filme,
  id_categoria FK → categoria,
  id_edicao   FK → edicao
)
```

## Normalização

### 1FN — Primeira Forma Normal ✅
Cada coluna contém um único valor atômico. Não há listas nem grupos repetidos.
`local_nascimento` é texto livre mas é um valor único por linha — não viola 1FN.

### 2FN — Segunda Forma Normal ✅
Todas as tabelas têm chave simples (id_*). 2FN só é violada com chave composta — não é o caso aqui.

### 3FN — Terceira Forma Normal ✅
Nenhum atributo não-chave depende de outro atributo não-chave.

**Análise do caso mais delicado — `ano_nascimento` em vencedor:**
- `ano_nascimento` poderia ser derivado de `data_nascimento` (ano = YEAR(data_nascimento))
- Isso seria uma dependência transitiva: `id_vencedor → data_nascimento → ano_nascimento`
- **Decisão:** manter ambos. Justificativa: 1 registro tem `data_nascimento` nula mas tem `ano_nascimento` preenchido — eliminar a coluna perderia informação real do dataset.

**Tabela `premio`:**
- Só tem FKs e PK — não há atributos não-chave, então 3FN é trivialmente satisfeita.

### Constraint adicional de negócio
A combinação `(id_vencedor, id_categoria, id_edicao)` deve ser única:
uma pessoa não pode ganhar a mesma categoria duas vezes na mesma edição.
Isso será implementado como `UNIQUE` no DDL.
