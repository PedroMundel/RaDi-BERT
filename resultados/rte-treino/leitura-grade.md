# Leitura da grade do RTE (20 treinos), 10/11/2026, 03:07

Leitura do Claude sobre `analise-grade.md` (gerado por `analise_grade.py --agrawal` sobre os CSVs do PC copiados em
`pc/`). Dev do RTE, 277 pares, no papel de teste; 5 sementes por célula; comparação pareada por semente.

## O que os números dizem

| | 500 (cópia da Tabela 4) | prop (10% dos passos) |
|---|---|---|
| BERT cru | 0,711 ± 0,021 | **0,736 ± 0,020** |
| BERT + decoder | 0,718 ± 0,019 | 0,707 ± 0,030 |
| Decoder − BERT, pareado | +0,007 (IC 95% −0,031 a +0,045), vence 2/5 | **−0,028 (IC −0,071 a +0,015), vence 0/5** |

1. **O BERT cru é o melhor braço da grade** (0,736 no `prop`), e fica 0,26 acima do baseline MS MARCO do Agrawal
   (0,4754) e 0,15 acima do método deles (0,5873). O "+11 pontos" do paper no RTE não se sustenta contra um
   baseline ajustado no próprio RTE.
2. **O decoder não ajuda.** No `500` empata. No `prop` perde nas 5 sementes (−0,001 a −0,087). O intervalo ainda
   cruza o zero, e um teste de sinal com 5/5 dá p = 0,0625 (bilateral). Então a leitura honesta é **"nulo, com
   tendência a atrapalhar"**, não "atrapalha".
3. **O aquecimento copiado (500 de 624 passos) custa 0,025 no BERT.** O `prop` é o que vale para o resto.
4. **Medidas de gradiente** (`prop`, média de 5 sementes): o cosseno L_aux × L_cls fica entre −0,05 e +0,02 o
   treino todo, então a L_aux empurra o BERT numa direção ortogonal à da classificação. As palavras copiadas do par
   (C) são 33% dos tokens e dão 60–65% do empurrão. A L_aux cai de 7,0 para 3,0 por token e para por aí.
5. **Sugestivo, com n = 1:** a semente 5, a pior do decoder (−0,087), é a única em que o cosseno ficou negativo
   depois do passo 200 (−0,13 de média, contra +0,01 a +0,04 nas outras quatro). É compatível com a L_aux
   atrapalhando quando empurra contra a L_cls, mas uma semente não prova nada.

## Procedência e limites

- O BERT cru rodou no commit `5ef6fed` e o `bert_decoder` no `59278b8`. A diferença entre os dois commits é só o
  lote em 2×16, que não muda a conta (I16). As sementes 2–5 do `bert_decoder prop` rodaram com micro-lote 8 e o
  código `59278b8-dirty` (braços T5 e e-SNLI acrescentados; o caminho do RTE com BERT é o mesmo, testado). O motivo
  foi a VRAM transbordando com micro-lote 16 (`AUTONOMIA.md`, 02:10).
- O tempo por treino no `bert_decoder prop` mistura 2.770 s (semente 1, transbordando, com medida por palavra) e
  530 s (sementes 2–5, micro-lote 8). A média de 16 min da tabela não é o custo real: sem transbordo, um treino com
  decoder custa ~9 min, e o BERT cru ~2 min.
- A avaliação é no dev, como no Agrawal: não há test com rótulo no GLUE. Com 277 pares, 0,01 de ROC-AUC fica dentro
  do ruído entre sementes (desvio de 0,02 a 0,03).
