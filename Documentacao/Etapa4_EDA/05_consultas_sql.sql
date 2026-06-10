-- =============================================================
-- Passo 13 — Consultas Investigativas
-- Oscar AMPAS — Disciplina: Banco de Dados — DCC/UFMG
-- =============================================================

-- -------------------------------------------------------------
-- P1 — Filmes com múltiplas vitórias na mesma edição
-- Técnica: JOIN + GROUP BY + HAVING
-- -------------------------------------------------------------
SELECT
    f.titulo,
    e.ano,
    COUNT(*)                                            AS categorias_vencidas,
    STRING_AGG(c.nome, ', ' ORDER BY c.nome)           AS quais_categorias
FROM premio p
JOIN filme    f ON f.id_filme     = p.id_filme
JOIN edicao   e ON e.id_edicao    = p.id_edicao
JOIN categoria c ON c.id_categoria = p.id_categoria
GROUP BY f.titulo, e.ano
HAVING COUNT(*) > 1
ORDER BY categorias_vencidas DESC, e.ano;

-- -------------------------------------------------------------
-- P2 — Evolução da representatividade étnica por década
-- Técnica: GROUP BY com cálculo de década + proporção percentual
-- -------------------------------------------------------------
SELECT
    (e.ano / 10) * 10                                           AS decada,
    COUNT(*)                                                    AS total_premios,
    COUNT(*) FILTER (WHERE v.etnia <> 'White')                  AS nao_brancos,
    ROUND(
        COUNT(*) FILTER (WHERE v.etnia <> 'White') * 100.0
        / COUNT(*), 1
    )                                                           AS pct_nao_brancos
FROM premio p
JOIN vencedor v ON v.id_vencedor = p.id_vencedor
JOIN edicao   e ON e.id_edicao   = p.id_edicao
GROUP BY decada
ORDER BY decada;

-- -------------------------------------------------------------
-- P3a — Idade média por categoria no momento da premiação
-- Técnica: JOIN + AVG + GROUP BY
-- -------------------------------------------------------------
SELECT
    c.nome                                          AS categoria,
    ROUND(AVG(e.ano - v.ano_nascimento), 1)         AS idade_media,
    MIN(e.ano - v.ano_nascimento)                   AS mais_jovem,
    MAX(e.ano - v.ano_nascimento)                   AS mais_velho
FROM premio p
JOIN vencedor  v ON v.id_vencedor  = p.id_vencedor
JOIN edicao    e ON e.id_edicao    = p.id_edicao
JOIN categoria c ON c.id_categoria = p.id_categoria
WHERE v.ano_nascimento IS NOT NULL
GROUP BY c.nome
ORDER BY idade_media;

-- -------------------------------------------------------------
-- P3b — Os 5 mais jovens e os 5 mais velhos ao ganhar
-- Técnica: subquery + ORDER BY + LIMIT
-- -------------------------------------------------------------
(
    SELECT v.nome, c.nome AS categoria, e.ano,
           (e.ano - v.ano_nascimento) AS idade, 'mais jovem' AS tipo
    FROM premio p
    JOIN vencedor  v ON v.id_vencedor  = p.id_vencedor
    JOIN edicao    e ON e.id_edicao    = p.id_edicao
    JOIN categoria c ON c.id_categoria = p.id_categoria
    WHERE v.ano_nascimento IS NOT NULL
    ORDER BY idade ASC
    LIMIT 5
)
UNION ALL
(
    SELECT v.nome, c.nome, e.ano,
           (e.ano - v.ano_nascimento), 'mais velho'
    FROM premio p
    JOIN vencedor  v ON v.id_vencedor  = p.id_vencedor
    JOIN edicao    e ON e.id_edicao    = p.id_edicao
    JOIN categoria c ON c.id_categoria = p.id_categoria
    WHERE v.ano_nascimento IS NOT NULL
    ORDER BY (e.ano - v.ano_nascimento) DESC
    LIMIT 5
)
ORDER BY tipo, idade;

-- -------------------------------------------------------------
-- P4 — Maior intervalo entre vitórias consecutivas
-- Técnica: CTE + window function LAG
-- -------------------------------------------------------------
WITH vitorias_ordenadas AS (
    SELECT
        v.nome,
        e.ano,
        LAG(e.ano) OVER (PARTITION BY v.id_vencedor ORDER BY e.ano) AS ano_anterior
    FROM premio p
    JOIN vencedor v ON v.id_vencedor = p.id_vencedor
    JOIN edicao   e ON e.id_edicao   = p.id_edicao
)
SELECT
    nome,
    ano_anterior  AS primeiro_oscar,
    ano           AS segundo_oscar,
    (ano - ano_anterior) AS intervalo_anos
FROM vitorias_ordenadas
WHERE ano_anterior IS NOT NULL
ORDER BY intervalo_anos DESC
LIMIT 10;

-- -------------------------------------------------------------
-- P5 — Primeiro vencedor não-branco por categoria
-- Técnica: CTE + ROW_NUMBER + filtro
-- -------------------------------------------------------------
WITH ranking AS (
    SELECT
        c.nome                                              AS categoria,
        v.nome                                              AS vencedor,
        v.etnia,
        e.ano,
        ROW_NUMBER() OVER (PARTITION BY c.id_categoria ORDER BY e.ano) AS rn
    FROM premio p
    JOIN vencedor  v ON v.id_vencedor  = p.id_vencedor
    JOIN edicao    e ON e.id_edicao    = p.id_edicao
    JOIN categoria c ON c.id_categoria = p.id_categoria
    WHERE v.etnia <> 'White'
)
SELECT categoria, vencedor, etnia, ano AS primeiro_ano_nao_branco
FROM ranking
WHERE rn = 1
ORDER BY primeiro_ano_nao_branco;
