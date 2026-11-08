# Tópicos de Interesse — CSCE 2026 (ICAI'26 / ICDATA'26 / ACC'26)

Congresso: **CSCE'26** — 2026 World Congress in Computer Science, Computer Engineering, & Applied Computing
Data/Local: **20–23 de julho de 2026**, Luxor (MGM), Las Vegas, USA
Publicação: **Springer Nature** (proceedings indexados em Scopus, DBLP, EI Compendex, CPCI/Web of Science, ACM DL, MathSciNet)
Estrutura: 21 tracks principais, 112 sessões técnicas/painéis, 1.000–1.500 participantes

Fontes (extraídas em 17/08/2026):
- ICAI'26 — https://www.american-cse.org/csce2026/conferences-ICAI
- ICDATA'26 — https://icdatascience.org/cfp-topics/
- ACC'26 — https://www.american-cse.org/csce2026/conferences-ACC

---

## ⚠ Leitura crítica das CfPs (verificado em 17/08/2026)

Contagem literal de termos nas três páginas de tópicos:

| Termo | ICAI | ICDATA | ACC |
|---|---|---|---|
| `LLM` | 0 | 0 | 0 |
| `large language` | 0 | 1 | 0 |
| `generative` | 0 | 3 | 0 |
| `transformer`, `foundation model`, `agentic`, `diffusion`, `prompt`, `GPT`, `self-supervised`, `attention` | 0 | 0 | 0 |
| `deep learning` | 0 | 1 | 1 |
| `multimodal` | 0 | 0 | 1 |

**Nenhuma das 21 conferências do CSCE'26 tem track de LLM, GenAI ou foundation models.**
(21 tracks: ACC, BIOCOMP, BIOENG, CSC, EEE, ESCS, FCS, FECS, GCC, HIMS, ICAI, ICDATA, ICEQT, ICOMP, ICWN, IKE, IPCV, MSV, PDPTA, SAM, SERP)

Evidências de que as listas são recicladas sem revisão:
- `<title>` do ICDATA ainda diz "ICDATA'25 ... 21th ... 2025" enquanto o corpo diz "22th ... 2026"
- Menu do ICDATA: link rotulado `CSCE'25` apontando para o caminho `/csce19/`
- "22th"/"21th" (deveria ser 22nd/21st) sobrevivem há edições
- ICAI lista "Intelligent web-based business" e "Intelligent tutoring systems", mas não menciona deep learning

**Duas leituras possíveis — decidir qual adotar:**

1. *A CfP é filtro fraco.* A própria ICAI diz "not meant to be exhaustive". Trabalho moderno entra sob rótulo antigo (LLM → `A02 NLP` ou `E01 Deep Learning/LLM`). O rótulo é burocracia.
2. *O vocabulário revela a comunidade.* Se a CfP não menciona transformers em 2026, o público que ela atrai talvez também não trabalhe com isso — e o venue pode não ser onde quero ser reconhecido.

**Teste para decidir:** olhar o que foi de fato publicado, não o que a CfP anuncia →
https://link.springer.com/conference/csce-1

---

## Notas dos macro-temas

| Macro | Nota | Status |
|---|---|---|
| M1 LLMs/GenAI/NLP | 3 | ✔ micros pontuados (17/08/2026) |
| M2 Fundamentos ML/DL | 3 | ✔ micros pontuados (17/08/2026) |
| M3 Agentes/RL/autônomos | 2.5 | ✔ micros pontuados (17/08/2026) |
| M4 Grafos | 2.5 | ✔ micros pontuados (17/08/2026) |
| M5 Bayesianos/estatísticos | 2 | ✔ micros pontuados (17/08/2026) |
| M6 Otimização/meta-heurísticas | 2.5 | ✔ micros pontuados (17/08/2026) |
| M7 Fuzzy/rough sets | 2 | ✔ micros pontuados (17/08/2026) |
| M8 IA simbólica/conhecimento | 2 | ✔ micros pontuados (17/08/2026) |
| M9 Processo/qualidade de dados | 3 | ✔ micros pontuados (17/08/2026) — TODOS os micros = 3 |
| M10 Infra big data | 2.5 | ✔ micros pontuados (17/08/2026) |
| M11 Busca/IR/recomendação | 2.5 | ✔ micros pontuados (17/08/2026) |
| M12 Privacidade/segurança | 3 | ✔ micros pontuados (18/08/2026) |
| M13 Séries temporais | 2.5 | ✔ micros pontuados (18/08/2026) |
| M14 Visão/sinal/multimídia | 2.5 | ✔ micros pontuados (18/08/2026) |
| M15 Cognição/neuro-inspirados | 1 | ✔ micros pontuados (18/08/2026) — todos os micros = 1 |
| M16 Aplicações de domínio | 2.5 | ✔ micros pontuados (18/08/2026) — FUNIL COMPLETO |

## Como preencher

Coluna **N** = nota de interesse. Seja rígido — se tudo virar 2, a tabela não serve pra nada.

| Nota | Significado |
|---|---|
| **0** | Ignoro / não me interessa |
| **1** | Curiosidade — leria um post sobre |
| **2** | Quero estudar de verdade |
| **3** | Quero ser **reconhecido** nisso |

Coluna **Obs** = só para as notas 2 e 3, uma linha: *por que* isso te interessa.

Marcação `[=]` indica tópico que aparece em mais de uma conferência (sobreposição = área madura e bem posicionada — vale reparar nesses).

---

# ICAI'26 — The 28th Int'l Conf on Artificial Intelligence

> "AI é a ciência e engenharia de construir máquinas e sistemas inteligentes. Como Machine Learning tem laços fortes com IA, a conferência também cobre a área de Machine Learning. A lista de tópicos abaixo não pretende ser exaustiva."

## Bloco A — Artificial Intelligence

| # | Tópico | N | Obs |
|---|---|---|---|
| A01 | Brain models, Brain mapping, Cognitive science `[=ACC]` | 1 | |
| A02 | Natural language processing `[=ICDATA, ACC]` | 3 | |
| A03 | Fuzzy logic and soft computing `[=ICDATA, ACC]` | 1 | |
| A04 | Software tools for AI | 2 | |
| A05 | Expert systems | 2 | |
| A06 | Decision support systems | 2 | poda 2: era 3 (área irmã C5) |
| A07 | Automated problem solving | 2 | poda 2: era 3 (área irmã C5) |
| A08 | Knowledge discovery `[=ICDATA]` | 2 | |
| A09 | Knowledge representation `[=ICDATA, ACC]` | 2 | |
| A10 | Knowledge acquisition | 3 | réplica de B40 |
| A11 | Knowledge-intensive problem solving techniques | 2 | réplica de A07; poda 2: era 3 |
| A12 | Knowledge networks and management | 2 | poda: era 3 |
| A13 | Intelligent information systems | 2 | |
| A14 | Intelligent data mining and farming | 2.5 | |
| A15 | Intelligent web-based business | 1 | réplica de A19 |
| A16 | Intelligent agents `[=ICDATA, ACC]` | 2.5 | |
| A17 | Intelligent networks | 2 | |
| A18 | Intelligent databases | 2 | réplica de A17 |
| A19 | Intelligent user interface | 1 | |
| A20 | AI and evolutionary algorithms `[=ICDATA, ACC]` | 2 | |
| A21 | Intelligent tutoring systems | 1 | réplica de A47 |
| A22 | Reasoning strategies | 2.5 | |
| A23 | Distributed AI algorithms and techniques | 2.5 | |
| A24 | Distributed AI systems and architectures | 2.5 | réplica de A23 |
| A25 | Neural networks and applications `[=ICDATA, ACC]` | 2 | poda 2: era 3 (lado do modelo) |
| A26 | Heuristic searching methods `[=ACC]` | 2 | réplica de A31; poda: era 3 |
| A27 | Languages and programming techniques for AI | 2 | réplica de A04 |
| A28 | Constraint-based reasoning and constraint programming | 2 | poda: era 3 |
| A29 | Intelligent information fusion `[=ICDATA, ACC]` | 2.5 | |
| A30 | Learning and adaptive sensor fusion | 2.5 | réplica de A29 |
| A31 | Search and meta-heuristics `[=ICDATA]` | 2 | poda: era 3 |
| A32 | Multisensor data fusion using neural and fuzzy techniques | 2.5 | réplica de A29 |
| A33 | Integration of AI with other technologies | | |
| A34 | Evaluation of AI tools | 2 | réplica de A04 |
| A35 | Social intelligence (markets and computational societies) | 1 | réplica de A36 |
| A36 | Social impact of AI | 1 | |
| A37 | Emerging technologies | 2.5 | réplica de A48 |
| A38 | Applications — computer vision | 2.5 | |
| A39 | Applications — signal processing `[=ICDATA, ACC]` | 2 | poda: era 3 |
| A40 | Applications — military, surveillance `[=ICDATA]` | 2.5 | |
| A41 | Applications — robotics | 1 | |
| A42 | Applications — medicine `[=ICDATA]` | 1 | |
| A43 | Applications — pattern recognition | 2.5 | |
| A44 | Applications — face recognition | 2 | |
| A45 | Applications — finger print recognition | 2 | réplica de A44 |
| A46 | Applications — finance and marketing, stock market `[=ICDATA]` | 2.5 | |
| A47 | Applications — education `[=ICDATA]` | 1 | |
| A48 | Applications — emerging applications | 2.5 | |

> **Nota de fidelidade:** os itens A38–A48 são a expansão de um único bullet da CfP original
> (`Applications (including: computer vision, signal processing, military, surveillance, robotics,
> medicine, pattern recognition, face recognition, finger print recognition, finance and marketing,
> stock market, education, emerging applications, ...)`). Foram separados para permitir nota
> individual. A CfP original tem 38 bullets nesta seção; aqui são 48 linhas.

## Bloco B — Machine Learning: Models, Technologies and Applications

| # | Tópico | N | Obs |
|---|---|---|---|
| B01 | Statistical learning theory | 2 | |
| B02 | Unsupervised and Supervised Learning | 2 | poda: era 3 |
| B03 | Multivariate analysis | 2 | |
| B04 | Hierarchical learning models `[=ACC]` | 2 | repontuado após explicação |
| B05 | Relational learning models | 2.5 | |
| B06 | Bayesian methods `[=ACC]` | 2.5 | |
| B07 | Meta learning | 2.5 | |
| B08 | Stochastic optimization `[=ACC]` | 2 | poda: era 3 |
| B09 | Simulated annealing | 2.5 | |
| B10 | Heuristic optimization techniques | 2 | réplica de A31; poda: era 3 |
| B11 | Neural networks `[=ICDATA, ACC]` | 2 | réplica de A25; poda 2: era 3 |
| B12 | Reinforcement learning `[=ACC]` | 2.5 | |
| B13 | Multi-criteria reinforcement learning | 2.5 | |
| B14 | General Learning models | 2.5 | |
| B15 | Multiple hypothesis testing | 2 | |
| B16 | Decision making `[=ACC]` | 2 | repontuado após explicação; poda 2: era 3 (área irmã C5) |
| B17 | Markov chain Monte Carlo (MCMC) methods | 1 | |
| B18 | Non-parametric methods | 1 | |
| B19 | Graphical models | 2 | |
| B20 | Gaussian graphical models | 2 | réplica de B19 |
| B21 | Bayesian networks `[=ACC]` | 2.5 | |
| B22 | Particle filter | 1 | |
| B23 | Cross-Entropy method | 2.5 | |
| B24 | Ant colony optimization | 2 | |
| B25 | Time series prediction `[=ICDATA]` | 2.5 | |
| B26 | Fuzzy logic and learning `[=ICDATA, ACC]` | 2 | poda: era 3 |
| B27 | Inductive learning and applications | 2.5 | |
| B28 | Grammatical inference | 1 | |
| B29 | Graph kernel and graph distance methods | 2.5 | |
| B30 | Graph-based semi-supervised learning | 2.5 | |
| B31 | Graph clustering | 2 | poda: era 3 |
| B32 | Graph learning based on graph transformations | 2.5 | |
| B33 | Graph learning based on graph grammars | 2.5 | réplica de B32 |
| B34 | Graph learning based on graph matching | 2.5 | réplica de B32 |
| B35 | Information-theoretical approaches to graphs `[=ACC]` | 2.5 | |
| B36 | Motif search | 1 | |
| B37 | Network inference | 2.5 | |
| B38 | Aspects of knowledge structures | 2 | |
| B39 | Computational Intelligence `[=ICDATA]` | 2 | repontuado após explicação |
| B40 | Knowledge acquisition and discovery techniques | 3 | poda 2: mantido (leitura: estruturar conhecimento a partir de fontes) |
| B41 | Induction of document grammars | 2 | |
| B42 | General Structure-based approaches in information retrieval, web authoring, information extraction, and web content mining `[=ICDATA]` | 2.5 | réplica de N03 |
| B43 | Latent semantic analysis `[=ACC]` | 2.5 | |
| B44 | Aspects of natural language processing | 3 | réplica de A02 |
| B45 | Intelligent linguistic | 2.5 | |
| B46 | Aspects of text technology | 2.5 | |
| B47 | Biostatistics | 0 | |
| B48 | High-throughput data analysis | 1 | réplica de H01 |
| B49 | Computational Neuroscience `[=ACC]` | 1 | |
| B50 | Computational Statistics `[=ICDATA]` | 1 | |

---

# ICDATA'26 — The 22th Int'l Conference on Data Science

> Escopo: "papers devem estar relacionados a Data Science, Data Mining, Machine Learning, AI for Data Analytics, e tópicos similares."
> Taxa de aceitação histórica: **~40 a 50%** (≥2 revisores independentes). Deadline estendido de submissão: **18 de junho de 2026**.
> Planeja publicar livro (De Gruyter) com versões estendidas de papers selecionados.

## Bloco C — Applications of AI for Data Science Tasks

| # | Tópico | N | Obs |
|---|---|---|---|
| C01 | Applications of generative AI for generating data | 3 | |
| C02 | Applications of (generative) AI for data handling | 3 | |
| C03 | Applications of (generative) AI for analytics, visualization, reporting | 3 | |

## Bloco D — Data Mining / Machine Learning Tasks

| # | Tópico | N | Obs |
|---|---|---|---|
| D01 | Regression / Classification | 2 | poda: era 3 |
| D02 | Time series forecasting `[=ICAI]` | 2.5 | réplica de B25 |
| D03 | Segmentation / Clustering / Association | 2 | poda 2: era 3 (análise, não pipeline) |
| D04 | Deviation and outlier detection | 3 | poda: mantido, alocado em C2 |
| D05 | Explorative and visual data mining | 3 | |
| D06 | Web mining | 2 | |
| D07 | Mining text and semi-structured data | 2.5 | |
| D08 | Temporal and spatial data mining | 2 | |
| D09 | Multimedia mining (audio/video) | 2 | poda: era 3 |
| D10 | Mining "Big Data" | 2.5 | |

## Bloco E — Data Mining Algorithms

| # | Tópico | N | Obs |
|---|---|---|---|
| E01 | Artificial neural networks / Deep Learning / **Large Language Models** `[=ICAI, ACC]` | 3 | |
| E02 | Fuzzy logic and rough sets `[=ICAI, ACC]` | 1 | réplica de A03 |
| E03 | Decision trees / rule learners | 2 | poda: era 3 |
| E04 | Support vector machines | 2.5 | |
| E05 | Evolutionary computation / meta heuristics `[=ICAI, ACC]` | 2 | réplica de A20 |
| E06 | Statistical methods | 1 | |
| E07 | Collaborative filtering | 2 | réplica de N08; poda: era 3 |
| E08 | Case based reasoning | 2 | poda: era 3 |
| E09 | Link and sequence analysis | 2 | poda 2: era 3 (análise, não pipeline) |
| E10 | Ensembles / committee approaches | 2 | poda: era 3 |

## Bloco F — Data Mining Integration

| # | Tópico | N | Obs |
|---|---|---|---|
| F01 | Mining large scale data / big data | 2.5 | réplica de D10 |
| F02 | Data and knowledge representation `[=ICAI, ACC]` | 2 | réplica de A09 |
| F03 | Data warehousing and OLAP integration | 3 | poda 2: promovido (estruturação), era 2 |
| F04 | Integration of prior domain knowledge | 3 | |
| F05 | Metadata and ontologies | 3 | poda: promovido (essencial C2, esquema de anotação), era 2 |
| F06 | Agent technologies for data mining `[=ICAI, ACC]` | 2 | |
| F07 | Legal and social aspects of data mining `[=ICAI]` | 1 | réplica de A36 |

## Bloco G — Data Mining Process

| # | Tópico | N | Obs |
|---|---|---|---|
| G01 | Data cleaning and preparation | 3 | |
| G02 | Feature selection and transformation `[=ACC]` | 3 | |
| G03 | Attribute discretisation and encoding | 3 | réplica de G02 |
| G04 | Sampling and rebalancing | 3 | |
| G05 | Missing value imputation | 3 | |
| G06 | Model selection / assessment and comparison | 3 | |
| G07 | Induction principles | 2 | poda 2: era 3 (teoria de modelo, não dado) |
| G08 | Model interpretation | 3 | poda 2: mantido (fecha o ciclo de confiança no dado) |

## Bloco H — Data Mining Applications

| # | Tópico | N | Obs |
|---|---|---|---|
| H01 | Bioinformatics | 1 | |
| H02 | Medicine Data Mining `[=ICAI]` | 1 | réplica de A42 |
| H03 | Business / Corporate / Industrial Data Mining | 2.5 | |
| H04 | Credit Scoring | 2.5 | réplica de A46 |
| H05 | Direct Marketing | 2.5 | réplica de A46 |
| H06 | Database Marketing | 2.5 | réplica de A46 |
| H07 | Engineering Mining | 2.5 | réplica de J05 |
| H08 | Military Data Mining `[=ICAI]` | 2.5 | réplica de A40 |
| H09 | Security Data Mining | 2.5 | |
| H10 | Social Science Mining | 1 | réplica de A36 |
| H11 | Data Mining in Logistics | 2.5 | |

> Nota da CfP: *"encorajamos especialmente submissões de aplicações industriais e estudos de caso de praticantes. Estes não serão avaliados apenas por critérios teóricos de pesquisa."*

## Bloco I — Data Mining Software & Tópicos Alternativos

| # | Tópico | N | Obs |
|---|---|---|---|
| I01 | Data Mining Software — all aspects, modules, frameworks | 2 | poda: era 3 |
| I02 | Data Mining for Business Intelligence | 2.5 | réplica de H03 |
| I03 | Emerging technologies in data mining `[=ICAI]` | 2 | poda: rótulo genérico, era 3 |
| I04 | Computational performance issues in data mining | 2.5 | réplica de J02 |
| I05 | Data mining in usability | 1 | réplica de A19 |
| I06 | Advanced prediction modelling using data mining | 2 | poda: era 3 |
| I07 | Data mining and national security | 2.5 | réplica de H09 |
| I08 | Data mining tools | 2 | réplica de I01; poda: era 3 |
| I09 | Data analysis | 2 | poda: rótulo genérico, era 3 |
| I10 | Data preparation techniques (selection, transformation, and preprocessing) | 3 | réplica de G01 |
| I11 | Information extraction methodologies | 2.5 | réplica de N03 |
| I12 | Clustering algorithms used in data mining | 2 | réplica de D03; poda 2: era 3 |
| I13 | Genetic algorithms and categorization techniques used in data mining `[=ACC]` | 2 | réplica de A20 |
| I14 | Data and information integration | 3 | |
| I15 | Microarray design and analysis | 1 | réplica de H01 |
| I16 | Privacy-preserving data mining | 3 | |
| I17 | Active data mining | 3 | poda: mantido, alocado em C2 (active learning / anotação eficiente) |
| I18 | Statistical methods used in data mining `[=ICAI]` | 1 | réplica de E06 |
| I19 | Multidimensional data | 3 | réplica de F03; poda 2: promovido |
| I20 | Case studies and prototypes | 2.5 | réplica de A48 |
| I21 | Automatic data cleaning | 3 | réplica de G01 |
| I22 | Data visualization | 3 | réplica de D05 |
| I23 | Theory and practice — knowledge representation and discovery `[=ICAI]` | 2 | réplica de A09 |
| I24 | Knowledge Discovery in Databases (KDD) `[=ICAI]` | 2 | réplica de A08 |
| I25 | Uncertainty management | 2 | |
| I26 | Data reduction methods | 3 | réplica de G02 |
| I27 | Data engineering | 3 | |
| I28 | Content mining | 2 | réplica de D06 |
| I29 | Indexing schemes | 2.5 | réplica de I34 |
| I30 | Information retrieval `[=ACC]` | 2 | poda: era 3 (C4; faltou no painel de veto — avisar Pedro) |
| I31 | Metadata use and management | 3 | réplica de F03; poda 2: promovido |
| I32 | Multidimensional query languages and query optimization | 3 | réplica de F03; poda 2: promovido |
| I33 | Multimedia information systems | 2 | réplica de D09; poda: era 3 |
| I34 | Search engine query processing | 2.5 | |
| I35 | Pattern mining | 2 | poda 2: era 3 (análise, não pipeline) |
| I36 | Applications (data mining em educação, marketing, finanças e serviços financeiros, negócios, medicina, bioinformática, ciências biológicas, ciência e tecnologia, indústria e governo, …) `[=ICAI]` | 2.5 | réplica de A48 |

## Bloco J — Algorithms for Big Data

| # | Tópico | N | Obs |
|---|---|---|---|
| J01 | Data and Information Fusion `[=ICAI, ACC]` | 2.5 | réplica de A29 |
| J02 | Algorithms (including Scalable methods) | 2.5 | |
| J03 | Natural Language Processing `[=ICAI, ACC]` | 3 | réplica de A02 |
| J04 | Signal Processing `[=ICAI, ACC]` | 2 | réplica de A39; poda: era 3 |
| J05 | Simulation and Modeling | 2.5 | |
| J06 | Data-Intensive Computing | 2.5 | réplica de J02 |
| J07 | Parallel Algorithms | 2.5 | réplica de L03 |
| J08 | Testing Methods | 3 | réplica de G06 |
| J09 | Multidimensional Big Data | 3 | réplica de F03; poda 2: promovido |
| J10 | Multilinear Subspace Learning | 2.5 | |
| J11 | Sampling Methodologies | 3 | réplica de G04 |
| J12 | Streaming | 3 | |

## Bloco K — Big Data Fundamentals

| # | Tópico | N | Obs |
|---|---|---|---|
| K01 | Novel Computational Methodologies `[=ACC]` | 2 | repontuado após explicação |
| K02 | Algorithms for Enhancing Data Quality | 3 | réplica de G01 |
| K03 | Models and Frameworks for Big Data | 2.5 | |
| K04 | Graph Algorithms and Big Data `[=ICAI, ACC]` | 2 | |
| K05 | Computational Science | 2.5 | réplica de J05 |
| K06 | Computational Intelligence `[=ICAI]` | 2 | réplica de B39 |

## Bloco L — Infrastructures for Big Data

| # | Tópico | N | Obs |
|---|---|---|---|
| L01 | Cloud Based Infrastructures (applications, storage & computing resources) | 2 | poda: era 3 |
| L02 | Grid and Stream Computing for Big Data | 3 | réplica de J12 |
| L03 | High Performance Computing, Including Parallel & Distributed Processing | 2.5 | |
| L04 | Autonomic Computing | 2 | |
| L05 | Cyber-infrastructures and System Architectures | 2.5 | réplica de K03 |
| L06 | Programming Models and Environments to Support Big Data | 2.5 | réplica de K03 |
| L07 | Software and Tools for Big Data | 2.5 | réplica de K03 |
| L08 | Big Data Open Platforms | 2.5 | réplica de K03 |
| L09 | Emerging Architectural Frameworks for Big Data | 2.5 | réplica de K03 |
| L10 | Paradigms and Models for Big Data beyond Hadoop/MapReduce | 2.5 | réplica de K03 |

## Bloco M — Big Data Management and Frameworks

| # | Tópico | N | Obs |
|---|---|---|---|
| M01 | Database and Web Applications | 2 | |
| M02 | Federated Database Systems | 2.5 | réplica de M03 |
| M03 | Distributed Database Systems | 2.5 | |
| M04 | Distributed File Systems | 2.5 | réplica de M03 |
| M05 | Distributed Storage Systems | 2.5 | réplica de M03 |
| M06 | Knowledge Management and Engineering `[=ICAI]` | 2 | réplica de A12; poda: era 3 |
| M07 | Massively Parallel Processing (MPP) Databases | 2.5 | réplica de M03 |
| M08 | Novel Data Models | 3 | poda 2: promovido (estruturação), era 2.5 |
| M09 | Data Preservation and Provenance | 3 | poda: promovido (essencial C2, proveniência de dataset), era 2 |
| M10 | Data Protection Methods | 3 | |
| M11 | Data Integrity and Privacy Standards and Policies | 3 | mesma nota de M10 (linha MB10 do painel) |
| M12 | Data Science | 2 | poda: rótulo genérico, era 3 |
| M13 | Novel Data Management Methods | 3 | réplica de M08; poda 2: promovido |
| M14 | Crowdsourcing | 3 | poda: promovido (essencial C2, anotação humana); desvinculado de P02 |
| M15 | Stream Data Management | 3 | réplica de J12 |
| M16 | Scientific Data Management | 1 | |

## Bloco N — Big Data Search

| # | Tópico | N | Obs |
|---|---|---|---|
| N01 | Multimedia and Big Data | 2 | réplica de D09; poda: era 3 |
| N02 | Social Networks | 2.5 | |
| N03 | Web Search and Information Extraction | 2.5 | |
| N04 | Scalable Search Architectures | 2.5 | réplica de I34 |
| N05 | Cleaning Big Data (noise reduction), Acquisition & Integration | 3 | réplica de G01 |
| N06 | Visualization Methods for Search | 2.5 | |
| N07 | Time Series Analysis `[=ICAI]` | 2.5 | réplica de B25 |
| N08 | Recommendation Systems | 2 | poda: era 3 (C4; faltou no painel de veto — avisar Pedro) |
| N09 | Graph Based Search and Similar Technologies | 2.5 | |

## Bloco O — Privacy in the Era of Big Data

| # | Tópico | N | Obs |
|---|---|---|---|
| O01 | Cryptography | 2.5 | |
| O02 | Threat Detection Using Big Data Analytics | 2.5 | réplica de H09 |
| O03 | Privacy Threats of Big Data | 3 | |
| O04 | Privacy Preserving Big Data Collection | 3 | réplica de I16 |
| O05 | Intrusion Detection | 2.5 | réplica de H09 |
| O06 | Socio-economical Aspect of Big Data in the Context of Privacy and Security | 1 | |

## Bloco P — Applications of Big Data

| # | Tópico | N | Obs |
|---|---|---|---|
| P01 | Big Data as a Service | 2 | réplica de L01; poda: era 3 |
| P02 | Big Data Analytics in e-Government and Society | 2.5 | |
| P03 | Applications em Science, Engineering, Healthcare, Visualization, Business, Education, Security, Humanities, Bioinformatics, Health Informatics, Medicine, Finance, Law, Transportation, Retailing, Telecommunication, e todas aplicações baseadas em busca | 2.5 | réplica de A48 |

---

# ACC'26 — The 10th International Conference on Applied Cognitive Computing

> "Sistemas de computação cognitiva usam modelos computacionais para simular o processo de cognição humana e encontrar soluções em situações complexas onde as respostas podem ser ambíguas e incertas. Embora o termo *cognitive computing* seja frequentemente usado de forma intercambiável com IA, a expressão está fortemente associada ao sistema cognitivo da IBM, o Watson."
>
> A CfP pede: "trabalho teórico, matemático, empírico e experimental" com pesquisa **original e não publicada**.

| # | Tópico | N | Obs |
|---|---|---|---|
| Q01 | Novel Computationally Intelligent algorithms `[=ICDATA]` | 2 | réplica de K01 |
| Q02 | Bio Inspired Cognitive Algorithms | 1 | |
| Q03 | Improving Cognition in machine learning systems | 1 | |
| Q04 | Modeling Human Brain processing systems `[=ICAI]` | 1 | réplica de A01 |
| Q05 | Multimodal learning systems | 2 | |
| Q06 | Autonomous learning systems | 2.5 | |
| Q07 | Reinforced learning `[=ICAI]` | 2.5 | réplica de B12 |
| Q08 | Cognitive evolution | 1 | |
| Q09 | Concept Drift and Evolution | 3 | poda: mantido, alocado em C2 |
| Q10 | Cognitive inferential systems | 1 | |
| Q11 | Cognitive improvement in deep learning networks `[=ICDATA]` | 1 | réplica de Q03 |
| Q12 | Hebbian Learning Systems | 1 | |
| Q13 | Advancements in Neural Networks `[=ICAI, ICDATA]` | 2 | réplica de A25; poda 2: era 3 |
| Q14 | Fuzzy Engineering `[=ICAI, ICDATA]` | 1 | réplica de A03 |
| Q15 | Multiscale Learning systems | 2 | |
| Q16 | Fractal based learning and decision support systems | 1 | repontuado após explicação |
| Q17 | Application of chaos Engineering in machine intelligence | 1 | repontuado após explicação |
| Q18 | Dynamical learning systems | 1 | repontuado após explicação |
| Q19 | Application of Information Theory in Machine Intelligence `[=ICAI]` | 1 | |
| Q20 | Application of linear and nonlinear optimization theory in machine intelligence | 2.5 | |
| Q21 | New algorithms for Predictive Analytics and Applied Data Science `[=ICDATA]` | 2 | poda: era 3 |
| Q22 | Self-Adaptive and Self Organizing Systems | 2.5 | |
| Q23 | Manifold and Metric learning | 2.5 | |
| Q24 | Cognitive Modeling, Visualization and Analytics of Big Data `[=ICDATA]` | 1 | |
| Q25 | Application of Graph Theoretic approaches in dimensionality reduction and machine intelligence `[=ICAI, ICDATA]` | 2.5 | |
| Q26 | Information and Knowledge retrieval and searching algorithms `[=ICDATA]` | 2 | réplica de I30; poda: era 3 |
| Q27 | Big data knowledge mining `[=ICDATA]` | 2 | réplica de A08 |
| Q28 | Mathematical modeling of Big Data and Artificial Intelligence | 1 | |
| Q29 | Cognitive Signal Processing `[=ICAI, ICDATA]` | 2 | réplica de A39; poda: era 3 |
| Q30 | Rough Set Theory `[=ICDATA]` | 2 | poda: era 3 |
| Q31 | Knowledge Representation and Classification Systems `[=ICAI, ICDATA]` | 2 | réplica de A09 |
| Q32 | Agent Based Modeling in Machine Learning Systems `[=ICAI, ICDATA]` | 2 | |
| Q33 | Information Processing and Decision Making Systems `[=ICAI]` | 2 | |
| Q34 | Natural Language Processing `[=ICAI, ICDATA]` | 3 | réplica de A02 |
| Q35 | Big Data Fusion and Information Retrieval `[=ICAI, ICDATA]` | 2.5 | |
| Q36 | Time and Space Analysis in Machine Learning | 2 | réplica de D08 |
| Q37 | New application of classical stochastic and statistical analysis for big data machine learning | 1 | |
| Q38 | Bayesian modeling applications `[=ICAI]` | 2.5 | réplica de B06 |
| Q39 | Hierarchical learning systems `[=ICAI]` | 2 | réplica de B04 |
| Q40 | Cognition in Genetic and Evolutionary algorithms for learning and decision making `[=ICAI, ICDATA]` | 2 | réplica de A20 |
| Q41 | Nature inspired cognitive computing algorithms | 1 | |
| Q42 | Heuristic Analysis `[=ICAI]` | 2 | réplica de A31; poda: era 3 |
| Q43 | Cognitive Feature Extraction `[=ICDATA]` | 1 | |
| Q44 | Extraction of latent semantics from big data `[=ICAI]` | 2.5 | |

---

# Poda (18/08/2026)

Ranking dos clusters definido pelo Pedro: **1º C2 (qualidade/pipeline de dados) · 2º C1 (GenAI para dados) · 3º C6 (privacidade)**.

**Poda 1** — regra: só C2/C1 mantêm 3; rebaixamentos com direito a veto; essenciais promovidos.
- Rebaixados 3→2: B02, D01, E03, E10, I06, Q21, B31, A12 (M06), E08, A31 (A26, B10, Q42), A28, B08, L01 (P01), A39 (J04, Q29), D09 (I33, N01), B26, Q30, I01 (I08) e rótulos genéricos I09, M12, I03.
- Vetos do Pedro (mantidos em 3): cluster C6 inteiro, A02, A25, D03, D05, E09, I35, A06, A07, B16, B40, F04, J12.
- Ambíguos alocados em C2 com 3: D04, Q09, I17. Promovidos a 3: M14, M09, F05.

**Poda 2** — critério corrigido pelo Pedro: interesse é o **pipeline de dados inteiro** (coleta → limpeza → estruturação → integração/engenharia → qualidade/avaliação → documentação/governança), com ênfase em estruturação. O tema estacionado (datasets pt-BR jurídico) NÃO é critério.
- Rebaixados 3→2 (fora do pipeline): A25 (B11, Q13) e G07 (lado do modelo); D03 (I12), E09, I35 (análise que consome o pipeline); A06, A07 (A11), B16 (área irmã C5).
- Borderline mantidos em 3: G08 (confiança no resultado), B40 (estruturar conhecimento).
- Promovidos a 3 (estruturação subpontuada): F03 (I19, I31, I32, J09), M08 (M13).

Tudo que caiu de 3/2.5 está preservado em `../interesses-estudos-futuros.md`.

---

# Consolidação — preencher DEPOIS de pontuar tudo

## Tópicos com nota 3 (quero ser reconhecido nisso)

29 conceitos únicos após as duas podas. Colunas pessoais preenchidas onde há evidência (auditoria do Ultimatum); "—" = Pedro completa.

**C2 — âncora: o pipeline de dados (21)**

| # ref | Tópico | Conf. | Minha base hoje | Liga com o que já faço |
|---|---|---|---|---|
| G01 (I10, I21, K02, N05) | Data cleaning and preparation | ICDATA | normalização e gates de qualidade no Ultimatum | ~60% do código do Ultimatum é trabalho de dados |
| G02 (G03, I26) | Feature selection / transformation / redução | ICDATA | usei em projeto — disciplinas, nunca com muito foco | — |
| G04 (J11) | Sampling and rebalancing | ICDATA | rebalanceamento de classes no Ultimatum | Ultimatum |
| G05 | Missing value imputation | ICDATA | usei em projeto — disciplinas, como quick-fix | — |
| G06 (J08) | Model selection / assessment / testing | ICDATA | avaliação F1 sintético vs real no Ultimatum | gap 0,918→0,655 é pergunta viva |
| G08 | Model interpretation | ICDATA | nunca toquei — só outputs interpretados pelo Claude Code | fecha o ciclo "quando confiar no resultado" |
| D04 | Deviation and outlier detection | ICDATA | só teoria — 1x via Claude Code (guideline de anotação + dataset p/ análise) | detecção de erro de anotação |
| D05 (I22) | Explorative and visual data mining | ICDATA | EDA em projetos de curso | — |
| Q09 | Concept drift and evolution | ACC | só teoria | reavaliação contínua de datasets |
| I17 | Active data mining | ICDATA | nunca toquei | anotação eficiente (active learning) |
| I14 | Data and information integration | ICDATA | só teoria — versionei datasets bronze/silver/gold em 1 atividade de disciplina; entendo o ganho | montar corpus de fontes heterogêneas |
| I27 | Data engineering | ICDATA | pipeline completo do Ultimatum | — |
| F03 (I19, I31, I32, J09) | Data warehousing and OLAP | ICDATA | nunca toquei | estruturação — promovido na poda 2 |
| M08 (M13) | Novel data models | ICDATA | nunca toquei | estruturação além da tabela — promovido |
| M09 | Data preservation and provenance | ICDATA | nunca toquei | documentação de dataset — promovido |
| F05 | Metadata and ontologies | ICDATA | nunca toquei | esquema de anotação — promovido |
| M14 | Crowdsourcing | ICDATA | só teoria — anotei dataset de imagens 1x em disciplina; ouvinte na anotação do Ultimatum | anotação humana — promovido |
| J12 (L02, M15) | Streaming / stream data management | ICDATA | nunca toquei | pipeline contínuo — veto do Pedro |
| B40 (A10) | Knowledge acquisition | ICAI | usei em projeto — camada de regras BRMS num PoC de motor de crédito (protótipo) | estruturar conhecimento de fontes — veto |
| F04 | Integration of prior domain knowledge | ICDATA | conhecimento jurídico no Ultimatum | veto |
| A02 (B44, J03, Q34) | Natural language processing | ICAI/ICDATA/ACC | NER jurídico no Ultimatum | estruturar dado não-estruturado — veto |

**C1 — satélite 1: GenAI para dados (4)**

| # ref | Tópico | Conf. | Minha base hoje | Liga com o que já faço |
|---|---|---|---|---|
| C01 | Generative AI for generating data | ICDATA | corpus sintético via LLM no Ultimatum | Ultimatum É C2×C1 executado |
| C02 | (Generative) AI for data handling | ICDATA | anotação/limpeza assistida no Ultimatum | — |
| C03 | (Generative) AI for analytics, visualization, reporting | ICDATA | usei em projeto — uso o Claude Code para isso o tempo todo | ponta de consumo do pipeline |
| E01 | Deep Learning / LLMs | ICDATA/ICAI/ACC | uso de LLMs em pipelines | ferramenta central do C1 |

**C6 — satélite 2: privacidade de dados (4)**

| # ref | Tópico | Conf. | Minha base hoje | Liga com o que já faço |
|---|---|---|---|---|
| I16 (O04) | Privacy-preserving data mining / collection | ICDATA | só teoria — vi implementações (hash com salt etc.), nunca apliquei | dado jurídico sensível no Ultimatum |
| M10 | Data protection methods | ICDATA | nunca toquei | — |
| M11 | Data integrity and privacy standards / policies | ICDATA | nunca toquei | LGPD |
| O03 | Privacy threats of big data | ICDATA | nunca toquei | o "por quê" do satélite |

## Tópicos com nota 2 (quero estudar de verdade)

Os 2 e 2.5 remanescentes — incluindo tudo que desceu nas podas — estão catalogados por área em **`../interesses-estudos-futuros.md`** (C3 mineração/ML, grafos, C4 busca/IR, C5 conhecimento/decisão, C7 otimização, C8 escala/infra, C9 áudio/multimídia, fuzzy, séries temporais, segurança, aplicações). Não replicar a lista aqui.

## Clusters (3 a 5) — se não consegue nomear, não é cluster

| Cluster | Tópicos que entram | Por que fazem sentido juntos |
|---|---|---|
| **C2 — Engenharia e qualidade de dados (âncora)** | G01, G02, G04, G05, G06, G08, D04, D05, Q09, I17, I14, I27, F03, M08, M09, F05, M14, J12, B40, F04, A02 | São as etapas de um único processo: coletar → limpar/preparar → estruturar/integrar → anotar/adquirir → documentar/governar → avaliar/confiar. É o pipeline de dados inteiro, com ênfase em estruturação. |
| **C1 — GenAI para dados (satélite 1)** | C01, C02, C03, E01 | O LLM como ferramenta dentro do pipeline: gerar dados, manuseá-los/anotá-los e entregar análise na ponta. Sustenta a âncora tecnicamente. |
| **C6 — Privacidade de dados (satélite 2)** | I16, M10, M11, O03 | O pipeline lida com dado sensível: ameaças (por quê), técnicas de proteção (como) e normas/LGPD (regras do jogo). Diferencial de confiança sobre a âncora. |

## Configuração final

- **Âncora** (o tópico onde quero ser reconhecido): **C2 — engenharia e qualidade de dados: o pipeline inteiro**, da coleta à avaliação, com ênfase em estruturação.
- **Satélite 1** (sustenta a âncora tecnicamente): **C1 — GenAI para dados** (LLMs para gerar, limpar, anotar e analisar).
- **Satélite 2**: **C6 — privacidade de dados** (proteção, LGPD, anonimização).

**Teste do elevador** (2 frases, sem jargão de CfP) — APROVADO pelo Pedro em 18/08/2026:
> Eu faço dados prestarem: estruturo, limpo, anoto e documento dados de ponta a ponta, usando LLMs como ferramenta do pipeline.
> E provo quando dá para confiar no resultado — inclusive quando o dado é sensível.

**Ainda não está resolvido:**
> O gap sintético→real: dados gerados por LLM passam nos gates de qualidade mas o desempenho despenca no dado real (Ultimatum: F1 0,918 → 0,655). Medir e fechar esse gap é pergunta de pesquisa viva — e o candidato natural a tema.
