# Pool de termos — screening da Etapa 1

**Versão:** v0 (17/09/2026) · **emenda 1 (21/09/2026)** — dois termos saem de `área` para o grupo novo `edge` (string-filha); ver §1 e Histórico. **Regra-mãe:** `docs/screening/metodo-screening-etapa1.md`, §2.
**O que é:** o vocabulário versionado do screening. As strings de busca são **composições** deste pool,
regeneradas a cada versão — nunca decretadas à parte. Nenhuma string abaixo foi executada; são texto,
prontas para a Fase 1 quando o Pedro mandar.

**Procedência dos termos:** `pedro` = sementes do Pedro, de conhecimento prévio, sem consulta;
`claude 15/09` = termos que o Claude acrescentou e o Pedro desconhece ou não lembraria de listar —
**não verificados contra survey nenhum** (nível 3 por definição); `survey:<id>` = termo que apareceu como nome de
divisão/seção na taxonomia de um survey aprovado (só a partir do pool v1).

---

## 1. Tabela do pool

Status: **ativo** · **aposentado** (fica na tabela, riscado, com motivo — nunca se apaga).
Retorno: nº de surveys aprovados que o termo trouxe — preenchido pela Fase 1; vazio = não rodado.

### Grupo `filtro-tipo` — o que restringe a busca a fontes de screening

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| survey | "a survey", "comprehensive survey", "systematic survey" | pedro | ativo | |
| review | "literature review", "a review" | pedro | ativo | |
| overview | "an overview" | pedro | ativo | |
| taxonomy | "a taxonomy" | pedro | ativo | |

### Grupo `área` — sinônimos do nome da área (compõem a string-mãe)

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| efficient inference | "inference efficiency" | pedro | ativo | |
| inference optimization | "inference acceleration", "accelerating inference" | pedro | ativo | |
| model compression | "compressing", "compression techniques" | pedro | ativo | |
| efficient large language models | "efficient LLMs", "efficient LLM" | pedro | ativo | |
| efficient transformers | "efficient transformer" | pedro | ativo | |
| efficient deep learning | "efficient neural networks", "efficient deep neural networks" | pedro | ativo | |
| LLM serving | "serving large language models", "LLM inference serving" | pedro | ativo | |
| efficient NLP | "green NLP", "efficient methods for NLP" | pedro | ativo | |

### Grupo `edge` — implantação em dispositivo restrito (string-filha; **fora da string-mãe**)

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| resource-efficient | "resource-constrained", "resource-limited" | pedro | ativo | exec. 1 (na mãe): puxou ruído fora da área — IoT, quântica, fotônica, materiais |
| on-device | "edge deployment", "edge devices", "mobile deployment" | pedro | ativo | exec. 1 (na mãe): idem; no arXiv `on-device` bateu 30 de 409 |
| lightweight | "lightweight models", "lightweight deep learning", "lightweight neural networks" | retorno exec. 3 (22/09, emenda 5) | ativo | não rodado — lacuna: *Lightweight Deep Learning: An Overview* perdido no teste |
| embedded | "embedded systems", "embedded devices", "embedded deployment" | retorno exec. 3 (22/09, emenda 5) | ativo | não rodado — lacuna: *Resource-Efficient Neural Networks for Embedded Systems* perdido no teste |

*Mudança de grupo (Pedro, 21/09, calibração sobre o bruto da execução 1):* os dois termos estavam
em `área` e compunham a string-mãe. Casados com `review` solto, trouxeram a maior parte do ruído
fora da área (pool §4, observação 3). Passam a **string-filha** própria: continuam no pool, com os
mesmos termos e variantes, mas só rodam na filha `edge` — não na mãe. A mãe da execução 2 é
regenerada sem eles (§4.1).

### Grupo `compressão` — técnicas sobre o modelo antes da implantação

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| knowledge distillation | distillation, "distilling", "teacher-student" | **pedro** ("destilação") | ativo | |
| reasoning distillation | "chain-of-thought distillation", "rationale distillation", "distilling step-by-step", "CoT distillation" | **pedro** ("destilação de raciocínio") | ativo | |
| quantization | "post-training quantization", PTQ, "quantization-aware training", QAT, "weight-only quantization", "low-bit" | **pedro** | ativo | |
| pruning | "network pruning", "structured pruning", "unstructured pruning", sparsity, "sparse" | **pedro** | ativo | |
| tensor decomposition | "low-rank factorization", "low-rank approximation", "low-rank decomposition", "matrix factorization" | claude 15/09 | ativo | |
| small language models | SLM, SLMs, "small LMs", "compact language models" | **pedro** ("SLMs") | ativo | |

### Grupo `inferência/serving` — técnicas que agem na inferência

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| memory management | "KV cache", "key-value cache", "paged attention", "memory-efficient inference" | claude 15/09 | ativo | |
| continuous batching | "dynamic batching", "in-flight batching", "iteration-level scheduling" | claude 15/09 | ativo | |
| early exiting | "early exit", "adaptive computation", "dynamic inference", "adaptive depth" | **pedro** | ativo | |
| efficient attention | FlashAttention, "linear attention", "sparse attention", "attention approximation" | pedro | ativo | |
| KV cache compression | "KV cache quantization", "cache eviction", "token eviction" | claude 15/09 | ativo | |
| speculative decoding | "speculative sampling", "draft model", "parallel decoding" | claude 15/09 | ativo | |
| kernels and compilers | "operator fusion", "kernel optimization", "model compiler", "hardware-aware" | claude 15/09 | ativo | |

### Grupo `ferramentas` — como se acha a ferramenta (criado pelo Pedro em 22/09; pilar de §3, eixo de atividade §3.3)

Retornos medidos em 22/09 (S2, `+ (survey|review|overview|taxonomy)`, 2020+, CS, cit >= 60) — **a
expectativa é baixa por natureza: a área não faz survey da própria ferramenta**, ela documenta.

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| inference engine | "inference system", "LLM inference framework" | pedro (vinha do grupo `inferência/serving`; movido em 22/09) | ativo | 2 (TinyML; RRAM) |
| model serving | "serving system", "serving framework", "model server" | claude 22/09 | ativo | 3 / 1 — só 1 na área (serving de LLM generativo) |
| deployment framework | "deployment toolkit", "deployment pipeline" | claude 22/09 | ativo | 1 |
| inference library | "runtime library" | claude 22/09 | ativo | 1 |
| deep learning compiler | "model compiler", "tensor compiler", "graph compiler" | claude 22/09 | ativo | 1 / 1 |
| inference server | "inference runtime" | claude 22/09 | ativo | **0 / 0** — mantido: retorno zero só aposenta após rodada completa *e* nenhum survey usando (§3) |

**Fora do grupo, por medição de 22/09:** `machine learning systems` (56 — frase genérica: XAI, domain
generalization, saúde), `benchmarking` (1.374), `toolkit` (116) e `inference framework` (3, **todos de
*causal inference*** — "inference" é ambíguo entre inferência estatística e inferência de modelo).
Não entram: trariam ruído sem trazer ferramenta.

**Como este grupo roda:** **sem `filtro-tipo`** (§2) — procura paper de sistema, não survey. As
outras rotas de descoberta do pilar ferramentas estão no método §3: ferramentas **nomeadas pelos
surveys** durante a extração (§7, rota de custo zero), ementas de curso (§4.1) e registros de
ecossistema — HF, ONNX, MLPerf Inference — como descoberta **nível 3, não citável**.

**Nota de fronteira:** `kernels and compilers` fica no grupo `inferência/serving` porque as variantes
dele (operator fusion, kernel optimization) são **técnica**; só o compilador como software veio para
cá, como `deep learning compiler` (§3.1, ferramenta x técnica).

### Grupo `dado/confiança` — eixo (iii) de §1.2 e "saber quando confiar"

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| data-efficient | "label-efficient", "few labels", "low-resource", "sample-efficient" | pedro | ativo | |
| weak supervision | "distant supervision", "LLM-generated labels", "synthetic labels" | claude 15/09 | ativo | |
| calibration | "confidence calibration", "uncertainty estimation", "selective prediction" | claude 15/09 | ativo | |

### Grupo `adaptação` — dentro por §1.2 (efeito no serving)

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| parameter-efficient fine-tuning | PEFT, "parameter-efficient", adapters | pedro | ativo | |
| LoRA | "low-rank adaptation", "multi-LoRA serving", "adapter serving" | pedro | ativo | |
| mixture of experts | MoE, "conditional computation", "sparse activation" | pedro | ativo | |

### Grupo `arquiteturas` — pilar fixo (§1.1)

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| transformer architecture | "transformer models", "transformers" | pedro | ativo | |
| encoder-only / decoder-only / encoder-decoder | "encoder-decoder", "decoder-only", "encoder-only", "architecture comparison" | pedro | ativo | |
| pre-training objectives | "masked language modeling", MLM, "causal language modeling", "span corruption", "denoising" | pedro | ativo | |
| attention mechanism | "self-attention", "multi-head attention", "cross-attention" | pedro | ativo | |
| positional encoding | "rotary position embedding", RoPE, "relative position" | pedro | ativo | |
| tokenization | "subword tokenization", BPE, "vocabulary size" | pedro | ativo | |
| sequence-to-sequence | seq2seq, RNN, LSTM, "neural attention", "attention-based" | pedro (base pré-transformer, §1.3) | ativo | |

### Grupo `uso?` — a testar contra §1.2

| termo (en) | variantes | origem | status | retorno |
|---|---|---|---|---|
| prompt engineering | prompting, "prompt optimization", "prompt compression" | **pedro** | ativo — **testar §1.2** no confronto; "prompt compression" pode ser a variante que pertence | |
| MLOps | "machine learning operations", "ML lifecycle", "continuous delivery for ML" | claude 22/09 | ativo — **testar §1.2** | 11, cluster coerente (*MLOps: Overview, Definition and Architecture*; *MLOps: A Taxonomy and a Methodology*). **O caso mais interessante da lista:** descreve **atividades** de implantação — insumo direto do eixo de §3.2 — mas não reduz custo em nenhum dos três eixos de §1.2. Decisão do Pedro no confronto |
| model deployment | "deploying machine learning", "production deployment" | claude 22/09 | ativo — **testar §1.2** | 27, mistura saúde/ASR/IoT; 1–2 na área |

---

## 2. Regras de composição

- **string-mãe** = (grupo `área` unido por OR) AND (grupo `filtro-tipo` unido por OR).
- **string-filha de um grupo G** = (termos e variantes de G unidos por OR) AND (`filtro-tipo`).
- **Exceção — a filha `ferramentas` roda SEM `filtro-tipo`** (Pedro, 22/09): o pilar ferramentas
  quer **paper de sistema** (vLLM/PagedAttention, FlashAttention, LightSeq, TensorRT), que por
  definição não é survey — o filtro de tipo barraria exatamente o que se procura. Mesma forma da
  §4.3 (seminal e história). Precedência do §3 do método vale: se a ferramenta tem paper, o paper é
  a fonte; senão, a página de visão geral. *Precedente registrado:* na Fase 1 o **LightSeq** apareceu
  e foi classificado "não é survey — candidato a ferramenta (§3.1)" — barrado pelo filtro de tipo
  sendo o que o pilar ferramentas procura.
- Variantes entram na mesma string que o termo — são o mesmo conceito com outra grafia.
- Toda string leva a versão do pool que a gerou (`pool v0`) e a data.
- Filtros de §3.2 e §11 vão **embutidos na base** quando ela permite (ano ≥ 2020; citações ≥ 100 como
  uma das pernas; tipo = review). Onde a base não permite, o filtro é aplicado à mão sobre o retorno.
- **Filtro de ano só para mapa e divisões.** Buscas de história (§2.4) e seminais (§4) rodam a
  string-filha **sem** o filtro de tipo e **sem** o filtro de ano.

## 3. Regras de entrada e saída do pool

- **Entra:** como semente (origem `pedro` ou `claude`, só no v0) **ou** quando aparece como nome de
  divisão ou de seção na taxonomia de um survey aprovado (origem `survey:<id>`, do v1 em diante).
  Termo trazido por survey é a única via de entrada depois do v0.
- **Aposenta:** se, depois de uma rodada completa, teve **retorno zero** *e* **nenhum survey
  aprovado o usa**. Fica na tabela, riscado, com motivo e data. Não se apaga: é dado do confronto
  (§2.1 do método).
- **Muda de grupo:** quando um survey aprovado o classifica em outra divisão — anotar a origem da
  mudança.
- **Revisão por evidência de retorno (Pedro, 22/09 — ⟨rev-25⟩ do método):** o pool também muda por
  evidência do **próprio retorno**, não só por survey. Uma regra, **duas direções**:

  | direção | evidência | quando se decide | consequência |
  |---|---|---|---|
  | **(a) ruído** — o termo devolve majoritariamente coisa fora da área (§1.2) | o **bruto**, antes de qualquer classificação | logo depois da busca | o termo **sai da string em que polui e passa a rodar numa string-filha própria** |
  | **(b) lacuna** — célula vazia ou bolha de 1 no bubble plot A (§9.1), **ou pergunta de §1.4 do método sem termo que a cubra** (Pedro, 22/09, A4) | o **registro**, depois da extração; ou o confronto do pool com as perguntas | a cada rodada | pergunta "lacuna da **área** ou da **busca**?"; se da busca, termo novo ou string nova |

  **Cláusula anti-viés, que é o coração da regra:** em (a) o termo **nunca é apagado nem apenas
  removido** — ele é obrigado a rodar na filha, e o bruto que motivou a mudança fica salvo. Se o
  termo só saísse, a área encolheria para o que o Pedro já acreditava, que é exatamente o que o
  método existe para evitar. Consequência direta: **a string-filha de um termo movido não é
  opcional** — a filha `edge` passa a ser obrigatória por esta regra.
  Toda revisão por retorno leva **motivo, data e o arquivo de bruto** que a sustenta.

- **Versão × emenda (Pedro, 22/09):** **versão** = rodada de saturação (v0, v1, v2+, por ⟨rev-22⟩);
  **emenda** = ajuste por evidência de retorno **dentro** de uma versão, numerada (emenda 1, 2, …).
  Emenda não avança a versão; a versão é o que o confronto de vereditos usa.

- **Versões:** v0 = sementes (este arquivo). **v1** = após saturação do mapa (§5.1), com os termos
  que os surveys trouxeram e as strings regeneradas. v2+ = revisões por divisão.
- **Veredito por termo (Pedro, 21/09 — ⟨rev-22⟩ do método):** reescrito **a cada rodada de
  saturação** — no v1 e em cada v2+. Uma rodada = uma versão do pool = uma coluna `veredito-vN`.

## 4. Strings v0 compostas

**Execução 1 — 21/09/2026, ordem do Pedro.** String-mãe rodada em Semantic Scholar (bulk; três
variantes: A tipo=Review + cit>=100 → 1.721; B tipo=Review sem piso → 41.412; C sem tipo + cit>=100
→ 1.734) e arXiv (409). Retorno bruto sem filtro em `screening/fase1/raw/*.json`; leitura em
`screening/fase1/2026-09-21-string-mae-retorno-bruto.md`. Google Scholar não rodado (manual).
Observações do bruto, para calibrar §3.2 antes de qualquer filtro: (1) A e C são quase iguais (13
papers de diferença) — a etiqueta *Review* do S2 é redundante com piso de citação + palavra de tipo;
(2) A é dominada por 2020–2021 (1.167 de 1.721) e tem 19 de 2025 — o piso de 100 citações penaliza
o recente, como §3.2 previa; (3) a maior parte do retorno S2 é ruído fora da área (IoT, quântica,
fotônica, materiais, COVID), puxado pelos termos largos `resource-constrained`, `on-device`,
`resource-efficient` casados com `review` como palavra solta; (4) no arXiv, onde o resumo está
disponível, os termos que mais bateram foram `model compression` (46), `resource-constrained` (37),
`on-device` (30), `resource-efficient` (18), `efficient inference` (13); `efficient transformers`,
`efficient neural networks` e `serving large language models` bateram 1 vez cada.

**Execução 2 — 21/09/2026, após a calibração (a)/(b) do Pedro.** String-mãe regenerada sem os termos de
`edge`, piso 60. Semantic Scholar: A2 (Review, >= 60) → **100**; C2 (sem tipo, >= 60) → **103**, com A2 ⊂ C2.
arXiv → **89**. Bruto em `screening/fase1/raw/*exec2*.json` e `*A2*`/`*C2*`; lista de candidatos com decisão por
obra em `screening/fase1/2026-09-21-candidatos-string-mae-exec2.md` (155 linhas: 58 entra · 9 não entra —
sem filtro · 36 borda §1.2 · 40 fora · 12 não é survey). Observações: (1) tirar os três termos de `edge`
derrubou o retorno em ~94% mesmo com piso menor — eles *eram* o ruído; (2) a etiqueta *Review* do S2 é
redundante (A2 ⊂ C2), bastam piso + palavra de tipo; (3) o piso 60 trouxe 38 obras entre 60 e 99, quase
todas dentro da área — o piso 100 estava cortando surveys de 2024–25; (4) contagem nos **títulos** das 58 obras
que entraram (substring, contado 21/09): compress 14 · edge 12 · distill 4 · efficient inference 4 ·
efficient large language 4 · resource-efficient 4 (o termo saiu da mãe, mas os surveys que o usam no
título continuam vindo por outros termos) · serving 3 · embedded 3 · pruning 2 · quantization 1 ·
`efficient NLP`/`tinyml` 0 no título (o Treviso et al. 2022 entrou como "Efficient Methods for NLP").

### 4.1 String-mãe (mapa da área) — forma da execução 2 (emenda 1: sem os termos de `edge`)

**Semantic Scholar** (`/graph/v1/paper/search/bulk`; `+` = AND, `|` = OR, aspas = frase; filtros como
parâmetros — sintaxe a validar na primeira execução):

```
query = ("efficient inference" | "inference efficiency" | "inference optimization" | "inference acceleration" | "model compression" | "efficient large language models" | "efficient LLMs" | "efficient transformers" | "efficient deep learning" | "efficient neural networks" | "LLM serving" | "serving large language models" | "efficient NLP") + (survey | review | overview | taxonomy)
year = 2020-
fieldsOfStudy = Computer Science
publicationTypes = Review        # perna (a)/(b) de §3.2: rodar também SEM este filtro e cruzar
# minCitationCount: REMOVIDO da busca (Pedro, 22/09, rev-30). O piso e criterio de REGISTRO (metodo 3.2), nao de busca:
#   buscar largo -> classificar por relevancia (1.2) -> filtrar por qualidade (3.2, piso 60).
#   Motivo: piso na busca e idade disfarcada de qualidade. Populacao sem piso no S2: 863.
sort = citationCount:desc
```

**arXiv** (API `search_query`; campos `ti:` título, `abs:` resumo; `AND`/`OR`; sintaxe a validar):

```
(ti:survey OR ti:review OR ti:overview OR ti:taxonomy) AND (abs:"efficient inference" OR abs:"inference optimization" OR abs:"inference acceleration" OR abs:"model compression" OR abs:"efficient large language models" OR abs:"efficient LLM" OR abs:"efficient transformers" OR abs:"efficient deep learning" OR abs:"LLM serving" OR abs:"serving large language models" OR abs:"efficient NLP") AND (cat:cs.CL OR cat:cs.LG OR cat:cs.AI)
submittedDate: [20200101 TO *]
```

**Google Scholar** (manual; `OR` e aspas; ano pelo filtro da interface, ≥ 2020; sem filtro de citação —
aplicar à mão):

```
(survey OR review OR overview) ("efficient inference" OR "model compression" OR "efficient large language models" OR "efficient transformers" OR "efficient deep learning" OR "LLM serving")
```

### 4.2 Strings-filhas (uma por grupo) — forma geral

Mesma estrutura da mãe, trocando o bloco de área pelo bloco do grupo. Exemplo, grupo `compressão`,
Semantic Scholar:

```
query = ("knowledge distillation" | distillation | "reasoning distillation" | "chain-of-thought distillation" | "rationale distillation" | quantization | "post-training quantization" | "quantization-aware" | "weight-only quantization" | pruning | sparsity | "tensor decomposition" | "low-rank factorization" | "low-rank approximation" | "small language models" | SLMs) + (survey | review | overview | taxonomy)
year = 2020-  ·  fieldsOfStudy = Computer Science  ·  sort = citationCount:desc
```

Filha `edge` (emenda 1), Semantic Scholar — os termos que saíram da mãe:

```
query = ("resource-efficient" | "resource-constrained" | "resource-limited" | "on-device" | "edge deployment" | "edge devices" | "mobile deployment") + (survey | review | overview | taxonomy)
year = 2020-  ·  fieldsOfStudy = Computer Science  ·  sort = citationCount:desc
```
Esta filha é a que mais precisa do contorno de §1.2 na triagem: os termos são largos e pegam IoT,
redes e hardware sem modelo.

As outras cinco filhas (`inferência/serving`, `dado/confiança`, `adaptação`, `arquiteturas`, `uso?`)
seguem o mesmo molde com os termos da tabela; são geradas na hora da execução a partir do pool, não
mantidas à mão — para não divergir da tabela.

### 4.3 Strings de seminal e história (sem filtro de tipo, sem filtro de ano)

Para cada divisão do mapa v1, a string-filha da divisão **sem** o bloco `filtro-tipo` e **sem** ano,
ordenada por citação — é a busca do "top-3 mais citados" da inclusão forçada (§4) e do "paper que
abriu a divisão" (§2.4). Só roda depois do mapa v1 existir.

---

## Histórico

- **v0 — 17/09/2026.** Sementes do Pedro (34) + sementes do Claude (8, de 15/09), sete grupos,
  strings compostas como texto. Nenhuma execução.
- **v0 — emenda 1 — 21/09/2026.** *(Autorizada retroativamente pela regra "revisão por evidência de
  retorno", direção (a), escrita em 22/09 — na data em que foi feita, a regra não existia; ver §3.)* Calibração do Pedro sobre o bruto da execução 1: (a)
  `resource-efficient` e `on-device` saem de `área` para o grupo novo `edge`, string-filha, fora da
  mãe; (b) piso de citação da mãe em teste a 60 (era 100). Strings de §4.1 regeneradas. Não é
  versão nova do pool (⟨rev-22⟩: versão = rodada de saturação); é emenda dentro do v0.
- **v0 — emenda 2 — 22/09/2026.** Criado o grupo `ferramentas` (decisão do Pedro), com 6 termos —
  1 movido de `inferência/serving` (`inference engine`) e 5 novos, todos com retorno medido no dia.
  `MLOps` e `model deployment` entraram em `uso?`, a testar contra §1.2. Ficaram de fora, por
  medição, `machine learning systems`, `benchmarking`, `toolkit` e `inference framework` (ruído).
  **Achado que motivou o registro:** termo preciso de ferramenta devolve 0–3 surveys — a área
  documenta suas ferramentas, não as pesquisa. O pilar ferramentas depende de documentação (§3) e
  ementas (§4.1) tanto quanto da busca.
  *Gatilho desta emenda: confronto do pool com as perguntas de §1.4 (Q5) — ver pendência A2.*
- **v0 — emenda 3 — 22/09/2026.** A filha `ferramentas` passa a rodar **sem `filtro-tipo`** (exceção
  registrada em §2), para alcançar paper de sistema. Decisão do Pedro, junto com as outras duas rotas
  de descoberta fora de survey (extração de ferramentas nomeadas; registros de ecossistema em nível 3),
  escritas no método §3, §6 e §7 ⟨rev-29⟩.
- **v0 — emenda 4 — 22/09/2026.** O **piso de citação sai da string** (Pedro): a busca roda sem piso
  e o piso passa a valer só no registro (método §3.2, valor 60). População no S2 com a string-mãe
  limpa e sem piso: **863** — e não os 41.412 da execução 1, que foram medidos com a string suja.
- **v0 — emenda 5 — 22/09/2026.** Revisão por evidência de retorno, **direção (b), lacuna** (§3):
  entram `lightweight` e `embedded` no grupo `edge`, porque obras da área que usam essas palavras no
  título foram perdidas no teste de recuperação da volta 1 da execução 3
  (`docs/screening/fase1/2026-09-22-volta-1-radicais.md`). Pedido do Pedro: *"deixe tudo igual, só preencha
  as lacunas do pool que foram reveladas"* — filtros e seleção da volta 1 não mudam.
  **`small language models` não muda:** o termo já está no pool (grupo `compressão`); a perda veio do
  filtro por radicais, que tratou *small* e *language* como genéricas — defeito do filtro, não lacuna
  do pool. Os dois termos novos ainda **não rodaram**.
