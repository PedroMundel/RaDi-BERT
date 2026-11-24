# Leitura da grade do e-SNLI (10 treinos, 4.000 pares), 10/11/2026, 06:05

Leitura do Claude sobre `analise-grade.md` (gerado por `../rte-treino/analise_grade.py` sobre `pc/`). Treino: 4.000
pares sorteados (semente 0) das 16.000 primeiras linhas do lote 35B, com justificativas da variante F; avaliação no
dev do e-SNLI (9.842 pares, 3 classes). Mesmo treino da grade do RTE: BERT base, AdamW 5e-5, lote 32, 8 épocas
(1.000 passos), fases A 63 / B 1–300 / C 301–1.000, aquecimento `prop` (100), peso da L_aux 0,1, 5 sementes. Código
`59278b8-dirty`.

## Classificação

| | ROC-AUC (um-contra-os-outros) | acurácia | F1 macro | min/treino |
|---|---|---|---|---|
| BERT cru | 0,916 ± 0,005 | 0,797 ± 0,009 | 0,797 | 1,6 |
| BERT + decoder | 0,909 ± 0,003 | 0,787 ± 0,003 | 0,787 | 8 (19 na semente 1, que mede por palavra) |
| Decoder − BERT, pareado | **−0,007 (IC 95% −0,015 a +0,002), vence 1/5** | −0,009 (IC −0,023 a +0,005) | | |

1. **O nulo se repete no e-SNLI.** O decoder perde em 4 das 5 sementes por pouco (de −0,015 a −0,003) e ganha
   na semente 3 (+0,001). O intervalo cruza o zero, então a leitura é a mesma do RTE: **nulo, com tendência
   pequena a atrapalhar.** O decoder também deixa as sementes mais parecidas entre si (desvio de 0,003 contra 0,009
   na acurácia). É só observação: não foi medido como efeito.
2. **O regime de poucos pares não salvou o método.** 4.000 pares é a faixa em que o Agrawal viu o maior ganho; aqui
   o BERT cru já chega a 0,80 de acurácia em 3 classes, e o decoder não acrescenta nada.

## A hipótese 3 (a justificativa só ajuda quando traz o que o par não tem)

| | RTE (FA) | e-SNLI (F) |
|---|---|---|
| Tokens do alvo no grupo N (palavra nova, fora do par) | 13% | 24% |
| Parcela do empurrão da L_aux no encoder vinda de N | ~15% | ~40% |
| Parcela vinda de C (copiada do par) | ~60–65% | ~30% |
| cos(L_aux, L_cls) no treino | −0,05 a +0,02 | −0,02 a +0,07 |
| Decoder − BERT | −0,028 | −0,007 |

3. **No e-SNLI a justificativa traz bem mais conteúdo novo, e o empurrão no encoder vem dele**: o grupo N responde
   por ~40% do gradiente da L_aux, contra 15% no RTE. Mesmo assim não houve ganho. Então, nesta receita, "trazer
   informação que o par não tem" **não basta**. A condição da hipótese 3 foi atendida pela medida lexical e o efeito
   não apareceu. Ressalva: N é palavra nova, não informação nova (sinônimos e hiperônimos contam como N).
4. **O empurrão da L_aux continua ortogonal ao da classificação** (cosseno perto de zero o treino todo). É o mesmo
   padrão do RTE: o decoder move o BERT numa direção que não ajuda nem atrapalha a L_cls. No BERT, a cabeça de
   classificação não precisa do que o decoder ensina.
5. **A L_cls da sonda (pares do treino) vai a 0,003 no fim**: o BERT decora o treino nos dois braços. A L_aux por
   token cai de 5,2 para 2,5. As palavras de rótulo (S) e as gramaticais (F) ficam em 1,4 e 1,7, e as copiadas e novas
   em 3,6 e 3,9: de novo o decoder aprende o molde, não o conteúdo.
6. **Por palavra (semente 1, passo 1.000):** as palavras de rótulo (S, como "constitutes", "confirms", "is a
   person") têm parcela **negativa** do alinhamento (−0,77), e as novas (N) positiva (+0,97). Fazer o decoder
   prever a palavra que nomeia o rótulo empurra o BERT contra a classificação. É uma semente só, e no RTE a medida
   por palavra foi instável.

## Limites

- Uma receita só (a do BERT no RTE, sem varredura). Peso da L_aux, taxa e número de pares não foram variados.
- Avaliação no dev, lido uma vez por treino; nada foi ajustado nele. O test do e-SNLI não está no disco.
- 7,8% das justificativas do lote estão marcadas como eco (`marcas.csv`) e não foram filtradas, nos dois braços.

## Controle de calendário com 4.000 pares (18/11): não distinguível

**Procedência:** pedido do Pedro ("roda o calendario nos 4k do e-snli"); critério escrito antes em
`docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 4c". Braço `bert_calendar` (BERT sem decoder, sem passo de
classificação nos passos 1 a 300, pico da taxa do BERT no passo 300), 5 sementes, PC, cerca de 6 minutos;
`../esnli-treino-calendario/pc/resultados.csv`. Pareia com os dois braços de 10/11 deste arquivo.

**Conferido:** as 15 linhas dos dois CSVs e as diferenças pareadas calculadas sobre eles; os três braços têm o
mesmo plano (1.000 passos, fase B 300, aquecimento 100). **Não conferido:** o braço `bert` de 10/11 não foi rodado
de novo com o código de hoje (mesmo rótulo `59278b8-dirty`, `src/` diferente).

**Como ler:** média de 5 sementes no dev do e-SNLI; diferenças pareadas por semente, com intervalo de 95% e em
quantas das 5 sementes a diferença é positiva.

| | ROC-AUC | Acurácia |
|---|---|---|
| BERT sem decoder (10/11) | 0,916 ± 0,005 | 0,797 ± 0,009 |
| BERT sem decoder, com o calendário | 0,920 ± 0,007 | 0,798 ± 0,007 |
| BERT com decoder (10/11) | 0,909 ± 0,003 | 0,787 ± 0,003 |
| Calendário menos BERT sem decoder | +0,004 (−0,002 a +0,011), 4 de 5 | +0,001 (−0,006 a +0,008), 3 de 5 |
| Decoder menos calendário | −0,011 (−0,023 a +0,000), 1 de 5 | −0,010 (−0,022 a +0,002), 1 de 5 |

7. **Com 4.000 pares o calendário não se distingue do BERT sem decoder:** a média é positiva (+0,004), o intervalo
   cruza o zero. Pela regra escrita antes, "o calendário ajuda" fica como efeito visto só com 16.000 pares
   (+0,007, intervalo fora do zero).
8. **O decoder fica abaixo do calendário nas duas métricas, com os dois intervalos encostando no zero** (limites
   superiores de +0,0004 e +0,002). Pela regra é nulo; a direção é a mesma dos 16.000 pares, onde a acurácia saiu
   do ruído.
9. **O calendário não custa em nenhuma das três medidas feitas** (RTE +0,010 cruzando o zero; e-SNLI 4.000 +0,004
   cruzando; e-SNLI 16.000 +0,007 fora do zero). A hipótese "o braço com decoder perde por ter menos treino de
   classificação" continua derrubada, agora também no e-SNLI.
