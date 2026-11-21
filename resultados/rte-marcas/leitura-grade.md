# Leitura da grade das marcas de atenção no RTE (15 treinos), 10/11/2026

Leitura do Claude sobre `pc/resultados.csv` (copiado do PC). Ideia do Pedro (10/11): a query do decoder marca as
palavras-chave do par; aqui a marcação vai direto ao encoder, sem decoder. BERT base cru, Tabela 4, aquecimento
`prop`, L_cls desde o passo 1, 5 sementes, código `59278b8-dirty`. Dev do RTE (277 pares) no papel de teste.

Três braços, que só diferem na perda das marcas (auditado):
- `marks_none`: só a L_cls.
- `marks_real`: L_cls + 1,0 × perda que puxa a atenção do `[CLS]` (última camada, média das cabeças) para as posições
  do par cujas palavras a justificativa do Qwen copia (grupo C). 15,9% dos tokens de entrada, mediana de 10 por par.
- `marks_random`: a mesma perda, com o mesmo número de posições por par sorteadas ao acaso.

## O que os números dizem

| Braço | ROC-AUC | acurácia | perda das marcas na última época |
|---|---|---|---|
| `marks_none` | 0,739 ± 0,023 | 0,681 ± 0,032 | |
| `marks_real` | 0,745 ± 0,012 | 0,687 ± 0,006 | 0,020 |
| `marks_random` | 0,691 ± 0,017 | 0,633 ± 0,015 | 0,162 |

| Comparação pareada | Δ ROC-AUC (IC 95%) | vence em | Δ acurácia (IC 95%) |
|---|---|---|---|
| real − aleatória | **+0,055 (+0,031 a +0,078)** | 5/5 | +0,054 (+0,039 a +0,070) |
| real − nenhuma | +0,006 (−0,019 a +0,031) | 3/5 | +0,006 (−0,031 a +0,043) |
| aleatória − nenhuma | **−0,049 (−0,077 a −0,020)** | 0/5 | −0,048 (−0,093 a −0,003) |

1. **Não há ganho sobre o BERT sem marcas.** +0,006, com o intervalo cruzando o zero. Contra o baseline, é nulo.
2. **O conteúdo das marcas importa, e isso sai do ruído.** Marca real fica 0,055 acima da aleatória nas 5 sementes,
   com o intervalo longe do zero nas duas métricas. É o primeiro contraste do projeto em que a justificativa do LLM
   mostra, contra um controle, que carrega informação útil para a classificação.
3. **Forçar a atenção para palavras ao acaso custa 5 pontos; forçar para as palavras da justificativa não custa
   nada.** A perda das marcas reais vai a 0,020, ou seja, ~98% da atenção do `[CLS]` na última camada fica nos ~16%
   de tokens marcados, e o classificador continua tão bom quanto antes. As palavras que a justificativa copia bastam
   para o `[CLS]` decidir.
4. **Diferente do Herrewijnen et al. (2026)**, onde marca aleatória rendia ganho parecido com a humana: aqui a
   aleatória piora. As condições não são as mesmas (perda, peso e tarefa diferentes; o artigo está em nível 3 no
   projeto), então é contraste a investigar, não refutação.
5. **Observação, não medida como efeito:** as sementes do braço real ficam mais parecidas entre si (desvio de 0,006
   na acurácia contra 0,032 sem marcas).

## Com poucos pares de treino (500 e 1.000), 30 treinos, 10/11

Mesmos três braços, `--pares 500` e `--pares 1000` (o de 500 está contido no de 1.000), 5 sementes. Duas notas por
treino: no dev (277) e nos 1.470 pares de treino que nenhum dos dois tamanhos usa (ideia do Pedro). Dados em
`../rte-marcas-500/pc/` e `../rte-marcas-1000/pc/`.

| Pares | Braço | ROC-AUC no dev | ROC-AUC nos 1.470 | acurácia nos 1.470 |
|---|---|---|---|---|
| 500 | sem marcas | 0,578 ± 0,018 | 0,637 ± 0,007 | 0,604 |
| 500 | real | 0,579 ± 0,022 | 0,638 ± 0,009 | 0,606 |
| 500 | aleatória | 0,590 ± 0,025 | 0,614 ± 0,018 | 0,582 |
| 1.000 | sem marcas | 0,656 ± 0,025 | 0,678 ± 0,009 | 0,642 |
| 1.000 | real | 0,650 ± 0,031 | 0,673 ± 0,012 | 0,624 |
| 1.000 | aleatória | 0,610 ± 0,022 | 0,667 ± 0,010 | 0,631 |

| Comparação nos 1.470 pares | 500 pares | 1.000 pares |
|---|---|---|
| real − sem marcas, ROC-AUC | +0,000 (IC −0,006 a +0,007) | −0,004 (IC −0,019 a +0,010) |
| real − sem marcas, acurácia | +0,002 (IC −0,012 a +0,015) | **−0,019 (IC −0,028 a −0,010), perde 5/5** |
| real − aleatória, ROC-AUC | **+0,023 (IC +0,012 a +0,035), vence 5/5** | +0,007 (IC −0,001 a +0,014), vence 4/5 |

6. **A hipótese dos poucos dados não se confirmou.** Com 500 pares a marca real empata com o BERT sem marcas; com
   1.000 empata no ROC-AUC e perde 0,019 de acurácia nos 1.470 pares, nas 5 sementes. A marca não vira ganho onde
   o dado é escasso.
7. **Real acima de aleatória continua aparecendo**, mas menor e menos regular que com o treino inteiro: claro nos
   1.470 pares com 500 de treino e no dev com 1.000 (+0,040, IC +0,013 a +0,068), fraco nos 1.470 com 1.000.
8. **O conjunto de 1.470 pares mede melhor que o dev.** O desvio entre sementes cai de ~0,02 para ~0,01 e os
   intervalos encolhem cerca de 3 vezes. As notas também saem mais altas que no dev (0,637 contra 0,578 com 500
   pares): o dev de 277 pares é ruidoso e, aqui, mais difícil.

Ressalvas deste bloco: o lançamento não passou pelo auditor (mesmo treino, só o recorte e uma avaliação a mais); a
lista de expressões de rótulo usa os rótulos dos 2.470 pares, inclusive os 1.470 reservados (afeta só quais
palavras podem ser marcadas no treino).

## Limites

- **A perda é calculada sobre a atenção depois do dropout** (a biblioteca devolve os pesos assim): a massa tem ruído.
  Vale igual para real e aleatória.
- **O corte de gradiente em 1,0 junta as duas perdas**, e no começo o gradiente das marcas é ~3× o da classificação
  (auditoria). Parte da queda do braço aleatório pode vir disso; o braço real sofre o mesmo e não cai.
- **22,5% das posições reais também caem no sorteio** do mesmo par: o contraste real × aleatória está atenuado.
- **Palavras gramaticais nunca são marcadas**, mesmo quando decidem ("no", "not", "yet", "found"). A negação fica
  fora das marcas.
- Peso 1,0 e última camada são escolhas do Claude, sem varredura. Uma receita, um conjunto, 5 sementes, dev de 277
  pares, só `prop`.
- O `marks_none` (0,739) repete o BERT cru de ontem (0,736), com a atenção em outra implementação (`eager`).
