-- -------------------------------------------------------------
-- P5 — Primeiro vencedor não-branco por categoria
-- Técnica: CTE + ROW_NUMBER + filtro
-- -------------------------------------------------------------


WITH ranking AS (
    SELECT c.nome AS categoria, v.nome AS vencedor, v.nome_etnia, e.ano,
            ROW_NUMBER() OVER (PARTITION BY c.id_categoria ORDER BY e.ano) AS rn
    FROM premio p
    JOIN vencedor  v ON v.id_vencedor  = p.id_vencedor
    JOIN edicao    e ON e.id_edicao    = p.id_edicao
    JOIN categoria c ON c.id_categoria = p.id_categoria
    WHERE v.nome_etnia <> 'White'
)
SELECT categoria, vencedor, nome_etnia AS etnia, ano
FROM ranking WHERE rn = 1 ORDER BY ano;
