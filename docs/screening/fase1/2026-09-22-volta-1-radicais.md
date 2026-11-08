# Fase 1, execução 3 — volta 1: filtro por radicais + teste de recuperação (22/09/2026)

**Aprovado pelo Pedro (22/09):** radicais no título, bola de neve como rede de segurança, conjunto de referência (a) agora e (b) depois da bola de neve. Nível 3, mecânico, sem leitura de modelo.

## Como os radicais foram feitos (para não viciar o teste)

Gerados **mecanicamente** dos termos dos grupos núcleo do pool (`área`, `edge`, `compressão`, `inferência/serving`, `adaptação`): cada palavra do termo, menos uma **lista de palavras genéricas declarada antes do teste**, reduzida a radical por corte de sufixo. Casamento: radical igual, ou palavra do título começando pelo radical quando ele tem 5+ letras.

**Radicais (42):** acceler, accelerat, adapt, batch, cach, compil, compress, constrain, cot, decod, deploym, depth, distill, early, edge, effici, evict, exit, factor, flashattent, green, infer, limit, llm, llms, lms, lora, mobil, moe, nlp, paged, peft, prun, ptq, qat, quant, resourc, serv, slm, slms, spars, speculativ

**Genéricas excluídas:** activation, adaptive, and, approximation, architecture, attention, aware, based, bit, chain, compact, computation, conditional, continuous, decomposition, deep, device, devices, draft, dynamic, expert, experts, fine, flight, for, framework, fusion, hardware, in, iteration, kernel, kernels, key, knowledge, language, large, learning, level, linear, low, management, matrix, memory, method, methods, mixture, model, models, multi, network, networks, neural, of, only, operator, optimization, parallel, parameter, post, rank, rationale, reasoning, sampling, scheduling, small, step, structured, student, system, systems, teacher, technique, techniques, tensor, the, thought, to, token, train, training, transformer, transformers, tuning, unstructured, value, weight, with

**Conjunto de referência:** 57 obras 'entra' da execução 2 presentes no bruto, divididas com semente 42 em **ajuste (28)** e **teste (29)**. O número que vale é o do **teste**.

**Contaminação residual declarada:** o Claude já tinha visto as perdas das 58 antes de gerar a lista de genéricas; a lista não foi ajustada ao teste, mas não é cega.

## Resultado

| filtro | selecionadas | ajuste | **teste** |
|---|---|---|---|
| atual (termo exato do pool) | 2604 | 17/28 | **19/29** |
| tipo + radical | 5655 | 22/28 | **23/29** |
| tipo ampliado + radical | 6285 | 25/28 | **24/29** |

**Perdas no teste — atual (termo exato do pool):**
- Adaptive Inference through Early-Exit Networks: Design, Challenges and Directions
- Data-Free Knowledge Transfer: A Survey
- Lightweight Deep Learning: An Overview
- From Algorithm to Hardware: A Survey on Efficient and Safe Deployment of Deep Neural Networks
- A Survey on Green Deep Learning
- Faster and Lighter LLMs: A Survey on Current Challenges and Way Forward
- Enable Deep Learning on Mobile Devices: Methods, Systems, and Applications
- A Survey on Transformer Compression
- A Review on Edge Large Language Models: Design, Execution, and Applications
- Resource-Efficient Neural Networks for Embedded Systems

**Perdas no teste — tipo + radical:**
- Adaptive Inference through Early-Exit Networks: Design, Challenges and Directions
- Data-Free Knowledge Transfer: A Survey
- Lightweight Deep Learning: An Overview
- A Survey of Small Language Models
- Enable Deep Learning on Mobile Devices: Methods, Systems, and Applications
- Resource-Efficient Neural Networks for Embedded Systems

**Perdas no teste — tipo ampliado + radical:**
- Data-Free Knowledge Transfer: A Survey
- Lightweight Deep Learning: An Overview
- A Survey of Small Language Models
- Enable Deep Learning on Mobile Devices: Methods, Systems, and Applications
- Resource-Efficient Neural Networks for Embedded Systems

## Radicais que mais selecionam (tipo + radical)

| radical | obras |
|---|---|
| mobil | 976 |
| edge | 654 |
| effici | 654 |
| resourc | 546 |
| quant | 393 |
| llm | 343 |
| adapt | 336 |
| compress | 331 |
| llms | 226 |
| early | 217 |
| factor | 201 |
| constrain | 186 |
| nlp | 177 |
| deploym | 159 |
| spars | 137 |
| infer | 132 |
| limit | 131 |
| distill | 128 |
| acceler | 121 |
| accelerat | 101 |

Seleção completa, ordenada por nº de radicais e citação: `2026-09-22-volta-1-radicais-selecao.csv` (5655 obras).

## Diagnóstico do ruído (feito sobre a SELEÇÃO, não sobre a referência — não contamina o teste)

O corte de sufixo é grosseiro e gerou radicais curtos demais:

| radical | casa com (títulos) |
|---|---|
| quant | **quantum 254**, quantitative 53, quantization 49, quantification 38 |
| factor | **factors 120**, factorization 46 |
| adapt | adaptive 187, adaptation 101 |
| mobil | mobile 931, mobility 71 |
| limit | limitations 77, limited 35 |
| early | early 218 |
| depth | depth 87 |

**2.100 das 5.655** seleções se sustentam num único desses radicais.

**Lacunas do pool reveladas pelas perdas no teste** (direção (b) da revisão por retorno, pool §3):
`lightweight` não existe no pool; `small language models` só casa pela sigla (SLM), porque *small* e
*language* estão na lista de genéricas; `embedded` não existe no pool.
