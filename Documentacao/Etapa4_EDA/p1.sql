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
ORDER BY categorias_vencidas DESC, e.ano
LIMIT 15;
