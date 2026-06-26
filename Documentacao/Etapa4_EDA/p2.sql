-- -------------------------------------------------------------
-- P2 — Evolução da representatividade étnica por década
-- Técnica: GROUP BY com cálculo de década + proporção percentual
-- -------------------------------------------------------------


SELECT
    (ed.ano / 10) * 10 AS decada,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE v.nome_etnia <> 'White') AS nao_brancos,
    ROUND(COUNT(*) FILTER (WHERE v.nome_etnia <> 'White') * 100.0 / COUNT(*), 1) AS pct
FROM premio p
JOIN vencedor v  ON v.id_vencedor = p.id_vencedor
JOIN edicao   ed ON ed.id_edicao   = p.id_edicao
GROUP BY decada ORDER BY decada;
