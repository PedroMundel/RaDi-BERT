# Leitura da grade do RTE com o T5 como encoder (10 treinos), 10/11/2026, 05:05

Leitura do Claude sobre `analise-grade.md` (gerado por `../rte-treino/analise_grade.py` sobre `pc/`) e sobre a saída
de `comparar_ponte.py`. Checkpoint `google/t5-v1_1-base` (só C4; o t5-base original viu RTE e MNLI no pré-treino).
Mesmo treino da grade do BERT: AdamW 5e-5, lote 32, 8 épocas, corte da norma em 1,0, peso da L_aux 0,1, fases
A/B/C, aquecimento `prop`, 5 sementes, micro-lote 8. Cabeça sobre a média dos tokens reais (o T5 não tem [CLS]).

## Classificação

| | ROC-AUC | acurácia | min/treino |
|---|---|---|---|
| BERT cru (`prop`, grade do BERT) | 0,736 ± 0,020 | 0,675 | 2,4 |
| `t5enc` (encoder do T5 + cabeça) | 0,636 ± 0,032 | 0,588 | 2,7 |
| `t5enc_decoder` (+ decoder do mesmo T5) | 0,522 ± 0,026 | 0,505 | 18–29 |
| `t5enc_decoder` − `t5enc`, pareado | **−0,115 (IC 95% −0,140 a −0,089), perde 5/5** | −0,083 | |

1. **Com esse treino, o T5 v1.1 como encoder fica 0,10 abaixo do BERT.** E nenhuma probabilidade do dev chega a
   0,7 com acerto nos dois braços T5 (precisão e cobertura em 0,7 = 0): a cabeça mal sai do 0,5. A suspeita que o pré-voo
   levantou se confirma: 5e-5 é taxa de BERT, e o T5 costuma ser ajustado com 1e-4 a 3e-4. Isso é uma
   **comparação de receita, não de arquitetura.**
2. **Com o decoder, o classificador não aprende nada.** Na sonda (64 pares do treino), a L_cls fica em 0,695
   (= ln 2, o valor do acaso) do passo 1 ao 600, nas 5 sementes (mínimo 0,6925, máximo 0,6962). O motivo aparece nas normas de gradiente:

   | passo | ‖g_c‖ BERT | 0,1·‖g_a‖ / ‖g_c‖ BERT | ‖g_c‖ T5 | 0,1·‖g_a‖ / ‖g_c‖ T5 |
   |---|---|---|---|---|
   | 1 | 0,83 | 1,1 | 0,07 | 10,8 |
   | 200 | 0,77 | 0,38 | 0,07 | 3,7 |
   | 400 | 2,73 | 0,09 | 0,16 | 1,7 |
   | 600 | 4,61 | 0,05 | 0,14 | 1,9 |

   Pelo T5 (média dos tokens), o gradiente da L_cls é ~10× menor que pelo BERT ([CLS]). Com peso 0,1, a L_aux
   ainda manda no passo de 2 a 11 vezes, e o corte da norma em 1,0 encolhe o pouco que sobra. No BERT acontece o
   contrário: a L_cls passa a dominar depois do passo 200. **O resultado negativo do T5 com decoder é desequilíbrio
   de escala entre as duas perdas, não evidência contra o método.** O teste justo pede taxa de T5 e/ou peso da L_aux
   ajustado à escala do gradiente.

## Teste da ponte (L_aux por token na sonda, média de 5 sementes)

| passo | L_aux, decoder lê o BERT | L_aux, decoder lê o próprio encoder | C (copiadas), BERT → T5 | S (rótulo), BERT → T5 | F (gramaticais), BERT → T5 |
|---|---|---|---|---|---|
| 1 | 7,02 | 4,20 | 9,89 → 3,31 | 6,31 → 6,32 | 4,48 → 3,92 |
| 175 | 3,30 | 3,88 | 4,96 → 3,03 | 2,23 → 5,83 | 1,89 → 3,64 |
| 600 | 3,04 | 3,15 | 4,49 → 2,55 | 1,99 → 4,53 | 1,80 → 2,80 |

3. **Lendo o próprio encoder, o decoder copia muito melhor**: as palavras copiadas do par (C) ficam em 2,5 nats por
   token contra 4,5 lendo o BERT, e já começam em 3,3 contra 9,9. A ponte custa ~2 nats por palavra copiada. A
   fase A curta (39 passos) e a ausência de adaptador não fecham essa diferença.
4. **No total por token, os dois terminam iguais (3,0 × 3,15)**, porque o decoder do t5-base aprende as palavras de
   molde (S, F) muito mais rápido. Isso é efeito de checkpoint: o t5-base foi pré-treinado com tarefas de texto para
   texto (RTE e MNLI incluídos), e o v1.1 só com preenchimento de lacunas. Então o patamar de ~3,1 não vem só da
   ponte. Ele vem da ponte nas palavras copiadas e do decoder nas de molde, e os dois efeitos se compensam no total.
   A L_aux do v1.1 ainda caía no passo 600, então a taxa 5e-5 também pode limitar o decoder.
5. **Ruído com dropout:** a L_aux do treino na última época varia de 3,6 a 6,1 entre as sementes do T5, contra 3,15
   na sonda, que é medida sem dropout. O v1.1 foi pré-treinado sem dropout (cartão do HF) e aqui treina com 0,1.
   Esse é um terceiro fator contra o T5 nesta receita.

## Limites

- Os decoders vêm de checkpoints diferentes (t5-base × t5-v1_1-base). A comparação da ponte limpa seria o t5-base
  inteiro, mas como encoder classificador ele está contaminado pelo RTE. Para o teste da ponte isso não importa,
  porque ali só se mede a L_aux.
- As medidas do T5 deixam o embedding `shared` de fora; as do BERT incluem o embedding do BERT (`AUTONOMIA.md`,
  02:20).
- Os treinos com decoder levaram 18–29 min, contra ~9 do BERT, com pico de 7,3 GB: perto do limite da 5060. A
  semente 1 (1.747 s) também mediu por palavra.
