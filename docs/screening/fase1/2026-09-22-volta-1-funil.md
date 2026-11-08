# Fase 1, execução 3 — volta 1: relato de funil (22/09/2026)

**Filtro mecânico, nível 3, sem leitura de modelo. Ordena, não apaga:** toda obra está em `2026-09-22-volta-1-obras.csv` com o estágio que atingiu. Nada aqui é decisão — a decisão da volta é do Pedro.

## Bruto por string e base

| string | base | total na base | baixados |
|---|---|---|---|
| adaptação | arxiv | 899 | 899 |
| arquiteturas | arxiv | 1232 | 1232 |
| compressão | arxiv | 385 | 385 |
| dado/confiança | arxiv | 305 | 305 |
| edge | arxiv | 396 | 396 |
| ferramentas | arxiv | 1496 | 1496 |
| inferência/serving | arxiv | 43 | 43 |
| mãe (forma exec2) | arxiv | 99 | 99 |
| mãe (pool completo) | arxiv | 193 | 193 |
| uso? | arxiv | 532 | 532 |
| adaptação | s2 | 1322 | 1322 |
| arquiteturas | s2 | 24107 | 24107 |
| compressão | s2 | 9141 | 9140 |
| dado/confiança | s2 | 7490 | 7490 |
| edge | s2 | 42202 | 42200 |
| ferramentas | s2 | 13201 | 13201 |
| inferência/serving | s2 | 579 | 579 |
| mãe (forma exec2) | s2 | 863 | 863 |
| mãe (pool completo) | s2 | 2561 | 2561 |
| uso? | s2 | 12643 | 12643 |

**Registros baixados:** 119686 · **obras após dedup:** 104640

## Estágios

| trilha | estágio | critério | obras |
|---|---|---|---|
| survey | 1 | sem palavra de tipo no título | 58001 |
| survey | 2 | tipo no título, sem termo do pool no título | 30826 |
| survey | **3** | **tipo + termo do pool no título** | **2604** |
| ferramentas (sem filtro-tipo) | 1 | sem termo do pool no título | 9796 |
| ferramentas (sem filtro-tipo) | **3** | **termo do pool no título** | **3413** |

*Trilha ferramentas* = obra que veio **só** da filha `ferramentas`, que roda sem `filtro-tipo` (pool §2): exigir tipo no título barraria o paper de sistema que ela procura.

## Estágio 3 por ano

| ano | obras |
|---|---|
| 2020 | 682 |
| 2021 | 717 |
| 2022 | 601 |
| 2023 | 697 |
| 2024 | 868 |
| 2025 | 1312 |
| 2026 | 1140 |

## Estágio 3 por n.º de grupos do pool atravessados (título + abstract)

| grupos | obras |
|---|---|
| 7 | 1 |
| 6 | 4 |
| 5 | 23 |
| 4 | 127 |
| 3 | 396 |
| 2 | 878 |
| 1 | 4588 |

**Estágio 3 com abstract:** 4572 de 6017.

## Composição da trilha survey, estágio 3 (2.604)

| recorte (grupos do pool no título) | obras |
|---|---|
| **só `arquiteturas`** (transformer/attention em qualquer domínio) | 1.174 |
| só `dado/confiança` | 339 |
| só `uso?` | 187 |
| **com algum grupo núcleo** (`área`, `compressão`, `inferência/serving`, `adaptação`, `edge`) | **893** |
| núcleo sem contar `edge` | 699 |

## Leitura (nível 3, a confirmar pelo Pedro)

1. **Filtro de tipo no título funcionou:** 104.640 obras -> 33.430 com tipo no título -> 2.604 com
   tipo + termo do pool no título. A inflação do S2 (passo 0) era sobretudo palavra de tipo no resumo.
2. **`arquiteturas` é quase metade do estágio 3** (1.174 só dela) — "transformer" casa em survey de
   qualquer domínio (visão, medicina, séries temporais). É a pergunta P2 do plano.
3. **A trilha ferramentas (3.413) é outra população** — papers de sistema, não surveys; precisa de
   critério próprio antes da escada.
4. **n.º de grupos é sinal fraco para ordenar:** o topo mistura surveys da área com aplicação médica
   que casa muitos termos. Serve para ordenar dentro de um recorte, não para escolher o recorte.
5. Diferença mínima total × baixado no S2 (`edge` 42.202 × 42.200; `compressão` 9.141 × 9.140) —
   variação do bulk, sem efeito prático.

## Teste de perda do filtro de título (22/09, depois da crítica do Pedro)

Pedro: *"não estamos deixando passar conteúdos que podem ser críticos que não têm o termo no título?"*

**Conjunto de referência:** as 58 obras "entra" da execução 2 (julgadas dentro da área, nível 3, por
outro mecanismo). 57 estão no bruto da execução 3. **Chegaram ao estágio 3: 36 de 58 (62%).**
Perdidas: 22 — em dois modos:

| modo de perda | n | exemplos |
|---|---|---|
| sem palavra de tipo no título (estágio 1) | 8 | *Sparsity in Deep Learning: Pruning and growth…* (1.019 cit.) · *Bringing AI To Edge* · *Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective* |
| tipo no título, mas o termo do pool é literal demais (estágio 2) | 13 | *A Survey on Transformer Compression* (pool tem `model compression`) · *Mobile Edge Intelligence for LLMs* · *LLM Inference Unveiled* · *Efficient Reasoning Models* · *A Survey on Green Deep Learning* |
| ausente do bruto (id divergente) | 1 | *Efficient Large Language Models: A Survey* |

**Usar o abstract no lugar do título não resolve sozinho:** 3.794 obras do estágio 2 têm termo núcleo
no abstract, e as mais citadas são ruído (*A Survey on Vision Transformer*, *YOLOv11*, *Industry 5.0*).

**Conclusão (nível 3):** o filtro de título como está perde ~4 em 10 obras da área. Decisão sobre o
que fazer: do Pedro.

**Alternativa medida: título com radicais** (compress, prun, quantiz, distill, sparsi, efficien,
lightweight, edge, on-device, mobile, embedded, inference, serving, accelerat, green, low-rank,
early exit, speculative, KV cache, small language, resource):

| filtro | selecionadas (trilha survey) | referência recuperada |
|---|---|---|
| atual (tipo + termo exato do pool no título) | 2.604 | 36/58 |
| tipo + radical no título | 3.816 | 47/57 |
| tipo ampliado (+ perspective, trends, challenges) + radical | 4.245 | 51/57 |

**Viés da medição:** os radicais foram escolhidos **olhando as perdas** desse mesmo conjunto de
referência — a recuperação acima é otimista. Medir de verdade exige um conjunto de referência que
não tenha sido usado para ajustar o filtro.
