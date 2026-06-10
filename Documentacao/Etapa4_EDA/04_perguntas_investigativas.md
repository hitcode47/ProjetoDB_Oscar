# Perguntas Investigativas — Oscar AMPAS

## Motivação
Com o banco populado, formulamos perguntas que exploram padrões históricos de diversidade,
prestígio e longevidade de carreira entre os vencedores do Oscar (1927–2014).

---

## P1 — Filmes com múltiplas vitórias na mesma edição
**Pergunta:** Quais filmes venceram mais de uma categoria na mesma cerimônia?
**Técnica SQL:** JOIN + GROUP BY + HAVING
**Por que é interessante:** Revela os filmes mais dominantes de cada época.

---

## P2 — Evolução da representatividade étnica por década
**Pergunta:** Como a proporção de vencedores não-brancos mudou ao longo das décadas?
**Técnica SQL:** GROUP BY com cálculo de década + proporção percentual
**Por que é interessante:** Permite visualizar se (e quando) o Oscar se tornou mais diverso.

---

## P3 — Idade no momento da premiação
**Pergunta:** Qual a idade média dos vencedores por categoria? Quem ganhou mais jovem e mais velho?
**Técnica SQL:** JOIN + agregação (AVG, MIN, MAX) + subquery
**Por que é interessante:** Compara perfis de carreira entre categorias (atores vs. diretores).

---

## P4 — Maior intervalo entre vitórias consecutivas
**Pergunta:** Entre quem ganhou mais de um Oscar, qual foi o maior intervalo de anos entre as vitórias?
**Técnica SQL:** CTE + window function LAG
**Por que é interessante:** Identifica carreiras longas e retornos históricos ao palco do Oscar.

---

## P5 — Primeira vitória não-branca por categoria
**Pergunta:** Em que ano cada categoria teve seu primeiro vencedor não-branco?
**Técnica SQL:** CTE + MIN + filtro por etnia
**Por que é interessante:** Marca momentos históricos de quebra de barreira em cada categoria.
