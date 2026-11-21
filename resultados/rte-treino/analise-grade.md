# Análise da grade do RTE

Gerado por `analise_grade.py` sobre `resultados\rte-treino\pc`: 20 treinos. Avaliação no dev do RTE (277 pares), que faz o papel de teste. Média ± desvio padrão entre sementes.

## Métricas por braço

| Braço | Aquecimento | n | roc_auc | accuracy | f1_macro | precision_at_0_7 | recall_at_0_7 | f1_entailment | f1_not_entailment | min/treino |
|---|---|---|---|---|---|---|---|---|---|---|
| bert | 500 | 5 | 0.7113 ± 0.0205 | 0.6542 ± 0.0203 | 0.6438 ± 0.0250 | 0.6415 ± 0.0203 | 0.7521 ± 0.0426 | 0.7031 ± 0.0110 | 0.5845 ± 0.0422 | 1.7 |
| bert | prop | 5 | 0.7358 ± 0.0201 | 0.6751 ± 0.0258 | 0.6690 ± 0.0276 | 0.6794 ± 0.0296 | 0.7479 ± 0.0367 | 0.7127 ± 0.0208 | 0.6254 ± 0.0381 | 2.4 |
| bert_decoder | 500 | 5 | 0.7181 ± 0.0194 | 0.6628 ± 0.0055 | 0.6533 ± 0.0073 | 0.6550 ± 0.0153 | 0.7548 ± 0.0326 | 0.7091 ± 0.0118 | 0.5976 ± 0.0218 | 16.0 |
| bert_decoder | prop | 5 | 0.7074 ± 0.0297 | 0.6513 ± 0.0318 | 0.6425 ± 0.0352 | 0.6543 ± 0.0294 | 0.7329 ± 0.0506 | 0.6964 ± 0.0252 | 0.5886 ± 0.0520 | 16.3 |

## Diferença pareada por semente contra o mesmo encoder sem decoder

| Braço − base | Aquecimento | sementes pareadas | Δ ROC-AUC (IC 95%) | vence em | Δ acurácia (IC 95%) |
|---|---|---|---|---|---|
| bert_decoder − bert | 500 | 5 | +0.0068 (-0.0314, 0.0450) | 2/5 | +0.0087 (-0.0156, 0.0329) |
| bert_decoder − bert | prop | 5 | -0.0284 (-0.0712, 0.0145) | 0/5 | -0.0238 (-0.0678, 0.0202) |

Referência do Agrawal (Tabela 2, ROC-AUC no RTE): BERT (MS MARCO) 0.4754, + Reasoning 0.5873 (Δ +0.1119).

## Medidas de gradiente por grupo (média entre sementes)

L_aux/token = perda da justificativa na sonda (64 pares do treino, fixos). Em cada célula de grupo: fração dos tokens do alvo no grupo → parcela do gradiente da L_aux que vem dele (cosseno com a L_cls). Parcela maior que a fração quer dizer que o grupo empurra o encoder mais do que o seu tamanho. As parcelas somam 1.

#### bert_decoder, aquecimento 500 (5 sementes)

| passo | L_aux/token | ‖g_c‖ | ‖g_a‖ | cos(g_c, g_a) | S: tokens → parcela (cos) | F: tokens → parcela (cos) | C: tokens → parcela (cos) | N: tokens → parcela (cos) |
|---|---|---|---|---|---|---|---|---|
| 1 | 7.02 | 0.825 | 9.579 | -0.005 | 0.09 → 0.09 (-0.00) | 0.44 → 0.24 (+0.00) | 0.33 → 0.50 (-0.01) | 0.13 → 0.17 (+0.01) |
| 25 | 6.50 | 0.731 | 8.391 | -0.015 | 0.09 → 0.08 (-0.01) | 0.44 → 0.27 (-0.01) | 0.33 → 0.49 (-0.01) | 0.13 → 0.16 (-0.00) |
| 100 | 4.03 | 0.428 | 4.850 | -0.000 | 0.09 → 0.08 (-0.00) | 0.44 → 0.15 (-0.01) | 0.33 → 0.64 (+0.01) | 0.13 → 0.12 (-0.01) |
| 175 | 3.52 | 0.407 | 4.166 | +0.007 | 0.09 → 0.17 (-0.00) | 0.44 → 0.17 (+0.01) | 0.33 → 0.52 (-0.00) | 0.13 → 0.13 (+0.02) |
| 200 | 3.45 | 1.857 | 3.739 | +0.009 | 0.09 → 0.13 (-0.01) | 0.44 → 0.11 (+0.02) | 0.33 → 0.61 (+0.01) | 0.13 → 0.15 (+0.01) |
| 300 | 3.33 | 1.993 | 3.442 | +0.050 | 0.09 → 0.17 (-0.02) | 0.44 → 0.13 (-0.03) | 0.33 → 0.55 (+0.08) | 0.13 → 0.15 (+0.02) |
| 400 | 3.25 | 3.625 | 3.469 | +0.031 | 0.09 → 0.17 (+0.02) | 0.44 → 0.16 (+0.00) | 0.33 → 0.49 (+0.03) | 0.13 → 0.18 (+0.01) |
| 500 | 3.17 | 4.494 | 3.183 | +0.053 | 0.09 → 0.15 (+0.04) | 0.44 → 0.14 (+0.02) | 0.33 → 0.55 (+0.04) | 0.13 → 0.17 (-0.00) |
| 600 | 3.11 | 1.210 | 2.997 | +0.028 | 0.09 → 0.15 (+0.01) | 0.44 → 0.14 (-0.03) | 0.33 → 0.57 (+0.04) | 0.13 → 0.14 (-0.01) |

#### bert_decoder, aquecimento prop (5 sementes)

| passo | L_aux/token | ‖g_c‖ | ‖g_a‖ | cos(g_c, g_a) | S: tokens → parcela (cos) | F: tokens → parcela (cos) | C: tokens → parcela (cos) | N: tokens → parcela (cos) |
|---|---|---|---|---|---|---|---|---|
| 1 | 7.02 | 0.825 | 9.456 | -0.006 | 0.09 → 0.09 (-0.00) | 0.44 → 0.24 (+0.00) | 0.33 → 0.50 (-0.01) | 0.13 → 0.17 (+0.01) |
| 25 | 6.42 | 0.725 | 8.094 | -0.011 | 0.09 → 0.07 (-0.00) | 0.44 → 0.26 (-0.02) | 0.33 → 0.50 (-0.00) | 0.13 → 0.16 (-0.01) |
| 100 | 3.76 | 0.396 | 3.723 | +0.003 | 0.09 → 0.15 (-0.01) | 0.44 → 0.16 (-0.01) | 0.33 → 0.57 (+0.01) | 0.13 → 0.12 (-0.00) |
| 175 | 3.30 | 0.645 | 2.774 | +0.002 | 0.09 → 0.09 (+0.01) | 0.44 → 0.10 (+0.02) | 0.33 → 0.65 (-0.02) | 0.13 → 0.15 (+0.01) |
| 200 | 3.23 | 0.772 | 2.916 | +0.021 | 0.09 → 0.13 (+0.00) | 0.44 → 0.11 (+0.02) | 0.33 → 0.61 (+0.01) | 0.13 → 0.15 (+0.01) |
| 300 | 3.12 | 1.718 | 2.462 | -0.003 | 0.09 → 0.13 (-0.02) | 0.44 → 0.10 (-0.02) | 0.33 → 0.60 (+0.02) | 0.13 → 0.16 (-0.01) |
| 400 | 3.09 | 2.730 | 2.432 | +0.014 | 0.09 → 0.13 (+0.01) | 0.44 → 0.10 (-0.01) | 0.33 → 0.61 (+0.01) | 0.13 → 0.17 (-0.00) |
| 500 | 3.07 | 3.343 | 2.540 | -0.002 | 0.09 → 0.11 (+0.02) | 0.44 → 0.11 (-0.00) | 0.33 → 0.63 (-0.01) | 0.13 → 0.15 (-0.00) |
| 600 | 3.04 | 4.613 | 2.413 | -0.046 | 0.09 → 0.09 (+0.01) | 0.44 → 0.10 (-0.04) | 0.33 → 0.65 (-0.02) | 0.13 → 0.15 (-0.04) |

## Influência por palavra (semente 1)

align_t = quanto do empurrão da palavra no encoder aponta na direção da L_cls (positivo ajuda a classificar). A parcela do alinhamento total soma 1 sobre todas as palavras da sonda.

#### bert_decoder, aquecimento 500, passo 1

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.15 | 0.0405 |
| F | 1538 | +0.27 | 0.0316 |
| C | 860 | +0.37 | 0.0579 |
| N | 393 | +0.21 | 0.0488 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): mention (S, +0.0019), people (C, +0.0015), who (F, +0.0015), specific (N, +0.0014), identifies (N, +0.0014), as (F, +0.0013), there (F, +0.0011), being (F, +0.0011), are (F, +0.0011), information (S, +0.0010)

Menos alinhadas: south (C, -0.0005), he (F, -0.0006), citizens (C, -0.0009), first (F, -0.0010), </s> (F, -0.0010)

#### bert_decoder, aquecimento 500, passo 187

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.22 | 0.0189 |
| F | 1538 | +0.55 | 0.0120 |
| C | 860 | +0.34 | 0.0324 |
| N | 393 | -0.11 | 0.0287 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): ▁" (F, +0.0004), identified (N, +0.0004), new (C, +0.0004), established (S, +0.0004), described (F, +0.0003), " (F, +0.0003), rather (F, +0.0003), were (F, +0.0002), her (F, +0.0002), them (F, +0.0002)

Menos alinhadas: implies (F, -0.0003), its (F, -0.0004), this (F, -0.0004), states (F, -0.0004), directly (S, -0.0004)

#### bert_decoder, aquecimento 500, passo 624

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.22 | 0.0175 |
| F | 1538 | +0.15 | 0.0122 |
| C | 860 | +0.50 | 0.0324 |
| N | 393 | +0.12 | 0.0300 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): people (C, +0.0006), an (F, +0.0005), new (C, +0.0004), not (S, +0.0004), with (F, +0.0004), were (F, +0.0004), no (S, +0.0003), was (F, +0.0003), text (F, +0.0003), does (S, +0.0003)

Menos alinhadas: specifies (N, -0.0004), citizens (C, -0.0004), from (F, -0.0004), its (F, -0.0005), location (N, -0.0010)

#### bert_decoder, aquecimento prop, passo 1

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.15 | 0.0405 |
| F | 1538 | +0.27 | 0.0316 |
| C | 860 | +0.38 | 0.0577 |
| N | 393 | +0.21 | 0.0487 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): mention (S, +0.0017), people (C, +0.0017), who (F, +0.0014), identifies (N, +0.0014), specific (N, +0.0014), as (F, +0.0013), million (C, +0.0011), there (F, +0.0011), information (S, +0.0011), being (F, +0.0011)

Menos alinhadas: south (C, -0.0005), he (F, -0.0006), first (F, -0.0008), citizens (C, -0.0009), </s> (F, -0.0010)

#### bert_decoder, aquecimento prop, passo 187

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.12 | 0.0159 |
| F | 1538 | +0.39 | 0.0103 |
| C | 860 | +0.22 | 0.0284 |
| N | 393 | +0.27 | 0.0253 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): specifies (N, +0.0004), implying (N, +0.0003), explicitly (S, +0.0003), specific (N, +0.0003), meaning (N, +0.0003), ▁" (F, +0.0003), confirming (S, +0.0002), information (S, +0.0002), text (S, +0.0002), text (F, +0.0002)

Menos alinhadas: who (F, -0.0002), established (S, -0.0002), but (S, -0.0002), citizens (C, -0.0003), rather (F, -0.0004)

#### bert_decoder, aquecimento prop, passo 624

| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |
|---|---|---|---|
| S | 309 | +0.27 | 0.0173 |
| F | 1538 | +0.23 | 0.0114 |
| C | 860 | +0.38 | 0.0306 |
| N | 393 | +0.11 | 0.0279 |

Mais alinhadas com a L_cls (≥ 5 ocorrências, média): no (S, +0.0005), not (S, +0.0004), citizens (C, +0.0004), implies (F, +0.0003), rather (F, +0.0003), to (F, +0.0003), ; (F, +0.0002), mentions (S, +0.0002), but (S, +0.0002), there (F, +0.0002)

Menos alinhadas: which (F, -0.0003), specifies (N, -0.0004), explicitly (S, -0.0004), location (N, -0.0005), described (F, -0.0006)
