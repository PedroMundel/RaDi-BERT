# Registro de artigos verificados (09–10/09/2026)

Este é o registro único. Argumentos e decisões ficam em `docs/pesquisa/tema-v3-racionalizacao-encoder.md`;
critérios de julgamento em `docs/pesquisa/mapa-do-terreno.md`.

## ⚠ Procedência — leia antes de usar qualquer coisa daqui

**Declaração do Pedro em 10/09/2026: ele leu apenas o Distilling Step-by-Step e o DHRD.**
Todo o resto deste arquivo é leitura de terceiro. Três níveis de distância da fonte, e eles NÃO são
equivalentes:

| Nível | O que significa | Confiabilidade |
|---|---|---|
| **1 — Pedro leu** | conhecimento próprio, citável com segurança | alta |
| **2 — Claude leu o texto completo** | PDF integral extraído e lido | alta para fatos, mas é leitura de terceiro |
| **3 — Agente verificou** | acessou a página oficial, confirmou título/autores/ID/ano/venue e leu o **resumo**; o corpo do artigo NÃO foi lido | **existência e metadados confiáveis; interpretação de método e resultado pode conter erro de sumarização** |

**A quase totalidade das tabelas abaixo é nível 3.** Os números, mecanismos e conclusões
resumidos aqui servem para **triagem e priorização**, não para citação. Antes de escrever qualquer
frase de artigo apoiada num destes trabalhos, o texto tem que ser lido.

### Estado real de leitura

| Artigo | Quem leu | Até onde |
|---|---|---|
| **RoBERTaLexPT** | ⚠ **a confirmar** | estava marcado como lido pelo Pedro antes desta sessão, mas a declaração de 10/09 diz "apenas destilação e DHRD". **Não citar como leitura do Pedro até ele confirmar.** |
| **Distilling Step-by-Step** (arXiv:2305.02301) | **Pedro** e Claude | **Pedro: leu e escreveu resumo próprio** (`Downloads/Distilling Step-by-Step.pdf`, cobre até limitações) — **nível 1** · Claude: §1–3, §4.4 e *Limitations* |
| **Herrewijnen et al., EACL 2026** | Claude | integral — notas em `docs/artigos/notas-herrewijnen-eacl2026.md`. **Pedro não leu** |
| **DHRD** — Xu et al., arXiv:2509.21487 | **Pedro** e Claude | Claude: §1–5, ablações, limitações e trabalho futuro, PDF reconferido número por número em 10/09/2026 — notas em `docs/artigos/notas-dhrd-xu2025.md`. **Venue resolvido: workshop.** **Pedro: leu e escreveu resumo próprio** (`Downloads/DHRD Resumo.pdf`, cobre até a conclusão) — **nível 1** |
| **Li et al.**, ICD, arXiv:2508.16777 | Claude | §5, §6, §7, §8 e Tabelas 3–4 (não leu §3–4 nem apêndices), 10/09/2026 — notas em `docs/artigos/notas-li-icd-2508.16777.md`. **Venue "EACL 2026" NÃO se sustenta na fonte.** Pedro não leu |
| Todos os demais (~50) | agente de pesquisa | página oficial e resumo apenas |

**Só as quatro linhas com nota em `docs/artigos/` estão em nível citável** (e mesmo essas são nível 2,
leitura de terceiro). Todo o resto deste arquivo é nível 3.

Campos marcados "não confirmado" são justamente isso — não completar de memória depois.

---

## Frente A — Escala pequena e eficiência

| Artigo | Objeto | Propriedade medida | 8GB? | Código |
|---|---|---|---|---|
| **QLoRA** — Dettmers, Pagnoni, Holtzman, Zettlemoyer, arXiv:2305.14314, NeurIPS 2023 | procedimento + artefato | qualidade pós-ajuste e footprint de memória | parcial (7B/13B em 4-bit, apertado) | github.com/artidoro/qlora |
| **Scaling Laws for Precision** — Kumar et al., arXiv:2411.04330, 2024 | resultado (lei preditiva) | perda em função de bits de precisão; 465+ runs até 1.7B | não | não localizado |
| **MobileLLM** — Liu et al. (Meta), arXiv:2402.14905, ICML 2024 | artefato (arquitetura sub-1B) | acurácia zero-shot por escolha arquitetural; **ablação exemplar** | checkpoints sim, treino não | github.com/facebookresearch/MobileLLM |
| **AWQ** — Lin, Tang, Han et al., arXiv:2306.00978, MLSys 2024 (Best Paper) | técnica + sistema | erro de quantização, acurácia, throughput | **sim — é o ponto do paper** | github.com/mit-han-lab/llm-awq |
| **PowerInfer** — Song, Mi, Xie, Chen, arXiv:2312.12456, SOSP 2024 | sistema | tokens/s e uso de VRAM, offload CPU/GPU | princípio portável (usaram 4090 24GB) | github.com/SJTU-IPADS/PowerInfer |
| **Distilling Step-by-Step** — Hsieh et al., arXiv:2305.02301, ACL 2023 Findings | procedimento | acurácia vs. volume de dado rotulado | **sim** (T5 small/base) | github.com/google-research/distilling-step-by-step |
| **Benchmarking Post-Training Quantization** — Zhao et al., arXiv:2502.13178, 2025 | resultado (comparação pura) | acurácia pós-quantização por método | parcial (7B) | github.com/zjq0455/PTQ_Benchmark |
| **SmolLM2** — Ben Allal et al. (HF), arXiv:2502.02737, 2025 | artefato + procedimento | qualidade downstream por mistura de dados | checkpoints sim, pré-treino não | github.com/huggingface/smollm |

## Frente B — Português e medição como objeto

| Artigo | Objeto | Nota |
|---|---|---|
| **Sabiá-2** — Almeida, Abonizio, Nogueira, Pires, arXiv:2403.09887, 2024 | produto | 64 exames brasileiros reais; API proprietária, sem pesos |
| **TeenyTinyLlama** — Corrêa et al., arXiv:2401.16640, *Machine Learning with Applications* v.16 | produto | 160M/460M do zero em pt-BR; **melhor relato de custo do lote** (280h A100, 113 kWh, ~US$500); Apache 2.0 |
| **Building High-Quality Datasets for Portuguese LLMs** — Almeida, Nogueira, Pedrini, arXiv:2509.08824, 2025 | **processo** | pipeline de curadoria, corpus 120B tokens; código não localizado |
| **Organizing the ASSIN 2 Shared Task** — Real, Fonseca, Gonçalo Oliveira, CEUR-WS Vol-2583, 2019 (STIL) | processo + produto | 6.500+500 pares pt-BR, STS e RTE |
| **BLUEX** — Almeida, Laitz, Bonás, Nogueira, arXiv:2307.05410, BRACIS 2023 | produto (benchmark) | desenho anti-contaminação; CC-BY |
| **PoETa v2** — Almeida et al., arXiv:2511.17808, 2025 | a própria medição | 40+ tarefas pt-BR, 20+ modelos; CC BY |
| **Documenting Large Webtext Corpora (auditoria do C4)** — Dodge et al., arXiv:2104.08758, EMNLP 2021 | processo + produto | **auditoria canônica**; roda em qualquer hardware |
| **Are Emergent Abilities a Mirage?** — Schaeffer, Miranda, Koyejo, arXiv:2304.15004, NeurIPS 2023 (Outstanding Paper) | a própria medição | **não treinou nada**; reanálise de resultados publicados |

**Impressão da amostra (não é levantamento exaustivo):** saturado — "mais um LLM para português" e
"mais um benchmark de prova brasileira"; os mesmos autores (Almeida, Nogueira, Pedrini) aparecem em
quase metade. Lacunas percebidas: não há auditoria de corpus em pt-BR no formato Dodge et al.;
curadoria/síntese para pt-BR é recente (set/2025); quase não há literatura pt-BR medindo com rigor
modelos pequenos ou comprimidos.

## Frente C — Fronteira dados↔modelo e aplicados

| Artigo | Objeto | Nota |
|---|---|---|
| **LIMA** — Zhou et al., arXiv:2305.11206, NeurIPS 2023 | resultado | 1.000 exemplos curados em LLaMA-65B; dataset `GAIR/lima`, pesos não |
| **Scaling Data-Constrained LMs** — Muennighoff, Rush, Barak et al., arXiv:2305.16264, NeurIPS 2023 | resultado (curva) | ~400 treinos; lei de escala reutilizável; github.com/huggingface/datablations |
| **AlpaGasus** — Chen et al., arXiv:2307.08701, ICLR 2024 | procedimento | 52k→9k por juiz LLM; **o desenho mais simples de imitar do lote** |
| **D4** — Tirumala, Simig, Aghajanyan, Morcos (Meta), arXiv:2308.12284, NeurIPS 2023 | procedimento | dedup+diversificação em pré-treino 6,7B; repo oficial não localizado |
| **LESS** — Xia, Malladi et al. (Princeton), arXiv:2402.04333, ICML 2024 | procedimento | seleção por influência de gradiente, 5% dos dados; github.com/princeton-nlp/LESS |
| **Nougat** — Blecher et al. (Meta), arXiv:2308.13418 | produto | PDF→markup, 250–350M, **roda em 8GB**; github.com/facebookresearch/nougat |
| **Docling** — IBM Research, arXiv:2501.17887, 2025 (relatório anterior arXiv:2408.09869) | produto | roda em CPU; MIT; github.com/docling-project/docling |
| **Better Bill GPT** — Whitehouse et al., arXiv:2504.02881, 2025 | resultado | humano vs. LLM em revisão de fatura jurídica; **custo e tempo como eixos**; código não localizado |

## Frente D — Pré-treino em português geral vs. baseline

| Modelo | Baseline | Do zero / continuado | Custo reportado? | Resultado |
|---|---|---|---|---|
| **BERTimbau** — Souza, Nogueira, Lotufo, BRACIS 2020, DOI 10.1007/978-3-030-61377-8_28 | mBERT | do zero (BrWaC) | **não** | STS 0,852 vs 0,809; NER 83,7 vs 79,2 |
| **PTT5** — Carmo et al., arXiv:2008.09144, 2020 | T5, mBERT | do zero | **não** | ganho; números não confirmados no PDF original |
| **DeBERTinha** — Campiotti et al., arXiv:2309.16844, 2023 | BERTimbau-Large | continuado (DebertaV3 XSmall) | **sim** — 8×A100 + 8×V100, 12,5h, ~US$400 | **misto**: ganha LeNERBR e RTE, perde STS e HateBR, com modelo ~40x menor |
| **Albertina PT-*** — Rodrigues et al., arXiv:2305.06721, EPIA 2023 | BERTimbau, mBERT, XLM-R | continuado (DeBERTa V2 XLarge) | **sim** — 16 GPUs, 1d11h | ASSIN2-RTE 0,913 vs 0,891 |
| **Gervásio PT*** — Santos et al., ACL Anthology 2024.sigul-1.3 (SIGUL @ LREC-COLING) | LLaMA 2 7B, Sabiá-7B | continuado (instrução) | **sim** — 16 GPUs, ~2h | ganho grande, **mas confundido com efeito de instruction-tuning** |
| **Bode** — Garcia et al., arXiv:2401.02909, 2024 | LLaMA 2 7B/13B, Mistral, Falcon | LoRA sobre LLaMA2 | parcial (máquina sim, horas não) | **misto**: Bode-7B abaixo do LLaMA2-13B em multiclasse (esquecimento catastrófico) |
| **TeenyTinyLlama** — ver Frente B | Pythia-410m, Bloom-560m, BERTimbau-L | do zero, 6,2B tokens | **sim, o mais completo** | **misto**: ganha ARC e MMLU, perde HellaSwag (33,00 vs 41,29) |
| **Sabiá** — Pires et al., BRACIS 2023, DOI 10.1007/978-3-031-45392-2_15 · arXiv:2304.07880 | GPT-J, LLaMA, GPT-3.5 | continuado, **≤3% do budget original** | parcial (só fração relativa) | ganho significativo; pesos não abertos |

**Transversais:** 4 de 8 reportam custo utilizável. Três resultados negativos ou mistos
(DeBERTinha, Bode, TeenyTinyLlama). **Só o DeBERTinha analisa custo × ganho explicitamente**; o
Sabiá enquadra em % de budget sem formalizar. Os outros seis reportam custo e ganho separadamente.

## Frente E — Pré-treino de domínio em português

| Modelo | Domínio | Baseline | Custo? | Resultado |
|---|---|---|---|---|
| **BioBERTpt** — Schneider et al., Clinical NLP @ EMNLP 2020, aclanthology.org/2020.clinicalnlp-1.7 | clínico | mBERT, BERTimbau | **não** | +1,6 F1; melhor em 11 de 13 entidades; HF `pucpr/biobertpt-all` |
| **JurisBERT** — Viegas, Costa, Ishii, ICCSA 2023, DOI 10.1007/978-3-031-36805-9_24 | jurídico | mBERT, BERTimbau | só relativo ("5x mais rápido") | +3,30% F1; HF `alfaneo/jurisbert-*` |
| **LegalBert-pt** — Silveira et al., BRACIS 2023, DOI 10.1007/978-3-031-45392-2_18 | jurídico | BERTimbau | **não** | supera em todas; **compara do-zero vs. continuado vs. genérico**; HF `raquelsilveira/legalbertpt_fp` |
| **BERTikal / LegalNLP** — Polo et al., arXiv:2110.15709, 2021 | jurídico | BERTimbau, Word2Vec | **sim** — T4, ~1 semana, corpus 1,63GB | ganho que **os autores dizem não ser estatisticamente significativo** |
| **FinBERT-PT-BR** — Santos, Bianchi, Costa, BWAIF 2023 (SBC) | financeiro | "estado da arte" (não confirmado) | **não** | converge com 500 textos rotulados; HF `lucas-leme/FinBERT-PT-BR` |
| **HelBERT** — Lima et al., JBCS v.32 n.1, DOI 10.5753/jbcs.2026.5511 | licitações públicas | BERTimbau, JurisBERT | vago | +5% F1 sobre BERTimbau; pesos não localizados |
| **PetroBERT** — Rodrigues et al., PROPOR 2022, DOI 10.1007/978-3-030-98305-5_10 | óleo e gás | mBERT, BERTimbau | não confirmado | números não confirmados (paywall) |
| **Benchmark de NER clínico** — Almeida et al., arXiv:2603.26510, 2026 | clínico | BioBERTpt, mmBERT, BERTimbau, ModernBERT, GPT-5, Gemini | qualitativo | **mmBERT genérico VENCE o BioBERTpt especializado** (micro-F1 0,76); github.com/GRUPOMED4U/clinical_ner_benchmark_paper |

**Transversais:** só **1 de 8** reporta custo utilizável (BERTikal). Dois resultados negativos.
**Nenhum compara "pré-treinar no domínio" contra "ajustar modelo geral com mais dados da tarefa"** —
lacuna real. Domínios pt-BR sem modelo dedicado observados: científico/acadêmico, governamental
amplo, agronegócio, jornalismo, educacional.

## Frente F — Racionalização em modelos encoder

| Artigo | Fonte da racionalização | Mecanismo | Alvo |
|---|---|---|---|
| **Zaidan, Eisner & Piatko**, NAACL-HLT 2007 | humana extrativa | features de contraste | SVM (origem histórica do termo) |
| **ERASER** — DeYoung et al., ACL 2020, arXiv:1911.03429 | — | benchmark: *plausibility* e *faithfulness* | agnóstico; eraserbenchmark.com |
| **Bao, Chang, Yu & Barzilay**, EMNLP 2018, arXiv:1808.09367 | humana extrativa | mapeia racionalização para pesos de atenção | encoder (RNN/CNN); github.com/YujiaBao/R2A |
| **Huang, Zhu, Feng & Zhao**, ACL 2021, arXiv:2106.01809 | **ruidosa / distante** | duas perdas auxiliares para racionalização imperfeita | classificador encoder |
| **REFER** — Ghasemi Madani & Minervini, CoNLL 2023, arXiv:2310.14418 | humana | extrator diferenciável fim-a-fim | não confirmado |
| **Herrewijnen, Nguyen, Bex & Gatt**, EACL 2026, aclanthology.org/2026.eacl-long.31 | humana extrativa | regularização de atenção | **encoder-only confirmado**; github.com/UtrechtUniversity/attention-regularisation-with-rationales |
| **Kamp, Beinborn & Fokkens**, AACL 2025 | humana | token-classification vs. atenção regularizada | encoder-classificador |
| **SRA** — Eilertsen et al., AAAI 2026, arXiv:2511.07065 | humana | perda conjunta atenção↔racionalização | classificador transformer; avalia em **HateBRXplain (pt-BR)** |
| **CAGE** — Rajani, McCann, Xiong, Socher, ACL 2019, arXiv:1906.02361 | humana texto livre (CoS-E) | gera explicação e concatena | **gerador (GPT)**; github.com/salesforce/cos-e |
| **Hase & Bansal**, arXiv:2102.02201, LNLS @ ACL 2022 | — | framework formal sobre quando explicação ajuda | conceitual |
| **Pruthi et al.**, TACL 2022, arXiv:2012.00893 | — | mede utilidade da explicação pelo ganho do "aluno" | framework de avaliação |
| **Wiegreffe & Marasović**, NeurIPS D&B 2021 | — | taxonomia: *highlights* / *free-text* / *structured* | survey de posicionamento |
| **Li, Schlegel et al.**, arXiv:2508.16777 (venue não confirmado) | **LLM texto livre → reduzido a spans** | BCE de atenção contra máscara binária · formulação NER | codificação ICD; **mecanismo LIDO 10/09: canal de atenção, não ocupa H1/H2** — `docs/artigos/notas-li-icd-2508.16777.md` |

**Em português:** HateBRXplain (Salles, Vargas, Benevenuto, COLING 2025,
aclanthology.org/2025.coling-main.446 — 7 mil comentários com racionalização humana,
github.com/isadorasalles/HateBRXplain) · HateBRMoralXplain / SMRA (Vargas et al., Findings ACL 2026,
arXiv:2601.03481). **Nenhum destila racionalização de LLM para encoder em pt-BR.**

## Frente G — Verificação dos mecanismos H1 e H2

| Artigo | Relevância |
|---|---|
| **LRKD** — Qiu et al., arXiv:2601.21611, WWW'26, DOI 10.1145/3774904.3792812 (Alibaba) | **Ocupa o H1**: MSE entre vetor latente de um cross-encoder BERT e embedding BGE-M3 congelado da racionalização de LLM. Sem código |
| arXiv:2609.05363 — GenAIECommerce @ RecSys 2026 (submetido 04/09/2026) | Muito próximo do H1: MSE + InfoNCE + KL relacional; projeção **descartada na inferência** |
| **Rationale-Guided Distillation for E-Commerce Relevance** — Agrawal, Ahemd, Sembium (Amazon), COLING 2025 Industry, aclanthology.org/2025.coling-industry.12 | **LIDO EM NÍVEL 2 (Claude, 10/09). OCUPA O H2** — BERT 110M + decoder T5 base como cabeça auxiliar, descartado na inferência; variante de embedding ocupa o H1. Sem controle, sem OOD, BR não-significante, baseline de GLUE quebrado. Notas: `docs/artigos/notas-agrawal-coling2025.md`. (A nota anterior "PDF ilegível" estava errada — o PDF da ACL extrai limpo.) |
| **KEPLER** — arXiv:1911.06136 | Precedente distante: injeção de conhecimento por perda latente, sem professor congelado |
| **ExpBERT** — Murty, Koh & Liang, ACL 2020, arXiv:2005.01932 | Canal diferente: explicação como **texto de entrada concatenado**; github.com/MurtyShikhar/ExpBERT |
| **DHRD** — Xu et al., arXiv:2509.21487, NeurIPS 2025 Efficient Reasoning Workshop | **Vizinho do H2**: cabeça de raciocínio treino-only desligada no teste, mas **backbone decoder-only**. Sem código |
| **Deeply-Supervised Nets** — Lee, Xie, Gallagher, Zhang, Tu, arXiv:1409.5185, AISTATS 2015 | Precedente do padrão "cabeça descartada na inferência" (visão) |
| **WT5** — Narang, Raffel et al., arXiv:2004.14546 · **SCOTT** — Wang et al., ACL 2023, arXiv:2305.01879 | Contraste: auto-explicação **mantém** o gerador na inferência |
| **Chronopoulou, Baziotis, Potamianos**, NAACL 2019, arXiv:1902.10547 | Parente distante: perda auxiliar de LM genérico no fine-tuning |

---

# Taxonomia de métodos (análise sobre a Frente A+B+C, 18 artigos)

Pergunta que originou: quantos dos "grupos temáticos" compartilham o mesmo método?

**Resposta: 11 dos 18 usam literalmente o mesmo método; somando os que o contêm como núcleo de
avaliação (MobileLLM, QLoRA, Nougat), são 14 de 18.**

O esqueleto dominante:

> 1. Escolha tarefas com métrica objetiva.
> 2. Fixe tudo — protocolo de ajuste, dados de avaliação, sementes.
> 3. Varie **um único fator**.
> 4. Meça contra baseline, idealmente com teto e piso.
> 5. Relate a diferença e discuta se ela é maior que o ruído.

O que muda entre os "grupos" é **apenas qual fator varia**: o modelo (Frentes D e E), o dado de
treino (LIMA, AlpaGasus, LESS), qual artefato entra no protocolo (benchmarks), quem executa a tarefa
(Better Bill GPT), ou um componente interno (MobileLLM — que é ablação, o mesmo esqueleto com o
fator dentro do sistema).

**Só quatro fogem disso**, em três famílias: análise descritiva sem treino (auditoria do C4);
reanálise de resultado publicado (Mirage); construção e relato (Docling, SmolLM2).

**Consequência prática:** não há dezoito coisas a aprender — há uma (comparação controlada) mais
duas variantes baratas. Os seis instrumentos do `docs/pesquisa/mapa-do-terreno.md` são o kit dessa uma.

## Lista de leitura — versão de 10/09/2026 (tema v3)

⚠ **A lista anterior, deduplicada por método (DeBERTinha, QLoRA, MobileLLM, SmolLM2, auditoria do
C4, Better Bill GPT, benchmark clínico), foi DESCARTADA** — servia ao tema v2, quando a âncora era
SLM e fusão. Com o tema em encoders, papers de eficiência de memória de modelo grande perderam
função: ajustar um BERT-base não é essa luta.

### Nível 1 — ler ANTES de comprometer as 16 semanas

| # | Artigo | Por que agora | O que procurar |
|---|---|---|---|
| 1 | **Distilling Step-by-Step** · arXiv:2305.02301 · ACL 2023 Findings | origem da ideia e mecanismo a transportar. **Pedro em andamento** | como sinalizam ao T5 qual tarefa produzir; gráficos com % de dados no eixo x |
| 2 | **BERT, are you paying attention?** · aclanthology.org/2026.eacl-long.31 | define o que NÃO fazer e o controle obrigatório. **Claude leu integral** | protocolo do dataset sintético de correlação espúria (§3.2.2, código público); teste com rótulos embaralhados |
| 3 | **DHRD** · arXiv:2509.21487 · NeurIPS 2025 Workshop | **decide se o H2 é novo.** Só resumo de agente | como acoplam a cabeça; perda exata; escala; **limitações e trabalho futuro declarados** |
| 4 | **LRKD** · arXiv:2601.21611 · WWW'26 | ocupa o H1 e usa aluno BERT. Só resumo de agente | por que extrator GAT em vez do CLS direto; se comparam canais |
| 5 | **Rationale-Guided Distillation** · aclanthology.org/2025.coling-industry.12 | incógnita — extração de PDF falhou, exige leitura manual | **uma coisa só:** qual é o mecanismo (regressão latente? texto concatenado?) |

### Nível 2 — para desenhar o estudo

6. **HateBRXplain** · aclanthology.org/2025.coling-main.446 — se for o dataset: como anotaram, concordância, formato da racionalização.
7. **Exploring Distantly-Labeled Rationales** · arXiv:2106.01809 — racionalização **ruidosa**, que é o que racionalização de LLM é. Provavelmente o mais útil deste nível.
8. **Teach Me to Explain** — Wiegreffe & Marasović, NeurIPS D&B 2021 — taxonomia *highlights / free-text / structured*, a frase de posicionamento.
9. **ERASER** · arXiv:1911.03429 — vocabulário de *plausibility* e *faithfulness*.

### Nível 3 — para escrever e citar

10. ~~**Li et al.** (ICD) · arXiv:2508.16777~~ — **LIDO 10/09** · 11. **SCOTT** · arXiv:2305.01879 (contraste: auto-explicação mantém o gerador) · 12. **Deeply-Supervised Nets** · arXiv:1409.5185 (curto, precedente da cabeça descartada) · 13. **Bao et al.** · arXiv:1808.09367 (origem de "racionalização vira peso de atenção").

**Excluído por decisão do Pedro (10/09):** reanálise de resultado publicado como *objeto de estudo
próprio* — exige julgar premissas de outros pesquisadores e demanda precisão que não cabe numa
primeira pesquisa. Continua válida como **interferência anterior** para ler e citar.
