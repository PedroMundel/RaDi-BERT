# Destilação de conhecimento dentro da árvore — medição (24/09)

**Procedência: nível 3.** Contagens e metadados (título, ano, citações) do Semantic Scholar; ninguém leu
nenhum dos artigos abaixo por causa desta medição. Serve para decidir o que ler, não para citar.

**Motivo:** ideia do Pedro (24/09) — não descartar a árvore da F1; podar o que é obrigatoriamente
desnecessário, gerar uma árvore nova e filtrar por área, começando por destilação de conhecimento, para já
ter leituras enquanto o screening anda. **Nada decidido; é medição para a conversa.**

## 1. Quantas obras de destilação existem

Casamento: `distill` no título (sem distinção de maiúscula).

| Recorte | Obras |
|---|---|
| Floresta inteira (118.659), título | 331 |
| Floresta inteira, título ou abstract | 1.963 |
| Camada C (14.901), título | **211** |
| — com palavra de tipo no título (survey/review/…) | 121 |
| — com lista de referências no S2 | 132 |

Destino na F1 das 211: ligada 131 · solta recente 35 · solta (desce) 27 · sem dado de citação 16 · golden 2.
Ano: 2020 7 · 2021 15 · 2022 19 · 2023 29 · 2024 36 · 2025 52 · 2026 53 (a área cresce rápido).

As 120 que ficaram fora da camada C caíram quase todas em "fora (outra área)" na camada B — `distill` também
é destilação química, e visão computacional (CNN) está fora por §1.2.1.

## 2. O que as obras de destilação citam em comum

As 132 com referências citam 5.914 obras distintas. **205 são citadas por 5 ou mais** delas; **45 por 10 ou
mais**. Esta é a árvore "externa": artigos primários, não surveys — a F1 usou só as ligações internas entre
as 14.901.

Top da lista (n = quantas das 132 citam), já separado por tipo. Genéricos (citados por qualquer área) são o
candidato óbvio a "poda do obrigatoriamente desnecessário".

**Destilação — história e núcleo**

| n | Ano | Título |
|---|---|---|
| 17 | 2006 | Model compression (Buciluă et al.) |
| 9 | 2013 | Do Deep Nets Really Need to be Deep? (Ba & Caruana) |
| 73 | 2015 | Distilling the Knowledge in a Neural Network (Hinton et al.) |
| 27 | 2014 | FitNets: Hints for Thin Deep Nets |
| 38 | 2020 | Knowledge Distillation: A Survey (Gou et al.) — survey hub |
| 22 | 2019 | Improved Knowledge Distillation via Teacher Assistant |
| 20 | 2019 | Relational Knowledge Distillation |
| 19 | 2016 | Paying More Attention to Attention (attention transfer) |
| 16 | 2019 | Contrastive Representation Distillation |
| 16 | 2022 | Decoupled Knowledge Distillation |
| 14 | 2018 | Born Again Neural Networks |
| 13 | 2017 | Deep Mutual Learning |
| 11 | 2019 | On the Efficacy of Knowledge Distillation |

**Destilação em linguagem (encoder, decoder, encoder-decoder)**

| n | Ano | Título | Família |
|---|---|---|---|
| 11 | 2016 | Sequence-Level Knowledge Distillation (Kim & Rush) | encoder-decoder |
| 18 | 2019 | DistilBERT | encoder |
| 13 | 2019 | TinyBERT | encoder |
| 12 | 2019 | Patient Knowledge Distillation for BERT Model Compression | encoder |
| 10 | 2023 | Distilling Step-by-Step! | encoder-decoder (T5) — **Pedro já leu (nível 1)** |
| 9 | 2023 | On-Policy Distillation of Language Models | decoder |

**Ramos que usam o nome "destilação" mas são outra coisa** (decisão de escopo do Pedro)

- Visão/CNN: detecção, segmentação, self-distillation em CNN (fora por §1.2.1?).
- *Dataset distillation / condensation* (2020–2022): comprime o **dado**, não o modelo.
- Destilação federada (FedMD, Ensemble Distillation for Federated Learning): comunicação, não implantação.

**Genéricos (candidatos à poda):** BERT, Attention is All you Need, ResNet, CIFAR (Tiny Images), ImageNet,
RoBERTa, GPT-2/GPT-3, ViT, Faster R-CNN, COCO, GAN, Wide ResNet, AlexNet.

## 3. Limites

- Só 132 das 211 têm lista de referências no S2; as de editora (IEEE/Elsevier/ACM) ficaram ocultas. O
  OpenAlex cobre parte delas, mas os ids do OpenAlex não foram casados com os do S2 nesta medição.
- `distill` no título perde obras de compressão geral com seção de destilação — é recorte de área, não
  mapa da área.
- Contagem por co-citação favorece o antigo (teve mais tempo para ser citado).

Script e listas brutas: `scripts/screening/kd/` (`kd_medir.py`, `kd_top.json`, `kd_top_meta.json`).
