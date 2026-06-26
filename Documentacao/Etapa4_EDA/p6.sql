-- P6: Distribuição de prêmios por país

SELECT v.pais_nascimento pais, COUNT(*) vitorias
FROM vencedor v
JOIN premio p ON p.id_vencedor = v.id_vencedor
GROUP BY v.pais_nascimento
ORDER BY vitorias DESC;
