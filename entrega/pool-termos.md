# Pool de termos - screening da Etapa 1

**Regido por:** `metodo-screening.md`, cap. 2.
**O que é:** o vocabulário versionado do screening. As strings de busca são **composições** deste pool,
regeneradas a cada versão, nunca decretadas à parte. Nenhuma string abaixo foi executada; são texto,
prontas para a Fase 1.

**Procedência dos termos:** `eu` = sementes minhas, de conhecimento prévio, sem consulta;
`claude 15/09` = termos que o Claude acrescentou e que eu desconhecia ou não lembraria de listar,
**não verificados contra survey nenhum** (nível 3 por definição); `survey:<id>` = termo que apareceu
como nome de divisão/seção na taxonomia de um survey aprovado (só a partir do pool v1).

---

## 1. Tabela do pool

Status: **ativo** - **aposentado** (fica na tabela, riscado, com motivo; nunca se apaga).
Retorno: n. de surveys aprovados que o termo trouxe; preenchido pela Fase 1; vazio = não rodado.

### Grupo `filtro-tipo`: o que restringe a busca a fontes de screening

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| survey | "a survey", "comprehensive survey", "systematic survey" | eu | ativo | |
| review | "literature review", "a review" | eu | ativo | |
| overview | "an overview" | eu | ativo | |
| taxonomy | "a taxonomy" | eu | ativo | |

### Grupo `área`: sinônimos do nome da área (compõem a string-mãe)

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| efficient inference | "inference efficiency" | eu | ativo | |
| inference optimization | "inference acceleration", "accelerating inference" | eu | ativo | |
| model compression | "compressing", "compression techniques" | eu | ativo | |
| efficient large language models | "efficient LLMs", "efficient LLM" | eu | ativo | |
| efficient transformers | "efficient transformer" | eu | ativo | |
| efficient deep learning | "efficient neural networks", "efficient deep neural networks" | eu | ativo | |
| LLM serving | "serving large language models", "LLM inference serving" | eu | ativo | |
| resource-efficient | "resource-constrained", "resource-limited" | eu | ativo | |
| on-device | "edge deployment", "edge devices", "mobile deployment" | eu | ativo | |
| efficient NLP | "green NLP", "efficient methods for NLP" | eu | ativo | |

### Grupo `compressão`: técnicas sobre o modelo antes da implantação

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| knowledge distillation | distillation, "distilling", "teacher-student" | **eu** ("destilação") | ativo | |
| reasoning distillation | "chain-of-thought distillation", "rationale distillation", "distilling step-by-step", "CoT distillation" | **eu** ("destilação de raciocínio") | ativo | |
| quantization | "post-training quantization", PTQ, "quantization-aware training", QAT, "weight-only quantization", "low-bit" | **eu** | ativo | |
| pruning | "network pruning", "structured pruning", "unstructured pruning", sparsity, "sparse" | **eu** | ativo | |
| tensor decomposition | "low-rank factorization", "low-rank approximation", "low-rank decomposition", "matrix factorization" | claude 15/09 | ativo | |
| small language models | SLM, SLMs, "small LMs", "compact language models" | **eu** ("SLMs") | ativo | |

### Grupo `inferência/serving`: técnicas que agem na inferência

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| memory management | "KV cache", "key-value cache", "paged attention", "memory-efficient inference" | claude 15/09 | ativo | |
| continuous batching | "dynamic batching", "in-flight batching", "iteration-level scheduling" | claude 15/09 | ativo | |
| early exiting | "early exit", "adaptive computation", "dynamic inference", "adaptive depth" | **eu** | ativo | |
| efficient attention | FlashAttention, "linear attention", "sparse attention", "attention approximation" | eu | ativo | |
| KV cache compression | "KV cache quantization", "cache eviction", "token eviction" | claude 15/09 | ativo | |
| speculative decoding | "speculative sampling", "draft model", "parallel decoding" | claude 15/09 | ativo | |
| inference engine | "serving system", "inference system", "LLM inference framework" | eu | ativo | |
| kernels and compilers | "operator fusion", "kernel optimization", "model compiler", "hardware-aware" | claude 15/09 | ativo | |

### Grupo `dado/confiança`: eixo (iii) do cap. 1.2 e "saber quando confiar"

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| data-efficient | "label-efficient", "few labels", "low-resource", "sample-efficient" | eu | ativo | |
| weak supervision | "distant supervision", "LLM-generated labels", "synthetic labels" | claude 15/09 | ativo | |
| calibration | "confidence calibration", "uncertainty estimation", "selective prediction" | claude 15/09 | ativo | |

### Grupo `adaptação`: dentro pelo cap. 1.2 (efeito no serving)

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| parameter-efficient fine-tuning | PEFT, "parameter-efficient", adapters | eu | ativo | |
| LoRA | "low-rank adaptation", "multi-LoRA serving", "adapter serving" | eu | ativo | |
| mixture of experts | MoE, "conditional computation", "sparse activation" | eu | ativo | |

### Grupo `arquiteturas`: pilar fixo (cap. 1.1)

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| transformer architecture | "transformer models", "transformers" | eu | ativo | |
| encoder-only / decoder-only / encoder-decoder | "encoder-decoder", "decoder-only", "encoder-only", "architecture comparison" | eu | ativo | |
| pre-training objectives | "masked language modeling", MLM, "causal language modeling", "span corruption", "denoising" | eu | ativo | |
| attention mechanism | "self-attention", "multi-head attention", "cross-attention" | eu | ativo | |
| positional encoding | "rotary position embedding", RoPE, "relative position" | eu | ativo | |
| tokenization | "subword tokenization", BPE, "vocabulary size" | eu | ativo | |
| sequence-to-sequence | seq2seq, RNN, LSTM, "neural attention", "attention-based" | eu (base pré-transformer, cap. 1.3) | ativo | |

### Grupo `uso?`: a testar contra o cap. 1.2

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| prompt engineering | prompting, "prompt optimization", "prompt compression" | **eu** | ativo; **testar o cap. 1.2** no confronto; "prompt compression" pode ser a variante que pertence | |

---

## 2. Regras de composição

- **string-mãe** = (grupo `área` unido por OR) AND (grupo `filtro-tipo` unido por OR).
- **string-filha de um grupo G** = (termos e variantes de G unidos por OR) AND (`filtro-tipo`).
- Variantes entram na mesma string que o termo: são o mesmo conceito com outra grafia.
- Toda string leva a versão do pool que a gerou (`pool v0`) e a data.
- Filtros de caps. 3.2 e 10 do método vão **embutidos na base** quando ela permite (ano >= 2020; citações >= 100 como
  uma das pernas; tipo = review). Onde a base não permite, o filtro é aplicado à mão sobre o retorno.
- **Filtro de ano só para mapa e divisões.** Buscas de história (cap. 2.4) e seminais (cap. 4) rodam a
  string-filha **sem** o filtro de tipo e **sem** o filtro de ano.

## 3. Regras de entrada e saída do pool

- **Entra:** como semente (origem `eu` ou `claude`, só no v0) **ou** quando aparece como nome de
  divisão ou de seção na taxonomia de um survey aprovado (origem `survey:<id>`, do v1 em diante).
  Termo trazido por survey é a única via de entrada depois do v0.
- **Aposenta:** se, depois de uma rodada completa, teve **retorno zero** *e* **nenhum survey
  aprovado o usa**. Fica na tabela, riscado, com motivo e data. Não se apaga: é dado do confronto
  (cap. 2.1 do método).
- **Muda de grupo:** quando um survey aprovado o classifica em outra divisão; anotar a origem da
  mudança.
- **Versões:** v0 = sementes (este arquivo). **v1** = após saturação do mapa (cap. 5.1), com os termos
  que os surveys trouxeram e as strings regeneradas. v2+ = revisões por divisão.

## 4. Strings v0 compostas: texto, não executadas

### 4.1 String-mãe (mapa da área)

**Semantic Scholar** (`/graph/v1/paper/search/bulk`; `+` = AND, `|` = OR, aspas = frase; filtros como
parâmetros: sintaxe a validar na primeira execução):

```
query = ("efficient inference" | "inference efficiency" | "inference optimization" | "inference acceleration" | "model compression" | "efficient large language models" | "efficient LLMs" | "efficient transformers" | "efficient deep learning" | "efficient neural networks" | "LLM serving" | "serving large language models" | "resource-efficient" | "resource-constrained" | "on-device" | "edge deployment" | "efficient NLP") + (survey | review | overview | taxonomy)
year = 2020-
fieldsOfStudy = Computer Science
publicationTypes = Review        # perna (a)/(b) do cap. 3.2: rodar também SEM este filtro e cruzar
minCitationCount = 100           # perna (b) do cap. 3.2: rodar também SEM, para a perna (c): citação cruzada
sort = citationCount:desc
```

**arXiv** (API `search_query`; campos `ti:` título, `abs:` resumo; `AND`/`OR`; sintaxe a validar):

```
(ti:survey OR ti:review OR ti:overview OR ti:taxonomy) AND (abs:"efficient inference" OR abs:"inference optimization" OR abs:"inference acceleration" OR abs:"model compression" OR abs:"efficient large language models" OR abs:"efficient LLM" OR abs:"efficient transformers" OR abs:"efficient deep learning" OR abs:"LLM serving" OR abs:"serving large language models" OR abs:"resource-efficient" OR abs:"on-device" OR abs:"efficient NLP") AND (cat:cs.CL OR cat:cs.LG OR cat:cs.AI)
submittedDate: [20200101 TO *]
```

**Google Scholar** (manual; `OR` e aspas; ano pelo filtro da interface, >= 2020; sem filtro de citação -
aplicar à mão):

```
(survey OR review OR overview) ("efficient inference" OR "model compression" OR "efficient large language models" OR "efficient transformers" OR "efficient deep learning" OR "LLM serving" OR "resource-efficient" OR "on-device")
```

### 4.2 Strings-filhas (uma por grupo): forma geral

Mesma estrutura da mãe, trocando o bloco de área pelo bloco do grupo. Exemplo, grupo `compressão`,
Semantic Scholar:

```
query = ("knowledge distillation" | distillation | "reasoning distillation" | "chain-of-thought distillation" | "rationale distillation" | quantization | "post-training quantization" | "quantization-aware" | "weight-only quantization" | pruning | sparsity | "tensor decomposition" | "low-rank factorization" | "low-rank approximation" | "small language models" | SLMs) + (survey | review | overview | taxonomy)
year = 2020-  -  fieldsOfStudy = Computer Science  -  sort = citationCount:desc
```

As outras cinco filhas (`inferência/serving`, `dado/confiança`, `adaptação`, `arquiteturas`, `uso?`)
seguem o mesmo molde com os termos da tabela; são geradas na hora da execução a partir do pool, não
mantidas à mão, para não divergir da tabela.

### 4.3 Strings de seminal e história (sem filtro de tipo, sem filtro de ano)

Para cada divisão do mapa v1, a string-filha da divisão **sem** o bloco `filtro-tipo` e **sem** ano,
ordenada por citação: é a busca do "top-3 mais citados" da inclusão forçada (cap. 4) e do "paper que
abriu a divisão" (cap. 2.4). Só roda depois do mapa v1 existir.

---

## Histórico

- **v0 - 17/09/2026.** Sementes minhas (34) + sementes do Claude (8, de 15/09), sete grupos,
  strings compostas como texto. Nenhuma execução.
