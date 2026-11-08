# Calibração da cadeia de agentes (M4) — relatório (26/09)

**Procedência: nível 3.** Os vereditos são de agentes que leram título e abstract (agentes 1 e 2) ou só as
frases transcritas (agente 3). Ninguém leu as obras. Serve para saber se a cadeia é confiável o bastante
para a F2, não para decidir nenhuma obra.

## 1. O que foi feito e por quê

Antes de gastar ~115 chamadas de agente na F2, a cadeia rodou sobre um conjunto em que **a resposta já é
conhecida** (M4, decidido em 23/09):

- **28 obras de ajuste do gabarito**: surveys da área, a mesma metade de ajuste da camada B e da F1
  (semente 42). A metade de teste (29) continua intocada, reservada para medir a perda no fim.
- **30 obras sorteadas das excluídas na camada A** (semente 26): lixo conhecido, excluído por campo de estudo.

As 58 obras foram embaralhadas e ganharam ids anônimos (C01–C58), para nenhum agente ver a origem. O
gabarito ficou num arquivo separado que os agentes não liam.

| Agente | Modelo | Chamadas | Entra | Sai |
|---|---|---|---|---|
| 1, triagem do óbvio | Haiku | 2 | 58 | 18 claramente fora · 38 passa · 2 sem acesso |
| 2, extração | Haiku | 2 | 40 | 143 frases (3,6 por obra) |
| 3, julgamento | Sonnet | 2 | 40 (só as frases) | 26 relevante · 11 fora · 1 dúvida · 2 sem acesso |

Roteiros: `docs/screening/agentes/roteiro-agente-{1,2,3}-v1.md`.

## 2. Resultado contra as metas

| Meta (M4) | Resultado | |
|---|---|---|
| Agente 1 não elimina nenhuma das 28 de ajuste | **0 eliminadas** (27 passa, 1 sem acesso) | cumprida |
| Agente 3 marca relevante ou dúvida em >= 90% das 28 | **26 de 27 acessíveis = 96%** | cumprida |
| (extra) Lixo que chega a `relevante` | **0 de 30** (28 fora, 1 dúvida, 1 sem acesso) | — |

**O único erro contra o gabarito não é erro do agente.** C45, *Resource-Efficient Convolutional Networks: A
Survey…*, recebeu `fora` pela regra §1.2.1 (b): técnica da área aplicada só a CNN. Essa regra foi decidida em
22/09 (⟨rev-34⟩). O gabarito é de 21/09, **de antes da regra**. O agente aplicou o método; o gabarito é que
ficou velho. Isso entra na revisão do gabarito que você já pediu.

**Os 2 `sem acesso`** (C18, lixo; C43, ajuste: *Deep Model Compression and Architecture Optimization for Embedded
Systems: A Survey*) passaram pelas rotas floresta -> S2 -> OpenAlex sem abstract. Nenhum agente decidiu sobre
eles (M6). C43 é um survey da área sem abstract acessível, exatamente o caso do Agrawal: vai para a lista
`sem acesso` da volta.

## 3. Achado: o agente 2 nem sempre copia

Das 143 frases, **14 não batem exatamente com o texto** (10%):

- **Tipografia (~6):** aspas curvas trocadas por retas, `deg$^2$` virou `deg²`, maiúscula no começo. Não muda nada.
- **Alteração real (~8, 6%):** sigla expandida ("KD plays a crucial role" virou "Knowledge Distillation (KD)
  plays…"); dois trechos colados numa frase só; itens de lista retirados; "provide" virou "provides". O
  sentido se mantém em todos os casos, mas o contrato era "cópia exata", e o agente 3 julga só com isso.

**Correção proposta para a F2 (roteiro do agente 2 v2 + conferência por script):**
1. O roteiro proíbe explicitamente expandir sigla, colar trechos e editar listas.
2. Um script confere cada frase contra o abstract. A tipografia é normalizada antes da comparação. Frase
   que não bate fica marcada `não verbatim` no arquivo e na auditoria, sem ser apagada.

A calibração não foi refeita com a v2: o agente 3 cumpriu a meta mesmo com essas frases, e a v2 só aperta.

## 4. O rótulo de objetivo (decidido em 26/09: só ordena)

Entre as 26 relevantes: **21 `saber`** · **5 `saber + saber fazer`** · 0 só `saber fazer`. É o que se esperava
de uma população de surveys (§3 do plano): o saber fazer vai morar nos papers de sistema e de ferramenta.

## 5. Um desvio do desenho, declarado

O M3 previa **exemplos do gabarito de ajuste** dentro dos roteiros. Não coloquei: a calibração mede a cadeia
justamente sobre essas 28 obras, e com exemplos dentro do roteiro o teste mediria memória, não julgamento. Os
roteiros v1 têm só as regras do método. Como a meta foi cumprida sem exemplos, proponho manter assim na F2.

## 6. Tabela obra a obra

| id | origem | título | agente 1 | agente 3 | regra | objetivo |
|---|---|---|---|---|---|---|
| C01 | ajuste | Beyond Efficiency: A Systematic Survey of Resource-Efficient Large Language Models | passa | relevante | §1.2.1 (a) | saber + saber fazer |
| C03 | ajuste | A Survey on Knowledge Distillation of Large Language Models | passa | relevante | §1.2.1 (a) | saber |
| C08 | ajuste | Sparsity in Deep Learning: Pruning and growth for efficient inference and training in neur | passa | relevante | §1.2.1 (a) | saber + saber fazer |
| C09 | ajuste | Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective | passa | relevante | §1.2.1 (a) · (e) | saber + saber fazer |
| C10 | ajuste | Knowledge Distillation and Student-Teacher Learning for Visual Intelligence: A Review and  | passa | relevante | §1.2.1 (a) | saber |
| C11 | ajuste | A survey of model compression techniques: past, present, and future | passa | relevante | §1.2.1 (a) | saber |
| C12 | ajuste | Efficient Inference for Large Reasoning Models: A Survey | passa | relevante | §1.2.1 (a) | saber |
| C13 | ajuste | Model Compression and Efficient Inference for Large Language Models: A Survey | passa | relevante | §1.2.1 (a) | saber + saber fazer |
| C17 | ajuste | Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | passa | relevante | §1.2.1 (a) · (d) | saber |
| C19 | ajuste | Efficient Reasoning Models: A Survey | passa | relevante | §1.2.1 (a) | saber |
| C21 | ajuste | Knowledge distillation and dataset distillation of large language models: emerging trends, | passa | relevante | §1.2.1 (a) | saber |
| C28 | ajuste | Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Sys | passa | relevante | §1.2.1 (a) · (d) | saber |
| C31 | ajuste | Bringing AI To Edge: From Deep Learning's Perspective | passa | relevante | §1.2.1 (a) · (d) | saber |
| C34 | ajuste | An Overview of Neural Network Compression | passa | relevante | §1.2.1 (a) | saber |
| C35 | ajuste | Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimiza | passa | relevante | §1.2 (i) · §1.2.1 (a) | saber |
| C40 | ajuste | Vision Transformers on the Edge: A Comprehensive Survey of Model Compression and Accelerat | passa | relevante | §1.2.1 (a) | saber |
| C42 | ajuste | Knowledge Distillation: A Survey | passa | relevante | §1.2 (ii) · §1.2.1 (a) | saber |
| C43 | ajuste | Deep Model Compression and Architecture Optimization for Embedded Systems: A Survey | sem acesso | sem acesso |  |  |
| C44 | ajuste | LLM Inference Unveiled: Survey and Roofline Model Insights | passa | relevante | §1.2 (i) · §1.2.1 (a) | saber + saber fazer |
| C45 | ajuste | Resource-Efficient Convolutional Networks: A Survey on Model-, Arithmetic-, and Implementa | passa | fora | §1.2.1 (b) |  |
| C46 | ajuste | Edge Intelligence: A Review of Deep Neural Network Inference in Resource-Limited Environme | passa | relevante | §1.2.1 (d) | saber |
| C50 | ajuste | Full Stack Optimization of Transformer Inference: a Survey | passa | relevante | §1.2 (i) · §1.2.1 (a) | saber |
| C51 | ajuste | Efficient Neural Networks for Tiny Machine Learning: A Comprehensive Review | passa | relevante | §1.2.1 (d) | saber |
| C53 | ajuste | A Survey on Efficient Inference for Large Language Models | passa | relevante | §1.2 (i) · §1.2.1 (a) | saber |
| C54 | ajuste | Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculat | passa | relevante | §1.2 (i) · §1.2.1 (a) | saber |
| C56 | ajuste | Efficient Methods for Natural Language Processing: A Survey | passa | relevante | §1.2 (i) · §1.2.1 (a) | saber |
| C57 | ajuste | Compressing Large-Scale Transformer-Based Models: A Case Study on BERT | passa | relevante | §1.2 (ii) · §1.2.1 (a) | saber |
| C58 | ajuste | Hardware-Aware Neural Architecture Search: Survey and Taxonomy | passa | relevante | §1.2 (ii) · §1.2.1 (a) | saber |
| C02 | lixo_A | Recent progress in material selection and device designs for photoelectrochemical water-sp | claramente fora | — |  |  |
| C04 | lixo_A | Synaptic devices based on semiconductor nanocrystals | claramente fora | — |  |  |
| C05 | lixo_A | TEGLIE: Transformer encoders as strong gravitational lens finders in KiDS. From simulation | passa | fora | §3.4 não é survey · fora da área |  |
| C06 | lixo_A | Framework for the Provision of User Felt Protected Mobile Banking Services | claramente fora | — |  |  |
| C07 | lixo_A | From Inquiry to Purchase: An LLM-Powered Framework for Uncovering Granular Consumer Decisi | passa | fora | §3.4 não é survey · fora da área |  |
| C14 | lixo_A | Application of Artificial Intelligence to Predict CO2 Emissions: Critical Step towards Sus | claramente fora | — |  |  |
| C15 | lixo_A | Turning a new leaf: PhenoVision provides leaf phenology data at the global scale | passa | fora | §3.4 não é survey · fora da área |  |
| C16 | lixo_A | On the peer review reports: does size matter? | claramente fora | — |  |  |
| C18 | lixo_A | ICT adoption among women-owned SMEs in a matrilineal society: evidence from West Sumatra,  | sem acesso | sem acesso |  |  |
| C20 | lixo_A | "Talk to me, I'm secure": investigating information disclosure to AI chatbots in the conte | claramente fora | — |  |  |
| C22 | lixo_A | Comprehensive review of hyperspectral image compression algorithms | claramente fora | — |  |  |
| C23 | lixo_A | Design for Hope: Cultivating Deliberate Hope in the Face of Complex Societal Challenges | claramente fora | — |  |  |
| C24 | lixo_A | Application of Hybrid Intelligent Systems for Forecasting and Managing Sustainable Develop | claramente fora | — |  |  |
| C25 | lixo_A | Unbiasing Greek: In-Context Learning Strategies for Gender Bias Identification and Mitigat | passa | fora | §3.4 não é survey · fora da área |  |
| C26 | lixo_A | Establishing Coupled Models for Estimating Daily Dew Point Temperature Using Nature-Inspir | claramente fora | — |  |  |
| C27 | lixo_A | Foundation Models for Environmental Science: A Survey of Emerging Frontiers | passa | dúvida | §1.2.1 (c) |  |
| C29 | lixo_A | BSL: Sustainable Collaborative Inference in Intelligent Transportation Systems | passa | fora | §3.4 não é survey · primário da área |  |
| C30 | lixo_A | The consequences of online partisan media | claramente fora | — |  |  |
| C32 | lixo_A | TRANSFORMING AGILE PROJECT MANAGEMENT THROUGH ARTIFICIAL INTELLIGENCE | claramente fora | — |  |  |
| C33 | lixo_A | Maintaining Transient Diversity Is a General Principle for Improving Collective Problem So | claramente fora | — |  |  |
| C36 | lixo_A | Evaluating Large Language Models as Tools to Navigate Researchers in Rapidly Evolving Rese | passa | fora | §3.4 nao e survey · fora da area |  |
| C37 | lixo_A | Machine Learning-Aided Real-Time Optimized Multibeam for 6G Integrated Satellite-Terrestri | passa | fora | §3.4 nao e survey · fora da area |  |
| C38 | lixo_A | TALES: A Taxonomy and Analysis of Cultural Representations in LLM-generated Stories | passa | fora | §3.4 nao e survey · fora da area |  |
| C39 | lixo_A | Learnings from a Retail Recommendation System on Billions of Interactions at bol.com | passa | fora | §3.4 nao e survey · sistema/ferramenta |  |
| C41 | lixo_A | A Dataset for Studying the Relationship between Human and Smart Devices | claramente fora | — |  |  |
| C47 | lixo_A | Harnessing Digital Phenotyping to Advance University Student Mental Health (Brightline): S | claramente fora | — |  |  |
| C48 | lixo_A | FUZZY APPLICATION (MAMDANI METHOD) IN DECISION-MAKING ON LED TV SELECTION | claramente fora | — |  |  |
| C49 | lixo_A | Causal Artificial Intelligence in Legal Language Processing: A Systematic Review | passa | fora | §1.2.1 sem eixo |  |
| C52 | lixo_A | Micromobility Sensing Systems and Safety Services: A Brief Review | claramente fora | — |  |  |
| C55 | lixo_A | Adoption of Artificial Intelligence in Organizational Coaching Processes | claramente fora | — |  |  |
## 7. Decisões suas

1. **A calibração serve?** Se sim, a F2 roda com as 962 leituras (plano §4, passos 3 a 6).
2. **Roteiro do agente 2 v2 + conferência por script (§3):** ok?
3. **Roteiros sem exemplos do gabarito (§5):** ok?
4. **C45 (CNN):** confirma que sai do gabarito pela regra §1.2.1 (b)? Isso entra na revisão do gabarito.

## 8. Arquivos

`docs/screening/fase1/agentes/calibracao/`: `entrada.json` (as 58, anônimas) · `gabarito-oculto.json` · `a1-*`,
`a2-*`, `a3-*` (entrada e saída por lote) · `tabela.md`. Script: `scripts/screening/agentes/calib_prep.py`.

**Respostas do Pedro (26/09):** (1) calibração serve, F2 liberada; (2) roteiro v2 do agente 2 + conferência por
script: sim; (3) roteiros sem exemplos do gabarito: sim; (4) **C45 fica no gabarito** ("pode deixar lá").
