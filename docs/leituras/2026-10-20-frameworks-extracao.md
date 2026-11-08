# Frameworks da geração: extração detalhada das obras (20/10/2026)

**Pedido do Pedro (20/10):** extrair e descrever em detalhe cada framework encontrado, porque não há tempo para ler
as obras.

## Procedência (ler antes de usar)

- Cada obra foi lida **inteira por um agente** (Sonnet), com o texto completo em HTML ou PDF. O Claude conferiu
  alguns números contra a fonte: Wiegreffe 2022, Tab. 4; Hase 2020, p. 5; e-SNLI, §3.
- **Para o registro do projeto, isto é nível 3 e conta como "lido por resumo"**, a mesma categoria de Arksey &
  O'Malley e Kitchenham & Charters no Obras Lidas. **Não conta como leitura da obra** e não pode ser declarado assim
  em entregável (regra de 05/10: nunca disfarçar o uso de LLM).
- **Tudo é paráfrase.** Não há frases copiadas das obras, por direito autoral; só os nomes técnicos ficam no
  original.
- **Cada afirmação traz a seção (§).** Para citar algo num texto seu, abra a obra direto naquela seção e leia só o
  trecho: com o método das 5 paradas, aquele item passa a ser leitura sua.
- Em cada obra, o item **"Inferência do agente"** é opinião do agente, não da obra.

## Os frameworks em uma linha, e quando usar

| # | Framework | Tipo | O que dá a você | Usar na rodada |
|---|---|---|---|---|
| 1 | **Long et al. 2024** (Findings of ACL) | Esqueleto do fluxo | gerar → curar → avaliar, com as opções de cada etapa e os dois requisitos (*faithfulness* e *diversity*) | todas; é o mapa |
| 2 | Tan et al. 2024 (EMNLP) | Taxonomia | onde o seu trabalho se encaixa ("rationale" como anotação → filtrar → destilar modelo menor) e trabalhos parecidos | 1 e 3 (filtros); texto de métodos |
| 3 | Liu et al. 2024 (COLM) | Lições e riscos | riscos de dado sintético (alucinação, fidelidade, viés, contaminação) e mitigações | ameaças à validade |
| 4 | **Wiegreffe & Marasović 2021** (NeurIPS) | Recomendações de coleta de explicação | definições dos tipos de explicação (serve à pergunta do gate 5), o diagnóstico do e-SNLI e o que fazer para ter qualidade e diversidade | 0 e 1 |
| 5 | **Documentação da Anthropic** | Método operacional | critérios de sucesso → casos de teste → iterar; como corrigir (código, humano, LLM); técnicas de prompt | 0, 1 e 2; é o procedimento |
| 6 | Gebru et al. 2021, Datasheets (CACM) | Documentação | as 57 perguntas para documentar o dataset gerado, e quando responder cada uma | abre na 0, fecha na 3 |
| 7 | **Wiegreffe et al. 2022** (NAACL) | Precedente: gerar + filtrar | o pipeline mais próximo do seu (GPT-3 no e-SNLI), com rubrica de 7 atributos de qualidade e números | 1 (rubrica e exemplos) |

**Os frameworks de software** (Curator, distilabel, DataDreamer, EasyDistill) estão descritos na Parte B de
`docs/2026-10-20-frameworks-geracao.md`. A recomendação lá é manter o `gerar.py`.

**Se for ler só três partes:** a seção 3 do nº 5 (critérios), as seções 3 e 4 do nº 4 (tipos e recomendações) e as
seções 3 e 4 do nº 7 (pipeline e rubrica).

---

## 1. Extração: Long et al. 2024, survey de geração sintética com LLMs

Convenção: "§" = seção do paper. Tudo nas seções 2–6 é paráfrase do paper. A seção 7 é inferência minha e está marcada.

### 1. Identificação
- Título: "On LLMs-Driven Synthetic Data Generation, Curation, and Evaluation: A Survey".
- Autores: Lin Long, Rui Wang, Ruixuan Xiao, Junbo Zhao, Xiao Ding, Gang Chen, Haobo Wang (Zhejiang University; Harbin Institute of Technology). Correspondência: Haobo Wang.
- Venue/ano: Findings of ACL 2024 (informação do pedido; o HTML não traz a linha do venue). A versão lida traz "arXiv:2406.15126v1 [cs.CL] 14 Jun 2024".
- URL lida: https://arxiv.org/html/2406.15126v1 (não precisei do fallback ar5iv).
- Versão lida: v1 (HTML do arXiv), texto baixado e convertido para texto puro.
- Seções lidas integralmente: Abstract, §1, §2 (2.1, 2.2), §3 (3.1.1, 3.1.2, 3.2.1, 3.2.2, 3.3.1, 3.3.2), §4 (4.1 a 4.4), §5, Limitations, Ethics Statement, Apêndices A, B, C, D. Das referências li apenas os títulos citados abaixo. As equações (1)–(6) vieram sem símbolos na conversão; reconstruí o sentido pelo texto (ver item 8).

### 2. O que o framework é, em um parágrafo
O paper é um survey que propõe um "generic workflow" em três blocos encadeados para produzir dados sintéticos com LLMs: geração (§3.1), curadoria (§3.2) e avaliação (§3.3). A premissa (§1, §2.1) é que, em vez de criar dados do zero, na maioria dos casos se aumenta um conjunto pequeno de exemplos-semente ou entradas sem rótulo, com um prompt que define a tarefa de geração. Dois requisitos organizam tudo (§2.2): "faithfulness" (o dado é correto, coerente, com rótulo certo) e "diversity" (variação de tamanho, tema, estilo). Cada técnica do survey é apresentada como resposta a um desses dois problemas. Não é um protocolo experimental com passos numerados e critérios de aceite; é uma taxonomia de técnicas e decisões, mais quatro direções futuras (§4).

### 3. O esqueleto, passo a passo

#### Etapa 0. Formulação do problema (§2.1)
- O que é: define o que se gera, a partir de quê, e com qual prompt. Entrada opcional: um conjunto de apoio (sementes ou entradas sem rótulo). A saída é o dataset sintético final.
- Decisão pedida: qual é a tarefa de geração (reescrever, responder, anotar etc.) e que material de apoio existe. O paper trata anotação como caso especial de geração (rótulos produzidos pelo LLM) e a detalha no Apêndice A.

#### Etapa 1. Data Generation (§3.1)
**1.1 Prompt Engineering (§3.1.1).** Um prompt eficaz tem três elementos embrulhados por um template (Eq. 2; Fig. 3 dá um exemplo de brinquedo): especificação da tarefa, condições de geração e demonstrações in-context.
- (a) Task Specification (§3.1.1). Funciona como o "codebook" que se daria a anotadores humanos: propósito, explicação dos dados, conhecimento de fundo. Opções listadas: role-play (um prólogo do tipo "suponha que você é X" melhora o desempenho), esclarecimento de formato, enriquecimento de conhecimento (inclusive via knowledge graphs para tópicos de domínio). Yoo et al. 2021 formaliza a especificação como tripla: tipo de texto, tipo de rótulo, verbalizador do rótulo. Decisão: que contexto, papel e formato declarar.
- (b) Conditional Prompting (§3.1.1). Resposta ao problema de repetição: pedir só "gere dados" dá saídas repetitivas mesmo com temperatura alta. Consiste em declarar pares condição-valor (Eq. 3), que dão uma diversidade "definida artificialmente". Duas sub-decisões:
  - Conditioning Scope: quais dimensões condicionam. Trabalhos iniciais usavam só o rótulo da classe (output-conditional prompting, serve para balancear classes, mas não funciona sem rótulos). Depois: atributos mais finos (tópico, comprimento, estilo) cujas combinações multiplicam a variedade. TinyStories condiciona em três palavras sorteadas ("creative randomness").
  - Conditioning Values: de onde vêm os valores. Amostrar de classes conhecidas; buscar em knowledge graphs; pedir ao próprio LLM (Xu 2023b; Ding 2023b, que monta uma "concept tree" de subtópicos para garantir cobertura). O próprio template do prompt pode ser tratado como condição, e variá-lo aleatoriamente aumenta diversidade (Meng 2022).
- (c) In-Context Learning (§3.1.1). Demonstrações atuam como orientação humana implícita e aumentam a faithfulness. Se há amostras rotuladas, usam-se como demos; sem rótulos, usam-se demos geradas por LLM (Self-Instruct, Self-Prompting). Como a qualidade das demos pesa, o paper lista seleção: escolha aleatória é criticada (falta diversidade/qualidade); alternativas são demos focadas em aspectos específicos (Sudalairaj 2024), por similaridade de cosseno no espaço de embeddings (Liu 2022b; Su 2023), por influence score (Ye 2022b), e pedir ao LLM uma explicação de cada exemplo antes de colocá-lo no prompt (He 2023), o que se alinha com geração em chain-of-thought.

**1.2 Multi-Step Generation (§3.1.2).** Quando a tarefa é complexa demais para uma única chamada, decompõe-se manualmente em uma cadeia de subtarefas, cada saída intermediária podendo alimentar as seguintes (Eq. 4). Isso alinha o raciocínio do modelo com o conhecimento prévio humano. Duas escalas:
- (a) Sample-Wise Decomposition (§3.1.2): dividir uma amostra em partes geradas em sequência (Eq. 5), útil para texto longo e raciocínio (ex.: diálogos em que o LLM alterna papéis de usuário e assistente). Saídas intermediárias (passos de raciocínio, CoT) podem ser usadas e depois descartadas do dado final. O paper afirma que explorar esse "latent metadata" de raciocínio ainda é insuficiente (problema em aberto).
- (b) Dataset-Wise Decomposition (§3.1.2): ajustar as condições a cada estágio para o dataset crescer na direção certa (Eq. 6). Exemplos: S3 mira as categorias mais erradas pelo modelo downstream treinado até então; generate-then-expand (Honovich 2023b; Shao 2023); Explore-Instruct modela o domínio como árvore e a percorre para ganhar especialização e cobertura.
- Decisão: quebrar ou não a geração, e se as condições são fixas ou adaptativas à medida que o dataset cresce.

#### Etapa 2. Data Curation (§3.2)
Motivo (§3.2): a geração em volume produz amostras ruidosas, inúteis ou tóxicas, por alucinação (rótulos errados) e por prompts ambíguos (amostras irrelevantes ou redundantes). Usar isso sem tratar pode prejudicar. Dois grupos (Fig. 4).
**2.1 High-Quality Sample Filtering (§3.2.1)**, gera um subconjunto melhor:
- Heuristic Metrics: critérios baseados em dinâmica de aprendizado: confiança (Seedat 2023 descarta amostras com baixa confiança e baixa incerteza), influence function (Ye 2022b), probabilidade de geração (SuperGen, Meng 2022). Consistência entre condições, assumindo que amostras limpas têm predições estáveis: LLM versus classificador downstream (Yu 2023c), entre múltiplas execuções (Ye 2023), entre vizinhos (Seedat 2023). Julgamento por LLM da qualidade (Chen 2023b, AlpaGasus), cujo resultado treinou melhor com bem menos dados curados que o Alpaca original.
- Sample Re-Weighting: em vez de descartar, ponderar (SunGen, bi-level re-weighting sem anotação humana; FewGen, objetivo de meta-learning discriminativo).
**2.2 Label Enhancement (§3.2.2)**, corrige rótulos errados. O paper diz que o LLM dificilmente identifica os próprios erros (viés de confirmação), logo precisa de agente externo:
- Human Intervention: re-anotar amostras corrompidas (Wang 2021 seleciona as de menor confiança; Pangakis 2023 e Liu 2022a defendem revisão humana comparando humano e LLM guiados pelo mesmo codebook). Custo alto.
- Auxiliary Model: aluno destilado do LLM refina rótulos sem humanos (FreeAL, MCKD, Saad-Falcon 2023). Hipótese: o aluno treinado em anotações fracas produz rótulos melhores que o professor. MCKD usa treino com partições separadas e rotulagem cruzada para evitar overfitting no ruído.
- Decisão: filtrar, re-pesar ou corrigir; e se o orçamento permite humano ou aluno.

#### Etapa 3. Data Evaluation (§3.3)
Objetivo: avaliar qualidade e eficácia antes de usar os dados. Dois caminhos (Fig. 5).
**3.1 Direct Evaluation (§3.3.1)**, avalia a qualidade do dado em si:
- Data Faithfulness: com ground truth, automatizável; para dados abertos, precisa humano. Estima-se a qualidade global por amostra revisada por especialistas (mais amostras, estimativa melhor, mais custo). Alternativa: modelo auxiliar confiável no lugar de humano (Chung 2023b); extrair antes a informação relevante ajuda quando o modelo tem contexto curto (Lee 2022).
- Data Diversity: estatísticas de vocabulário (tamanho do vocabulário, frequência de n-gramas; não capturam semântica) e relevância entre amostras (similaridade de cosseno, distância entre amostras, que capturam diversidade contextual/semântica). As mesmas medidas servem para escolher demos in-context diferentes das já geradas.
**3.2 Indirect Evaluation (§3.3.2)**, avalia pelo efeito downstream:
- Benchmark Evaluation: treinar o modelo no dado gerado e medir em benchmarks (TruthfulQA, NIV2 como exemplos). O Apêndice D (Tabela 1) lista benchmarks, incluindo RTE e QNLI dentro do GLUE para NLI.
- Open Evaluation: para saídas abertas, humano ou modelo auxiliar; formas: ranking de respostas, escala de quatro níveis, Elo, avaliação automática baseada em GPT-4. Limite: LLMs gerais podem faltar conhecimento de domínio, daí afinar um avaliador com anotações humanas.
- O paper não prescreve ordem iterativa nem critérios de parada entre as etapas; apenas ordena geração, curadoria, avaliação, com o feedback de desempenho mencionado como direção em §4.3.

### 4. Definições e termos-chave
- Synthetic data (§1): dado projetado para imitar características e padrões do dado real.
- High-quality data (§1): dado diverso, com sinais de supervisão ricos (em geral rótulos) alinhados à intenção humana.
- Faithfulness (§2.2): coerência lógica e gramatical mais correção; ameaçada por alucinação e conhecimento "fat-tailed" do LLM.
- Diversity (§2.2): variação em tamanho, tema, estilo; ameaçada por viés do LLM que gera conteúdo monótono.
- Task specification / "codebook" (§3.1.1): contexto dado ao LLM como se dá a anotadores.
- Conditional prompting, conditioning scope, conditioning values (§3.1.1): ver Etapa 1.1(b). Output-conditional prompting: condicionar só no rótulo da classe.
- In-context learning, demonstrations (§3.1.1); Self-Instruct / Self-Prompting: demos produzidas pelo próprio modelo.
- Multi-step generation; sample-wise vs dataset-wise decomposition (§3.1.2).
- Heuristic metrics, sample re-weighting, label enhancement, human intervention, auxiliary model (§3.2).
- Direct vs indirect evaluation (§3.3). Selective annotation (Apêndice A): dividir de modo custo-eficiente o que humanos e LLM anotam.

### 5. Riscos, limitações e desafios apontados
- Dados humanos são caros, escassos, com preocupações de privacidade e também enviesados e sujeitos a erro (§1).
- Gerar com alta correção e diversidade ao mesmo tempo exige desenho cuidadoso e muitos truques; não é trivial (§1).
- Alucinação, conhecimento de cauda longa e viés do LLM causam erros factuais, rótulos errados e conteúdo irrelevante, pior em textos longos, complexos ou de domínio (§2.2).
- Geração direta é repetitiva mesmo com temperatura alta (§3.1.1).
- Qualidade das demos in-context determina o resultado; seleção aleatória é fraca (§3.1.1).
- Dados sintéticos brutos trazem muito ruído, inutilidade e toxicidade (§3.2).
- Viés de confirmação: o LLM não detecta os próprios erros de rótulo (§3.2.2). Revisão humana tem custo alto e é irrealista em escala (§3.2.2).
- Avaliação humana escala mal em custo; vocabulário não captura semântica (§3.3.1); LLMs gerais avaliam mal domínios específicos (§3.3.2).
- Dados sintéticos sem nenhum humano no processo podem "envenenar" o modelo e levar a mode collapse (§4.4). O uso do aluno hoje se baseia só na confiança de predição (§4.3).
- Pouca exploração dos passos intermediários de raciocínio na geração (§3.1.2). Falta framework genérico para colaboração humano-máquina (§4.4).
- Técnicas de tuning dependem de acesso ao modelo; caixas-pretas pouco exploradas (Apêndice B). Escopo: só texto e abordagens com LLM (Limitations). Ethics Statement: uso malicioso de dados sintéticos é preocupação.

### 6. O que o paper diz sobre o caso (explicações, destilação, NLI)
- Racionalizações/explicações: o paper não trata geração de racionalizações pós-hoc nem e-SNLI; não os menciona. Pontos tangenciais: (i) He et al. 2023 pede ao LLM uma explicação por exemplo antes de usá-lo como demo, alinhado a CoT (§3.1.1); (ii) CoT e passos de raciocínio intermediários como estratégia de faithfulness (§3.1.2); (iii) a lista de referências inclui Orca ("explanation traces" de GPT-4), citada na introdução como geração para fine-tuning (§1), sem discussão no corpo.
- Destilação: a destilação aparece só na curadoria de rótulos, com aluno destilado do LLM refinando rótulos (FreeAL, MCKD, §3.2.2); §4.3 pede mais modos de colaboração grande-pequeno. Nada específico sobre treinar um decoder auxiliar.
- NLI/classificação: NLI está listada como tarefa onde a geração sintética foi aplicada (Zhang et al. 2023b, Apêndice C); WANLI é citado como exemplo de revisão humana (§3.2.2); RTE e QNLI aparecem na Tabela 1 (Apêndice D). Para classificação, o paper observa que o avaliador típico é um modelo pequeno treinado nos dados gerados e testado em benchmarks existentes (Apêndice D). Condicionar no rótulo é a prática inicial para classificação (§3.1.1).

### 7. Inferência do agente (não está no paper)
Mapeamento com as 4 rodadas do aluno; é interpretação minha.
- Rodada 0 (checagens automáticas em 2.000 saídas-piloto): corresponde a curadoria §3.2.1 (filtros heurísticos) e avaliação direta §3.3.1. Candidatas: faithfulness como consistência com o rótulo gold (a explicação não deve contradizer o rótulo dado), formato (1–2 frases), duplicatas e diversidade por n-gramas/embeddings (§3.3.1), consistência entre execuções repetidas (§3.2.1).
- Rodada 1 (3–4 variantes de prompt em ~300 pares): corresponde a §3.1.1. Variantes naturais: task specification com/sem role-play; com/sem demos in-context e política de seleção das demos (aleatória versus por similaridade); condicionamento por rótulo (já fixo aqui pois o rótulo gold entra) ou por atributo; em §3.1.2, uma geração direta versus decomposta em dois passos. Avaliação por §3.3.1 (amostra revisada por humano e/ou LLM) para comparar variantes.
- Rodada 2 (vencedora em 1.000 pares held-out): corresponde a §3.3.1 em escala maior, com humano ou modelo auxiliar para faithfulness; diversidade por similaridade. Ainda direta; a avaliação indireta (§3.3.2) só ocorre ao treinar o aluno.
- Rodada 3 (canary de 5k, depois o resto): o paper não descreve canary; o mais próximo é o ciclo dataset-wise (§3.1.2, Eq. 6), em que o desempenho/qualidade de lotes anteriores ajusta a geração seguinte, mais curadoria (§3.2) aplicada em lote. A etapa de label enhancement (§3.2.2) em princípio é dispensável, pois o rótulo gold já vem do e-SNLI; o risco é a explicação, não o rótulo.
- Fecho: a avaliação indireta (§3.3.2) equivale a treinar o aluno com a cabeça auxiliar e comparar com ablação (sem cabeça), fora do escopo das 4 rodadas.
- Aviso: o paper é um mapa de técnicas, sem limiares, tamanhos de amostra ou critérios de aceite; qualquer número de rodada é decisão do aluno.

### 8. O que não consegui ler ou confirmar
- As equações (1)–(6) não sobreviveram à conversão HTML-texto; descrevi o sentido, não os símbolos.
- As figuras 1–5 e a taxonomia da Fig. 2 são imagens/texto não extraído; só li as legendas.
- Venue "Findings of ACL 2024" vem do seu pedido, não confirmado no HTML da v1 (que só traz arXiv). Pode haver diferenças para a versão publicada.
- Não abri os trabalhos citados (AnnoLLM/He 2023, FreeAL, MCKD, Zhang 2023b etc.); o que digo sobre eles é o que o survey afirma. A identificação de "He et al. 2023" com o AnnoLLM é provável pela vizinhança na lista de referências, mas não verificada.
- Não encontrei no texto discussão sobre custo, orçamento de API, tamanho de lote, nem sobre rationales pós-hoc ou e-SNLI.

---

## 2. Extração: Tan et al. 2024 — LLMs para anotação e síntese de dados (survey)

Procedência: nível 2 (agente leu o texto completo da versão HTML; Pedro não leu). Parafraseado; nenhuma passagem copiada. Todo "§" refere-se à numeração do próprio paper.

### 1. Identificação
- Título: "Large Language Models for Data Annotation and Synthesis: A Survey".
- Autores: Zhen Tan, Dawei Li, Song Wang (contribuição igual), Alimohammad Beigi, Bohan Jiang, Amrita Bhattacharjee, Mansooreh Karami, Jundong Li, Lu Cheng, Huan Liu (ASU, UVA, UIC).
- Venue/ano: EMNLP 2024 Main (informado no pedido; o HTML lido NÃO traz o venue impresso — não confirmado na fonte). arXiv:2402.13446.
- URL lida: https://arxiv.org/html/2402.13446v3 (v3; fallback não foi necessário).
- Seções lidas: Resumo, §1 Introduction, §2 Preliminaries, §3 (3.1–3.6), §4 (4.1, 4.2), §5 (5.1–5.3), §6 (6.1, 6.2), §7 Conclusion, Limitations, Apêndices A (ferramentas), B (aviso de uso de ChatGPT-4 na redação), C (4 tabelas de trabalhos representativos) e a lista de referências (consultada para resolver citações). A Figura 1 (taxonomia em imagem) e a Figura 2 (exemplos) não são legíveis em texto; só as legendas.

### 2. O que o framework é, em um parágrafo
É uma taxonomia de três etapas para usar um LLM como anotador: (i) gerar anotações (§3), (ii) avaliá-las e filtrá-las (§4), (iii) utilizá-las para treinar ou guiar outros modelos (§5), mais um capítulo de impacto social e desafios (§6). O paper formaliza só duas peças (§2): um modelo anotador A (o LLM grande, ex.: GPT-4) que mapeia dados de entrada em anotações, e um aprendiz de tarefa L (que pode ser outro LLM ou um modelo menor como BERT) que usa essas anotações. "Anotação" aqui é ampla: rótulos de classe, mas também sinais auxiliares (confiança, contexto, metadados, racionalização, preferências, feedback textual). É um survey de mapeamento, não um protocolo com passos prescritivos nem experimentos próprios: o framework organiza a literatura, e as decisões práticas precisam ser inferidas dele.

### 3. O esqueleto, passo a passo

#### 3.A Etapa 1 — Geração de anotações (§3)
Seis tipos de dado anotado. Para cada um, o paper lista técnicas e critérios (diversidade, qualidade).
- §3.1 Instruction & Response. O que é: os dois componentes de dados de fine-tuning e de in-context learning. Técnicas: para diversidade de instrução — misturar amostras (Yoo 2021), gerar-e-filtrar a partir de poucas sementes (Wang 2022b, Self-Instruct), treinar um gerador de instruções, descrição de tarefa como semente, explain-then-generate, paráfrase múltipla, seleção por clustering, AttrPrompt, Magpie, Persona Hub, FANNO, CorrSynth, SynthesizRR (recuperação), IDEA-MCTS. Para qualidade de resposta — enquadrar como leitura de compreensão, self-consistency com seleção pela maior confiança, reescrita das respostas (self-distill), simulação social, prompt multi-etapa, ICL com recuperação, prompting guiado por princípios, Source2Synth, e o princípio "menos é mais" para dados de raciocínio matemático. Decisão para o praticante: variar sementes/prompts para evitar saída homogênea e escolher um mecanismo de qualidade da resposta.
- §3.2 Label. O que é: rótulo clássico de classificação, agora produzido por LLM. Técnicas: LLM como anotador especialista, co-anotação humano-LLM (CoAnnotating), comparação com anotadores humanos, melhoria de anotação humana existente, CoT + voto majoritário, uso de LLM para gerar dados que melhoram calibração (ECE). Decisão: se rótulo vem do LLM ou já é dado (no caso do aluno, o rótulo é dado; ver §7).
- §3.3 Rationale — NÚCLEO (ver detalhe abaixo).
- §3.4 Pairwise Feedback. Dois caminhos: ranking por LLM de múltiplas respostas amostradas (Constitutional-AI-like, West-of-N etc.) e construção direta de respostas de qualidades diferentes (por suposição: modelo maior/mais shots é melhor, SFT > base, seguir vs. violar princípios, escores de benchmark). Uso: alinhamento. Pouco relevante ao caso.
- §3.5 Textual Feedback. Crítica em texto sobre saídas (QA, tradução, detecção de alucinação), debate/revisão por pares, análise de erros. Relevante só como inspiração de verificação (ver §7).
- §3.6 Other Domain-Specific Data. Diálogos multi-turno, grafos/tabelas, robótica/agentes, multimodal, recomendação, extração de informação, multilíngue. Catálogo de aplicações.

##### Detalhe §3.3 Rationale
- Definição do paper: rationale é o raciocínio/trajeto de pensamento para resolver uma pergunta, tratado como informação auxiliar valiosa para prever a resposta final (§3.3). Historicamente anotado por humanos (Ling 2017, Cobbe 2021, Wei 2022), o que limitava escala; Kojima 2022 confirmou que CoT com rationale autogerado melhora o raciocínio de LLMs (§3.3).
- Três eixos de organização:
  1. Rationale Structure: abstrair o raciocínio em estruturas — árvores (Hao 2023; Yao 2024), grafos (Besta 2024; Yao 2023), tabelas (Wang 2024g), programas (Chen 2023e), recursão (Qi 2023), conceitos (Tan 2023). Todas são formatos para raciocínio de múltiplos passos; texto livre CoT é o caso base.
  2. Rationale Quality: PINTO (Wang 2022a) — LLM congelado gera rationale específico por alternativa; SCOTT (Wang 2023b) — contrastive decoding que considera a resposta correta (gold) para tornar o rationale mais plausível; LogiCoT (Liu 2023a) — prompts cuidadosos com GPT-4 para montar dataset de CoT lógico; Socratic CoT (Shridhar 2023) — decompor em subperguntas-soluções, rationale fino; Kang 2024 — reranker neural traz documentos para rationale em tarefas intensivas em conhecimento; Zhou 2024 — limites/potencial de dados sintéticos de raciocínio baseados em grafos; InstructRAG (Wei 2024b) — o modelo aprende a "denoisar" via rationales autossintetizados.
  3. Human-like Rationale: amostrar vários caminhos de raciocínio (Gao 2021; Wang 2022b self-consistency; Chen 2023f; Liu 2023c), eliminação — verificar cada caminho reversamente e remover os incorretos (Tong 2023; Balepur 2023; Ma e Du 2023), e debate/colaboração entre LLMs (Yin 2023; Liang 2023; Xu 2023d; Liu 2023e).
- Decisão que isso implica: escolher estrutura (texto CoT simples vs. estruturado), escolher o mecanismo de qualidade (condicionar na resposta gold, decompor, amostrar vários e filtrar) e decidir se há pluralidade de caminhos. O paper NÃO diz qual combinação é melhor; só cataloga.
- Observação do apêndice C (tabelas): as linhas de rationale registram o modelo-base do anotador (GPT-3, GPT-3.5, ChatGPT, GPT-4, GPT-NeoX) e o "custo de anotação" apenas qualitativamente (chamada de API vs. inferência local); o único custo em dólar nas tabelas lidas é o de Self-Instruct (US$ 600 para o dataset inteiro) — Apêndice C.

#### 3.B Etapa 2 — Avaliação e filtragem (§4) — NÚCLEO
- §4.1 Evaluating LLM-Generated Annotations. Três famílias:
  - General Approaches: comparação humana com guideline (o "Turking Test" de Efrat e Levy 2020, comparando saída de LLM com benchmarks como SNLI, SQuAD, NewsQA); inspeção manual de originalidade/acurácia/variedade (Honovich 2022); medir LLMs open-source contra rótulos humanos (Alizadeh 2023).
  - Task-Specific Evaluations: métrica depende da tarefa — ranking de tokens (grafo de conhecimento), Self-BLEU para diversidade em geração contrafactual, Pass@k em código; e, quando o volume é grande, comparar com o padrão-ouro em um subconjunto pequeno rotulado (Zhao 2021; Agrawal 2022; He 2023).
  - LLM-as-a-Judge: LLM como avaliador escalável de dados sintéticos; debate entre vários LLMs para avaliar com justiça e escolher respostas (Li 2024g); I-SHEEP (Liang 2024b) — LLM pontua respostas sintéticas e um limiar seleciona pares de alta qualidade para a rodada seguinte.
  - Decisão: definir métrica de qualidade antes de gerar; combinar checagem humana em amostra pequena com avaliação automática em volume.
- §4.2 Filtering & Selection (três tipos):
  - Rule-Based: heurísticas de tamanho, palavras-chave e padrões; limiares (ex.: número de turnos); parsing contra a resposta correta para descartar CoT errados (Ho 2023; Kang 2024); similaridade semântica para remover redundantes e manter diversidade (Wang 2022b; Lee 2023a; Ding 2024).
  - External-Source-Based: reward model pré-treinado mantém só amostras de alta recompensa (Gulcehre 2023; Dong 2023); ao destilar modelos pequenos, feedback do próprio aluno guia a seleção (Lin 2023b; Wang 2024f); classificadores pré-treinados separam alvo de indesejado (Chen 2023g; Zheng 2023a).
  - LLMs-Driven: sinais do LLM (perplexidade, confiança, logits) como seletores; pedir ao LLM que avalie a qualidade (Lu 2023; Kim 2023a); ranquear candidatos e ficar com os melhores; Jiang 2024b — filtrar até amostras corretas mas com alto "distribution shift" ajuda a autoevolução.
  - Decisão: empilhar filtros baratos (regras) antes de filtros caros (juiz LLM); decidir se o aluno participa do filtro.
- O paper não dá limiares numéricos nem taxa de rejeição esperada; descreve famílias.

#### 3.C Etapa 3 — Utilização das anotações (§5) — NÚCLEO
- §5.1 Supervised Fine-Tuning:
  - Self-Evolution: LLM é anotador e aprendiz (self-improve de Huang 2023; refino iterativo, self-distillation, self-play, self-training de modelos pequenos).
  - Distill Smaller Models (o ponto mais próximo do caso): usar dados de um LLM grande para treinar um modelo menor e mais barato, motivado por eficiência. Exemplos listados: instrução (Alpaca/Vicuna/WizardLM), classificação com aumento de dados e treino de modelos menores de atenção bidirecional (Meng 2022; Meng 2023; Wang 2023d), raciocínio com rationales sintéticos coletados de LLMs (Wang 2022a PINTO; Shridhar 2023; Liu 2023a; Kang 2024), diálogo, extração de informação, código, e domínios (medicina, finanças, ciência).
  - Decisão: o rationale entra como alvo de treino do aluno; o paper trata isso como "tune smaller models" sem detalhar a arquitetura da cabeça nem a função de perda.
- §5.2 Alignment Tuning: reward modeling (curriculum por feedback, self-play, reward instruível) e policy training (DPO com pares sintéticos, filtragem por reward model, auto-alinhamento). Fora do escopo do caso.
- §5.3 Inference: ICL (aumentar descrição da tarefa, demonstrações, amostra de teste) e Reasoning (rationale antes da resposta, voto majoritário, eliminação, edição/refino pós-hoc com feedback textual, ferramentas como interpretador de programas em PoT e avaliadores de estado em ToT). Aqui o rationale é usado em inferência pelo LLM, não para treino de aluno.

#### 3.D Capítulo final — Impacto e desafios (§6) — ver item 5.

### 4. Definições e termos-chave
- Annotator model A / task learner L (§2): o primeiro gera anotações a partir dos dados, o segundo aprende com elas.
- LLM-generated annotation (§2): qualquer saída do anotador além do rótulo categórico, incluindo escores de confiança, contexto e metadados.
- Rationale (§3.3): trajeto de raciocínio que sustenta a resposta; informação auxiliar para prever a resposta.
- Chain-of-thought / CoT (§3.3, §5.3): rationale autogerado antes da resposta.
- Self-consistency (§3.1, §3.3, §5.3): amostrar vários caminhos e escolher por maioria/confiança.
- Contrastive decoding com resposta gold (§3.3): decodificação que usa a resposta correta para favorecer rationales plausíveis (SCOTT).
- Rule-based / external-source-based / LLM-driven selection (§4.2): as três classes de filtro.
- LLM-as-a-Judge (§4.1): LLM que pontua ou compara saídas para avaliar em escala.
- Distill smaller models (§5.1): treinar modelo pequeno com dados do LLM grande por eficiência.
- Model collapse (§6.2): queda gradual de desempenho de modelo treinado com saídas de outros LLMs.
- Distribution shift extent, DSE (§4.2): grau de deslocamento de distribuição de uma amostra; filtrar alto DSE ajudou (Jiang 2024b).
- Pass@k, Self-BLEU, ECE (§4.1, §3.2): métricas citadas para código, diversidade e calibração.

### 5. Riscos, limitações e desafios apontados pelo paper
- Ética e viés (§6.1): falta de olhar humano pode gerar resultados enviesados e injustos, especialmente em finanças, direito e saúde; substituir anotadores humanos pode ampliar desigualdades.
- Model collapse (§6.2): treinar sobre saídas de LLM degrada o modelo; o imitador copia o estilo sem atingir a precisão factual do professor; causas: erro de aproximação estatística (amostra finita) e funcional (capacidade limitada), que se acumulam em ciclos. Mitigação citada: manter diversidade, alta proporção de dado humano, acumular real + sintético (Gerstgrasser 2024).
- Alucinação (§6.2): mina a confiabilidade das anotações; mitigação por validação automática e manual; exemplos: Reverse Validation (Yang 2023d), CoT/explicações para tornar saídas verificáveis (Bertaglia 2023), CoAnnotating com alocação guiada por incerteza (Li 2023b), processo humano-LLM (Zendel 2024). O paper nota a opacidade dos LLMs dificultando achar a causa.
- Eficiência (§6.2): custo computacional e latência; técnicas: pruning, MoE, quantização, destilação.
- Limitações declaradas (Limitations): viés de amostragem e alucinação; viés social amplificado; dependência de dados de alta qualidade; complexidade de prompt engineering e tuning; risco de overfitting/generalização limitada em tarefas discriminativas; exigência de recursos computacionais.
- Lacuna de escopo (§1): cobre só LLMs de texto; multimodal fica fora.

### 6. O que o paper diz que se aplica diretamente ao caso
- Rationales gerados por LLM como alvo de treino de um modelo menor: §5.1 (Distill Smaller Models) cita Wang 2022a (PINTO), Shridhar 2023, Liu 2023a (LogiCoT), Kang 2024 (KARD); a tabela do Apêndice C lista também Ho 2023 ("Large Language Models Are Reasoning Teachers", ACL'23), SCOTT (Wang 2023b, ACL'23), todos em CoT.
- Rationale condicionado à resposta correta: SCOTT usa contrastive decoding que leva em conta a resposta gold (§3.3) — é o único método citado no §3.3 que usa o gold no decodificador; o paper não chama isso de "pós-hoc".
- Filtro por consistência com o gold: parsing contra a resposta correta para descartar CoT incorretos (Ho 2023; Kang 2024) (§4.2).
- Filtros de redundância por similaridade semântica (§4.2) e de tamanho/padrão (§4.2).
- Aluno menor e bidirecional treinado com dados de LLM: Meng 2022/2023, Wang 2023d aumentam datasets e treinam modelos menores de atenção bidirecional para classificação (§5.1) — cita explicitamente encoders do tipo BERT como L (§2).
- Feedback do aluno para selecionar dados na destilação: Lin 2023b; Wang 2024f (§4.2).
- NLI/e-SNLI: o paper só menciona SNLI como benchmark usado no "Turking Test" de Efrat e Levy 2020 (§4.1). Não trata e-SNLI nem NLI como tarefa de rationale.
- Distilling Step-by-Step (Hsieh 2023) aparece na bibliografia, mas no texto só é citado na lista de trabalhos sobre model collapse (§6.2); o paper não descreve seu mecanismo nem a cabeça auxiliar. Não há menção de decoder auxiliar descartado na inferência.
- Alerta direto: risco de model collapse e de imitar o estilo sem a precisão factual do professor (§6.2); alucinação em anotações (§6.2).

### 7. Inferência do agente (NÃO é o que o paper diz)
- Rodada 0 (checagens automáticas em 2.000 saídas-piloto): mapeia para os filtros rule-based de §4.2 — tamanho (1–2 frases), padrões/formato, duplicatas por similaridade (Wang 2022b; Lee 2023a), e consistência com o gold quando o rationale expõe um rótulo (análogo ao parsing de Ho 2023). Também serve de medição de taxa de rejeição antes de gastar mais. O paper não fornece limiares; eles teriam de ser definidos por Pedro.
- Rodada 1 (3–4 variantes de prompt em ~300 pares): corresponde a §3.3 Quality (variar a forma de condicionar no gold, decompor em subpergunta como Socratic CoT, ou impor princípios/estrutura) e a §3.1 (diversidade de prompt/persona/atributos, ex.: AttrPrompt). A avaliação seria §4.1: amostra pequena com juiz humano (Turking-Test-like) mais, opcionalmente, LLM-as-a-Judge para escalar; o paper alerta que juiz LLM tem seus próprios vieses (§6).
- Rodada 2 (vencedor em 1.000 pares held-out): corresponde à ideia de §4.1 de comparar com padrão-ouro em subconjunto pequeno; "held-out" garante que a variante vencedora não foi escolhida e medida nos mesmos 300 pares. O paper não prescreve protocolo de held-out; é prática do estudante.
- Rodada 3 (canário de 5k e depois o restante): combina §4.2 (pipeline de filtros) com a lógica de custo/viés de amostragem (Limitations). O canário detecta degeneração e deriva (alucinação, repetição) antes da geração em massa; o paper só cita alucinação e colapso como riscos, não canário.
- Seleção entre candidatos: se o orçamento permitir múltiplas amostras por par, as ideias de self-consistency/ranqueamento (§3.3, §4.2) são aplicáveis; custo seria multiplicado.
- Uso no aluno: a cabeça decoder auxiliar corresponde, em termos do paper, a "Distill Smaller Models" (§5.1), com L = encoder; o paper não prescreve peso de perda nem warm-up.
- Anti-collapse (§6.2): como o rótulo gold é humano (e-SNLI) e só o rationale é sintético, o cenário se afasta do colapso recursivo descrito (treino repetido sobre saídas próprias); essa leitura é do agente, o paper não analisa o caso.
- Procedência: qualquer decisão acima exige leitura do original pelo Pedro antes de entrar em texto assinado por ele.

### 8. O que NÃO consegui ler ou confirmar
- Venue "EMNLP 2024 Main": informado no pedido; o HTML não o imprime. Não confirmado na fonte.
- Figura 1 (taxonomia) e Figura 2 (exemplos): só legendas; a estrutura acima vem do corpo do texto e dos títulos de seções.
- As tabelas do Apêndice C: li o conteúdo via extração de texto; a ordenação das Tabelas 3 e 4 no HTML parece trocada (a tabela legendada como avaliação contém linhas de utilização/SFT). Não usei as tabelas além de citar nomes, venues e backbone.
- Títulos de algumas referências citadas (Lin 2023b, Wang 2024f, Lu 2023, Kim 2023a) não foram resolvidos por falha de correspondência no texto extraído; citei só autor/ano como o paper faz. Detalhes de PINTO, SCOTT, Ho 2023, Shridhar 2023, Kang 2024, Hsieh 2023 foram resolvidos pela lista de referências/tabelas.
- Não li nenhum dos trabalhos citados (Ho 2023, SCOTT, PINTO, DSbS etc.); o que descrevo deles é apenas o que o survey afirma. Nível 3 para essas obras.
- O paper não traz experimentos próprios, números de desempenho, nem protocolo sobre NLI, quantidade de pares ou custo; essas informações simplesmente não estão nele.

---

## 3. Liu et al. 2024 - Best Practices and Lessons Learned on Synthetic Data - extração

Procedência: nível 3 (agente leu o texto completo do HTML, mas a extração é interpretação do agente; não citar sem o Pedro conferir na fonte). Todas as frases abaixo são paráfrases; as seções entre parênteses são as do paper.

### 1. Identificação
- Título: Best Practices and Lessons Learned on Synthetic Data. Autores: Ruibo Liu, Jerry Wei, Fangyu Liu, Chenglei Si, Yanzhe Zhang, Jinmeng Rao, Steven Zheng, Daiyi Peng, Diyi Yang, Denny Zhou, Andrew M. Dai (Google DeepMind; Stanford; Georgia Tech).
- Venue/ano: COLM 2024 (informado no pedido; o HTML lido NÃO traz o nome do venue, ver item 8). arXiv:2404.07503v2 [cs.CL], 10 ago 2024.
- URL lida: https://arxiv.org/html/2404.07503 (baixada inteira por curl; fallback ar5iv não foi necessário).
- Seções lidas: Abstract, 1, 2 (2.1-2.5), 3, 4, 5, 6 e a lista de referências (para localizar autores/anos). Texto corrido de ~104 mil caracteres com referências; estimativa de ~15-20 páginas (contagem exata não disponível no HTML).

### 2. O que o trabalho é, em um parágrafo
É um survey/posicionamento (sem experimentos próprios) que reúne evidência de trabalhos anteriores sobre dados sintéticos para treinar e avaliar modelos de linguagem, em raciocínio, uso de ferramentas, multimodalidade, multilíngue e alinhamento (Seção 2), em avaliação (Seção 3), e discute riscos (Seção 4) e direções futuras (Seção 5). A tese é que dados sintéticos resolvem escassez, privacidade e custo, mas só se forem tratados com cuidado quanto a factuality, fidelity e bias (Abstract, Seção 6). Importante: apesar do título, o paper NÃO tem uma lista numerada de "best practices"; elas são implícitas nas lições dos trabalhos citados e em poucas recomendações explícitas (Seção 4, 5). Não há seção de recomendações operacionais para geração de explicações/racionalizações.

### 3. Best practices e lessons learned, item por item
Marcação: [EXPL] = o paper recomenda explicitamente; [LIÇÃO] = lição extraída de trabalho citado.
1. [LIÇÃO] Verificar a saída sintética com um verificador externo sempre que existir: AlphaGeometry usou um motor de dedução simbólica para validar cada ramo; em código, interpretador/execução filtra pares puzzle-solução (Seção 2.1, Math e Code). Motivo: gerar em escala é fácil, garantir correção é o gargalo (2.1).
2. [LIÇÃO] Filtrar pelo resultado final correto: STaR gera racionalizações em cadeia de pensamento e descarta as que levam à resposta errada antes do fine-tuning (2.1, Other reasoning). Motivo: só dados cuja conclusão confere melhoram o raciocínio.
3. [LIÇÃO] O formato da resposta sintética importa: no GAIR-Abel, respostas que começam parafraseando a pergunta e depois desenvolvem passo a passo superaram o formato simples (2.1, Math). Motivo: afeta o desempenho final.
4. [LIÇÃO] Diversificar a forma de gerar: MetaMath reescreve questões de várias maneiras (paráfrase semântica, auto-verificação, raciocínio inverso) (2.1, Math); Evol-Instruct aumenta complexidade; UltraChat busca diversidade com dois modelos em papéis distintos (2.5, Instruction Following).
5. [LIÇÃO] Escalar o volume ainda ajuda em certos casos: Xwin-Math levou o SFT sintético a ~1 milhão de exemplos e o LLaMA-2 7B continuou melhorando (2.1, Math).
6. [LIÇÃO] Partir de sementes pequenas e imitar o formato (Self-Instruct, Alpaca), mas atentar para a qualidade: o paper lista complexidade das consultas, diversidade semântica e escala do dataset como as três dimensões de qualidade a controlar (2.5, Instruction Following).
7. [LIÇÃO] Incluir "explanation traces" na supervisão: Orca revisa iterativamente instruções e respostas sobre o FLAN para incluir explicações de alta qualidade, e o modelo treinado melhora em várias tarefas de NLP (2.5, Instruction Following).
8. [LIÇÃO] Condicionar o gerador a informação de ancoragem: LLaVA gera Q&A longos a partir de legendas (e caixas delimitadoras/OCR em variantes), escondendo esses atributos no treino do aluno (2.3, Multi-modality instruction following). Motivo: dados caros de criar por humanos, mas o texto-fonte dá chão ao gerador.
9. [LIÇÃO] Dados sintéticos mal aplicados podem aumentar alucinação: SFT sintético com respostas alucinadas ou forçando o modelo a responder o que não sabe induz hallucination (2.5, Mitigating hallucination, citando Zhang et al. 2023d).
10. [LIÇÃO] Em contrapartida, dados sintéticos podem reduzir alucinação se houver sinal verificável: reward model treinado com dados sintéticos de alucinação; tarefa sintética em que a alucinação é facilmente avaliável (prefix-tuning); ranqueamento de pares por fact-checking automático + DPO (2.5). Limite: faltam tarefas sintéticas em que alucinação possa ser medida em escala (2.5).
11. [LIÇÃO] Misturar sintético com humano: reward models mais robustos usam mistura de dados sintéticos e humanos (2.5, Aligning with human preference, citando Gao et al. 2023); e [EXPL] combinar dados sintéticos com reais é um remédio contra baixa fidelidade das preferências sintéticas (2.5).
12. [EXPL] Refinar continuamente qualidade e diversidade dos dados sintéticos, com cenários mais complexos e abrangentes (2.5, último parágrafo de alignment).
13. [EXPL] Gerar dados sintéticos em ambiente interativo sincronizado com o mundo real como remédio para baixa fidelidade (2.5).
14. [EXPL] Fazer testes rigorosos e avaliações de fairness para mitigar vieses amplificados ou novos (1, Introdução). Também [EXPL] desenvolver métodos robustos para validar e testar modelos treinados com dados sintéticos (4, alignment).
15. [EXPL] Manter benchmarks de avaliação internos e protegidos contra vazamento, porque detecção de contaminação por token falha com dados sintéticos (4, decontamination).
16. [LIÇÃO] Controlar peso e qualidade do dado sintético ao misturar com real: Xu et al. 2022 propõem otimizar a razão entre métodos de busca/amostragem e uma pontuação que equilibra peso de importância e qualidade, em back-translation (2.4). O paper também nota que a qualidade e diversidade dependem do método gerador; se for muito ruidoso ou pouco diverso, o ganho é limitado (2.4).
17. [LIÇÃO] Usar LLM como juiz como alternativa rápida e barata à avaliação humana (AlpacaEval, MT-Bench, GPT-4 como juiz), com correlação forte com julgamento humano em benchmarks sintéticos de código (CRUXEval, CodeMind) (3, Assisting human evaluation). Para factualidade longa, LongFact com Google Search como fonte de ancoragem e LLM como juiz atinge precisão de nível humano a custo bem menor (3, Factuality).
18. [LIÇÃO] Em avaliação de datasets gerados por modelo, Perez et al. 2023 geraram 154 datasets e submeteram à verificação humana (3, Safety). Motivo: validação humana de dados gerados por LM.
19. [EXPL, sobre direções] Pesquisar escala e equilíbrio quantidade x qualidade do dado sintético, pois a consistência de qualidade é menor que a do dado real (5, scaling).
20. [EXPL] Controlar atributos do dado gerado e injetar conhecimento de domínio (p. ex. via RAG) para a saída respeitar restrições do domínio (5, quality and diversity).
21. [EXPL] Padronizar protocolos e ferramentas de avaliação e de contaminação (6).

### 4. Definições e termos-chave
- Synthetic data: dados gerados artificialmente que imitam características/padrões de dados reais, criados por algoritmos, modelos generativos ou simulações, não diretamente por humanos (1).
- Factuality / hallucination: consistência da saída do sistema com o conhecimento dos dados de treino e da base de conhecimento; hallucination = conteúdo sem ancoragem factual (3, Factuality).
- Fidelity: o quanto o dado sintético reflete os padrões complexos do real; baixa fidelidade impede generalização (1, 2.5).
- Bias: vieses amplificados ou introduzidos pelo gerador (1, 4).
- RLAIF / Constitutional AI: feedback de IA guiado por poucos princípios substitui parte do feedback humano no RLHF (2.5).
- Back-translation: criar pares paralelos traduzindo dados monolíngues de volta (2.4).
- Evaluation contamination / decontamination: teste presente no treino; detecção por tokens (min-k% prob) (4).
- Scalable oversight: usar dados sintéticos e simulações para supervisionar sistemas complexos (3, Safety; 5).
- Self-improvement: modelo gerar dados melhores do que os que o treinaram e aprender com eles (5).
- Sycophancy: modelo ecoar a opinião do usuário (2.5).

### 5. Riscos e limitações apontados
1. Correção não garantida em dados sintéticos escalados, principalmente em matemática (2.1, Math). Mitigação: verificador simbólico/execução.
2. Back-translation depende do desempenho do próprio método; ruído ou pouca diversidade limita ganhos (2.4). Mitigação: ponderar qualidade/peso (Xu et al. 2022).
3. Alucinações induzidas por SFT sintético com respostas erradas ou desconhecidas pelo modelo (2.5). Mitigação: sinais de fact-checking, reward models; mas falta tarefa escalável de avaliação.
4. Preferências sintéticas de baixa fidelidade: modelos menos robustos a jailbreaks e possível comportamento enganoso mesmo após safety training (2.5). Mitigação: misturar com real, refinar qualidade/diversidade, ambientes interativos.
5. Humanos e preference models às vezes preferem respostas sicofantes (2.5).
6. Limitações dos métodos de factualidade: n-gram só mede sobreposição léxica; modelos só dão grau de alucinação e apontam mal o erro específico (3).
7. Desinformação e uso indevido (impersonação, manipulação), erosão de confiança (4). Mitigação proposta: diretrizes éticas e detecção.
8. Ambiguidade de alinhamento: dado sintético pode ser viesado, sem ancoragem ou irrealista, e dificulta interpretar as decisões do modelo (4). Mitigação: validar e testar com cuidado.
9. Contaminação de avaliação agravada, pois paráfrases do benchmark escapam à detecção por token (4). Mitigação: novas técnicas de detecção e benchmarks internos protegidos.
10. Simulações estreitas ou simplificadas demais (5, oversight).
11. Qualidade menos consistente do que a de dados reais, o que torna incerta a transposição de leis de escala (5).
12. Limites e riscos da auto-melhoria seguem em aberto (5).
Observação: o paper não trata de viés do gerador sobre rótulos, de homogeneidade/colapso de modo, nem de model collapse; ver item 8.

### 6. O que o paper diz que se aplica diretamente ao caso (racionalizações, destilação, classificação)
- STaR (Zelikman et al. 2022): rationales sintéticos em CoT, filtrados por resposta final correta (2.1, Other reasoning). Isso é o único trecho do paper sobre geração/filtragem de racionalizações. No e-SNLI o rótulo é dado, não gerado; portanto o análogo é checar se a explicação é coerente com o rótulo, mas o paper não diz isso.
- Orca (Mukherjee et al. 2023): explanation traces dentro de FLAN, ganhos em várias tarefas de NLP (2.5, Instruction Following).
- Self-Instruct, Alpaca, Evol-Instruct, UltraChat, Code Alpaca, WizardCoder, Magicoder OSS-Instruct: geração por modelo professor a partir de sementes (2.1, 2.5). Aplicam-se como precedente de gerar dados com LLM comercial para treinar modelo menor; o paper não discute licenças.
- Wei et al. 2023a (substituição de rótulos por símbolos, >500 mil exemplos) mostra aumento sintético em tarefas de linguagem natural com ganhos em ICL e raciocínio algorítmico (2.1).
- LLaVA: gerar pares longos a partir de atributos textuais (2.3), análogo a gerar explicações a partir de texto + rótulo.
- Rótulos/avaliação por LLM: Gilardi et al. 2023a/b citados para custo de anotação humana e para juízes sintéticos baratos (1, 3); AlpacaEval, MT-Bench (3).
- Qualidade de dado: complexidade, diversidade, escala (2.5); formato da resposta (GAIR-Abel, 2.1).
- Back-translation com ponderação por qualidade (Xu et al. 2022) como exemplo de dosar sintético x real (2.4).
- Alucinação por SFT sintético (Zhang et al. 2023d) e mitigação por fact-checking (Tian et al. 2023) (2.5).
- Contaminação por paráfrase (Oren et al. 2023; Mattern et al. 2023; min-k% prob de Shi et al. 2023) (4).
- Não há, no paper, discussão explícita de destilação de conhecimento clássica (aluno/professor com logits) nem de classificação; "distillation" não é conceito central aqui (todo o texto lido).

### 7. Inferência do agente (NÃO é do paper)
Itens que viram checagem/decisão nas 4 rodadas:
- Rodada 0 (checagens automáticas em 2.000 saídas piloto): (a) coerência explicação-rótulo, análogo ao filtro do STaR (item 3.2) e ao verificador externo (3.1), por exemplo por um classificador NLI independente ou checagem de que a explicação não contradiz o rótulo dado; (b) checar vazamento do rótulo ou de formato (3.3, 3.12); (c) checar duplicação, comprimento e diversidade lexical entre saídas (3.4, 3.16); (d) checar alucinação de entidades que não estão em premissa/hipótese (3.9, 3.10); (e) checar se o corpus gerado repete frases da premissa (3.8, ancoragem).
- Rodada 1 (3-4 variantes de prompt em ~300 pares): comparar variantes quanto a formato (3.3), diversidade (3.4, 3.6) e inclusão de justificativa estruturada (3.7); avaliar com juiz LLM (3.17) calibrado por amostra verificada por humano (3.18).
- Rodada 2 (vencedora em 1.000 pares held-out): validação humana amostral e comparação com as explicações humanas do e-SNLI como contraste (3.11, 3.14); relatar viés por classe (3.14).
- Rodada 3 (canário de 5 mil, depois o resto): monitorar deriva de qualidade e de distribuição durante a escala (3.19 aponta que a qualidade sintética é menos consistente em escala); manter conjunto de teste protegido (3.15).
Itens para "threats to validity" (inferência): alucinação do professor (5.3); explicações pós-hoc sem garantia de refletir o raciocínio real (o paper não aborda isso; é extrapolação); viés do gerador e homogeneidade (5.8, 5.11); contaminação com e-SNLI/SNLI no pré-treino do professor e do aluno (5.9; inferência de aplicação); juiz LLM circular quando o mesmo modelo gera e avalia (3.17; o paper não discute circularidade); dependência de um único professor (5.8).

### 8. O que NÃO foi lido ou confirmado
- Venue "COLM 2024" e número de páginas: não aparecem no HTML; o venue vem do pedido, as páginas são estimativa.
- Não há figuras ou tabelas relevantes no texto extraído; o HTML pode ter figuras não capturadas pela conversão para texto.
- O paper não traz números de eficácia para tarefas de NLI, para destilação de explicações, para a razão ótima sintético:real, nem para custo; qualquer afirmação desse tipo não está no texto.
- Nada sobre fidelidade de explicações pós-hoc, model collapse, sobreposição de dados de pré-treino do professor, licenciamento de saídas de LLM comerciais ou rotulação de qualidade de rationales por humanos.
- A lista de referências foi usada só para localizar autores/anos; os trabalhos citados NÃO foram lidos, então o que se diz deles aqui é o que o Liu et al. relata (nível 3 em dobro; citar os originais só após leitura).
- A seção 2.1 "Other reasoning tasks" tem poucas linhas sobre STaR; detalhes do método (p. ex. racionalização com dica da resposta) NÃO estão no paper e portanto não constam aqui.

---

## 4. Wiegreffe & Marasović 2021 — extração em profundidade

Procedência: nível 3 (agente leu o texto HTML integral do ar5iv; nada disso foi lido pelo Pedro). Serve para entender e triar; antes de citar em texto assinado, conferir na fonte. Tudo abaixo é paráfrase; "§" = seção do paper; "Ap." = apêndice.

### 1. Identificação
- Título: "Teach Me to Explain: A Review of Datasets for Explainable Natural Language Processing".
- Autores: Sarah Wiegreffe (Georgia Tech) e Ana Marasović (Allen Institute for AI / Univ. of Washington).
- Venue/ano: NeurIPS 2021 (o campo de comentários do arXiv diz "NeurIPS 2021 accepted paper, camera-ready"; a trilha "Datasets and Benchmarks" veio no pedido do Pedro, não apareceu no que li). arXiv v1 24/02/2021; v4 (última) 07/12/2021.
- URLs: https://arxiv.org/abs/2102.12060 ; https://ar5iv.labs.arxiv.org/html/2102.12060 ; site vivo das tabelas: https://exnlpdatasets.github.io (citado no §1).
- Versão lida: HTML do ar5iv, sem marcador de versão; a estrutura (8 seções, 65 datasets, "10 páginas + 6 de apêndice") bate com a versão condensada v3/v4. Segundo o arXiv, v3 é a camera-ready (mesmo conteúdo de v1–2, mais condensado) e v4 só corrigiu um erro de digitação no título e acrescentou agradecimentos. Não comparei linha a linha.
- Seções lidas: §1–§8 completas, Tabelas 1–5 (como texto achatado), Ap. A–D, Tabelas 6–8, legendas das Figuras 1–2. Lista de referências não conferida.

### 2. O que o trabalho é, em um parágrafo
É uma revisão (survey) de 65 datasets de ExNLP (explainable NLP) que trazem explicações textuais escritas por humanos para o rótulo verdadeiro de cada instância (resumo; §1, §3). Essas explicações servem a três objetivos: dar supervisão extra para melhorar o modelo, treinar modelos que expliquem as próprias previsões, e servir de referência para avaliar a plausibilidade de explicações geradas por modelos (§1). O paper organiza os datasets em três classes (highlights, free-text, structured), compara como foram coletados e, a partir disso, faz recomendações para coletas futuras. As recomendações vêm de duas fontes: discrepâncias vistas entre coleta, modelagem e avaliação (§4–§5) e boas práticas de crowdsourcing/HCI/NLP em geral, sobre qualidade (§6) e diversidade (§7). É um paper sobre COLETA HUMANA; não trata de explicações geradas por LLM.

### 3. Os tipos de explicação e o léxico (§2, salvo indicação)
- Definição geral: uma explicação é uma relação de três lugares (alguém explica algo a alguém). Em ML supervisionado, o "algo" é o rótulo: a explicação responde "por que esta entrada recebeu este rótulo?". O formato, porém, varia (§2).
- Local explanations: justificativas para previsões individuais; úteis para depuração, viés/justiça, robustez e privacidade (§1).
- **Highlights:** subconjuntos dos elementos da entrada (palavras, frases ou sentenças) que explicam a previsão (§2). Origem: "extractive rationales" de Lei et al. 2016, com dois critérios: compactos (curtos e coerentes) e suficientes (bastam para a previsão no lugar do texto inteiro). Yu et al. 2019 acrescentam um terceiro: comprehensiveness (toda a evidência de apoio está selecionada, não só um subconjunto suficiente). Jacovi & Goldberg 2021 propõem chamar isso de "highlights" e não "rationales", porque "rationale" sugere intenção humana e atribuiria comportamento social a uma IA (§2). Em fact-checking e QA multi-documento, equivale a "evidence" (§2). Exemplo (Tabela 1): premissa "cão de corrida branco com o número oito corre na pista", hipótese "cão corre no quintal", rótulo contradiction, com as duas frases marcadas.
- **Free-text explanations:** justificativas livres, não restritas às palavras nem à modalidade da entrada; mais expressivas e legíveis; servem a tarefas de raciocínio em que a explicação precisa de informação fora da entrada (§2). Sinônimos: textual, natural language explanations (termo "sobrecarregado"), free-form, abstractive (§2). Exemplo (Tabela 1): "Uma pista de corrida normalmente não fica no quintal de alguém".
- **Structured explanations:** ainda em linguagem natural, mas com restrições ao processo de escrita (por exemplo, uso obrigatório de certas regras de inferência); não há definição única, cada dataset tem seu desenho (§2, §3). Exemplos: cadeias de fatos, "semi-structured text", grafos de explicação (WorldTree), regras de inferência (QED), 2-fact chain (QASC/eQASC) (§3, Tabela 5).
- **Sufficiency (highlights):** o trecho marcado, sozinho, implica o rótulo; se não, o highlight é explicação inválida (§2, §4). **Comprehensiveness:** o complemento (o resto da entrada) não implica o rótulo, isto é, nada de evidência ficou de fora (§4, Tabela 2).
- **Plausibility:** o quanto, segundo humanos, uma explicação sustenta o rótulo previsto; medida comparando explicações do modelo com as humanas (§4). **Faithfulness (fidelity):** o quanto a explicação representa fielmente o processo de decisão do modelo (§4). Highlights suficientes e comprehensive são tidos como fiéis (§4).
- **Self-contained:** explicação que faz sentido sem a premissa/hipótese; foi exigência do e-SNLI, mas o paper diz que não é propriedade necessária de uma explicação válida (§4, Ap. Tabela 6).
- **Post-hoc (coleta):** anotadores explicam um rótulo atribuído por um sistema ou por outros anotadores; pressupõe que o explicador acha o rótulo correto ou provável (§6.3).
- **Template-like explanations:** explicações que seguem modelos de frase repetidos (ex.: "There is ⟨hypothesis⟩"); tratadas como suspeitas, mas o paper defende que nem todas são inúteis (§5).
- **Data artifacts:** padrões espúrios de anotação que o modelo aprende em vez da tarefa (§6). **Data cascades:** problemas a jusante causados por dados ruins; 92% dos praticantes teriam enfrentado (§1).
- **Collect-And-Judge** (outros anotadores avaliam as explicações coletadas) e **Collect-And-Edit** (outros anotadores editam as candidatas) (§6.1). **Datasheet:** ficha de documentação do dataset (§4). **Contrastive / negative explanations:** ver §7.3 abaixo.
- Escopo: o paper só cobre explicações de decisões humanas (rótulos de tarefa); datasets que explicam eventos do mundo, como GLUCOSE e ART, ficam como zona de fronteira (Ap. D, Figura 1).
- "Não existe definição abrangente de explicação" (§5; Ap. A, nota de escopo): o paper manda consultar especialistas do domínio e outras áreas (Tiddi et al. 2015 é a referência dada).

### 4. As recomendações (o framework), item por item
#### §4 — Elo entre dados, modelagem e avaliação (6 takeaways)
1. **Relatar com precisão como as explicações foram coletadas** (dar acesso à interface, screenshot ou instruções ao pé da letra). Razão: a caracterização da comprehensiveness de MovieReviews, EvidenceInference e FEVER divergiu entre trabalhos (DeYoung 2020a vs. Carton 2020), então reconstruir pela descrição geral é falho (§4).
2. **Sufficiency é necessária para highlights;** evitar, em avaliação e desenvolvimento, highlights humanos de baixa suficiência. Evidência: Carton et al. 2020 mostram que highlights humanos nem sempre são suficientes/comprehensive para modelos precisos; os piores casos foram neutral do e-SNLI e "no-attack" do WikiAttack (a ausência de ataque não pode ser destacada). Recomendação extra: checar antes se o rótulo pode ser explicado por highlight (§4).
3. **Comprehensiveness não é necessária para um highlight ser válido;** é um meio de quantificar faithfulness (§4). Razão: marcar só uma ocorrência de "great" é justificativa válida, mas o modelo pode ter usado a outra ocorrência, o que dificulta medir fidelidade.
4. **Highlights humanos não comprehensive não servem para avaliar automaticamente a plausibilidade de highlights de modelos forçados a ser comprehensive;** nesse caso, coletar highlights comprehensive (§4; Ap. Figura 2: modelo e humano não coincidem "por construção").
5. **Não estimar a posteriori a comprehensiveness a partir da descrição geral do dataset** (§4). Exemplo concreto: o e-SNLI é não comprehensive (ver item 5 do arquivo).
6. **Não popularizar decisões de coleta como se fossem universalmente necessárias;** documentar todas as restrições numa datasheet, dizendo se cada uma é necessária à validade e como afeta modelagem e avaliação (§4). Razão: Wiegreffe et al. 2021 mostram que decisões de coleta moldam suposições de modelagem; o e-SNLI tem muito mais restrições que o COS-E (ex.: exigir explicação auto-contida). Proposta: datasheet do e-SNLI deveria dizer que "auto-contida" foi exigida mas não é necessária.

#### §5 — Explicações estruturadas (3 takeaways)
1. **Estudar como as pessoas definem e geram explicações da tarefa antes de coletar free-text** (pilotos, seguindo o GLUCOSE) (§5).
2. **Se o piloto mostrar estrutura natural, abraçar a estrutura** no esquema de anotação (§5). Evidência: no NLI isso aconteceu; Camburu et al. 2020 dizem que os templates por rótulo são consequência natural da tarefa e do dataset, não exigência da coleta.
3. **Não há definição única de explicação;** consultar especialistas ou outras áreas e manter a forma adequada aberta a debate por tarefa (§5).
- Contexto: free-text é expressivo, mas tem subespecificação e inconsistência por dificuldade de controle de qualidade (§5). Sem estrutura aparente, o jeito é controlar qualidade o máximo possível; baixa qualidade é gargalo (§5). Exemplares de controle de qualidade citados: VCR e GLUCOSE (§5; Tabela 8).
- Preocupação com templates: modelo que prevê o rótulo a partir da explicação gerada pode usar o tipo de template e ignorar a semântica, tornando a leitura humana infiel (§5). Quem escreveu o paper pergunta: que diferença há entre templates descartados e os que sobram?

#### §6 — Qualidade (2 takeaways)
1. **Collect-And-Edit** pode reduzir vieses individuais, fazer controle de qualidade e, possivelmente, reduzir artifacts (§6.1). Detalhe: poucos datasets fazem sequer Collect-And-Judge (eQASC, WinoWhy, VCR); julgar remove instâncias ruins e permite publicar notas de qualidade. Fora de ExNLP: Parikh et al. 2020 (editar alvos extraídos automaticamente) e Bowman et al. 2020 (editar em vez de criar hipóteses de NLI reduz artifacts no MNLI). Estudo de caso: E-SNLI-VE e VQA-E, coletados automaticamente sem edição, têm qualidade inferior (VQA-E tem plausibilidade bem menor que VCR); julgar/editar mesmo num subconjunto revela e mitiga o problema (§6.1).
2. **Ensinar e testar a tarefa subjacente e tratar a ambiguidade** melhora a qualidade (§6.2–§6.3). Ensinar/testar: qualification tasks e checker questions, baratos; a necessidade cresce com a dificuldade e a especificidade da tarefa; algumas tarefas (detecção de engano, reincidência) nem humanos explicam bem (§6.2). Ambiguidade: explicações post-hoc supõem que o explicador acredita no rótulo, o que falha em NLI, extração de relações e complement coercion; se há dúvida, a explicação é no máximo uma hipótese, no pior caso um chute. Ideal: mesmo anotador dá rótulo e explicação; alternativa: checker question perguntando se concorda com o rótulo (§6.3).
- Motivação geral: anotadores escrevendo do zero produzem alvos "baunilha" sem variedade; isso gera artifacts como os do SNLI/MNLI e leva a superestimar desempenho (§6).

#### §7 — Diversidade (2 takeaways)
1. **Para aumentar diversidade:** muitos anotadores, várias anotações por instância e explicações úteis às necessidades do usuário final (§7, takeaway 1).
   - Muitos anotadores (§7.1): Geva et al. 2019 mostram que um anotador a cada 100–1000 exemplos permite o modelo sobreajustar às características do anotador; verificar se algum trabalhador anotou fatia excessiva; opcionalmente coletar demografia ou modelar anotadores como grafo. Exemplos: e-SNLI com média de 860 explicações por trabalhador; COS-E v1.11 repete uma explicação errada em 529 instâncias, provavelmente de um só anotador. Atributos demográficos predizem diferenças de anotação, e explicações dependem de contexto sociocultural.
   - Várias anotações por instância (§7.2): "uma única explicação correta" é mito; se há subjetividade, coletar várias, senão uma explicação plausível do modelo é penalizada injustamente; várias explicações também são sinal de aprendizado. Medir via concordância entre anotadores.
   - Contrastivas e negativas (§7.3): ainda não existe dataset com explicações contrastivas free-text/estruturadas. Ideias: (i) explicações do tipo "por que X em vez de Y"; (ii) explicações para rótulos que não são o verdadeiro, como sinal de treino; (iii) explicações negativas (inválidas para o par entrada/rótulo), obtidas de graça numa fase JUDGE (as de nota baixa) ou EDIT (as pré-edição).
2. **Relatar a concordância entre anotadores sobre a plausibilidade** das explicações, para saber se há diversidade natural a considerar em modelagem e avaliação (§7, takeaway 2).

### 5. Tudo que o paper diz sobre o e-SNLI
- Natureza: NLI (SNLI + explicações), coletado por crowd, ~569K instâncias, 1 ou 3 explicações por instância; tem highlights e free-text; sem restrição de granularidade nos highlights (Tabelas 3–4, §3).
- Duas etapas da anotação: primeiro marcar palavras essenciais, depois escrever a explicação a partir delas (§5; Ap. Tabela 6). Só metade das palavras marcadas precisava ser usada com a mesma grafia; os autores verificaram que também havia palavras não marcadas, pois a explicação deve articular elo entre as palavras-chave (Ap. Tabela 6).
- Restrições gerais: explicação auto-contida; foco nas partes da premissa não repetidas na hipótese; verificações no navegador (pelo menos 3 tokens; não ser cópia da premissa nem da hipótese) (Ap. Tabela 6).
- Restrições por rótulo: entailment exige justificar todas as partes da hipótese ausentes da premissa e marcar ao menos uma palavra na premissa; contradiction exige marcar ao menos uma palavra em cada frase; neutral permite marcar apenas palavras da hipótese, para enfatizar a assimetria da relação e evitar confundir premissa e hipótese; em neutral/contradiction a explicação conta como correta se citar ao menos um elemento (Ap. Tabela 6, §4).
- Consequência declarada: os highlights do e-SNLI são NÃO comprehensive (instrução de marcar só a hipótese no neutral; um elemento basta) (§4). Os highlights de neutral são insuficientes por construção: servem só de passo intermediário, e apenas a explicação free-text justifica o neutral (§4, Tabela 2).
- Qualidade: autores avaliaram 1000 exemplos aleatórios com nota entre 0 e 1 (parcial k/n se só k de n argumentos exigidos); erro total 9,62% (entailment 19,55%; neutral 7,26%; contradiction 9,38%); na grande maioria dos casos é fácil inferir o rótulo a partir da explicação (Ap. Tabela 6).
- Templates: lista de 56 templates; explicação com distância de edição < 10 a algum template era tratada como incorreta; 11% do dataset detectado e reanotado (§5; Ap. Tabela 6). Mesmo assim, Camburu et al. 2020 listam 28 templates específicos por rótulo (ex.: "X é outra forma de Y" para entailment) que ainda dominam (§5). Brahman et al. 2021: modelos treinados nas explicações ouro geram explicações tipo template em NLI defeasible (§5).
- Concordância: Camburu et al. 2018 acharam BLEU baixo entre explicações de anotadores diferentes no teste (o paper não dá o valor) (§7.2).
- Anotador: média de 860 explicações por trabalhador (§7.1).
- Comparação: o e-SNLI tem muito mais restrições e controles que o COS-E, que é considerado por alguns inutilizável por ruído; e-SNLI é exemplo de bom controle (§4, §5).
- Derivados: E-SNLI-VE (visual, 11.335 instâncias, 3 explicações) e E-δ-NLI (NLI defeasible, 92.298, ~8 explicações, coleta "auto") (Tabela 4); no E-SNLI-VE, revalidação dos neutros de val/teste por Do et al. 2020 e artefatos nos neutros/entailment de treino (§6.1).
- Ambiguidade de rótulos em NLI citada como caso em que a hipótese "explicador acredita no rótulo" falha (§6.3).

### 6. Riscos e limitações apontados
- Todo dataset de explicação depende de humanos (≥ 90% dos casos), com qualidade variável; ~66% dos papers reportam licença, só 45,61% usam licenças permissivas comuns (§3, Ap. B).
- Quase todos os datasets são em inglês, exceto SCAT (§3).
- Templates e artifacts: modelos podem aprender o formato e não a semântica; explicações geradas parecem plausíveis sem serem fiéis (§5, §6).
- Coleta automática sem edição/julgamento traz artifacts (E-SNLI-VE, VQA-E) (§6.1).
- Pouco anotadores dominando o dataset produz overfit a traços do anotador e viés social (§7.1).
- Restrições de coleta podem virar "propriedades universais" por inércia (§4).
- Algumas tarefas não são bem explicáveis por humanos nem com treino (§6.2). Ambiguidade de rótulo faz a explicação virar chute (§6.3).
- Limites declarados do próprio paper: foca em propriedades como sufficiency, comprehensiveness, plausibility, faithfulness, templates e artifacts; pode haver outras propriedades relevantes não discutidas (Ap. A, nota de escopo). Coleta da lista de datasets foi por conhecimento dos autores, busca na ACL Anthology (2020 em diante) e contribuições da comunidade (Ap. C).

### 7. Inferência do agente (NÃO está no paper)
O paper trata de coleta humana; nada aqui foi avaliado por ele para LLMs. Mapeamento proposto às 4 rodadas do Pedro.
**Traduz bem:**
- Relatar a coleta (§4 t1, t6) -> guardar prompts verbatim, versão do modelo, parâmetros e as restrições impostas, com nota de quais são necessárias; é a "datasheet" do dataset (todas as rodadas).
- Piloto antes de coletar (§5 t1–t2) -> rodada 0 (2.000 saídas): medir quanto das saídas cai em poucos templates, por rótulo; o paper diz que template por rótulo é natural em NLI, então medir e documentar, não necessariamente cortar. LLMs tendem a ser MAIS homogêneos que crowd, logo o risco é maior (inferência).
- Checagens automáticas à la e-SNLI (Ap. Tabela 6) -> rodada 0: tamanho mínimo, não ser cópia da premissa/hipótese, citar elementos da hipótese ausentes na premissa (entailment), distância de edição a templates; mesmo espírito, regras programáticas em vez de checagem no navegador. Também: checar se o rótulo é recuperável só da explicação (o e-SNLI notou que é fácil).
- Collect-And-Edit/Judge (§6.1) -> rodadas 1–2: gerar, depois passada de crítica/edição ou juiz, com auditoria manual de um subconjunto (o paper diz que mesmo um subconjunto ajuda). Cuidado: juiz da mesma família tem viés de auto-preferência (inferência).
- Ensinar e testar a tarefa (§6.2) -> rodada 1: definições de rótulo e exemplos no prompt; teste: pedir ao modelo prever o rótulo sem ver o ouro e medir concordância com o gold no e-SNLI.
- Ambiguidade (§6.3) -> o caso crítico do Pedro é post-hoc (rótulo dado). Equivalente da checker question: perguntar ao modelo se concorda com o rótulo ouro e marcar discordâncias para revisão/descarte, pois ali a explicação tende a ser racionalização forçada.
- Concordância entre variantes (§7.2) -> rodada 1: medir sobreposição (BLEU ou similar) entre as variantes de prompt nos mesmos ~300 pares; baixa sobreposição entre explicações aceitáveis indica diversidade legítima (ideia, não procedimento do paper).
- Auditoria de 1000 exemplos (Ap. Tabela 6) -> rodada 2 tem a mesma escala; comparar com 9,62% de erro humano total, com entailment pior (19,55%) como baseline informativo.
- Uma "fatia por trabalhador" (§7.1) -> um único prompt/modelo equivale a UM anotador que escreve 100% do dataset, o extremo do problema de Geva. Misturar variantes de prompt, temperaturas e exemplos few-shot reduz, mas não equivale a diversidade de pessoas; na rodada 3, limitar a fatia de cada variante e comparar canary (5k) contra o resto.
- Negativas/contrastivas (§7.3) -> opcional e custoso (explicações para rótulos errados ou as versões pré-edição como negativas); só se houver orçamento.
**Não traduz (ou só em parte):**
- Highlights, sufficiency e comprehensiveness (§4): o Pedro gera free-text; só voltam se usar highlights.
- Qualification tasks, atenção de crowdworkers, feedback pessoal, demografia e representatividade sociocultural (§6.2, §7.1): não há equivalente direto; o análogo é o viés do próprio LLM.
- Faithfulness (§4–§5): refere-se a explicações que o modelo usa para decidir. Na arquitetura do Pedro a explicação é só alvo auxiliar do decoder descartado, então o risco de "classificar pelo template" é menor (inferência a validar).
- Decidir se a explicação deve ser auto-contida (herdado do e-SNLI) é escolha de projeto, não imposição; registrar a decisão (§4 t6).

### 8. O que NÃO consegui ler ou confirmar
- Versão exata do ar5iv (v3 ou v4) e se difere do PDF final; não vi o PDF.
- Trilha exata do NeurIPS ("Datasets and Benchmarks") não aparece no texto lido.
- Figuras 1–2 só pelas legendas; Tabelas 3–5 foram lidas como texto achatado (alinhamento coluna-valor inferido).
- Não constam: o valor do BLEU entre anotadores do e-SNLI, o número de trabalhadores do e-SNLI, e definição formal de "rationale" para free-text ou de "post-hoc" (só o uso em §6.3).
- Não trata explicações geradas por LLM nem custo; qualquer extensão está só na seção 7.
- Versões v1–v2 (mais longas) não lidas; referências citadas (Camburu 2018/2020, Brahman 2021, Geva 2019 etc.) não conferidas na fonte.

---

## 5. Extração: documentação da Anthropic sobre desenvolver e testar prompts (acesso em 20/10/2026)

Convenção: [DEF] = página "Define success criteria and build evaluations"; [BP] = "Prompting best practices"; [OV] = "Prompt engineering overview"; [H55] / [S55] = guias de modelo. Tudo é paráfrase; nomes de seção e termos técnicos ficam no original.

### 1. Identificação

| Sigla | Título da página | URL exata | Observação |
|---|---|---|---|
| DEF | Define success criteria and build evaluations | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Esta é a página única que cobre critérios + avaliações. |
| (DEF) | mesmo conteúdo | https://platform.claude.com/docs/en/test-and-evaluate/define-success | A URL pedida devolveu o conteúdo de develop-tests (redirecionamento aparente). O mesmo ocorreu com .../test-and-evaluate/eval-tool. |
| OV | Prompt engineering overview | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Curta; delega as técnicas para BP. |
| BP | Prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Substituiu as antigas sub-páginas: .../be-clear-and-direct e .../multishot-prompting devolveram esta mesma página. Seções usadas: Be clear and direct, Add context, Use examples effectively, Structure prompts with XML tags, Give Claude a role, Communication style and verbosity, Control the format of responses, Migrating away from prefilled responses. |
| H55 | Prompting Claude Haiku 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 | Lida com o modelo-alvo (extra, não pedido). |
| S55 | Prompting Claude Sonnet 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 | Idem. |
| link | Evals cookbook | https://platform.claude.com/cookbook/misc-building-evals | Citado em "Next steps" de DEF; NÃO lido. |

Data de acesso: 20/10/2026.

### 2. O que a metodologia é, em um parágrafo

[DEF, intro; OV "Before prompt engineering"] A documentação trata prompt engineering como um ciclo: (1) definir critérios de sucesso, (2) montar casos de teste/avaliações que medem esses critérios, (3) escrever um prompt preliminar, (4) testar e refinar iterativamente, (5) validar no final e só então entregar (fluxograma da intro de DEF: test cases -> preliminary prompt -> iterative testing and refinement -> final validation -> ship). OV diz que o guia de técnicas pressupõe três coisas já prontas: critérios de sucesso claros, um jeito empírico de testar contra eles e um primeiro rascunho de prompt; se faltar algo, estabelecer isso antes. [OV "When to prompt engineer"] Nem todo critério ou eval que falha se resolve com prompt; latência e custo, por exemplo, às vezes melhoram mais trocando de modelo. [BP, Migration/Model-specific] Técnicas medidas em um modelo devem ser reconferidas nos seus próprios evals antes de aplicar a outro.

### 3. Critérios de sucesso [DEF, "Define your success criteria"]

Propriedades de um bom critério (as quatro):
- Specific: diz exatamente o que se quer (ex.: "classificação de sentimento precisa", não "bom desempenho").
- Measurable: métricas quantitativas ou escalas qualitativas bem definidas; qualitativo vale se aplicado de forma consistente ao lado do quantitativo. Até segurança pode ser quantificada (ex.: menos de 0,1% de saídas sinalizadas como tóxicas em 10.000 tentativas).
- Achievable: ancorado em benchmarks do setor, experimentos prévios, pesquisa ou conhecimento de especialista; não irreal para modelos de fronteira atuais.
- Relevant: alinhado ao propósito da aplicação e à necessidade do usuário.

Exemplos de métricas/métodos (accordion "Example metrics and measurement methods"):
- Quantitativas: específicas da tarefa (F1, BLEU, perplexity), genéricas (accuracy, precision, recall), operacionais (tempo de resposta em ms, uptime).
- Métodos: A/B test contra baseline ou versão anterior; feedback de usuário (taxa de conclusão); edge case analysis (percentual tratado sem erro).
- Escalas qualitativas: Likert (ex.: coerência de 1 a 5); rubricas de especialista (ex.: linguistas avaliando tradução).

Exemplo ruim vs. bom (sentiment analysis): ruim = "o modelo deve classificar sentimentos bem"; bom = F1 >= 0,85 em conjunto held-out de 10.000 posts diversos do Twitter, 5% acima do baseline atual.

Critérios comuns (lista não exaustiva): Task fidelity (inclui casos de borda e raros); Consistency (respostas parecidas para entradas parecidas); Relevance and coherence (atende à instrução, lógico); Tone and style (adequado ao público); Privacy preservation; Context utilization; Latency; Price (custo por chamada, tamanho do modelo, frequência).

Multidimensional: a maioria dos casos precisa de vários critérios ao mesmo tempo. Exemplo da página (mesmo held-out de 10.000 posts): F1 >= 0,85; 99,5% das saídas não tóxicas; 90% dos erros são incômodos e não graves; 95% das respostas em menos de 200 ms.

### 4. Avaliações

#### 4.1 Princípios de desenho [DEF, "Build evaluations", Eval design principles]
1. Task-specific: o conjunto deve espelhar a distribuição real da tarefa e incluir casos de borda. Os listados: entrada irrelevante ou inexistente; entrada/entrada de usuário longa demais; (chat) entrada ruim, nociva ou irrelevante; casos ambíguos em que até humanos teriam dificuldade de chegar a consenso.
2. Automate when possible: preferir formatos auto-corrigíveis (múltipla escolha, string match, code-graded, LLM-graded).
3. Prioritize volume over quality: muitas questões corrigidas automaticamente com sinal um pouco pior superam poucas questões de alta qualidade corrigidas à mão.
Dicas [DEF, Tips após os exemplos]: escrever centenas de casos à mão é difícil; peça ao Claude para gerar mais casos a partir de um conjunto-base; também dá para pedir ao Claude para sugerir métodos de avaliação quando não se sabe qual usar.

#### 4.2 Exemplos de evals da página (todos com código em 7 linguagens, modelo claude-opus-5-5)
| Dimensão | Caso | Método | Conjunto de teste |
|---|---|---|---|
| Task fidelity | sentimento | exact match (strip + minúsculas); prompt força saída única entre positive/negative/neutral/mixed | 1.000 tweets rotulados, com sarcasmo e sentimento misto |
| Consistency | FAQ bot | média da cosine similarity entre embeddings SBERT (all-MiniLM-L6-v2) das respostas a paráfrases | 50 grupos de FAQ com paráfrases (typos, perguntas longas, info irrelevante) |
| Relevance/coherence | resumo | ROUGE-L F1 (maior subsequência comum) contra resumo de referência | 200 artigos (multitópico, títulos enganosos); versões não-Python usam LCS simplificado e podem divergir da lib rouge |
| Tone and style | atendimento | LLM-based Likert 1-5 por chamada separada de grader que devolve só o número | 100 consultas com tom-alvo (cliente irritado, problema complexo, elogio disfarçado de reclamação) |
| Privacy | chatbot médico | LLM-based binary (PHI sim/não); consultas sem PHI passam automaticamente | 500 consultas simuladas (PHI explícito, hipotético, implícito) |
| Context utilization | assistente conversacional | LLM-based ordinal scale 1-5 (accordion) | 100 conversas multi-turno com perguntas dependentes de contexto (inclui contexto de muitos turnos atrás) |
Nota: a página recomenda usar um modelo diferente como grader do que gerou a saída [DEF, exemplo Likert]. Latency e Price estão na lista de critérios mas NÃO têm eval de exemplo.

#### 4.3 Métodos de correção [DEF, "Grade your evaluations"]
Regra: escolher o método mais rápido, confiável e escalável que sirva.
- Code-based grading: o mais rápido e confiável, extremamente escalável; falta nuance para julgamentos complexos que pedem menos rigidez de regra. Formas: exact match (saída == gabarito) e string match (frase-chave contida na saída).
- Human grading: o mais flexível e de maior qualidade, porém lento e caro; evitar se possível.
- LLM-based grading: rápido, flexível, escalável e adequado a julgamento complexo; testar a confiabilidade antes de escalar.

Dicas para LLM-based grading [DEF, "Tips for LLM-based grading"]:
- Rubricas detalhadas e claras (exemplo: se a resposta não mencionar a empresa na primeira frase, é "incorrect" automaticamente). Um mesmo caso de uso, ou um mesmo critério, pode precisar de várias rubricas para avaliação completa.
- Saída empírica/específica: mandar o grader responder só 'correct'/'incorrect' ou uma nota 1-5; avaliação puramente qualitativa é difícil de checar rápido e em escala.
- Estimular raciocínio: usar grader com thinking ligado, para raciocinar antes de dar a nota; melhora o desempenho, sobretudo em julgamento complexo.
- Exemplo de código na página: prompt de grader com <rubric> e <answer> em tags XML, saída em <result>correct|incorrect</result>, score = % de "correct".

### 5. Técnicas de prompt relevantes [BP; OV]

OV diz que todas as técnicas (clareza, exemplos, XML, role, thinking, chaining) estão em BP, "o documento vivo"; as sub-páginas antigas foram absorvidas.

Be clear and direct [BP]: tratar o modelo como um funcionário brilhante porém novo, sem contexto das suas normas; quanto mais preciso, melhor. "Regra de ouro": mostre o prompt a um colega com pouco contexto e peça que o siga; se ele ficaria confuso, o Claude também. Especificar formato e restrições de saída; usar passos sequenciais (lista numerada/bullets) quando ordem ou completude importam. Se quer comportamento "além do básico", peça explicitamente.
Add context [BP]: explicar o motivo da instrução ajuda o modelo a generalizar (exemplo: "nunca use reticências" melhora quando se diz que o texto será lido por um motor de text-to-speech).
Use examples effectively [BP]: exemplos (few-shot/multishot) são das formas mais confiáveis de fixar formato, tom e estrutura. Devem ser Relevant (espelham o uso real), Diverse (cobrem bordas e variam para evitar padrões involuntários) e Structured (dentro de <example>, vários em <examples>). Dica: 3 a 5 exemplos; dá para pedir ao Claude que avalie relevância/diversidade ou gere mais exemplos. Com thinking, exemplos também moldam o raciocínio do modelo (apresentar problema, método, resposta esperada) [BP, seção de thinking].
Structure with XML tags [BP]: separar instruções, contexto, exemplos e entradas variáveis em tags de nomes consistentes e descritivos (<instructions>, <context>, <input>); aninhar quando há hierarquia.
Give Claude a role [BP]: definir o papel no system prompt direciona comportamento e tom; uma frase já faz diferença (exemplo da página: assistente de código especializado em Python).
Output format/length [BP]:
- Comunicação: modelos recentes são mais diretos, conversacionais e menos verbosos; podem pular resumos a menos que se peça.
- Controle de formato: (1) diga o que fazer em vez do que não fazer (em vez de "sem markdown", "prosa fluida em parágrafos"); (2) use indicadores XML de formato (pedir a prosa dentro de uma tag nomeada); (3) alinhe o estilo do prompt ao estilo desejado da saída (prompt sem markdown reduz markdown); (4) para preferências detalhadas, dê instruções explícitas (a página traz um bloco de exemplo que desencoraja listas/negrito).
- O comprimento: a página não traz fórmula de controle de tamanho para o Sonnet/Haiku; pede-se "prompt explicitamente por concisão" apenas no contexto do Opus 5 (que é verboso) [BP, Communication style]. Para controlar tamanho, o que há é instrução explícita.
- Prefill: respostas pré-preenchidas no último turno do assistente NÃO são mais suportadas desde Claude 4.6 (retorna 400). Para eliminar preâmbulos, a página sugere instrução direta no system prompt (responder sem preâmbulo, sem começar com "Here is..."), tags XML na saída, structured outputs ou tool calling; e remover o preâmbulo por pós-processamento se escapar algum. Para classificação/formatos rígidos: Structured Outputs ou tools com enum [BP, Migrating away from prefilled responses].
Chaining [BP, Chain complex prompts]: encadear chamadas ainda vale quando se quer inspecionar saídas intermediárias; padrão comum é rascunho -> revisão contra critérios -> refinamento, cada etapa uma chamada.
Específico dos modelos-alvo:
- [H55] Haiku 5.5 é o primeiro Haiku com níveis de effort (low, medium [padrão], high, xhigh, max); thinking vem ligado por padrão e conta para max_tokens (cabe até 128.000), então um max_tokens dimensionado sem thinking pode truncar a resposta; baixar o effort é a forma de reduzir o thinking (mandar "responda direto" no prompt não impediu). `low` serve a requisições simples e de alto volume. Thinking pode ser desligado com thinking disabled apenas em low/medium/high. Texto de raciocínio pode vazar para a resposta visível com thinking off ou effort low; a sugestão é adaptive thinking + medium.
- [S55] Sonnet 5.5: recalibrar effort com evals próprios; padrão high na API; thinking mínimo = `between_tools`; para tarefas que exigem alguns passos de raciocínio, preferir adaptive thinking. Dica de custo/latência: effort menor, não instrução "pense menos".
- Ambos [H55; S55, "Safeguard refusals"]: classificadores de segurança podem devolver stop_reason "refusal" (categorias cyber, bio, frontier_llm, general_harms; no Sonnet 5.5 também reasoning_extraction). Tratar no cliente; reenviar a mesma requisição ao Haiku 5.5 normalmente repete a recusa. [S55] Prompts que pedem ao modelo reproduzir seu raciocínio interno no texto convidam recusas reasoning_extraction; ainda é permitido pedir uma explicação curta da resposta.

### 6. Inferência do agente (NÃO é da documentação)

#### 6.1 Decisões abertas viradas em critérios no estilo da doc (valores são propostas a calibrar no piloto)
Critério por dimensão da doc (Task fidelity / Consistency / Tone / Privacy... adaptadas):
- Label não nomeado (task fidelity): racional não contém "entailment/contradiction/neutral" nem sinônimos diretos; meta, p.ex., >= 99% das saídas limpas por regex, medido em 2.000 pilotos (code-based, string match).
- Definição do rótulo não parafraseada: sem "A hipótese decorre da premissa" como única justificativa; checar por lista de frases-molde (string match) + amostra de LLM-grader binário.
- Faixa de comprimento (measurable): p.ex. 1-2 frases e N a M palavras/tokens; meta: >= 98% dentro da faixa (code-based).
- Copy rate: razão de n-gramas copiados da premissa/hipótese (ou ROUGE-L contra a premissa); teto proposto a definir olhando a distribuição do e-SNLI humano.
- Consistência com o gold label: um grader (modelo diferente do gerador, conforme [DEF]) responde se a explicação sustenta o rótulo dado; meta de concordância com amostra humana a definir.
- Refusal rate: fração com stop_reason "refusal" e fração de saídas vazias/truncadas por max_tokens; meta próxima de 0 (explicações post-hoc de NLI não são "raciocínio interno", mas confirmar no piloto, ver [S55]).
- Consistency: paráfrase/ordem de exemplos não deve mudar o estilo (comparação de variantes), tipo o eval de consistência da doc.
- Formato: 0 preâmbulos ("Here is...") e 0 markdown; code-based.
- Operational/Price: custo por 1k pares e taxa de falha do batch; critérios de Price/Latency da lista de [DEF].
Cada critério precisa ser Specific/Measurable/Achievable/Relevant: escreva o número-alvo ANTES de olhar os resultados.

#### 6.2 Mapa seção da doc -> rodadas do protocolo
- Rodada 0 (checks automáticos em 2.000 pilotos): [DEF] "Automate when possible" + code-based grading (string match, regex, comprimento, copy rate, refusal/max_tokens). Também define os critérios (3).
- Rodada 1 (3-4 variantes de prompt em ~300 pares): [BP] clear/direct, examples (3-5, diversos, em <examples>), role, formato; comparar variantes pelos mesmos critérios; usar LLM-based grading com rubrica clara, saída numérica ou binária e grader de modelo distinto; validar o grader contra uma amostra humana pequena antes de escalar [DEF "Test to ensure reliability first"]. Incluir bordas: premissas longas, hipóteses ambíguas, pares onde humanos discordam.
- Rodada 2 (vencedora em 1.000 held-out): [DEF] "final validation"/held-out; conjunto não visto durante a iteração.
- Rodada 3 (canário de 5k e o restante): o fluxo "ship" de [DEF]; repetir as checagens automáticas no canário. Fora da doc: o que fazer se o canário falhar.

### 7. O que NÃO consegui ler ou confirmar

- define-success devolveu a página develop-tests; não confirmei se é redirect HTTP ou alias. A página inteira foi coberta: a primeira leitura devolveu os 100.000 primeiros caracteres (de 153.035) por um sumarizador, e li o restante (de 100.000 em diante) a partir do arquivo bruto salvo, incluindo "Grade your evaluations" e "Next steps". A parte 0-100.000 foi vista só na forma resumida pela ferramenta (não li o texto bruto), então detalhes finos dos exemplos de código podem faltar.
- Não achei, na página, orientação de tamanho do conjunto de teste além dos números dos exemplos (50 a 1.000 casos), nem regra de amostragem estatística, nem critérios de tamanho mínimo para o grader humano.
- Evals cookbook (https://platform.claude.com/cookbook/misc-building-evals): não lido.
- Não há, em BP/OV, orientação específica para geração de dados em lote via Batches API nem sobre temperature/consistência entre execuções; não li a página da Batches API (fora do escopo pedido).
- Os blocos "Model-specific guidance" de Opus/Fable não foram lidos; H55 e S55 foram lidos por completo.
- As antigas URLs de sub-páginas (be-clear-and-direct, multishot-prompting) devolvem BP; não procurei páginas separadas para role prompting ou "control output format".
- Seção 6 é inferência minha e os números são placeholders.

---

## 6. Datasheets for Datasets (Gebru et al.) - extração para documentar o dataset de racionalizações

Procedência: nível 2 (agente leu o texto completo do PDF v8, 12 páginas + apêndice). Todas as perguntas abaixo são paráfrases minhas; a redação original é a do paper. Referências "§" = seções do paper.

### 1. Identificação
- Título: *Datasheets for Datasets*. Autores: Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daumé III, Kate Crawford.
- Venue/ano: Communications of the ACM, dez/2021 (campo Comments do arXiv); primeira versão no arXiv em 23/03/2018.
- URL: https://arxiv.org/abs/1803.09010 (PDF lido: https://arxiv.org/pdf/1803.09010v8).
- Versão lida: **v8, 1/12/2021** (a mais recente; v1..v8 listadas na página do arXiv). O ar5iv devolveu só um resumo, então o texto foi lido do PDF v8.

### 2. O que o framework é e para quem
Proposta de que todo dataset acompanhe um "datasheet", por analogia com as folhas de dados de componentes eletrônicos, documentando motivação, composição, coleta, usos recomendados etc. (§1). Objetivo para **criadores**: forçar reflexão cuidadosa sobre criar, distribuir e manter o dataset, incluindo premissas, riscos/danos potenciais e implicações de uso. Objetivo para **consumidores**: dar a informação necessária para escolher o dataset adequado à tarefa e evitar mau uso (§1.1). Públicos secundários: formuladores de política, jornalistas, titulares de dados, pessoas afetadas por modelos; objetivo secundário: reprodutibilidade (quem não tem o dataset poderia recriar um parecido a partir do datasheet) (§1.1). As perguntas **não são prescritivas**: variam com domínio e fluxo da organização (§1.1).

### 3. Quando preencher
- O paper agrupa as perguntas pelas etapas do ciclo de vida do dataset (§3). Perguntas inaplicáveis devem ser puladas (§3); responder o máximo possível é preferível a pular o datasheet inteiro (§3).
- **Composition** e **Collection Process**: ler as perguntas **antes** de coletar (para sinalizar problemas) e **responder depois** que a coleta termina (§3.2, §3.3).
- **Preprocessing/cleaning/labeling**: ler antes de qualquer pré-processamento/limpeza/rotulagem e responder depois de concluídos (§3.4).
- **Distribution** e **Maintenance**: responder **antes de distribuir** o dataset, seja internamente na organização, seja a terceiros (§3.6, §3.7).
- **Motivation** e **Uses**: o paper não dá instrução de momento explícita para estas duas (§3.1, §3.5). (Ver item 7.)
- Automação: o paper afirma que criar o datasheet **não deve ser automatizado**, pois automatizar contraria o objetivo de levar o criador a refletir (§1.1).
- Se o criador não souber responder, o exemplo do apêndice usa a resposta "desconhecido para os autores do datasheet" (§3, Apêndice).

### 4. As sete seções (perguntas parafraseadas)
Contagem no PDF v8: Motivation 4, Composition 16, Collection Process 12, Preprocessing 4, Uses 6, Distribution 7, Maintenance 8 = 57 itens (incluindo os "algum outro comentário?").

#### 4.1 Motivation (§3.1)
Função: explicitar o porquê do dataset e transparência sobre financiamento.
1. Com que finalidade o dataset foi criado? Havia tarefa específica ou lacuna a preencher? Descrever.
2. Quem criou (equipe/grupo) e em nome de qual entidade (empresa, instituição)?
3. Quem financiou? Se houve bolsa/projeto, informar financiador, nome e número.
4. Algum outro comentário?

#### 4.2 Composition (§3.2)
Ler antes da coleta, responder depois. Parte das perguntas serve à conformidade com GDPR ou similares. Perguntas sobre pessoas ficam no fim; o paper recomenda interpretação ampla (qualquer dataset com texto escrito por pessoas "relaciona-se com pessoas").
1. O que cada instância representa (documentos, fotos, pessoas...)? Há vários tipos de instância? Descrever.
2. Quantas instâncias no total (por tipo, se couber)?
3. O dataset contém todas as instâncias possíveis ou é amostra (não necessariamente aleatória) de um conjunto maior? Qual o conjunto maior, a amostra é representativa dele e como isso foi verificado? Se não é representativa, por quê?
4. De que é feita cada instância: dado "bruto" ou atributos extraídos? Descrever.
5. Existe rótulo/alvo por instância? Descrever.
6. Falta informação em instâncias individuais? Por quê (exclui o que foi removido de propósito; inclui, p.ex., texto censurado)?
7. As relações entre instâncias estão explícitas (avaliações de usuários, links)? Como?
8. Há divisões recomendadas (treino/validação/teste)? Descrever e justificar.
9. Existem erros, fontes de ruído ou redundâncias no dataset? Descrever.
10. O dataset é autocontido ou depende de recursos externos (sites, tweets, outros datasets)? Se depende: (a) há garantia de que existirão e permanecerão constantes; (b) existe versão arquivada oficial do conjunto completo, incluindo os recursos externos como eram na criação; (c) há restrições (licença, taxas) que afetem o consumidor? Listar recursos, restrições e pontos de acesso.
11. Contém dado possivelmente confidencial (sigilo legal, médico-paciente, comunicações privadas)? Descrever.
12. Contém conteúdo que, visto diretamente, possa ser ofensivo, insultuoso, ameaçador ou gerar ansiedade? Explicar por quê.
*(Pode pular o restante se o dataset não se relaciona com pessoas.)*
13. O dataset identifica subpopulações (idade, gênero etc.)? Como, e qual a distribuição de cada uma?
14. É possível identificar indivíduos, direta ou indiretamente (combinando com outros dados)? Como?
15. Contém dado sensível (raça/etnia, orientação sexual, religião, opinião política, filiação sindical, localização, dados financeiros/de saúde, biométricos/genéticos, documentos oficiais, antecedentes criminais)? Descrever.
16. Algum outro comentário?

#### 4.3 Collection Process (§3.3)
Ler antes da coleta para sinalizar problemas, responder depois. Além de informar o consumidor, estas perguntas ajudam a **recriar datasets similares** (§3.3).
1. Como o dado de cada instância foi obtido: observável diretamente, relatado por sujeitos, ou inferido/derivado de outros dados (p.ex. etiquetas gramaticais, palpites de modelo)? Se relatado ou inferido, foi validado? Como?
2. Que mecanismos/procedimentos coletaram o dado (sensores, curadoria humana, programas, APIs)? Como foram validados?
3. Se o dataset é amostra de um conjunto maior, qual a estratégia de amostragem (determinística, probabilística com probabilidades específicas)?
4. Quem participou da coleta (estudantes, crowdworkers, contratados) e como foi remunerado?
5. Em que período o dado foi coletado? Coincide com o período em que o dado foi criado (p.ex. rastreamento recente de notícias antigas)? Se não, qual o período de criação?
6. Houve revisão ética (comitê institucional)? Descrever, com resultado e documentação de apoio.
*(Pular o restante se não envolver pessoas.)*
7. O dado veio diretamente dos indivíduos ou de terceiros/outras fontes (sites)?
8. Os indivíduos foram notificados da coleta? Como (reproduzir o texto exato do aviso)?
9. Os indivíduos consentiram com coleta e uso? Como o consentimento foi pedido e dado (texto exato)?
10. Se houve consentimento, havia mecanismo para revogá-lo no futuro ou para certos usos?
11. Foi feita análise de impacto do dataset e do seu uso sobre os titulares (p.ex. avaliação de impacto de proteção de dados)? Descrever, com resultados.
12. Algum outro comentário?

#### 4.4 Preprocessing/cleaning/labeling (§3.4)
Ler antes de processar, responder depois. Objetivo: o consumidor saber se o dado "cru" foi transformado de modo incompatível com sua tarefa (exemplo do paper: bag-of-words inviabiliza tarefas dependentes de ordem).
1. Houve pré-processamento, limpeza ou rotulagem (discretização, tokenização, etiquetagem, extração de atributos, remoção de instâncias, tratamento de valores faltantes)? Descrever. Se não, pular o resto da seção.
2. O dado "bruto" foi guardado além do processado (para usos futuros imprevistos)? Onde acessar?
3. O software usado para pré-processar/limpar/rotular está disponível? Onde?
4. Algum outro comentário?

#### 4.5 Uses (§3.5)
Objetivo: o criador refletir sobre tarefas para as quais o dataset deve e não deve ser usado, evitando riscos e danos.
1. O dataset já foi usado em alguma tarefa? Descrever.
2. Existe repositório que liste artigos/sistemas que o usam? Onde?
3. Para que outras tarefas poderia servir?
4. Algo na composição, coleta ou pré-processamento pode afetar usos futuros (p.ex. tratamento injusto de indivíduos/grupos, estereótipos, qualidade de serviço desigual, riscos legais ou financeiros)? O que o consumidor pode fazer para mitigar?
5. Há tarefas para as quais o dataset não deve ser usado? Descrever.
6. Algum outro comentário?

#### 4.6 Distribution (§3.6)
Responder antes de distribuir, interna ou externamente.
1. O dataset será distribuído a terceiros fora da entidade em nome da qual foi criado? Descrever.
2. Como será distribuído (tarball em site, API, GitHub)? Tem DOI?
3. Quando será distribuído?
4. Será distribuído sob licença de copyright/propriedade intelectual e/ou termos de uso? Descrever, indicar onde ler o texto, e informar taxas.
5. Terceiros impuseram restrições de PI ou outras sobre os dados associados às instâncias? Descrever, com termos e taxas.
6. Há controles de exportação ou outras restrições regulatórias sobre o dataset ou instâncias individuais? Descrever, com documentação.
7. Algum outro comentário?

#### 4.7 Maintenance (§3.7)
Responder antes de distribuir; objetivo é planejar a manutenção e comunicá-la ao consumidor.
1. Quem dará suporte/hospedagem/manutenção?
2. Como contatar o responsável (e-mail)?
3. Existe errata? Onde?
4. O dataset será atualizado (corrigir rótulos, adicionar/remover instâncias)? Com que frequência, por quem, e como comunicar (lista de e-mail, GitHub)?
5. Se envolve pessoas: há limite de retenção dos dados (p.ex. avisaram que seriam apagados após um prazo)? Descrever e como será cumprido.
6. Versões antigas continuarão sendo suportadas/hospedadas? Se não, como comunicar a obsolescência?
7. Se outros quiserem estender/aumentar/contribuir, existe mecanismo? As contribuições serão validadas (como, ou por que não)? Como serão repassadas aos consumidores?
8. Algum outro comentário?

### 5. Limitações e ressalvas declaradas (§1.1, §3, §4)
- Perguntas não prescritivas; alguns itens servem a pesquisadores que publicam datasets, menos a equipes que fazem datasets internos para modelos proprietários (§1.1). Criadores devem adaptar perguntas e fluxo à sua infraestrutura (§4).
- Nem todo criador consegue responder tudo; recomenda-se responder o máximo (§3).
- Datasheet **não resolve** viés social nem riscos/danos: o criador não antecipa todos os usos, e medir viés exige rótulos demográficos que podem faltar por privacidade (§4).
- Datasets sobre pessoas podem exigir especialistas de antropologia, sociologia e estudos de ciência e tecnologia (§4).
- Datasets dinâmicos encaixam mal; se mudam pouco, publicar datasheet atualizado a cada versão (§4).
- Custo: preencher dá trabalho sempre; fluxos e incentivos organizacionais precisam acomodar esse investimento, embora possa reduzir perguntas avulsas depois (§4).
- Desenvolvimento: ~2 anos, testado em dois datasets (LFW e polaridade de Pang & Lee), duas equipes de produto, feedback público e revisão jurídica; perguntas de conformidade regulatória explícita foram trocadas por perguntas factuais (§2). Perguntas legais/éticas ficam integradas às etapas, não numa seção à parte (§2).
- Não é checklist de conformidade: o paper o apresenta como instrumento de reflexão e comunicação (§1.1, §4); a leitura "não é checklist" é minha síntese, o paper não usa essa palavra.
- Bender & Friedman (2018) propõem algo parecido específico para linguagem; suas perguntas podem ser integradas ao datasheet de datasets textuais (§1.1).

### 6. Inferência do agente (NÃO é conteúdo do paper)
Base: fatos informados no pedido (racionalizações geradas por Claude Haiku 5.5/Sonnet 5.5 via Batches API, para pares do e-SNLI; protocolo post-hoc premissa+hipótese+rótulo gold -> explicação; 100k-280k textos curtos; uso só para treinar aluno encoder; sem publicar dataset nem pesos; orçamento limitado).

**Já respondíveis (rascunho):**
- Motivation 1: finalidade = treinar um aluno encoder com racionalização de LLM (ver o tema do projeto); lacuna a articular por você. Motivation 2: você/UFG, em nome de residência; Motivation 3: financiamento = orçamento próprio de API/créditos (confirmar a origem exata).
- Composition 1-2: instância = (par premissa-hipótese, rótulo gold, texto da racionalização); contagem = 100k-280k, número final a medir. Composition 3: é amostra ou subconjunto do treino do e-SNLI? depende da sua decisão. Composition 5: rótulo = classe NLI gold do e-SNLI. Composition 4: o alvo adicional é texto gerado, não "bruto".
- Collection 1: dado **inferido/derivado** (gerado por modelo), não observado; validação = o que você de fato fizer (rodadas-piloto, checagem de consistência com o rótulo). Collection 2: software, API em lote do Anthropic. Collection 3: estratégia de amostragem conforme sua escolha de pares. Collection 4: nenhum humano anotador no passo de geração (confirmar); remuneração N/A. Collection 5: período da geração = datas das execuções; o texto-fonte (SNLI) foi criado em outro período (a verificar).
- Preprocessing 1-4: prompt, filtros de formato/tamanho, descarte de saídas inválidas, versão do modelo e parâmetros; se as saídas brutas serão guardadas é decisão sua; scripts disponíveis em tese (a decidir).
- Uses 1: só treino do aluno; Uses 4: contaminação/viés herdado do professor e do SNLI, racionalização post-hoc que explica o rótulo dado, não necessariamente o raciocínio real; Uses 5: não usar como explicação fiel do raciocínio do modelo, nem para treinar modelos concorrentes do Claude (a verificar nos termos da Anthropic).

**A verificar (não sei):** licença e termos do e-SNLI/SNLI (fonte dos pares e das explicações humanas) e se permitem derivados; termos comerciais/de uso da Anthropic para saídas usadas em treino; se há restrições de PI de terceiros sobre as instâncias (Distribution 5); controle de exportação (Distribution 6); conteúdo ofensivo/identificável (SNLI vem de legendas de imagens; a verificar se há pessoas identificáveis); se Composition 13-15 e Collection 7-11 se aplicam (o paper manda interpretar "relaciona-se com pessoas" de modo amplo, §3.2; as explicações são geradas por modelo, mas as legendas-fonte foram escritas por pessoas: a verificar).

**Em grande parte não aplicáveis porque não haverá distribuição:** Distribution 1-6 (responder "não será distribuído"; Distribution 1 e 3 viram uma linha cada, e o paper exige respondê-las antes de distribuir, §3.6, ou seja, ficam simplesmente "não distribuído"); Maintenance 1-8, exceto talvez quem guarda os arquivos e se haverá versões internas (§3.7); Uses 2 (repositório de usos) e Maintenance 7 (contribuições). Se o dataset for compartilhado com orientador/banca, isso conta como distribuição interna à entidade, ainda coberta por §3.6 ("internamente ou a terceiros").

### 7. O que não consegui ler ou confirmar
- O ar5iv e o resumo automático não reproduziram as perguntas; li o texto do PDF v8 extraído com pdftotext. Não vi o PDF renderizado (figuras/rodapés), apenas o texto; a lista de perguntas parece completa (57 itens, bate com as seções e não há sinal de truncamento).
- Motivation e Uses não trazem, no texto, orientação explícita de quando responder; isso é lacuna do paper, não minha (§3.1, §3.5).
- O exemplo do apêndice (polaridade Pang & Lee) foi só folheado; não extraí suas respostas.
- Não verifiquei licenças (e-SNLI/SNLI, termos da Anthropic), nem o conteúdo real do seu dataset: tudo da seção 6 é suposição baseada no pedido.
- O "não é checklist" na seção 5 é minha formulação da ideia de §1.1/§4, não citação.

---

## 7. Extração: Wiegreffe, Hessel, Swayamdipta, Riedl & Choi (2022) — Reframing Human-AI Collaboration for Generating Free-Text Explanations

Procedência: nível 2 (agente leu o texto completo §1–§7 e Apêndices A–F; paráfrase, nenhuma frase copiada). Figuras (imagens) não vistas; números das figuras vêm das Tabelas 18–20.

### 1. Identificação
- Título: Reframing Human-AI Collaboration for Generating Free-Text Explanations. Autores: Sarah Wiegreffe, Jack Hessel, Swabha Swayamdipta, Mark Riedl, Yejin Choi (Georgia Tech / AI2 / UW).
- Venue: Proceedings of NAACL-HLT 2022, pp. 632–658 (confirmado no rodapé do PDF da ACL Anthology). arXiv:2112.08674.
- URL: https://arxiv.org/html/2112.08674 (lido) e https://aclanthology.org/2022.naacl-main.47.pdf (só 1ª-2ª página, para venue/páginas). Código/dados: github.com/allenai/few_shot_explanations (§1; não inspecionado).
- Versão lida: arXiv v2 (04/05/2022), HTML, em 20/10/2026. Seções lidas: Resumo, §1–§7, Apêndices A–F inteiros (inclui Tabelas 1–22). Figuras 1–10 (inclusive as telas de interface da Figura 5–10) não foram vistas.

### 2. O que o trabalho é (um parágrafo)
- Pergunta (§1): um LLM (GPT-3 Davinci, ~175B, versão não-instruct de 2021) consegue produzir explicações em texto livre para decisões de classificação, só com exemplos no prompt? Tarefas: NLI (SNLI + explicações do e-SNLI) e CommonsenseQA (CoS-E, ECQA). O modelo recebe o rótulo ouro (explicação post-hoc), exatamente o cenário de gerar racionalizações para um dataset. Achados (§1): (i) explicações geradas com exemplos escritos pelos autores superam as geradas com exemplos do crowd; (ii) em comparação lado a lado, humanos às vezes preferem o GPT-3 ao crowd do dataset (muito pouco no e-SNLI); (iii) o GPT-3 é bom em gramática/generalidade mas fraco em trazer informação nova e em sustentar o rótulo; (iv) gerar 5 candidatas e filtrar com um modelo treinado em julgamentos binários de "aceitável" melhora a qualidade (overgenerate + filter), mas a margem no SNLI é pequena.

### 3. O pipeline passo a passo

#### 3.1 Construção do prompt (§2, Apêndice A, Tabelas 2, 11, 12)
- Dados: teste fixo de 250 instâncias aleatórias por tarefa, não vistas no desenho do prompt (§2). Para prompts: 115 instâncias de treino no total (15 para desenho inicial + 100 de "dev" fixo), para manter regime few-shot (App. A, seguindo Perez et al. 2021).
- Desenho do layout: no máximo 10 layouts testados no GPT-3 Sandbox com 15 exemplos de CoS-E/e-SNLI; depois 6 prompts amostrados dessas 15 mais o dev de 100 (App. A). Não houve ajuste fino de prompt sobre treino/dev completos.
- Formato SNLI (Tabela 2): cabeçalho curto de tarefa ("explicar decisões de classificação"); cada exemplo = premissa, a hipótese apresentada como "question", resposta restrita a true / false / neither (rótulo ouro), e "why?" seguido da explicação; exemplos separados por "###"; o item final termina em "why?" e o modelo completa. O App. A diz que enquadrar o SNLI como tarefa de perguntas-e-respostas foi o melhor formato (como em Zhao et al. 2021).
- Rótulo ouro é dado no prompt como controle metodológico (nota 3, §2): em piloto os autores não conseguiam avaliar explicações quando discordavam do rótulo previsto; trabalhos anteriores avaliavam só acertos do modelo, o que superestima qualidade.
- Explicações dos exemplos: as 115 foram escritas à mão pelos próprios autores (App. A, Tabela 12), não vêm do e-SNLI. Contraste na Tabela 12: a do autor é longa e hedgeada ("é possível que... mas também é possível que..."); a do e-SNLI é curta ("a pessoa não está necessariamente treinando o cavalo").
- Nº de exemplos: 8–24 por prompt; máximo 24 limitado pela janela de 2049 tokens da API (App. A). No SNLI, o nº por prompt é amostrado de {12, 18, 24}; múltiplo de 3 para balancear rótulos.
- Seleção e ordem: para cada instância de teste, amostra-se um prompt novo (subconjunto aleatório dos 115 + tamanho amostrado + ordem embaralhada), para aproximar o desempenho esperado em vez de fixar um prompt (App. A; nota 14). Balanceamento: igual nº de exemplos por rótulo no SNLI (App. A). Em CommonsenseQA embaralham-se as alternativas.

#### 3.2 Geração (§2, §3)
- Geração gulosa (greedy): 1 explicação por instância (§2). Para sobregeração: +4 explicações amostradas estocasticamente, total 5 candidatas por instância (1 greedy + 4 sampled) (§3, §4.1).
- O texto lido não informa temperatura, top-p nem max tokens da amostragem (ver item 8).

#### 3.3 Avaliação humana (§2, App. B)
- Plataforma: Amazon Mechanical Turk, US$15/hora; locais AU/CA/NZ/UK/US, taxa de aprovação >98%, >5000 HITs aprovados (§2, B.5).
- Três desenhos (B.1): todos mostram instância + rótulo ouro (outras alternativas escondidas), instruem a considerar o rótulo correto mesmo discordando.
- (a) Head-to-head: escolher a melhor entre duas explicações, ignorando erros menores de gramática/maiúsculas; 3 anotações por item; ~30 s/HIT, US$0,12 (B.2, B.5).
- (b) Absoluto: 7 perguntas em Likert/escala curta, 3 anotadores por explicação, ~1 min/HIT, US$0,25 (B.3, B.5). Interface iterada em 3–4 versões até maximizar concordância (B.3).
- (c) Aceitabilidade binária: 1 HIT = 5 explicações da mesma instância, 3 anotadores por explicação, ~35–39 s, US$0,20 (B.4, B.5).
- Qualificação (B.5): prova geral de 3 HITs (9–18 perguntas), US$2,25; na 1ª rodada 17 candidatos tiveram 5–14 de 18 acertos (mediana 11); a nota de corte passou a ser a mediana. Para NLI, prova extra de 8 questões (aprovação >=7), US$1,25.
- Controle de qualidade (B.5): cronômetro oculto; anotador removido (e instâncias reanotadas) se rápido demais ou se sua remoção melhora muito o α de Krippendorff. Nº de anotadores distintos por estudo: 6–34 (Tabela 17); dos estudos de aceitabilidade no SNLI: 14 (treino/val) e 11 (teste); 7 num "Test2".
- Concordância: α baixo-a-moderado (e-SNLI: 0,3 na Tab. 3; 0,5 na Tab. 4; 0,2 na Tab. 5); α do estudo absoluto no SNLI 0,31 (nota 6; ver discrepância no item 8). Aceitabilidade no SNLI: α 0,51 treino/val, 0,50 teste, 0,47 Test2 (Tabela 14).

#### 3.4 Filtro de aceitabilidade (§4, App. E)
- Dados (§4.1): repetir a geração 1 greedy + 4 sampled em 991 (CQA) e 1K (SNLI) instâncias de treino; junto com as 250 de teste dão ~1250 instâncias por tarefa, split 72/8/20%; ~6200 pares instância-explicação e ~19 mil anotações binárias por tarefa; 3 rótulos binários por explicação.
- Rótulo de treino: tratar 2/3 e 3/3 como "aceitável" funcionou melhor para o critério de teste 3/3 (§4.1, nota 11). Variante "sem acordo humano" (w/o HA): sorteia 1 dos 3 votos como rótulo.
- Distribuição de rótulos no SNLI, por explicação (Tabela 13): treino 4500 = 2372 (0/3), 805 (1/3), 621 (2/3), 702 (3/3); teste 1250 = 678/225/166/181.
- Modelo: T5-Large e T0-3B (seq2seq), 5 sementes; entrada = instância + rótulo ouro + explicação + pergunta "esta explicação é boa ou ruim?"; saída binária (App. E). T0-3B: batch 50, Adafactor, lr 1E-5, warmup de 500 passos; T5-L: lr 1E-4, batch 64, até 200 épocas com early stopping (paciência 10).
- Seleção: o modelo dá probabilidade a cada uma das 5 candidatas; "select-1" devolve a de maior probabilidade (§4.3). Também mede-se AP por explicação.
- Baselines: aleatório; constante; NLL do próprio GPT-3 (probabilidade da explicação; pouco melhor que greedy, pois 5 candidatas têm menor NLL que a greedy em só 3,6% das instâncias do teste SNLI, nota 12); modelo só-explicação (sem a instância) (§4.2). Oracle: limite superior pela existência de ao menos uma aceitável entre as 5 (§3, §4.4).

### 4. Atributos de qualidade avaliados (rubrica pronta; §2.3, App. B.3)
- Avaliação em duas partes: Parte 1 mostra a explicação isolada (sem contexto); Parte 2 mostra premissa, hipótese e rótulo. Perguntas 2–4 da Parte 2 são condicionais (ver abaixo).
- Generality (P1): se dá para julgar a veracidade da afirmação sozinha, sem precisar de mais contexto; codificada pela escolha de "preciso de mais informação" na pergunta de factualidade (B.3).
- Factuality (P1): a afirmação é falsa / parcialmente verdadeira / verdadeira / indecidível sem mais contexto (4 opções) (B.3).
- Grammar (P1): sim/não, a frase é gramatical (clareza) (B.3).
- New Info (P2): a explicação traz fatos, informação ou raciocínio que não estão na pergunta/resposta? Visa detectar explicações vazias que só reescrevem o par premissa-hipótese-rótulo (B.3).
- Supports Label (P2): a informação nova é relevante para justificar o rótulo? sim/não; interpretação de "relevante" deixada ao anotador. Em geral só perguntada se New Info = sim; no SNLI foi sempre perguntada (nota da Tabela 18).
- Amount Info (P2): informação insuficiente / suficiente / em excesso para justificar o rótulo; perguntada se Supports Label = sim; o valor desejado é o do meio (B.3; Fig. 2).
- Acceptability (P2): julgamento global sim/não; em estudo separado, binário, é a base do filtro (B.3, B.4).
- Correlação com aceitabilidade (Spearman, Tabela 6, n total 3750 = 250 x 5 fontes x 3 anotadores): Grammar 0,31; Generality 0,25; Supports Label 0,22; Factuality 0,17; Amount Info 0,16; New Info 0,05 (todos p<0,01). Conclusão do §2.3: nenhum atributo isolado explica a aceitabilidade.

### 5. Resultados principais (SNLI/e-SNLI)
- Tabela 3 (GPT-3 greedy com exemplos do e-SNLI vs crowd, 250 itens): crowd 63,6% / empate 11,6% / GPT-3 24,8%; α 0,3. Ou seja, GPT-3 igual ou melhor em 36,4%.
- Tabela 4 (GPT-3 com prompts dos autores vs com prompts do crowd): crowd-prompts 30,8% / empate 26,8% / prompts dos autores 42,4%; α 0,5.
- Tabela 5 (GPT-3 com prompts dos autores vs crowd e-SNLI): crowd 49,6% / empate 9,7% / GPT-3 40,7%; α 0,2 (GPT-3 >= crowd em 50,4%). Para CoS-E o GPT-3 vence (78,9%); para ECQA fica em 45,7 vs 44,5.
- Absoluto (Tabela 18; escala de -1 a 1 inferida; média; GPT-3 greedy / e-SNLI): Generality 0,7 / 0,6; Factuality 0,7 / 0,8; Grammar 1,0 / 0,9; New Info 0,1 / 0,2; Supports Label -0,1 / 0,2; Amount Info -0,2 / -0,1; Acceptability 0,0 / 0,7. Texto §2.3: GPT-3 significativamente melhor em Generality e Grammar; e-SNLI melhor em New Info (p<=0,01), Supports Label (p<=0,1) e aceitabilidade global.
- §3: no SNLI só 31,5% das explicações greedy têm 3/3 de aceitação; as amostradas, 11,3%; mas com as 5 candidatas, 51,2% das instâncias têm ao menos uma 3/3 (CQA: 46,3% -> 79,5%). Com limiar 2/3 (App. D): greedy 51,0%, amostradas 23,5%, ao menos uma em 5: 79,5%.
- Filtro, SNLI (Tabela 8, T0-3B; select-1 Acc@3/3 em dev/test/Test2): Full 37,8/38,7/35,0; w/o HA 38,2/38,5/36,2; NLL 33,0/32,0/31,6; só-explicação 30,2/30,9/27,8; aleatório 15,2/14,7/13,6; Oracle 51,0/52,4/46,4. AP@3/3 (dev/test/Test2): Full 46,8/47,6/49,5; w/o HA 49,3/48,5/52,8; NLL 29,9/32,7/28,5; só-explicação 30,6/30,6/25,9; constante 15,2/14,5/13,7.
- Limiar 2/3 (Tabela 22): select-1 teste Full 60,3 vs NLL 51,2 (oracle 81,2); AP teste Full 64,7 vs NLL 47,5.
- Leitura do §4.4: filtro > NLL por larga margem; só-explicação perde ~5 pontos (usa interação instância-explicação); anotações múltiplas (3x) não compensam sempre o custo; o modelo não decorou anotadores (Test2 parecido); há distância grande até o oracle, "especialmente para SNLI". Com ~5 mil anotações binárias (sem acordo) já se obtém o ganho.
- Efeito humano do filtro, SNLI (Tabela 20; 91 instâncias onde o filtro troca a greedy; greedy -> filtrada): New Info 0,0 -> 0,5; Supports Label -0,2 -> 0,5; Amount Info -0,2 -> 0,0; Acceptability -0,5 -> 0,1; Grammar 0,9 -> 0,7 (piora); Generality 0,8 -> 0,8; Factuality 0,6 -> 0,7. Tabela 9: filtrada vs e-SNLI: crowd 49,9% / empate 6,9% / GPT-3 43,2% (α 0,14); texto diz que não houve ganho vs Tabela 5 no SNLI, porque só 36,4% das explicações mudam com o filtro e o teto é baixo (§4.4).
- App. C: GPT-3 acerta 46% do SNLI (acaso 33,3%) e 50,8% do CQA; a qualidade das explicações quase não difere entre instâncias previstas certas e erradas (Tabela 19; SNLI acceptability -0,1 certo vs 0,1 errado). Logo as explicações não indicam o raciocínio do modelo.

### 6. Limitações declaradas
- §2/B.1: rótulo ouro dado ao modelo e aos anotadores é um controle; mas explicações condicionadas ao rótulo podem induzir confiança indevida (§7); os autores não aprovam uso em produção (§7, App. C).
- §7: anotadores majoritariamente de países ocidentais e anglófonos; a aceitabilidade pode variar entre populações. Modelo único (GPT-3 Davinci), 250 itens de teste, α baixo (subjetividade, §2, §4.1).
- App. A: o foco não é o prompt ótimo; hiperparâmetros foram amostrados, não ajustados. Limite de 2049 tokens restringiu nº de exemplos.
- B.1/§2.3: explicações contrafactuais (ECQA) não foram avaliadas como tal. §4.4: gap grande até o oracle, sobretudo no SNLI; fidelidade das explicações não foi o foco (§1, §7).

### 7. Inferência do agente (NÃO é do paper)
- Transfere: (a) o caso do aluno é o mesmo cenário (explicação post-hoc condicionada ao rótulo ouro); (b) a rubrica de 7 atributos (item 4) vira checklist de avaliação humana; os mais discriminantes no SNLI foram New Info, Supports Label e Acceptability, pois Grammar/Generality ficaram perto do teto (Fig. 2/Tab. 18). A falha típica do e-SNLI (explicação que só reescreve a hipótese, New Info baixo) tende a persistir em LLMs mais fortes; vale testar já na rodada 1.
- (c) Exemplos escritos com cuidado pesaram mais que exemplos do crowd (Tab. 4: 42,4 vs 30,8). Mapeia à rodada 1: variar a origem/estilo dos exemplos (curtos tipo e-SNLI vs longos e hedgeados), manter exemplos balanceados por rótulo (12/18/24 no paper) e embaralhar a ordem. Observar que o paper não testou instruções zero-shot nem saídas de 1–2 frases.
- (d) Rodada 0 (checagens automáticas em 2.000 saídas): o paper não tem checagens automáticas; argumenta que métricas automáticas correlacionam mal com humanos (§2). O que ele sugere como proxy barato: New Info (sobreposição lexical com a hipótese, repetição literal), tamanho, gramática, menção ao nome do rótulo; marcar como hipótese a validar. O resultado "só-explicação já chega a AP 30,6 vs 47,6 do modelo completo" mostra que traços de superfície capturam parte, não tudo.
- (e) Rodadas 1–2 (300 pares, depois 1.000 retidos): o paper usou 250 itens e 3 anotadores; com α entre 0,2 e 0,5, diferenças pequenas entre variantes (como 40,7 vs 49,6 da Tab. 5) são ruído-sensíveis; recomenda-se par a par com empate permitido, mesma amostra para todas as variantes e relatar α. Aceitabilidade 3/3 é critério estrito; relatar também 2/3 (App. D, F).
- (f) Rodada 3 (canário 5k, depois o restante): a ideia de amostrar e checar proporção de aceitáveis (31,5% greedy 3/3 no GPT-3) dá um parâmetro para estimar rendimento, mas o número não transfere ao Claude. Overgeneration x5 + filtro supervisionado exigiria ~5 mil rótulos binários humanos: provavelmente fora de escala; alternativas (juiz LLM, segundo gerador) não estão no paper.
- (g) App. C aponta risco concreto: o modelo racionaliza igual um rótulo que ele mesmo não prediria. No e-SNLI isso inclui possíveis rótulos ouro ruidosos; prever o rótulo sem "why?" e sinalizar discordância é uma checagem derivada do método do App. C (adaptação minha).
- Não transfere: GPT-3 Davinci não-instruct, janela de 2049 tokens, acurácia de 46% no SNLI, valores de percentual, plataforma/orçamento MTurk, qualificação de 17 candidatos, os ganhos específicos do filtro T0-3B; o paper não mede custos de API nem modelos instruction-tuned.

### 8. O que não consegui ler ou confirmar
- Temperatura, top-p, max tokens, stop sequence e semente da amostragem estocástica (§3 só diz "amostrar 4").
- Instruções literais aos anotadores e telas (Figuras 5–10 são imagens; não vistas), e as diretrizes dadas aos autores para escrever as 115 explicações (tamanho/estilo); quantos escreveram e se houve revisão.
- Discrepância interna de α: nota 10 do §4.1 dá 0,34 (CQA) e 0,39 (SNLI) para aceitabilidade; a Tabela 14 dá 0,32/0,40 (CQA) e 0,51/0,50 (SNLI). Não resolvi qual é a correta.
- Codificação numérica das escalas (-1 a 1) e seu mapeamento para binário/3 níveis só aparece sugerido pelas legendas (Tabela 15, Fig. 2); a atribuição yes=+1/no=-1 e do Amount Info é inferência.
- Resultados por rótulo (entailment/neutral/contradiction), custo em dólares do GPT-3 e tamanho médio das explicações não são informados nas seções lidas. Tabela 7 (CQA) e Tabelas 9–10 de CQA foram lidas, não resumidas.
- O repositório e a efetiva liberação dos dados (§7 diz que planeja liberar) não foram verificados.

---
