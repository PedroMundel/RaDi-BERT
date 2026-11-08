# Tema v3 — Racionalização de LLM em modelos encoder

Estado: **direção viva, hipóteses formuladas, verificação de novidade PENDENTE.**
Origem: ideia do Pedro em 10/09/2026, lendo o Distilling Step-by-Step. É a primeira direção da
residência que nasceu dele lendo, não de lista proposta pelo Claude.

Substitui na prática o `tema-v2-fusao-slm.md` (fusão de adaptadores), que perdeu força quando o
próprio Pedro derrubou o argumento de mercado — servidores já carregam vários adaptadores sobre
uma base única, então fundir perde para trocar em quase todo cenário empresarial.

---

## A pergunta

**Como injetar conhecimento de racionalização (justificativa) num modelo que não gera texto?**

O Distilling Step-by-Step (Hsieh et al., arXiv:2305.02301) treina um T5 (encoder-decoder) em
multi-tarefa: prever o rótulo E gerar a racionalização produzida por um LLM. Ganha desempenho com
menos dado e modelo menor. Mas encoder-only (BERT, RoBERTa, DeBERTa) não gera texto — e é
justamente o que existe pronto e adaptado a domínio em português (BERTimbau, BioBERTpt,
JurisBERT, LegalBert-pt, FinBERT-PT-BR) e o que se implanta de verdade em tarefa de rotulagem.

## As duas hipóteses de mecanismo — VERIFICADAS em 10/09/2026

### H1 — Regressão para o embedding da racionalização — **OCUPADA**

Uma cabeça auxiliar do encoder prevê o **vetor** da racionalização, produzido por um codificador de
sentenças congelado (cosseno ou MSE).

**Já existe:**
- **LRKD** — Qiu et al., "Thinking Broad, Acting Fast: Latent Reasoning Distillation from
  Multi-Perspective Chain-of-Thought for E-Commerce Relevance", arXiv:2601.21611, **WWW'26**,
  DOI 10.1145/3774904.3792812 (Alibaba). Perda `L_guide = ||r_qp − e_cot||²` onde `e_cot` é o
  embedding BGE-M3 **congelado** da racionalização do LLM. Student é cross-encoder **BERT-based**.
  Sem código localizado.
- arXiv:2609.05363 (workshop GenAIECommerce @ RecSys, submetido **04/09/2026**) — MSE + InfoNCE +
  KL relacional contra embedding bge congelado; cabeça de projeção **descartada na inferência**.
- Não confirmado: Agrawal et al. (Amazon), "Rationale-Guided Distillation for E-Commerce Relevance
  Classification", COLING 2025 Industry (aclanthology.org/2025.coling-industry.12/) — abstract
  confirma racionalização de LLM guiando cross-encoders, **mecanismo não extraível do PDF**.
  Precisa de leitura manual.

**Lacuna que sobra:** classificação de texto único com regressão do CLS puro, fora de e-commerce.
Fina demais — é o tipo de diferença que se chama de incremental.

**Precedente de outro canal, a citar de qualquer forma:** ExpBERT (Murty, Koh & Liang, ACL 2020,
arXiv:2005.01932) usa explicação como **texto de entrada concatenado**, não como alvo latente.
Precedente estrutural mais distante: KEPLER (arXiv:1911.06136), injeção de conhecimento por perda
latente, mas sem professor congelado.

### H2 — Cabeça decodificadora auxiliar, descartada na inferência — **HIPÓTESE VIVA**

Decoder leve acoplado ao encoder **apenas no treino**, forçando a geração da racionalização;
descartado na entrega, sobrando encoder puro com custo de encoder puro.

**O mecanismo existe, mas não nesta arquitetura:**
- **DHRD (Dual-Head Reasoning Distillation)** — Xu et al., arXiv:2509.21487, **NeurIPS 2025
  Efficient Reasoning Workshop**. Cabeça de classificação (treino+inferência) + cabeça de raciocínio
  supervisionada por CoT do professor, **desligada no teste**. Perda = CE do rótulo + LM loss sobre
  entrada+racionalização. **Backbone decoder-only causal** — não testam BERT/RoBERTa/DeBERTa.
  Sem código localizado.
- Precedente do padrão "cabeça descartada": **deep supervision** / classificadores auxiliares —
  Deeply-Supervised Nets (Lee et al., AISTATS 2015, arXiv:1409.5185) e GoogLeNet. Visão, não NLP.
- Contraste confirmado: modelos auto-explicativos **mantêm** o gerador — WT5 (Narang et al.,
  arXiv:2004.14546) e SCOTT (Wang et al., ACL 2023, arXiv:2305.01879).
- Parente distante: Chronopoulou et al., NAACL 2019 (arXiv:1902.10547) — perda auxiliar de LM
  genérico durante fine-tuning, sem conteúdo de explicação.

**Lacuna:** puramente arquitetural e clara — ninguém aplicou o dual-head treino-only sobre encoder
bidirecional. Nome citável: "train-time-only reasoning head" (cunhado pelo DHRD), ancorado na
tradição de deep supervision.

**A pergunta a responder:** "você só construiu um T5 e jogou metade fora?" — a resposta é que se
inicializa a partir de um encoder **já adaptado ao domínio e à língua** (BERTimbau, BioBERTpt,
LegalBert-pt), e não existe T5 equivalente adaptado em português.

### Comparação

**H2 é a hipótese mais forte.** O que seria a novidade do H1 (aplicar a encoder) já foi feito pelo
LRKD sobre um BERT. A lacuna do H2 é arquitetural e ninguém a ocupou.

### H1 + H2 mesclados (Pedro, 10/09) — provavelmente o desenho certo

As duas hipóteses **não são excludentes**. As três cabeças penduram no mesmo encoder:

`L = α·L_classificação + β·L_embedding + γ·L_geração`

H1 sozinho é γ=0; H2 sozinho é β=0; baseline é ambos zerados. **A ablação vira o próprio desenho.**

**O que a mescla compra:**
1. **Elimina confundidor** — mesmo encoder, mesma semente, mesmo dado; só o canal varia. Comparar em
   rodadas separadas deixaria diferença de inicialização e ordem de dados contaminando o resultado.
2. **Cria pergunta que ninguém pode ter respondido:** os dois canais são **redundantes ou
   complementares?** Ninguém tem os dois no mesmo lugar.
3. Intuição de mecanismo por trás: embedding é sinal **global e grosso** (um vetor para a
   justificativa inteira); geração é sinal **sequencial e fino** (ordem e especificidades). Naturezas
   diferentes o bastante para plausivelmente somarem — ou não, e descobrir qual é o resultado.

**Custo:** três pesos a ajustar. O DHRD já relata sensibilidade só ao β (4B regride com β alto).

**A conta que fecha a favor:** o DHRD reporta **rodada única, sem IC, por restrição de computação**,
com backbones de 3–8B. Com encoder de 110M, uma rodada leva minutos. Cinco condições (baseline · H1 ·
H2 · ambos · **controle aleatório**) × 5 sementes × 1–2 tarefas = 25–50 rodadas, viável na RTX 5060.

→ **A restrição de hardware, que parecia limitação, viabiliza o desenho que o time do Google não pôde
pagar.** Eles tiveram escala e uma rodada por configuração; o Pedro tem grade completa com
estatística. É vantagem declarável no paper.

**Honestidade sobre novidade:** com H1 ocupado (LRKD) e H2 quase ocupado (DHRD), "os dois juntos num
encoder" é novo mas modesto. O trabalho não se sustenta numa alegação grande, e sim em três pequenas
somadas: transferência para encoder · pergunta redundante-vs-complementar · estatística que os
vizinhos não fizeram. Para um primeiro artigo isso é o formato normal e é suficiente.

**Disciplina de escopo:** um backbone, uma ou duas tarefas, cinco condições. Três backbones e quatro
tarefas não terminam em 16 semanas.

### Sinal de tempo e de competição

Os trabalhos de H1 são de **janeiro e setembro de 2026**, ambos de indústria (Alibaba, Amazon).
Lê-se dos dois lados: prova que a motivação de custo de inferência é real e não retórica do tema;
e indica que o terreno tem times com muito mais recurso trabalhando agora. Qualquer coisa aqui tem
prazo.

## A ponte teórica (o argumento de introdução)

Os papers-chave não se contradizem porque injetam racionalização por **canais diferentes**:

| | Canal | Fonte da racionalização | Resultado |
|---|---|---|---|
| Distilling Step-by-Step | **objetivo de saída** — o modelo tem que produzir a justificativa | LLM, texto livre | funciona |
| **DHRD** (Xu et al. 2025) | **objetivo de saída**, cabeça descartada no teste | LLM (Gemini 2.5 Flash) | funciona, e a ablação mostra que é **conteúdo**, não regularização |
| Herrewijnen et al., EACL 2026 | **restrição sobre mecanismo interno** — atenção forçada a olhar certos tokens | humana, extrativa | majoritariamente ruído (tokens aleatórios empatam) |
| **Li et al.** (arXiv:2508.16777) | **restrição sobre atenção** — BCE contra máscara de tokens | **LLM**, reduzida a spans | **sem ganho de acurácia** (68,18 → 67,93 F1-mac); só plausibilidade |

As quatro linhas separam limpo: **canal de saída rende acurácia; canal de atenção não** — e a última
linha fecha a escapatória de que o problema fosse a fonte humana da racionalização. Com LLM no canal
de atenção, também não rende. Ressalva a declarar: Li et al. não otimizavam acurácia.

O argumento: **atenção não é o processo de decisão.** O próprio Herrewijnen sustenta isso sem
explorar — as explicações SHAP não mudam depois da regularização, ou seja, o padrão de atenção
mudou e a forma de decidir não. Restringir atenção não restringe a decisão; um objetivo de saída
obriga a representação interna a carregar o conteúdo, porque sem isso o modelo não o produz.

H1 e H2 são as duas formas de dar objetivo de saída a um modelo que não tem saída de texto.

## O argumento forte — a arquitetura como INSTRUMENTO (10/09, ao diagramar)

Surgiu ao desenhar a versão encoder da Figura 2 do Distilling Step-by-Step, a pedido do Pedro.

**O que o desenho revela:** a racionalização é descartada na inferência **nos dois casos**, mas o
que é descartado é diferente.

| | O que é descartado | O que sobrevive |
|---|---|---|
| **T5 (paper original)** | só a **saída** de racionalização | o modelo inteiro — encoder E decoder. O caminho do rótulo passa pelo mesmo decoder que aprendeu a gerar justificativa |
| **Versão encoder (H2)** | a **cabeça inteira** | só o encoder |

**A pergunta que isso torna precisa:** no T5, onde mora o conhecimento que a racionalização ensinou?
Se mora em boa parte no decoder, descartar o decoder descarta o benefício. Se mora na representação
do encoder, a versão encoder preserva.

**E o ponto que muda o enquadramento do trabalho:** no T5 é *impossível* separar as duas coisas —
encoder e decoder são treinados juntos e mantidos juntos. Na versão encoder a separação é
**arquitetural**: se a cabeça é descartada, qualquer efeito que sobreviva TEM que estar na
representação, porque não sobrou outro lugar.

→ A arquitetura deixa de ser apenas um alvo mais barato de implantação e vira **instrumento de
medição** para uma pergunta que o desenho original não consegue responder.

Isso reposiciona a contribuição: sai de "portei uma técnica para outra arquitetura" (fraco, convida
o "por que não usar um T5") e vira "usei uma restrição arquitetural para isolar onde o sinal da
racionalização se aloja". **Funciona nos dois sentidos:** se der certo, o conhecimento cabe na
representação; se não der, ele precisa do decoder. Ambos são achados.

Detalhe menor que o desenho também expõe: os **prefixos de tarefa desaparecem** na versão encoder —
são necessários no T5 porque as duas saídas saem do mesmo lugar; com cabeças fisicamente separadas,
não há ambiguidade a resolver.

## O que já está estabelecido (verificado)

**Herrewijnen, Nguyen, Bex & Gatt (2026)** — "BERT, are you paying attention? Attention
regularisation with human-annotated rationales", EACL 2026, pp. 720–751.
Código: github.com/UtrechtUniversity/attention-regularisation-with-rationales
PDF lido integralmente em 10/09/2026. Achados:
- Regularização de atenção melhora desempenho ID e OOD, sobretudo com poucos dados (100–200 ex.).
- **Tokens aleatórios rendem melhora parecida com racionalização humana.**
- Explicação deles: o ganho vem do **ruído** impedindo sobreajuste (testado com rótulos
  embaralhados; citam Bishop 1995, ruído ≈ regularização de Tikhonov).
- **Exceção importante:** racionalização humana VENCE tokens aleatórios contra **correlação
  espúria** (dataset sintético deles), e λ maior reduz a dependência.
- SHAP não muda após regularização.
- Limitação declarada por eles: datasets de **texto curto**; convidam trabalho futuro em textos longos.

**Levantamento de trabalho anterior (verificado por agente, 10/09/2026):** existem duas literaturas
que não se cruzam — supervisão de racionalização em encoders usa racionalização **humana
extrativa** (Bao 2018; Huang ACL 2021; REFER CoNLL 2023; Herrewijnen EACL 2026; Kamp AACL 2025;
SRA AAAI 2026), e racionalização em **texto livre de LLM** alimenta modelos **geradores** (CAGE
ACL 2019; Distilling Step-by-Step 2023). A célula que cruza os dois aparece vazia. Vizinho mais
próximo: Li et al. (arXiv:2508.16777), codificação médica ICD — **mecanismo LIDO em 10/09/2026: é
extrativo (BCE de atenção contra máscara binária, e formulação NER). A célula segue vazia.**

**Em português:** existe racionalização humana com supervisão de atenção — HateBRXplain (COLING
2025, 7 mil comentários anotados, código aberto), HateBRMoralXplain (Findings ACL 2026), SRA (AAAI
2026). Não existe destilação de racionalização de LLM para encoder em pt-BR.

**Taxonomia para posicionar:** Wiegreffe & Marasović (2021) separa explicações em *highlights*
(extrativo), *free-text* e *structured*. Este trabalho pega fonte em free-text e alvo em highlight.

## Regra que passou a ser obrigatória

**Controle aleatório em qualquer experimento deste espaço.** Herrewijnen mostrou que um baseline
faltante invalidou boa parte de uma literatura. Propor supervisão por racionalização sem comparar
contra tokens aleatórios = trabalho derrubado em uma frase, citando esse paper.

## Desenho de estudo que emerge

Comparar os dois canais lado a lado, no mesmo encoder, no mesmo setup:

- Piso: sem racionalização
- **Controle: tokens aleatórios** (obrigatório)
- Canal 1: regularização de atenção (previsão: ruído)
- Canal 2: objetivo de saída, via H1 ou H2 (previsão: transfere conhecimento)
- Teto: racionalização humana, onde existir
- Eixos: desempenho geral · sensibilidade a correlação espúria (protocolo sintético do Herrewijnen,
  código público) · volume de dado (eixo do Distilling Step-by-Step)

Qualidade rara desse desenho: **hipótese com direção prevista**, derivada de dois resultados
publicados, e falsificável nos dois sentidos — se o canal de saída também for ruído, a conclusão
("racionalização não transfere para encoders") é achado forte que fecha uma pergunta aberta.

## Pendências

1. ~~Verificar H1~~ — FEITO 10/09. Ocupada (LRKD, WWW'26).
2. ~~Verificar H2~~ — FEITO 10/09. Viva; lacuna arquitetural.
3. **Ler o DHRD (arXiv:2509.21487)** — PDF baixado em `docs/artigos/2509.21487v2-dhrd.pdf`.
   **Claude leu e reconferiu em 10/09; falta o Pedro terminar.** Venue resolvido: é o **Efficient
   Reasoning Workshop** do NeurIPS 2025 (campo *Comments* do arXiv), não a conferência principal —
   o rodapé do PDF é só o texto padrão do estilo. Reconferência confirmou todos os números das notas
   e **fortaleceu** o argumento de entrada: a razão declarada para recusar bidirecionalidade tem duas
   metades (*evitar vazamento de token futuro* **e** *casar com pré-treino autorregressivo*) e
   **nenhuma das duas se aplica a um encoder**. Detalhes em `docs/artigos/notas-dhrd-xu2025.md`.
4. ~~**Ler Li et al. (arXiv:2508.16777)**~~ — **FEITO 10/09/2026 (Claude; Pedro não leu).
   NÃO derruba a novidade e reforça a premissa.** Os dois mecanismos deles são extrativos: BCE dos
   pesos de atenção contra máscara binária de tokens, e formulação NER. A racionalização de texto
   livre do LLM é **reduzida a spans antes de entrar no treino** — nunca é alvo de saída nem de
   representação. E o dado que interessa: sobre o **PLM-ICD, que é encoder**, supervisionar atenção
   com racionalização de LLM **não deu acurácia** (68,18 → 67,93 F1-macro), só plausibilidade (+1%).
   **Terceira corroboração independente de que o canal de atenção não carrega conhecimento**, agora
   com racionalização de LLM e em domínio clínico. Ressalva: eles não otimizavam acurácia e não
   usaram controle aleatório — é evidência convergente, não replicação. Notas em
   `docs/artigos/notas-li-icd-2508.16777.md`. Venue "EACL 2026" não se sustenta na fonte.
5. ~~**Ler manualmente Agrawal et al.**~~ — **FEITO 10/09/2026 (Claude, nível 2; Pedro não leu).
   RESULTADO RUIM: ocupa o H2, e a variante "Embedding-based Reasoning" ocupa o H1.**
   BERT base 110M + **decoder T5 base** como cabeça auxiliar autorregressiva,
   `L_total = L_classification + λ·L_aux` com λ=0,1, **cabeça descartada na inferência**. Professor
   Mixtral 8×7B. +6% ROC-AUC em GLUE (RTE e QNLI inclusos), 110M empatando com LLM de 7B a 50× a
   velocidade. Eles ainda resolvem a **pendência 9b**: warmup em duas fases, decoder treinado sozinho
   com BERT congelado em 50% dos dados, e o T5 é pré-treinado, não nasce do zero.
   Notas completas em `docs/artigos/notas-agrawal-coling2025.md`.

   **O que morre:** a cabeça auxiliar descartada como **contribuição de mecanismo**, e a célula vazia
   da taxonomia ("racionalização de LLM em texto livre → encoder pelo canal de saída"). Ocupada.

   **O que sobrevive, e é a pergunta melhor posta do projeto:** eles **não rodaram nenhum controle**.
   A §5.2 deles, intitulada "Ablations", é mapa de atenção e Shapley — sem racionalização embaralhada,
   sem texto aleatório, sem fora de domínio, sem varredura de λ. A alegação causal central do paper
   (que o ganho vem do **conteúdo**) não tem evidência que a sustente.

   | Trabalho | Arquitetura | Canal | Controle? | Conclusão |
   |---|---|---|---|---|
   | Herrewijnen (EACL 2026) | encoder | atenção | **sim** | **é ruído** |
   | Li et al. (2508.16777) | encoder | atenção | não | sem ganho de acurácia |
   | DHRD (Xu 2025) | **decoder** | **saída** | **sim** | **é conteúdo** |
   | Agrawal (COLING 2025) | **encoder** | **saída** | **NÃO** | afirma conteúdo, sem evidência |

   → **A célula vazia deixou de ser a do mecanismo e passou a ser a do controle.** Ninguém rodou
   racionalização embaralhada sobre o canal de saída de um encoder. É precedente direto do Herrewijnen,
   que é um paper inteiro de EACL construído sobre testar o baseline que faltava.

   **Tensão a decidir (do Pedro, não deslizar):** isso encosta no que o `CLAUDE.md` rejeitou em 10/09,
   "reanálise de resultado publicado como objeto de pesquisa próprio". Não é idêntico — não se julga a
   análise deles, roda-se uma condição experimental nova que eles não rodaram. Mas é adjacente o
   bastante para exigir decisão explícita.

   **Efeito colateral bom:** o Agrawal **reduz o risco da capacidade latente**, que era o risco nº 1.
   Com exatamente 110M de parâmetros, o sinal rende +6% em GLUE. Há algo lá para mexer; o que segue
   aberto é se foi conteúdo ou regularização.
6. Busca sistemática com string (uma passagem de agente não é revisão sistemática).
7. Decidir dataset e tarefa. **Correção de 10/09:** racionalização humana anotada NÃO é requisito —
   quem gera a racionalização é o LLM professor, olhando os dados. Basta um dataset **com rótulos**.
   Isso abre o leque (ex.: **ASSIN2**, inferência textual em pt-BR, presente em quase todos os papers
   levantados). HateBRXplain deixa de ser requisito e vira **extra valioso**: serve de teto humano
   para responder "quão perto a racionalização de LLM chega da humana".
   **Mas a escolha de tarefa é crítica** — ver hipótese do tipo de tarefa abaixo.

   **VERIFICAÇÃO CONCRETA FEITA EM 10/09 — `docs/datasets-nli-verificacao.md`.** Números,
   procedência e tabela dos dois eixos estão lá. Três achados que mudam o quadro:

   - **O ASSIN2 é BINÁRIO** (entailment / non-entailment), não três classes. Os organizadores
     removeram paráfrase e **excluíram contradição de propósito**. Fonte primária lida (overview
     CEUR, §2.3).
   - **O ASSIN2 foi construído A PARTIR do SICK-BR, que é tradução do SICK, que vem de legendas de
     imagem.** Os organizadores escrevem que escolheram essa base justamente por ter "**menos
     fenômenos linguísticos complexos**" e "**apenas fatos simples**" (§2.1). Isso é o **oposto**
     do critério da pendência 8, que elegeu inferência textual porque a racionalização carregaria um
     passo que não está na superfície. **O ASSIN2 pode ser o caso de análise de sentimento
     disfarçado de NLI** — e um resultado nulo nele seria ambíguo entre "não transfere" e "não
     havia o que transferir".
   - **O SICK-BR está QUEIMADO como conjunto fora de domínio do ASSIN2** (é a fonte dele). O único
     par OOD viável em pt-BR é **ASSIN2 → ASSIN 1** (notícias, 3 rótulos), colapsando
     `PARAPHRASE` em `ENTAILMENT`. Legítimo, porém montado por nós; o inglês tem protocolo
     consagrado e citável (e-SNLI → SICK-E / MultiNLI, com o piso de 46,7% de Bowman et al.).

   Recomendação registrada no arquivo (**e-SNLI subamostrado**), com o motivo: é o único eixo em
   que a hipótese consegue **falhar de forma informativa**. **A decisão é do Pedro.**

8. **Hipótese do tipo de tarefa (Claude, 10/09 — não é afirmação de nenhum paper lido):** talvez a
   diferença entre o resultado positivo do Distilling Step-by-Step e o negativo do Herrewijnen não
   seja encoder vs. gerador, e sim **tarefa de raciocínio vs. tarefa de classificação**. Os datasets
   do primeiro exigem passos de inferência (e-SNLI, ANLI, CQA, SVAMP); os do segundo são
   classificação por reconhecimento de padrão (sentimento, discurso de ódio, posição).

   Tornou-se concreto ao diagramar com exemplo: em NLI a racionalização carrega um passo de
   inferência ("pode estar treinando, mas não necessariamente") que **não está na superfície do
   texto**. Em sentimento, a racionalização apenas aponta para uma palavra que o modelo já vê — não
   sobra nada para a cabeça auxiliar ensinar.

   → **Inferência textual é o cruzamento**: é classificação (encoder resolve) e exige raciocínio.
   É a escolha natural de tarefa, e o ASSIN2 é o candidato em português.

9. **Decisão de projeto ainda aberta:** a seta do encoder para a cabeça auxiliar é, na prática,
   atenção cruzada. Quantas camadas? Atende a todos os estados do encoder ou só ao vetor da
   sentença? Afeta quanto sinal chega à representação — e, pelo argumento do instrumento, é
   exatamente isso que se quer maximizar.

9b. **CONFUNDIDOR NOVO (10/09, ao responder "por que o DHRD importa se é para decoder"): a cabeça
    auxiliar do DHRD é de graça, a do tema v3 não é.** O DHRD **reaproveita a cabeça de LM do
    próprio modelo base** — já pré-treinada, já sabe gerar. Um encoder não tem cabeça de geração
    sequencial para reaproveitar (a MLM do BERT não é geração autorregressiva), então o decoder
    auxiliar do H2 nasce **inicializado do zero**.

    **Por que isso é confundidor e não só custo:** se o H2 render pouco, há duas explicações
    opostas e o desenho atual não as separa —
    (a) racionalização não transfere para encoder (achado sobre o tema), ou
    (b) a cabeça nova era fraca demais para produzir gradiente útil (achado sobre a implementação).

    **Consequências para o desenho, a decidir:**
    - O braço H1 **não sofre disso** (projeção linear contra embedding congelado não precisa saber
      gerar). Então uma assimetria H1 > H2 pode ser artefato de inicialização, não de canal — o que
      atinge diretamente a pergunta "redundante ou complementar?".
    - Mitigação candidata: inicializar a cabeça do decoder a partir de um decoder pequeno já
      pré-treinado da mesma língua (ex.: decoder do PTT5, ou um GPT-2 pequeno em pt-BR), em vez de
      aleatório. Verificar se existe algo compatível em tokenizer.
    - Mitigação mais barata: incluir como condição de controle uma cabeça auxiliar **com pesos
      congelados aleatórios**, que mede o piso do canal de geração sem conteúdo aprendido.
    - Nada disso foi verificado. É decisão do Pedro.

10. **Avaliação FORA de domínio é obrigatória** — decorrente da objeção do Pedro (10/09): se a
    racionalização só ajuda em cenários parecidos com o treino, o método vale menos do que parece.
    Sem teste fora de domínio, o trabalho não consegue responder a própria pergunta.

    **Acrescentado em 10/09 pela verificação (`docs/datasets-nli-verificacao.md`):** o §4.5 do
    paper do e-SNLI **já testou isso** e o resultado foi fraco — a melhoria de acurácia com o sinal
    de explicação na transferência sem fine-tuning foi, nas palavras deles, "muito pequena", e a
    qualidade das explicações geradas fora de domínio desabou (30,64% corretas em SICK-E, 1,92% em
    MultiNLI). Era InferSent, arquitetura pré-Transformer, e a racionalização era humana, não de
    LLM. **Não derruba o tema, mas é interferência anterior direta sobre a pendência 10 e precisa
    ser citada** — quem propõe teste OOD com racionalização tem que dizer o que sabe do resultado
    de 2018. Claude leu (nível 2); o Pedro não.

## A objeção da generalização (Pedro, 10/09) e o que ela vira

**A objeção:** o modelo pequeno não raciocina na inferência — logo, aprende os resultados do
raciocínio sobre a distribuição de treino, e deve degradar em cenário novo.

**Análise (Claude — não está enunciada assim em nenhum paper lido):** a racionalização pode ajudar
por quatro mecanismos, que não generalizam igual.

| # | Mecanismo | Generaliza? |
|---|---|---|
| 1 | aponta onde olhar (afasta de atalhos espúrios) | sim, se as pistas forem parecidas no domínio novo |
| 2 | ruído regularizador (explicação do Herrewijnen) | sim — mas por motivo alheio a conhecimento |
| 3 | injeta conhecimento de mundo ausente do dataset | só se o caso novo precisar do MESMO conhecimento |
| 4 | ensina o procedimento de raciocínio | **não** — profundidade fixa não executa passos arbitrários |

O nome "raciocínio" sugere o mecanismo 4, que é justamente o que não transfere. A objeção do Pedro
procede exatamente aí.

**Fato empírico relevante (Herrewijnen, lido):** ele mediu fora de domínio e **achou ganho**, maior
com pouco dado de treino — mas atribui ao ruído, não ao conhecimento. Logo: o ganho OOD existe, a
causa está em disputa.

**Escopo:** a objeção vale igualmente para o paper original — no T5 também não há raciocínio em
tempo de inferência, só decodificação de um rótulo curto. **Não é argumento a favor de usar T5.**

**Destino da objeção — vira eixo de medida.** Copiar a estrutura do Herrewijnen (treina em um, testa
dentro e fora) e somar o controle de tokens aleatórios:
- aleatório dá o mesmo ganho OOD → é regularização (mec. 2);
- racionalização dá mais → é conhecimento (mec. 1 e 3);
- ganho some fora do domínio → mediu-se o limite que a objeção previa.

Os três resultados são publicáveis e os três respondem à pergunta.

### Desdobramento (Pedro, 10/09): o encoder produz vetor de justificativa sem decoder?

Sim no H1 — a cabeça é uma projeção linear, produz vetor a cada passagem, e **descartá-la é escolha,
não necessidade** (manter custa quase nada). Não no H2 — sem decoder não há racionalização alguma.

**Mas produzir vetor ≠ raciocinar:** em profundidade fixa o encoder *completa um padrão*, estima o
destino sem percorrer os passos. A objeção da generalização permanece intacta.

Espaço de projeto completo, e cada linha já tem ocupante:

| Variante | Saída na inferência | Custo | Ocupante |
|---|---|---|---|
| Cabeça descartada (H2) | só o rótulo | zero | DHRD |
| Vetor mantido (H1) | rótulo + vetor de justificativa | desprezível | LRKD e vizinhos |
| Gerando texto | rótulo + justificativa legível | caro | auto-explicação (WT5, SCOTT) |

**Ideia especulativa (Claude, 10/09 — não vista em nenhum paper lido, precisa de verificação):**
mantendo o vetor, dá para perguntar a cada exemplo se ele está próximo de alguma justificativa
plausível ou se é incoerente. Em cenário fora de distribuição — onde a objeção do Pedro prevê
degradação — o vetor previsto tenderia a ficar longe de qualquer coisa sensata. A cabeça de
racionalização mantida funcionaria como **sinal de confiança / detecção de OOD a custo desprezível**.
Não conserta a limitação; **torna a limitação detectável em tempo de inferência**.

Duas verificações antes de virar plano: (a) alguém já fez? (b) funciona mesmo, ou o vetor previsto
parece plausível mesmo quando o modelo erra?
8. Testar o ambiente na RTX 5060 (Blackwell / sm_120) — risco herdado do tema anterior, não some.

## Onde isso se aplica na indústria (análise do Claude, 10/09 — não é afirmação de paper lido)

A proposta de valor cabe numa frase: **acurácia de modelo que raciocina, ao custo de um BERT.** Logo,
as aplicações são onde se classifica em **volume alto**, com restrição de **latência ou custo**, e
onde a decisão exige uma **inferência que não está na superfície do texto**. Se qualquer um dos três
faltar, a alternativa mais simples ganha (chamar um LLM, ou usar um classificador raso).

**1. Verificação de consistência entre alegação e fonte — a mais forte.**
"Esse trecho recuperado sustenta a resposta dada?", "essa cláusula sustenta essa afirmação?", "esse
laudo sustenta esse código de diagnóstico?". Checagem de *grounding* em RAG, conferência de citação,
auditoria de evidência. **É inferência textual em produção** — mesma forma da tarefa acadêmica — e
roda várias vezes por resposta, que é exatamente onde chamar um LLM por item não fecha a conta.
→ Vantagem decisiva para o enquadramento: **a tarefa acadêmica e a história de mercado coincidem**,
em vez de uma ser enxertada na outra. Não é preciso justificar por que se estudou NLI.

**2. Triagem e roteamento em volume.** Ticket de suporte, e-mail, reclamação, protocolo. A inferência
é do tipo "isso é cobrança mesmo sem a palavra cobrança aparecer". Milhões por dia, latência conta.

**3. Conformidade e moderação por regra escrita.** "Esse texto viola a política X?" Aplicar regra é
inferência, não casamento de palavra-chave. Exige consistência, custo baixo e auditabilidade — e é
onde o **vetor mantido do H1** teria função real (confiança, priorização de revisão humana).

**4. Elegibilidade documental.** Sinistro, crédito, benefício: aplicar uma regra escrita a um texto e
decidir. Mesma forma das anteriores.

**Âncora que não é retórica:** os dois trabalhos do H1 são de **indústria** — Alibaba (LRKD, WWW'26) e
Amazon (Agrawal et al., COLING 2025 Industry) — e ambos fazem exatamente isso para relevância em
e-commerce. Prova de que o custo de inferência é motivação real; e aviso de que o terreno tem times
com muito mais recurso trabalhando agora.

**Ressalva honesta:** o trabalho entrega uma **medição**, não um produto. A aplicação é o que faz a
medição valer. Pelo teste do `docs/pesquisa/mapa-do-terreno.md` (§4), quem muda de comportamento é **a pessoa
decidindo entre pagar inferência de LLM por item ou ajustar um encoder pequeno** — decisão recorrente,
com orçamento atrás, inclusive em empresa grande.

**O que NÃO é aplicação disto** (perguntado pelo Pedro em 10/09, registrado para não voltar):
- **Geração de insight em prosa sobre documentos** — é decoder. Encoder produz rótulo ou trecho, não
  parágrafo. Nada no desenho conserta isso. O que existe é o **vetor** do H1: não é legível, mas serve
  para agrupar, ordenar por confiança e sinalizar caso fora de distribuição — estrutura sobre acervo,
  não texto explicativo.
- **NER como tarefa principal** — não é impedimento arquitetural (encoder rotula token nativamente),
  mas a maior parte das decisões de NER é superfície (maiúscula, contexto, formato); o efeito ficaria
  diluído nos poucos casos inferenciais (metonímia, aninhamento, desambiguação de domínio). Some-se
  que a racionalização passaria a ser por span, elevando as partes móveis. Descartado por custo de
  detecção, não por impossibilidade.

## Viabilidade (estimativa, não medida)

Computação alta (encoder ~110M em 8GB, rodadas de minutos, várias sementes possíveis — o que
permite distinguir efeito de ruído). Dados altos se usar HateBRXplain. Implementação média.
Escopo com risco baixo (grade pequena, sem explosão combinatória). O risco real é **tamanho de
efeito**: o Herrewijnen mostra que o teto no eixo de desempenho geral é baixo; o eixo de correlação
espúria é onde há sinal demonstrado.
