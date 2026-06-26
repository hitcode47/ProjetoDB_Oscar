-- -------------------------------------------------------------
-- P4 — Maior intervalo entre vitórias consecutivas
-- Técnica: CTE + window function LAG
-- -------------------------------------------------------------

WITH vitorias AS (
    SELECT v.nome, e.ano,
        LAG(e.ano) OVER (PARTITION BY v.id_vencedor ORDER BY e.ano) AS ano_anterior
    FROM premio p
    JOIN vencedor v ON v.id_vencedor = p.id_vencedor
    JOIN edicao   e ON e.id_edicao   = p.id_edicao
)
SELECT nome, ano_anterior AS primeiro, ano AS segundo,
    (ano - ano_anterior) AS intervalo
FROM vitorias
WHERE ano_anterior IS NOT NULL
ORDER BY intervalo DESC LIMIT 10;
