# Como definir o que é relevante: o que a literatura diz e o que falta no nosso método (27/09)

**Pergunta do Pedro (27/09):** *"como eu defino os critérios do que é relevante e do que não é? Não tem uma obra
que explora isso?"*

## Procedência

| Obra | Existe (conferido) | Quem leu |
|---|---|---|
| Kitchenham & Charters 2007, EBSE-2007-01, §6.2 | sim | **Claude, na fonte (19/09)**; notas em `docs/artigos/notas-kitchenham-charters-2007.md` |
| Petersen et al. 2008 | sim | **Pedro (nível 1)** |
| Petersen, Vakkalanka & Kuzniarz 2015, *Information and Software Technology*, doi 10.1016/j.infsof.2015.03.007 | sim (Crossref, 27/09) | **ninguém**: nível 3 |
| Peters et al. 2015, *Int. J. Evidence-Based Healthcare*, doi 10.1097/xeb.0000000000000050 | sim (Crossref, 27/09) | **ninguém**: nível 3 |
| Levac, Colquhoun & O'Brien 2010, *Implementation Science*, doi 10.1186/1748-5908-5-69 | sim (Crossref, 27/09) | **ninguém**: nível 3 |
| Saracevic 2007, *JASIST*, Parte II, doi 10.1002/asi.20682 | sim (Crossref, 27/09) | **ninguém**: nível 3 |

O que está dito abaixo sobre as quatro últimas é **conhecimento prévio do Claude, não leitura**. Serve para
escolher o que ler; não é citável até alguém ler.

## 1. Sim, existe, e o nome do assunto é "critérios de elegibilidade" (inclusão e exclusão)

Toda revisão sistemática, mapeamento ou scoping review tem esse passo. A regra que atravessa a literatura é uma
só: **o critério não se inventa, ele se deriva das perguntas de pesquisa.** Uma obra é relevante se ajuda a
responder uma das perguntas; o critério é essa ajuda escrita de forma operacional.

- **Kitchenham & Charters 2007, §6.2 (lido pelo Claude na fonte):** os critérios são decididos no protocolo, a
  partir das perguntas; são **refinados durante a busca** e **pilotados** numa amostra antes do uso. No título e no
  resumo, interpretam-se **com liberalidade** (na dúvida, lê-se mais). A confiabilidade se mede com **dois
  revisores e o Kappa de Cohen**. Com um pesquisador só, ele discute com o orientador ou faz **teste-reteste** numa
  amostra.
- **Peters et al. 2015 (guia da JBI para scoping review; não lido):** propõe montar a elegibilidade por três
  componentes, **PCC: População, Conceito, Contexto**. A scoping review é o tipo de estudo mais próximo do
  nosso screening, porque mapeia em vez de julgar evidência.
- **Levac et al. 2010 (não lido):** em scoping studies os critérios são **iterativos**, decididos no começo e
  revistos em reuniões no começo, no meio e no fim da triagem, à medida que se conhece a literatura.
- **Petersen et al. 2015 (não lido):** a atualização do guia de mapeamento que você leu (2008), com orientação
  sobre critérios de inclusão e exclusão e sobre medir a concordância entre revisores.
- **Saracevic 2007 (não lido):** a obra de referência sobre o **conceito** de relevância. A ideia central, útil
  aqui: relevância não é uma coisa só. Há a **relevância de tópico** ("a obra é sobre o assunto?") e a **relevância
  situacional** ("a obra serve para o que *eu* preciso fazer agora?"), e as duas não coincidem.

## 2. O que isso revela no nosso método

Os critérios que temos (§1.2 eixos de implantação, §1.2.1 casos a–e, §1.3 modelos, §3.4 não é survey) foram
decididos por você e são bons, mas respondem a **uma pergunta só: "a obra pertence à área?"**. É relevância de
**tópico**.

As perguntas de pesquisa do screening, porém, são outras (§1.4, decididas em 22/09):

| | Pergunta |
|---|---|
| Q1 | quais são as divisões da área e como os surveys as nomeiam e agrupam? |
| Q2 | qual é o vocabulário da área? |
| Q3 | que trabalho abriu cada divisão, e qual survey conta essa história? |
| Q4 | que conceitos os surveys assumem que o leitor já sabe? |
| Q5 | que ferramentas a área usa para cada atividade, e quais têm paper? |

**Nenhum critério foi derivado dessas cinco perguntas.** O agente 3 julgou "pertence à área?", não "ajuda a
responder Q1–Q5?". Isso explica três coisas que vimos:

1. **Por que sobram ~1.400 relevantes e não ~50.** Por tópico, centenas de surveys de compressão de LLM são
   igualmente relevantes. Pelas perguntas, o 40º survey de compressão que repete a mesma taxonomia não acrescenta
   nada a Q1 nem a Q2. É relevância de tópico sem relevância situacional.
2. **Por que a etapa C3 (de ~1.100 para ~50) não existe.** Ela é o critério situacional que falta: escolher as
   obras que, **juntas**, respondem Q1–Q5 para cada divisão.
3. **Por que as dúvidas (c) confundem.** Um survey de aplicação específica pode ser irrelevante para Q1 (não
   define divisão) e **relevante para Q5** (lista as ferramentas que a aplicação usa). "Relevante ou não" é a
   pergunta errada; a certa é "relevante **para qual pergunta**".

Os seus três objetivos (saber, saber fazer, saber ser) são a mesma ideia do lado pessoal: relevância situacional,
"serve para o que eu quero me tornar".

## 3. Proposta: relevância em dois níveis (decisão do Pedro)

| Nível | Pergunta | Quem aplica | Critério | Para que serve |
|---|---|---|---|---|
| **A — tópico** (já existe) | a obra pertence à área? | classificador + agente 3 | §1.2, §1.2.1, §1.3, §3.4 | tirar o que é de fora; é o que a F2 e o classificador já fazem |
| **B — situacional** (novo) | a quais perguntas Q1–Q5 a obra responde, e **o que ela acrescenta** ao que já temos? | agente de extração + você | por pergunta, escrito no protocolo e pilotado (exemplo abaixo) | **é a C3**: escolher o conjunto de ~50 que cobre Q1–Q5 em cada divisão |

Esboço do nível B, **a ser escrito por você** (a literatura manda o dono das perguntas escrever os critérios):
- **Q1 (divisões):** a obra propõe ou usa uma **taxonomia explícita** da área ou de uma divisão? Entra o survey com
  taxonomia; o que só lista trabalhos sem organizar não conta para Q1.
- **Q3 (história):** a obra conta a **origem** de uma divisão (primeiro trabalho, evolução)?
- **Q5 (ferramentas):** a obra **nomeia** ferramentas, bibliotecas ou sistemas usados na atividade?
- **Acréscimo:** uma obra que responde às mesmas perguntas, para a mesma divisão, que outra já escolhida só entra
  se trouxer algo novo (divisão, termo, ferramenta). É o critério de **saturação** que o método já tem para o pool,
  aplicado às obras.

**Como pilotar (Kitchenham & Charters §6.2, versão para pesquisador único):** você e a cadeia de agentes classificam
as **mesmas 30 obras**. Podem ser as de `F2/auditoria.md`, que já estão sorteadas e com abstract. O Kappa de Cohen
entre você e o agente mede se o critério está claro. Kappa baixo quer dizer critério ambíguo: reescreve-se e pilota-se
de novo. **Isso transforma a sua auditoria (D2) no teste formal de confiabilidade que a literatura pede.**

## 4. Leitura sugerida (decisão do Pedro)

Para decidir os critérios do nível B, a leitura mais direta é **Peters et al. 2015** (guia curto e prático de
elegibilidade em scoping review, com o PCC). A mais próxima do que você já leu é **Petersen et al. 2015**
(continuação do Petersen 2008). O Claude pode ler as duas antes (nível 2) e escrever notas dizendo qual responde
melhor à sua pergunta, para você ler só uma.

## 5. Decisões do Pedro

1. **Adotar relevância em dois níveis** (tópico + situacional por Q1–Q5)? Se sim, o nível B passa a ser a C3.
2. **Escrever os critérios do nível B**: você escreve a partir do esboço, ou o Claude redige uma versão para você
   corrigir?
3. **Pilotar com as 30 da auditoria**, você e o agente, com Kappa?
4. **Qual leitura**, ou o Claude lê as duas primeiro e recomenda?

## 6. As perguntas do Pedro (27/09) — rascunho do nível B

Escritas por ele, a partir da §3:

| # | Pergunta do Pedro | Liga com | Termo do professor |
|---|---|---|---|
| P1 | Me ensina o que preciso saber **sobre** a área (apresenta um mapa dela)? | Q1 divisões | divisões |
| P2 | Me ensina **o que** a área sabe (conteúdo)? | Q4 conceitos | fundamentos (as partes) |
| P3 | Mostra como a área nasceu ou o que a inspirou? | Q3 história | TEMPO |
| P4 | Me ensina **como fazer** algo da área? A maior parte sobre destilação, mas as bases que eles usam também contam (talvez bottom-up) | Q5 ferramentas | FERRAMENTAS / ATIVIDADE |
| P5 | Me ensina **como pensar** nessa área? | — (novo) | perto de "saber ser" |
| P6 | Traz base histórica ou conhecimento essencial para a área? | Q3 + §4 (seminal) | TEMPO + fundamentos |

### 6.1 O que o professor já tinha pedido e ainda não está nas seis

Das palavras dele registradas no projeto (15/09 e 22/09): *"levantando a história da área, as suas divisões,
fundamentos, **vocabulário** e etc."* e *"um especialista conhece 'o que forma' a sua área **ATUALMENTE**"*.

- **Vocabulário** não aparece sozinho em nenhuma das seis (está diluído em P1/P2). É uma das partes que ele
  nomeou, e é Q2 do método.
- **"Atualmente"** também não. Nenhuma das seis pergunta se a obra mostra a área **como ela é hoje**, e na área a
  virada para LLM (2022–23) mudou o mapa. O Pedro confirmou em 22/09: janela 2020+ para o mapa, sem janela para a
  história.

### 6.2 Sugestões do Claude (para o Pedro aceitar, mudar ou recusar)

1. **P1 e P6 se sobrepõem a P3 e P2.** Proposta de separação: **P3 = a obra conta a história** (um survey narra a
   origem); **P6 = a obra é a história** (é o trabalho que abriu a divisão, o seminal de §4). Um survey responde P3;
   Hinton 2015 responde P6. São achados de tipo diferente, por caminhos diferentes (um vem da busca, o outro da bola
   de neve pelas referências).
2. **P4 mistura área e trilha.** "Como fazer destilação" é fundamento da **trilha** (Etapa 3, o tema v3); "como
   fazer" na **área** é ferramenta e atividade (Q5), para compressão, serving, borda etc. Proposta: **P4a** (área:
   ferramentas e atividades de implantação em geral) e **P4b** (trilha: destilação e as bases que ela usa), com a
   P4b marcada à parte, para não empurrar a base da área inteira para destilação.
3. **Nova, do professor: vocabulário.** *"A obra me dá os nomes da área: definições, glossário, termos que eu não
   conhecia?"*
4. **Nova, do professor: atualidade.** *"A obra mostra o que forma a área hoje?"* (um survey de 2020 pode
   responder P1 e falhar aqui).
5. **Nova, sua própria meta de 15/09: arquitetura.** Você disse que quer *"conhecimento profundo sobre a arquitetura
   de encoders, decoders e encoder-decoders"*. *"A obra me ensina algo sobre como a família de arquitetura muda o
   problema de implantação?"*
6. **Nova e decisiva para chegar a ~50: acréscimo.** As outras perguntas avaliam **uma obra sozinha**; esta avalia
   **o conjunto**: *"o que esta obra traz que as já escolhidas não trazem?"* Sem ela, toda obra boa entra, e voltamos
   às ~1.100. Com ela, o 40º survey de compressão com a mesma taxonomia não entra. É a regra de saturação do método,
   aplicada às obras.

### 6.3 Quem consegue responder cada pergunta

Critério que não dá para aplicar não serve (Kitchenham & Charters: os critérios são **pilotados**). Estimativa, a
confirmar no piloto:

| Pergunta | Pelo abstract (agente) | Precisa do texto (introdução, sumário) | Só você |
|---|---|---|---|
| P1 mapa, P3 conta a história, vocabulário, atualidade | em geral sim | às vezes | — |
| P2 conteúdo, P4a/P4b como fazer, arquitetura | em parte | sim (sumário, seções) | — |
| P6 é seminal | não: vem da contagem de citações entre os surveys (§4) | — | — |
| **P5 como pensar** | não | mal | **sim**: é julgamento de quem lê |
| Acréscimo | não por obra: é uma regra sobre o conjunto, aplicada depois | — | confirma |

**Consequência:** P5 não entra na triagem por agente. Fica para as suas notas de leitura, junto com o saber ser
(decisão de 26/09).

### 6.4 Decisões do Pedro

1. Separar **P3 (conta) × P6 (é)**?
2. Separar **P4a (área) × P4b (trilha: destilação)**?
3. Acrescentar **vocabulário** e **atualidade** (do professor), **arquitetura** (sua meta) e **acréscimo** (conjunto)?
4. **P5 fora da triagem**, nas suas notas de leitura?
5. Depois disso: escrever para cada pergunta **o que conta como "sim"** (uma linha cada), e pilotar nas 30 obras
   da auditoria.

## 7. As obras finais vão trazer os frameworks da Etapa 2? (pergunta do Pedro, 27/09)

**Medição (nível 3, abstracts da F2):** das 55 relevantes, **5 nomeiam uma ferramenta no abstract** (TensorFlow
Lite, vLLM, SGLang, TensorRT-LLM, OpenVINO, GGUF); somando as dúvidas, 8 de 212. É um **piso**: surveys costumam
listar ferramentas no corpo do texto, em tabelas de comparação, não no resumo. No diagnóstico do classificador
(R5), a subárea `ferramentas` tinha **0 relevantes rotuladas**. E em 22/09 (⟨rev-29⟩) já se tinha medido que termo
preciso de ferramenta devolve de 0 a 3 surveys: **a área documenta as ferramentas, não as pesquisa**.

**Leitura:** as obras finais devem trazer o **índice** dos frameworks (nomes, para que atividade servem, às vezes
uma comparação), mas **não os frameworks em si**, que vivem em paper de sistema, documentação e repositório. O
método já prevê o caminho: ferramentas nomeadas pelos surveys viram item de extração (§6); a filha `ferramentas`
busca paper de sistema sem `filtro-tipo`; registros de ecossistema (HF, ONNX, MLPerf) entram como descoberta nível
3; e o eixo de atividade (§3.3) é declarado como "semente da Etapa 2".

**Ambiguidade a resolver com o professor:** "frameworks de apoio" pode ser **software** (vLLM, TensorRT, ONNX
Runtime, llama.cpp) ou **conceitual** (modos estruturados de decidir e trabalhar na área, por exemplo como escolher
entre quantizar, podar ou destilar para um dado hardware). Os dois pedem buscas diferentes, e o segundo fica perto
da P5 ("como pensar"). A palavra está entre aspas na fala dele, o que sugere sentido próprio.

**Respostas do Pedro (27/09) à §6.4:** decisões 1 a 4 **aprovadas** (P3 conta × P6 é; P4a área × P4b trilha;
acrescentar vocabulário, atualidade, arquitetura e acréscimo; P5 fora da triagem, nas notas de leitura). "Adiciona as
perguntas do professor na lista" (vocabulário e atualidade). Próximo passo pedido: construir o método de baixo para
cima, a partir destes critérios, até voltar à regressão: `docs/screening/fase1/2026-09-27-metodo-bottom-up.md`.

**Atualização de procedência (27/09):** Levac 2010 (inteiro), a seção de manifestações de Saracevic 2007 e as §10.2.3,
10.2.4 e 10.2.7 do Manual da JBI (sucessor aberto de Peters 2015) foram **lidos pelo Claude (nível 2)**. Petersen 2015
segue fechado e não lido. Notas e implicações: `docs/artigos/notas-relevancia-literatura.md`. O que a §1 atribuía a
Peters, Levac e Saracevic "por conhecimento prévio" foi confirmado na leitura. O PCC está no Manual, e Levac e Saracevic
dizem o que a §1 dizia. Achado novo da leitura: a **abordagem liberal acelerada** da JBI (1 inclui, 2 excluem) e o
critério de **pertinência** (o leitor consegue entender e usar), de Soergel via Saracevic.

## 8. Levando as quatro camadas até as consequências (27/09, pedido do Pedro: "raciocinar mais")

### 8.1 Tópico ("fraca", vai com os sistemas): o corte por tópico já foi feito

**Teste feito (nível 3; `docs/screening/fase1/C1-diagnostico/resultados-alvo-topico.json`):** o "relevante" do agente 3
misturava três coisas: tópico; tipo de fonte ("não é survey" é tipo, não tópico); e acréscimo, porque a regra (c) só
admite aplicação específica "se nenhum survey geral cobrir a divisão", o que depende do que já foi escolhido. Refazendo
o alvo como **tópico puro** (relevante + dúvida (c) + primário ou sistema da área = 328 das 797):

| Alvo | Prevalência ponderada | Precisão média (LR) | Acaso | Acha nos primeiros 25% |
|---|---|---|---|---|
| Relevante (P1, como antes) | ~15% | 0,50 | 0,15 | 72% |
| **Tópico puro (T)** | **~52%** | **0,81** | 0,52 | 44% (teto possível ~48%) |

**Consequência:** cerca de **metade das 11,5 mil obras, ~6 mil, é da área por tópico.** As camadas A e B e a F1 já
fizeram o corte de tópico. O que falta para chegar a ~50 **não é tópico**. A F2 e o K95 de 67% foram a tentativa de
fazer um corte situacional e cognitivo com uma ferramenta de tópico. O classificador acerta o tópico (0,81 × 0,52);
o que ele errava era o alvo.

### 8.2 Situacional (as perguntas): cada pergunta tem a sua população de fontes

As perguntas não moram todas em surveys:

| Pergunta | Tipo de fonte que responde |
|---|---|
| P1 mapa, P3 conta a história, V vocabulário, A atualidade | survey |
| P4a como fazer na área | paper de sistema, documentação, repositório (⟨rev-29⟩) |
| P6 é a história (seminal) | primário muito citado pelos surveys (§4), achado por referência, não por busca |
| P2 conteúdo, R arquitetura, Q4 conceitos assumidos | survey **e** obras de conceito |

**Consequências:**
1. **"Não é survey" não é "fora": é outra rota.** O §3.4 já dizia isso (primário volta como seminal; sistema vai para
   ferramentas), mas na prática os agentes colapsaram tudo em "fora".
2. **Os "genéricos" que a poda de especificidade tirou da lista de destilação** (BERT, Attention is All You Need,
   GPT-3) são fracos para o tópico "destilação" e **fortes para Q4 e R**: são os conceitos que todo survey assume. A poda
   estava certa para o ranking de tópico, mas eles devem ir para uma **lista de conceitos pré-requisito**, não para o lixo.
3. **É aqui que a regressão volta, com o alvo certo.** Em vez de prever relevância de tópico, que já está resolvida, um
   classificador pode prever **respostas situacionais que aparecem na estrutura do texto**: "tem taxonomia?" (P1), "é
   paper de sistema?" (P4a), "cobre a era LLM?" (A). Seria um classificador de vários rótulos, treinado com as respostas
   de nível B do piloto e das rodadas.

### 8.3 Cognitiva (acréscimo): é seleção de conjunto, não rótulo de obra

- O acréscimo depende **da ordem** e **do que já foi escolhido**. Não se aprende obra a obra; nenhum classificador o
  entrega.
- É um problema de **cobertura**: encher as células (pergunta × divisão) com o menor número de obras, penalizando a
  redundância. Na recuperação de informação, o equilíbrio entre relevância e novidade tem nome, **máxima relevância
  marginal** (Carbonell & Goldstein 1998, SIGIR; existência conferida, não lido).
- **A regra (c) sai do nível A** e vira caso de acréscimo: aplicação específica entra se preencher célula que nenhum
  survey geral preencheu. As 157 dúvidas deixam de ser dúvida: são candidatas de cobertura, esperando o mapa.
- **É o "ranking" da próxima etapa da pilha.**

### 8.4 Pertinência: depende de você, e muda enquanto você lê

- Pertinência é a relação com o **seu estado de conhecimento**, e Saracevic insiste que relevância é **dinâmica**. O que
  hoje é ilegível fica pertinente depois de três leituras.
- **Não filtra: ordena no tempo.** É um currículo. O insumo é a Q4 ("que conceitos os surveys assumem que o leitor já
  sabe?"): um grafo de pré-requisitos. A lista de destilação em ordem histórica já era, sem esse nome, uma ordem de
  pertinência.
- **Consequência mais funda:** como a novidade (8.3) se mede contra o que você já sabe, e o que você sabe muda ao ler,
  **as ~50 não são uma lista fixa, são uma trajetória**. Escolhe-se um lote, você lê, e a novidade do resto é
  recalculada. Isso fecha com o "loop por voltas" que o método já tem (⟨rev-31⟩).

### 8.5 Quem julga cada camada

| Camada | Quem pode julgar | Por quê |
|---|---|---|
| Tópico | máquina (classificador, agente 1) | "fraca": vai com os sistemas; medido, AP 0,81 |
| Situacional | agente com o texto (introdução, sumário), pilotado contra você | depende do conteúdo, não só do assunto |
| Cognitiva | algoritmo de cobertura + você | é sobre o conjunto e sobre o que você já leu |
| Pertinência | **só você** (o agente dá, no máximo, uma aproximação: tutorial, introdutório) | é o seu estado de conhecimento |
| Afetiva (P5, saber ser) | só você | decisão de 26–27/09 |

### 8.6 Decisões do Pedro

1. Aceitar a arquitetura: **tópico feito**; **situacional por rota de fonte**; **cognitiva = seleção por cobertura**;
   **pertinência = ordem dinâmica de leitura**?
2. "Não é survey" vira **rota** (§3.4 aplicado de verdade), e a regra **(c) sai do nível A** para a seleção?
3. A regressão passa a prever **respostas situacionais** (vários rótulos) em vez de relevância de tópico?
4. Os "genéricos" (Attention, BERT…) viram a **lista de conceitos pré-requisito** (Q4, R)?

### 7.1 Definição de framework trazida pelo Pedro (30/09)

Texto que o Pedro colou (origem a confirmar: provavelmente material do professor): framework é *"uma estrutura
flexível que oferece um conjunto de diretrizes, práticas e ferramentas pré-definidas para organizar e orientar o
desenvolvimento de um projeto"*; funciona como *"esqueleto"* que estabelece *"a base, a arquitetura e as
funcionalidades essenciais"*, para a equipe se concentrar no que é específico do projeto *"em vez de reinventarem a
roda"*; promove consistência, reduz erros, aumenta eficiência e escalabilidade, facilita manutenção.

**Teste derivado (Claude), três condições:** (1) oferece diretrizes, práticas **e** ferramentas prontas; (2) é um
**esqueleto** sobre o qual se constrói um projeto (base, arquitetura, funções essenciais); (3) o usuário escreve só
a parte específica. **Resolve a ambiguidade do §7 para o lado "estrutura de desenvolvimento":** software como PyTorch,
vLLM, TensorRT-LLM, TVM e TFLite Micro passa; **roofline, taxonomias e pipelines de método (Deep Compression) não
passam**: são modelos de análise ou métodos, não esqueletos de projeto.

**Correção do Pedro (30/09): "na verdade é os dois".** Framework vale nos dois sentidos, e o teste acima era estreito
demais. A própria definição fala em "diretrizes, práticas **e** ferramentas":
- **framework de software:** o esqueleto de código (PyTorch, vLLM, TVM, TFLite Micro…);
- **framework conceitual ou metodológico:** diretrizes e práticas que **orientam as decisões de um projeto**. Teste:
  ele **prescreve** passos, critérios ou escolhas para aplicar num projeto? O roofline passa (diagnostica o gargalo e
  aponta a otimização); o pipeline do Deep Compression passa (uma sequência de práticas); o arcabouço de métricas de
  Sze passa (como comparar hardware); o text-to-text do T5 passa (como formular qualquer tarefa). **Uma taxonomia só
  passa se disser quando usar cada ramo**; se só classifica, é mapa, não framework.
