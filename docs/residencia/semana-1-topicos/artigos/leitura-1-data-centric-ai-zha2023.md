# Leitura 1 — Data-centric AI (survey âncora)

**Referência:** Zha, D.; Bhat, Z. P.; Lai, K.-H.; Yang, F.; Jiang, Z.; Zhong, S.; Hu, X. **"Data-centric Artificial Intelligence: A Survey"**. arXiv:2303.10158, v3 (11/06/2023). https://arxiv.org/abs/2303.10158
**Verificado em:** 18/08/2026 (arXiv ao vivo). Survey mais citado da área segundo o dossiê C2.

## Por que esta leitura

É a leitura 1 do plano da Fase 4 (ver `../clusters.md`): cobre o coração da âncora C2 — **G01 limpeza, G02 transformação, G05 imputação, D04 outliers, G06 avaliação**. Base do Pedro aqui é a mais forte (prática em disciplinas + Ultimatum), então o objetivo é **organizar o que já sabe com o vocabulário do campo**, não aprender do zero.

## Como o survey organiza o campo (do abstract)

1. **Training data development** — desenvolver o dado de treino (coleta, limpeza, anotação, aumento).
2. **Inference data development** — desenvolver o dado de inferência/avaliação (conjuntos de teste, benchmarks).
3. **Data maintenance** — manter o dado vivo (qualidade contínua, drift — conecta com Q09).

Duas lentes transversais: **automação** (o que dá para automatizar) e **colaboração humana** (onde o humano entra — conecta com M14 crowdsourcing e I17 active learning).

## Perguntas-guia (responder durante a leitura)

1. Que nome o campo dá a cada coisa que o Ultimatum já faz (gates de qualidade, normalização, rebalanceamento)? — vocabulário para escrever depois.
2. Onde o survey coloca **avaliação de dados** (não do modelo)? Existe métrica de qualidade de dataset independente do F1 do modelo?
3. O que o survey diz sobre **dados sintéticos** como dado de treino? Algo sobre o gap sintético→real (a pergunta viva do Ultimatum: F1 0,918 → 0,655)?
4. Na lente de automação: o que já era automatizável em 2023 — e o que o survey diz que precisa de humano? (mapa para onde LLM-assistido entra, ponte com C1)
5. Que benchmarks o campo usa (DataPerf aparece?) — candidatos a baseline para trabalho próprio.

## Protocolo

- Ler: abstract → intro → figuras/tabelas de taxonomia → seções de training data development e data maintenance com calma; inference data development pode ser mais rápido.
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo.
- Tempo-alvo: 1 sessão de leitura lenta + 1 de fichamento.

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final; candidatos já verificados no dossiê C2: Xu et al. 2024, arXiv:2406.14473 — data-centric AI na era dos LLMs; Wan et al. 2023, arXiv:2310.01765 — limpeza de dados para ML; DataPerf, arXiv:2207.10062 — benchmark)_
