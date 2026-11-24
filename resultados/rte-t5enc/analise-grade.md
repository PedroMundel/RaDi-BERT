# Análise da grade do RTE com o T5 como encoder

Gerado por `analise_grade.py` sobre `resultados\rte-t5enc\pc`: 10 treinos. Avaliação no dev do RTE (277 pares), que faz o papel de teste. Média ± desvio padrão entre sementes.

## Métricas por braço

| Braço | Aquecimento | n | roc_auc | accuracy | f1_macro | precision_at_0_7 | recall_at_0_7 | f1_entailment | f1_not_entailment | min/treino |
|---|---|---|---|---|---|---|---|---|---|---|
| t5enc | prop | 5 | 0.6363 ± 0.0316 | 0.5884 ± 0.0289 | 0.5262 ± 0.0204 | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.6597 ± 0.1200 | 0.3928 ± 0.1265 | 2.7 |
| t5enc_decoder | prop | 5 | 0.5218 ± 0.0261 | 0.5054 ± 0.0369 | 0.4326 ± 0.0913 | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.3948 ± 0.2965 | 0.4704 ± 0.1977 | 20.6 |

## Diferença pareada por semente contra o mesmo encoder sem decoder

| Braço − base | Aquecimento | sementes pareadas | Δ ROC-AUC (IC 95%) | vence em | Δ acurácia (IC 95%) |
|---|---|---|---|---|---|
| t5enc_decoder − t5enc | prop | 5 | -0.1145 (-0.1402, -0.0887) | 0/5 | -0.0830 (-0.1467, -0.0194) |

## Medidas de gradiente por grupo (média entre sementes)

L_aux/token = perda da justificativa na sonda (64 pares do treino, fixos). Em cada célula de grupo: fração dos tokens do alvo no grupo → parcela do gradiente da L_aux que vem dele (cosseno com a L_cls). Parcela maior que a fração quer dizer que o grupo empurra o encoder mais do que o seu tamanho. As parcelas somam 1.

#### t5enc_decoder, aquecimento prop (5 sementes)

| passo | L_aux/token | ‖g_c‖ | ‖g_a‖ | cos(g_c, g_a) | S: tokens → parcela (cos) | F: tokens → parcela (cos) | C: tokens → parcela (cos) | N: tokens → parcela (cos) |
|---|---|---|---|---|---|---|---|---|
| 1 | 4.20 | 0.068 | 7.362 | +0.035 | 0.09 → 0.11 (+0.09) | 0.44 → 0.37 (+0.00) | 0.33 → 0.25 (+0.10) | 0.13 → 0.27 (+0.02) |
| 25 | 4.17 | 0.068 | 7.142 | +0.035 | 0.09 → 0.14 (+0.15) | 0.44 → 0.45 (+0.01) | 0.33 → 0.23 (+0.08) | 0.13 → 0.19 (+0.03) |
| 100 | 4.02 | 0.070 | 2.810 | +0.032 | 0.09 → 0.11 (+0.10) | 0.44 → 0.44 (+0.01) | 0.33 → 0.23 (-0.02) | 0.13 → 0.21 (+0.04) |
| 175 | 3.88 | 0.078 | 2.598 | +0.049 | 0.09 → 0.12 (+0.08) | 0.44 → 0.48 (-0.02) | 0.33 → 0.17 (+0.05) | 0.13 → 0.23 (+0.05) |
| 200 | 3.83 | 0.074 | 2.723 | +0.071 | 0.09 → 0.15 (+0.10) | 0.44 → 0.46 (+0.05) | 0.33 → 0.20 (-0.03) | 0.13 → 0.19 (+0.08) |
| 300 | 3.62 | 0.074 | 2.296 | +0.047 | 0.09 → 0.15 (+0.05) | 0.44 → 0.45 (+0.02) | 0.33 → 0.20 (-0.01) | 0.13 → 0.20 (+0.05) |
| 400 | 3.39 | 0.157 | 2.627 | +0.013 | 0.09 → 0.16 (+0.13) | 0.44 → 0.42 (-0.11) | 0.33 → 0.22 (+0.06) | 0.13 → 0.20 (+0.05) |
| 500 | 3.23 | 0.134 | 2.634 | +0.010 | 0.09 → 0.17 (+0.04) | 0.44 → 0.38 (+0.03) | 0.33 → 0.23 (-0.09) | 0.13 → 0.21 (+0.11) |
| 600 | 3.15 | 0.139 | 2.641 | +0.126 | 0.09 → 0.15 (+0.04) | 0.44 → 0.36 (-0.04) | 0.33 → 0.33 (+0.15) | 0.13 → 0.16 (-0.00) |

## Influência por palavra (semente 1)

align_t = quanto do empurrão da palavra no encoder aponta na direção da L_cls (positivo ajuda a classificar). A parcela do alinhamento total soma 1 sobre todas as palavras da sonda.

#### t5enc_decoder, aquecimento prop, passo 1

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +1.69 | 0.0196 |
| F | 1538 | -4.16 | 0.0163 |
| C | 860 | +2.51 | 0.0196 |
| N | 393 | +0.95 | 0.0229 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): implies (F, +0.0067), mention (S, +0.0061), being (F, +0.0060), from (F, +0.0045), mentions (S, +0.0037), text (S, +0.0031), new (C, +0.0031), u (F, +0.0027), constitutes (S, +0.0026), first (F, +0.0025)

Menos alinhadas: </s> (F, -0.0041), it (F, -0.0045), identifies (N, -0.0059), states (F, -0.0060), meaning (N, -0.0096)

#### t5enc_decoder, aquecimento prop, passo 187

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.04 | 0.0139 |
| F | 1538 | -0.71 | 0.0112 |
| C | 860 | +2.05 | 0.0146 |
| N | 393 | -0.37 | 0.0166 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): implies (F, +0.0077), location (N, +0.0050), they (F, +0.0042), new (C, +0.0036), constitutes (S, +0.0030), them (F, +0.0025), established (S, +0.0022), first (F, +0.0017), from (F, +0.0017), mention (S, +0.0015)

Menos alinhadas: does (S, -0.0023), identifies (N, -0.0024), citizens (C, -0.0028), information (S, -0.0031), meaning (N, -0.0045)

#### t5enc_decoder, aquecimento prop, passo 624

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.80 | 0.0107 |
| F | 1538 | -0.74 | 0.0067 |
| C | 860 | -0.29 | 0.0113 |
| N | 393 | +1.24 | 0.0129 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): constitutes (S, +0.0033), this (F, +0.0028), identifies (N, +0.0011), location (N, +0.0008), meaning (N, +0.0008), that (F, +0.0006), them (F, +0.0006), specific (N, +0.0006), rather (F, +0.0005), south (C, +0.0005)

Menos alinhadas: by (F, -0.0010), confirming (S, -0.0014), but (S, -0.0014), does (S, -0.0039), mention (S, -0.0048)
