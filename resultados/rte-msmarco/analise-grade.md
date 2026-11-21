# Análise da grade do RTE com BERT MS-MARCO

Gerado por `analise_grade.py` sobre `resultados\rte-msmarco\pc`: 10 treinos. Avaliação no dev do RTE (277 pares), que faz o papel de teste. Média ± desvio padrão entre sementes.

## Métricas por braço

| Braço | Aquecimento | n | roc_auc | accuracy | f1_macro | precision_at_0_7 | recall_at_0_7 | f1_entailment | f1_not_entailment | min/treino |
|---|---|---|---|---|---|---|---|---|---|---|
| bert | 500 | 5 | 0.7673 ± 0.0132 | 0.7213 ± 0.0160 | 0.7200 ± 0.0156 | 0.7344 ± 0.0123 | 0.7315 ± 0.0271 | 0.7382 ± 0.0194 | 0.7018 ± 0.0132 | 1.8 |
| bert_decoder | 500 | 5 | 0.7179 ± 0.0132 | 0.6650 ± 0.0059 | 0.6594 ± 0.0081 | 0.6668 ± 0.0106 | 0.7233 ± 0.0230 | 0.7016 ± 0.0089 | 0.6172 ± 0.0199 | 11.1 |

## Diferença pareada por semente contra o mesmo encoder sem decoder

| Braço − base | Aquecimento | sementes pareadas | Δ ROC-AUC (IC 95%) | vence em | Δ acurácia (IC 95%) |
|---|---|---|---|---|---|
| bert_decoder − bert | 500 | 5 | -0.0494 (-0.0775, -0.0213) | 0/5 | -0.0563 (-0.0820, -0.0306) |

Referência do Agrawal (Tabela 2, ROC-AUC no RTE): BERT (MS MARCO) 0.4754, + Reasoning 0.5873 (Δ +0.1119).

## Medidas de gradiente por grupo (média entre sementes)

L_aux/token = perda da justificativa na sonda (64 pares do treino, fixos). Em cada célula de grupo: fração dos tokens do alvo no grupo → parcela do gradiente da L_aux que vem dele (cosseno com a L_cls). Parcela maior que a fração quer dizer que o grupo empurra o encoder mais do que o seu tamanho. As parcelas somam 1.

#### bert_decoder, aquecimento 500 (5 sementes)

| passo | L_aux/token | ‖g_c‖ | ‖g_a‖ | cos(g_c, g_a) | S: tokens → parcela (cos) | F: tokens → parcela (cos) | C: tokens → parcela (cos) | N: tokens → parcela (cos) |
|---|---|---|---|---|---|---|---|---|
| 1 | 6.80 | 1.607 | 9.690 | +0.013 | 0.09 → 0.08 (+0.02) | 0.44 → 0.26 (+0.01) | 0.33 → 0.47 (-0.00) | 0.13 → 0.19 (+0.02) |
| 25 | 6.23 | 1.617 | 9.452 | +0.007 | 0.09 → 0.07 (+0.02) | 0.44 → 0.27 (-0.00) | 0.33 → 0.49 (+0.00) | 0.13 → 0.17 (+0.01) |
| 100 | 3.99 | 0.556 | 5.577 | +0.005 | 0.09 → 0.10 (+0.01) | 0.44 → 0.20 (+0.01) | 0.33 → 0.62 (-0.01) | 0.13 → 0.09 (+0.01) |
| 175 | 3.52 | 0.577 | 3.993 | -0.008 | 0.09 → 0.09 (+0.00) | 0.44 → 0.15 (+0.01) | 0.33 → 0.62 (-0.02) | 0.13 → 0.14 (+0.01) |
| 200 | 3.45 | 1.018 | 3.588 | +0.043 | 0.09 → 0.07 (-0.02) | 0.44 → 0.13 (+0.00) | 0.33 → 0.67 (+0.03) | 0.13 → 0.14 (+0.06) |
| 300 | 3.29 | 1.780 | 2.899 | +0.010 | 0.09 → 0.12 (-0.02) | 0.44 → 0.13 (-0.02) | 0.33 → 0.59 (+0.04) | 0.13 → 0.16 (-0.01) |
| 400 | 3.23 | 4.078 | 2.835 | +0.032 | 0.09 → 0.11 (+0.03) | 0.44 → 0.13 (+0.00) | 0.33 → 0.57 (+0.01) | 0.13 → 0.19 (+0.02) |
| 500 | 3.16 | 1.715 | 2.778 | +0.049 | 0.09 → 0.09 (+0.04) | 0.44 → 0.12 (+0.02) | 0.33 → 0.62 (+0.02) | 0.13 → 0.17 (+0.01) |
| 600 | 3.09 | 2.554 | 2.658 | +0.040 | 0.09 → 0.08 (+0.02) | 0.44 → 0.12 (+0.02) | 0.33 → 0.65 (+0.02) | 0.13 → 0.16 (-0.00) |

## Influência por palavra (semente 1)

align_t = quanto do empurrão da palavra no encoder aponta na direção da L_cls (positivo ajuda a classificar). A parcela do alinhamento total soma 1 sobre todas as palavras da sonda.

#### bert_decoder, aquecimento 500, passo 1

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +1.58 | 0.0329 |
| F | 1538 | -1.28 | 0.0272 |
| C | 860 | +0.40 | 0.0543 |
| N | 393 | +0.30 | 0.0443 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): no (S, +0.0010), text (F, +0.0008), text (S, +0.0007), specific (N, +0.0007), does (S, +0.0006), information (S, +0.0006), specifies (N, +0.0006), described (F, +0.0006), identifies (N, +0.0005), was (F, +0.0005)

Menos alinhadas: citizens (C, -0.0005), them (F, -0.0005), implying (N, -0.0005), their (F, -0.0005), u (F, -0.0007)

#### bert_decoder, aquecimento 500, passo 187

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.19 | 0.0194 |
| F | 1538 | +0.51 | 0.0133 |
| C | 860 | +0.16 | 0.0363 |
| N | 393 | +0.14 | 0.0313 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): meaning (N, +0.0009), does (S, +0.0007), confirming (S, +0.0007), implying (N, +0.0006), text (S, +0.0005), specifies (N, +0.0005), text (F, +0.0005), directly (S, +0.0004), its (F, +0.0004), implies (F, +0.0004)

Menos alinhadas: but (S, -0.0005), they (F, -0.0005), citizens (C, -0.0005), who (F, -0.0005), rather (F, -0.0009)

#### bert_decoder, aquecimento 500, passo 624

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.23 | 0.0170 |
| F | 1538 | +0.29 | 0.0122 |
| C | 860 | +0.37 | 0.0328 |
| N | 393 | +0.11 | 0.0288 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): citizens (C, +0.0017), information (S, +0.0016), explicitly (S, +0.0015), text (F, +0.0013), implies (F, +0.0013), implying (N, +0.0012), mention (S, +0.0011), mentions (S, +0.0011), but (S, +0.0010), text (S, +0.0008)

Menos alinhadas: specifies (N, -0.0008), directly (S, -0.0009), identified (N, -0.0009), rather (F, -0.0012), south (C, -0.0014)
