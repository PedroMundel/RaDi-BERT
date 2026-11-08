# Avaliação manual: notas do Pedro (13–14/10/2026)

Pares de `avaliacao-manual.csv`. X e Y são Haiku e Sonnet em ordem sorteada; a chave está em `avaliacao-chave.csv`
e é revelada só no fim. Três letras por explicação: **correta? · se sustenta sozinha? · circular?**

Valores: `s` sim, `n` não, e **`p` = explicação pobre** (valor criado pelo Pedro para "correta"). A coluna "melhor"
e as observações também são dele.

| # | Rótulo | Humano | X | Y | Melhor | Observação do Pedro |
|---|---|---|---|---|---|---|
| 1 | implicação | ssn | ssn | nnn | X | |
| 2 | contradição | pnn | ssn | ssn | X | Humano: "not circular, but cherry-picking, or straw-man fallacy" |
| 3 | implicação | psn | sss | ssn | Y | Humano: tautology |
| 4 | implicação | pnn | ssn | ssn | Y | "Y ganha nessa por ser mais simples, mas o X é bom também, empate técnico" |
| 5 | neutro | psn | ssn | ssn | empate | "Empate técnico, são quase a mesma frase" |
| 6 | implicação | ssn | ssn | ssn | X | "Y overexplains" |
| 7 | contradição | snn | ssn | ssn | Y | "Y foi melhor ao descrever o princípio da não contradição, mesmo o X descrevendo melhor o porquê" |
| 8 | implicação | ssn | ssn | nsn | X | |
| 9 | neutro | ssn | ssn | ssn | X (incerto) | "Esse eu não sei votar, mas acho que X" |
| 10 | contradição | snn | ssn | ssn | X (leve) | "Empate técnico com vantagem pra X" |
| 11 | neutro | ssn | ssn | ssn | empate (3) | "Empate entre os 3" |
| 12 | contradição | spn | snn | spn | Y | |
| 13 | neutro | ssn | psn | psn | Humano | "X falou 'which is consistent with waiting for a bride at a table', o que também pode ser falso, e Y pode induzir a dizer que é verdadeira por dizer 'nothing in the premise rules them out'" |
| 14 | contradição | ssn | ssn | ssn | Y | "Por ser mais simples" |
| 15 | neutro | psn | ssn | ssn | X | |
| 16 | neutro | ssn | ssn | ssn | Y | |
| 17 | neutro | psn | ssn | ssn | X (incerto) | "Acho que X" |
| 18 | implicação | ssn | ssn | ssn | X | |
| 19 | implicação | ssn | ssn | sss | X | |
| 20 | contradição | psn | ssn | ssn | X | |

## Chave revelada e contagem (14/10)

A chave foi revelada **depois** das 20 notas. Detalhe linha a linha em `avaliacao-revelada.csv`.

**Melhor explicação por par (escolha do Pedro, às cegas entre os dois LLMs):**

| Vencedor | Pares |
|---|---|
| **Sonnet 5.5** | **14** |
| Haiku 5.5 | 3 |
| Humano | 1 (par 13) |
| Empate | 2 |

Por rótulo, o Sonnet venceu 5 de 6 contradições, 6 de 7 implicações e 3 de 7 neutros. Os neutros concentram os
empates e a única vitória humana.

**Critérios** (contagem das letras; s = sim, n = não, p = pobre):

| | Correta (s / p / n) | Se sustenta (s / p / n) | Circular (s) |
|---|---|---|---|
| Humano | 13 / **7** / 0 | 15 / 1 / 4 | 0 |
| Haiku 5.5 | 17 / 1 / 2 | 18 / 0 / 2 | 1 |
| Sonnet 5.5 | **19** / 1 / 0 | **19** / 1 / 0 | 1 |

**Limitações:**

- n = 20, avaliado por uma pessoa só, que também criou os critérios.
- O humano não estava às cegas: o tamanho entrega quem é.
- O valor `p` surgiu durante a avaliação.
- As racionalizações dos LLMs foram geradas **com o rótulo no prompt**.
- "Circular" foi marcado em 2 de 40 explicações de LLM, mas várias trazem uma oração final que repete a definição
  do rótulo ("must be true if the premise is"). **Em aberto (Pedro):** circular é a explicação inteira ou basta
  uma oração?
