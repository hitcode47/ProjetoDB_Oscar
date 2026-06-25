-- -------------------------------------------------------------
-- P3a — Idade média por categoria no momento da premiação
-- Técnica: JOIN + AVG + GROUP BY
-- -------------------------------------------------------------


SELECT c.nome AS categoria,
        ROUND(AVG(e.ano - v.ano_nascimento), 1) AS idade_media,
        MIN(e.ano - v.ano_nascimento) AS mais_jovem,
        MAX(e.ano - v.ano_nascimento) AS mais_velho
FROM premio p
JOIN vencedor  v ON v.id_vencedor  = p.id_vencedor
JOIN edicao    e ON e.id_edicao    = p.id_edicao
JOIN categoria c ON c.id_categoria = p.id_categoria
WHERE v.ano_nascimento IS NOT NULL
GROUP BY c.nome ORDER BY idade_media;
