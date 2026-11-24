# Análise da grade do e-SNLI (4.000 pares)

Gerado por `analise_grade.py` sobre `resultados\esnli-treino\pc`: 10 treinos. Avaliação no dev do e-SNLI (9.842 pares, 3 classes; ROC-AUC = média um-contra-os-outros). Média ± desvio padrão entre sementes.

## Métricas por braço

| Braço | Aquecimento | n | roc_auc | accuracy | f1_macro | f1_entailment | f1_neutral | f1_contradiction | min/treino |
|---|---|---|---|---|---|---|---|---|---|
| bert | prop | 5 | 0.9158 ± 0.0051 | 0.7965 ± 0.0094 | 0.7965 ± 0.0095 | 0.8364 ± 0.0030 | 0.7519 ± 0.0155 | 0.8013 ± 0.0103 | 1.6 |
| bert_decoder | prop | 5 | 0.9092 ± 0.0025 | 0.7872 ± 0.0029 | 0.7873 ± 0.0030 | 0.8318 ± 0.0046 | 0.7419 ± 0.0038 | 0.7882 ± 0.0017 | 10.1 |

## Diferença pareada por semente contra o mesmo encoder sem decoder

| Braço − base | Aquecimento | sementes pareadas | Δ ROC-AUC (IC 95%) | vence em | Δ acurácia (IC 95%) |
|---|---|---|---|---|---|
| bert_decoder − bert | prop | 5 | -0.0066 (-0.0152, 0.0019) | 1/5 | -0.0093 (-0.0233, 0.0047) |

## Medidas de gradiente por grupo (média entre sementes)

L_aux/token = perda da justificativa na sonda (64 pares do treino, fixos). Em cada célula de grupo: fração dos tokens do alvo no grupo → parcela do gradiente da L_aux que vem dele (cosseno com a L_cls). Parcela maior que a fração quer dizer que o grupo empurra o encoder mais do que o seu tamanho. As parcelas somam 1.

#### bert_decoder, aquecimento prop (5 sementes)

| passo | L_aux/token | ‖g_c‖ | ‖g_a‖ | cos(g_c, g_a) | S: tokens → parcela (cos) | F: tokens → parcela (cos) | C: tokens → parcela (cos) | N: tokens → parcela (cos) |
|---|---|---|---|---|---|---|---|---|
| 1 | 5.15 | 1.624 | 8.767 | +0.003 | 0.15 → 0.20 (+0.00) | 0.46 → 0.30 (-0.00) | 0.16 → 0.18 (+0.00) | 0.24 → 0.33 (+0.00) |
| 25 | 4.81 | 1.466 | 6.496 | -0.021 | 0.15 → 0.23 (-0.03) | 0.46 → 0.26 (-0.01) | 0.16 → 0.19 (+0.01) | 0.24 → 0.32 (-0.03) |
| 100 | 3.41 | 1.223 | 3.036 | +0.034 | 0.15 → 0.16 (-0.01) | 0.46 → 0.19 (+0.01) | 0.16 → 0.23 (+0.00) | 0.24 → 0.42 (+0.04) |
| 175 | 2.98 | 0.989 | 2.441 | +0.020 | 0.15 → 0.10 (+0.01) | 0.46 → 0.27 (+0.02) | 0.16 → 0.27 (-0.01) | 0.24 → 0.36 (+0.01) |
| 200 | 2.90 | 1.081 | 2.285 | +0.011 | 0.15 → 0.09 (+0.03) | 0.46 → 0.22 (-0.00) | 0.16 → 0.30 (-0.01) | 0.24 → 0.39 (+0.01) |
| 300 | 2.65 | 1.005 | 2.083 | -0.014 | 0.15 → 0.09 (+0.01) | 0.46 → 0.22 (+0.01) | 0.16 → 0.31 (-0.03) | 0.24 → 0.38 (-0.01) |
| 400 | 2.64 | 4.131 | 2.178 | +0.004 | 0.15 → 0.10 (-0.00) | 0.46 → 0.22 (-0.00) | 0.16 → 0.20 (+0.02) | 0.24 → 0.49 (-0.01) |
| 500 | 2.60 | 3.434 | 1.858 | +0.072 | 0.15 → 0.08 (-0.01) | 0.46 → 0.24 (+0.04) | 0.16 → 0.29 (+0.05) | 0.24 → 0.39 (+0.03) |
| 600 | 2.58 | 2.567 | 1.785 | +0.024 | 0.15 → 0.08 (+0.00) | 0.46 → 0.22 (-0.00) | 0.16 → 0.30 (+0.03) | 0.24 → 0.40 (+0.01) |
| 700 | 2.56 | 2.212 | 1.900 | +0.017 | 0.15 → 0.08 (+0.01) | 0.46 → 0.23 (-0.01) | 0.16 → 0.28 (+0.02) | 0.24 → 0.41 (+0.01) |
| 800 | 2.54 | 0.597 | 1.860 | -0.012 | 0.15 → 0.08 (+0.00) | 0.46 → 0.23 (+0.01) | 0.16 → 0.29 (-0.01) | 0.24 → 0.39 (-0.02) |
| 900 | 2.51 | 0.285 | 1.818 | +0.006 | 0.15 → 0.10 (+0.02) | 0.46 → 0.23 (+0.01) | 0.16 → 0.27 (+0.00) | 0.24 → 0.40 (-0.01) |
| 1000 | 2.50 | 0.134 | 1.772 | +0.001 | 0.15 → 0.08 (+0.01) | 0.46 → 0.23 (+0.01) | 0.16 → 0.29 (+0.00) | 0.24 → 0.40 (-0.02) |

## Influência por palavra (semente 1)

align_t = quanto do empurrão da palavra no encoder aponta na direção da L_cls (positivo ajuda a classificar). A parcela do alinhamento total soma 1 sobre todas as palavras da sonda.

#### bert_decoder, aquecimento prop, passo 1

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 525 | +0.29 | 0.0308 |
| F | 1530 | +0.29 | 0.0229 |
| C | 469 | +0.05 | 0.0439 |
| N | 751 | +0.37 | 0.0428 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): outdoors (N, +0.0037), impossible (S, +0.0027), necessarily (S, +0.0021), involves (N, +0.0020), whereas (F, +0.0019), individuals (N, +0.0017), exclusive (S, +0.0016), simultaneously (S, +0.0015), cannot (S, +0.0014), water (C, +0.0013)

Menos alinhadas: any (F, -0.0007), someone (F, -0.0008), not (F, -0.0008), ball (C, -0.0008), dog (C, -0.0014)

#### bert_decoder, aquecimento prop, passo 300

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 525 | -0.16 | 0.0120 |
| F | 1530 | -2.56 | 0.0098 |
| C | 469 | +1.66 | 0.0223 |
| N | 751 | +2.07 | 0.0218 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): no (F, +0.0005), indicates (N, +0.0005), individuals (N, +0.0004), implies (F, +0.0004), ball (C, +0.0004), specific (N, +0.0003), her (F, +0.0003), ; (F, +0.0003), rather (F, +0.0003), during (F, +0.0003)

Menos alinhadas: physical (N, -0.0004), two (F, -0.0005), dog (C, -0.0006), standing (N, -0.0008), standing (C, -0.0010)

#### bert_decoder, aquecimento prop, passo 1000

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 525 | -0.77 | 0.0125 |
| F | 1530 | +0.51 | 0.0110 |
| C | 469 | +0.29 | 0.0246 |
| N | 751 | +0.97 | 0.0242 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): playing (C, +0.0004), ball (C, +0.0003), states (S, +0.0002), water (C, +0.0002), riding (C, +0.0002), riding (N, +0.0002), play (N, +0.0002), activity (N, +0.0002), indicates (N, +0.0001), which (F, +0.0001)

Menos alinhadas: standing (C, -0.0002), there (F, -0.0003), two (F, -0.0003), outside (C, -0.0003), outdoors (N, -0.0004)
