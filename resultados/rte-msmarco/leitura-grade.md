# Leitura da grade do RTE com BERT MS-MARCO (10 treinos), 10/11/2026

Leitura do Claude sobre `analise-grade.md` (gerado por `../rte-treino/analise_grade.py --agrawal` sobre `pc/`) e
sobre a saída de `zero_shot.py`. Checkpoint `nboost/pt-bert-base-uncased-msmarco` (escolha do Pedro, 10/11; o paper
não nomeia o dele). Mesmo treino da grade do BERT: Tabela 4, aquecimento `500`, fases A/B/C, 5 sementes,
micro-lote 8, código `59278b8-dirty`. Dev do RTE (277 pares) no papel de teste.

## O que os números dizem

| | ROC-AUC | acurácia |
|---|---|---|
| Agrawal 2025, Tabela 2: BERT (MS-MARCO) | 0,4754 | |
| Agrawal 2025, Tabela 2: + Reasoning | 0,5873 | |
| Aqui: BERT MS-MARCO ajustado no RTE | **0,767 ± 0,013** | 0,721 |
| Aqui: BERT MS-MARCO + decoder | 0,718 ± 0,013 | 0,665 |
| Decoder − BERT, pareado | **−0,049 (IC 95% −0,078 a −0,021), perde 5/5** | −0,056 (IC −0,082 a −0,031) |
| Aqui: o mesmo checkpoint sem nenhum treino no RTE (cabeça de relevância dele) | 0,620 (hipótese como consulta) e 0,575 (premissa como consulta) | |

1. **O resultado do Agrawal no RTE não se repetiu.** O baseline não fica abaixo do acaso: fica em 0,767, 0,29
   acima do 0,4754 do paper e 0,18 acima do método deles.
2. **O decoder piora, e desta vez o intervalo não cruza o zero.** Perde nas 5 sementes (de −0,018 a −0,072). É o
   primeiro efeito do decoder, nas quatro grades, que se separa do ruído, e é negativo.
3. **O 0,4754 também não é o modelo sem treino.** Sem ajuste nenhum no RTE, o reranqueador dá 0,58 a 0,62. Não
   achei, com este checkpoint, uma condição que dê 0,4754.
4. **O pré-treino em MS-MARCO ajuda o RTE** neste checkpoint: 0,767 contra 0,711 do BERT cru no mesmo aquecimento
   (`500`).
5. **Com o decoder, a vantagem do MS-MARCO some:** 0,7179, contra 0,7181 do BERT cru com decoder na grade de
   ontem. É uma coincidência de médias com 5 sementes, mas a leitura que ela sugere é que a fase B (187 passos só
   com a L_aux, decoder ainda sem saber ler o BERT) desfaz o que o encoder trazia. Isso apoia a H2 de
   `docs/2026-11-10-hipoteses-do-nulo.md`. A H1 (calendário) não explica este caso: no `500` o calendário favorece
   o braço com decoder.
6. **As medidas de gradiente repetem as das outras grades:** cosseno L_aux × L_cls entre −0,01 e +0,05, L_aux
   parada em ~3,1 por token, 57–67% do empurrão vindo das palavras copiadas do passo 100 em diante.

## A previsão que eu tinha feito

Em `docs/2026-11-10-hipoteses-do-nulo.md` (H4) eu previ que, se o baseline saísse perto de 0,47–0,55, o decoder
subiria. A condição não aconteceu: o baseline saiu em 0,767. Fica valendo a outra linha da H4: "se o baseline
MS-MARCO sair perto de 0,70, o 0,4754 não vem da descrição do paper".

## Duas condições rápidas do baseline (18/11): nenhuma dá o 0,4754

**Procedência:** pedido do Pedro; critério escrito antes em `docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 2b".
`condicoes_baseline.py`, 15 treinos no notebook (GTX 1650, micro-lote 4 por causa da memória, 50 minutos),
`condicoes-baseline.csv`. Mesmo checkpoint (nboost), sem decoder, 5 sementes, dev do RTE.

**Conferido:** as 15 linhas do CSV e as médias (`groupby` sobre o arquivo). **Não conferido:** as mesmas condições
no PC (o baseline de 0,767 rodou lá, com micro-lote 8; a auditoria diz que o gradiente é o mesmo, só o sorteio do
dropout muda).

**Como ler:** ROC-AUC médio de 5 sementes no dev do RTE, com o desvio padrão entre sementes e o menor e o maior
valor; a última coluna aplica a regra escrita antes (dá o número do artigo se a média ficar entre 0,44 e 0,51).

| Condição | ROC-AUC médio | Desvio | Menor a maior | Entre 0,44 e 0,51? |
|---|---|---|---|---|
| Encoder congelado, 8 épocas, só a cabeça treina | 0,590 | 0,009 | 0,580 a 0,605 | não |
| Uma época, aquecimento `500` (taxa até 15% de 5e-5) | 0,635 | 0,016 | 0,610 a 0,650 | não |
| Uma época, aquecimento `prop` | 0,741 | 0,017 | 0,725 a 0,767 | não |
| (referência, 10/11) ajuste completo, aquecimento `500` | 0,767 | 0,013 | | não |
| (referência, 10/11) sem nenhum treino no RTE | 0,620 e 0,575 | | | não |

1. **Nenhuma das três dá o número do artigo.** A mais baixa, o encoder congelado, fica em 0,590; nenhuma das 15
   rodadas fica abaixo de 0,58.
2. **Uma época já chega perto do ajuste completo** (0,741 contra 0,767): o baseline não precisa de muito treino
   para sair do acaso.
3. **Observação, sem conclusão:** o encoder congelado (0,590) cai no mesmo valor que o artigo relata para o método
   dele no RTE (0,5873). É uma coincidência de médias; não diz o que os autores fizeram.

**O que isso sustenta:** com este checkpoint, seis jeitos de usar o BERT MS-MARCO no RTE (ajuste completo, uma
época com dois aquecimentos, só a cabeça, e sem treino nas duas ordens) dão entre 0,575 e 0,767. **O que não
sustenta:** que o 0,4754 esteja errado; o artigo não descreve o ajuste e o checkpoint dele não é este.

## Limites

- **Um checkpoint só, e não é garantidamente o deles.** Outro BERT MS-MARCO pode se comportar de outro jeito
  (`Capreolus/bert-base-msmarco` não foi rodado).
- Só o aquecimento `500`, a cópia da Tabela 4. O paper não diz se usou a Tabela 4 no GLUE.
- 5 sementes, dev de 277 pares. A semente 1 do braço com decoder também mediu por palavra (1.144 s).
- O paper não descreve o ajuste do baseline no GLUE (épocas, se a cabeça foi trocada, qual classe é a positiva). Um
  ROC-AUC abaixo de 0,5 também sai de rótulo invertido; isso é suposição, não medida.
