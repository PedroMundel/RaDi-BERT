# Desenho do método de leitura por agentes (em construção, 23/09/2026)

**Status: desenho conjunto, decisão por decisão. Nada decidido além do marcado.** Proposta do Pedro
(23/09): *"alguns agentes pra realizar uma leitura resumida de alguns artigos de cada grupo pra
podermos filtrar ainda mais esse número, seria uma simulação do passo C, mas com agentes"*, com um
método *"muito bom"* — candidatos citados por ele: o keywording de Petersen e *"uma análise de árvore,
colocando os artigos raízes até as folhas"*.

**Entrada:** 14.901 obras da camada C. Já decidido: golden ticket (<= 20 obras por técnica) e
penúltima filtragem (21–50), com o bilhete mais favorável valendo (§11.1 ⟨rev-36⟩).

## Mapa das decisões

| # | decisão | estado |
|---|---|---|
| **M1** | **mecanismo de filtragem** — como se decide o que sai, e em que ordem | **DECIDIDA (Pedro, 23/09): b -> c -> a** (árvore de citação, depois amostragem com regra do três, depois keywording) |
| M2 | esqueleto das fases (o que é "penúltima" e "última") | **DECIDIDA (Pedro, 23/09)** — F1 árvore · F2 amostragem por tamanho de grupo · F3 keywording (penúltima) · F4 leitura completa + decisão do Pedro (última) |
| M3 | protocolo do agente: o que lê, o que devolve, que modelo | **DECIDIDA (Pedro, 23/09): proposta aceita** |
| M4 | validação: como saber que o agente acerta (gabarito, dupla leitura, amostra conferida pelo Pedro) | **DECIDIDA (Pedro, 23/09): proposta aceita** |
| M5 | conflito com §7 do método: hoje o agente **não julga relevância** | **DECIDIDA (Pedro, 23/09): três agentes em cadeia**, um por tarefa — ver seção M5 |
| **M6** | **o que o agente faz quando não consegue acessar a fonte** (a lição real do Agrawal) | **DECIDIDA (Pedro, 23/09): proposta aceita** |

## M1 — candidatos ao mecanismo de filtragem

| | mecanismo | o que faz | evidência | custo | limite |
|---|---|---|---|---|---|
| **a** | **Keywording** (Petersen et al. 2008) | agentes leem abstracts de uma amostra e anotam palavras-chave/conceitos; das palavras nasce um esquema de categorias; cada obra é classificada no esquema; categorias fora da área saem inteiras | é o procedimento do próprio mapping study que você leu | médio (agentes leem a amostra + classificam o resto) | o esquema nasce do que a amostra viu; categoria rara pode não aparecer |
| **b** | **Árvore de citação** — análise de caminho principal (Hummon & Doreian 1989, *Social Networks*) | monta quem-cita-quem **dentro** das 14.901 pelas referências do Semantic Scholar; raízes = obras muito citadas pelo conjunto; folhas = obras recentes que citam as raízes; obra **sem ligação** com o componente onde estão os cajuzeiros conhecidos é candidata a lixo | método clássico de análise de redes de citação, usado para traçar a espinha de uma área | baixo em leitura (zero), médio em API (~15 mil consultas de referências) | obra recente ainda sem citação fica solta e pareceria lixo; precisa de exceção por ano |
| **c** | **Amostragem por grupo com regra do três** (Hanley & Lippman-Hand 1983, *JAMA*) | agentes leem uma amostra aleatória de cada grupo/técnica; se nenhuma de *n* lidas é relevante, a proporção de relevantes no grupo é, com 95% de confiança, menor que 3/*n* (ex.: 0 de 30 -> < 10%) — o grupo sai ou desce de prioridade | resultado estatístico simples e consagrado para "zero ocorrências na amostra" | baixo a médio (30–60 abstracts por grupo) | dá um teto, não zero: grupo que sai pode ter alguns cajuzeiros — a bola de neve e o golden ticket são a rede |

Os três não se excluem. Uma composição natural: **b** primeiro (mecânico, sem leitura, tira o que não
se liga à área) -> **c** para decidir grupos inteiros com número -> **a** sobre o que sobrar, para dar
nome às categorias (que é o começo do mapa).

*Procedência:* os três artigos citados foram verificados quanto à existência (Crossref, 23/09) —
nível 3; Petersen 2008 é o único lido por você.

## M5 — DECIDIDA (Pedro, 23/09): três agentes em cadeia, uma tarefa cada

Nas palavras dele: *"3 agentes, o primeiro que atua na camada iii, apagando o que é óbvio. Do que
sobrar, o segundo agente age no ii, devolvendo as frases transcritas, que então passa pro 3º agente
que executa o i, devolvendo 'relevante / fora / dúvida', junto com a frase do abstract transcrita.
Separando assim evita do agente se perder com 3 tarefas distintas muito importantes."*

| agente | tarefa | entra | sai |
|---|---|---|---|
| **1 — triagem do óbvio** (iii) | eliminar só o que é **claramente** de fora | título + abstract | "claramente fora" + motivo, ou "passa" |
| **2 — extração** (ii) | transcrever, sem julgar, as frases que dizem do que a obra trata | título + abstract das que passaram | frases transcritas, verbatim |
| **3 — julgamento** (i) | aplicar §1.2 / §1.2.1 / §3.4 | as frases do agente 2 | relevante / fora / dúvida + frase transcrita + letra da regra |

Compatibilidade com §7: o **registro** continua só com extração (agente 2); os vereditos dos agentes 1 e
3 vivem fora do registro, como a proposta de agrupamento (⟨rev-32⟩), e **ordenam, não apagam**.

## M6 — sem acesso (a lição real do Agrawal, contada pelo Pedro em 23/09)

*"O problema do Agrawal foi que o agente não conseguiu acessar o paper, pediu pra você me avisar,
você me pediu pra olhar e eu demorei muito tempo pra olhar, só quando você cansou de pedir."*
(Correção do registro: o CLAUDE.md dizia que "a triagem não pegou o mecanismo" — a causa foi **acesso**,
e a falha foi de **processo**: pendência solta, sem prazo, dependente de alguém lembrar.)

**DECIDIDO (Pedro, 23/09: "sim"):**
1. **Estado próprio `sem acesso`** — não é "dúvida" nem "fora". Nenhum agente decide sobre obra sem
   acesso, e nenhuma obra `sem acesso` é eliminada (ordena, não apaga).
2. **Rotas automáticas antes de declarar**: Semantic Scholar -> arXiv (id) -> OpenAlex (DOI) -> PDF de
   acesso aberto. Cada tentativa é anotada. Só depois de todas falharem vira `sem acesso`.
3. **Não interrompe o fluxo**: o agente segue com as outras obras; nada fica esperando.
4. **Não depende de lembrar**: no fim de cada volta, **uma lista única** `…-sem-acesso.md` com as obras,
   as rotas tentadas e o que falta; e o número de `sem acesso` aparece **no relato de funil da volta**,
   ao lado dos outros estágios — se ele não cair, fica visível a cada volta.
5. **Prioridade**: `sem acesso` que tenha golden ticket, ou termo núcleo no título, vai para o topo da lista.

**Entrada do agente 3 — DECIDIDO (Pedro, 23/09, meio-termo):** ele julga **só com as frases do agente 2**;
se as frases não bastarem, devolve **"dúvida"** e a obra sobe um degrau na escada de §6.1 (introdução).

## M2 — esqueleto das fases (PROPOSTA)

| fase | o que acontece | quem | entra | sai |
|---|---|---|---|---|
| **F1** — árvore (b) | rede de citação dentro do conjunto; obra **sem ligação** com o componente dos cajuzeiros conhecidos desce para o fim da fila | script, sem leitura | 14.901 (menos golden e penúltima) | ligadas + soltas recentes (2025–26, exceção: ainda sem tempo de ser citadas) |
| **F2** — amostragem (c) | em cada grupo/técnica, 30 obras sorteadas passam pela cadeia 1 -> 2 -> 3; grupo com **0 relevantes em 30** desce inteiro (regra do três: < 10% de relevantes, 95% de confiança) | cadeia de agentes | o que sobrou da F1, por grupo | grupos que seguem |
| **F3** — **penúltima filtragem** | **todas** as obras restantes passam pela cadeia 1 -> 2 -> 3 | cadeia de agentes | grupos que seguiram + **bilhete 21–50** | relevantes + dúvidas (dúvida sobe a escada) |
| **F4** — **última fase** | keywording (a) sobre os relevantes: nomes de categoria, que são o começo do mapa; e **a sua decisão** (Fase 3 do método) | agentes + Pedro | saída da F3 + **golden ticket** | lista para registro |

`sem acesso` (M6) atravessa todas: nunca é eliminada, vai para a lista da volta.

## M3 — protocolo do agente (PROPOSTA)

| | modelo | por quê | lote |
|---|---|---|---|
| agente 1 (óbvio) | Haiku | tarefa mecânica e de baixo risco (só elimina o gritante) | ~40 obras por chamada |
| agente 2 (extração) | Haiku | transcrever frases, sem julgar | ~20 por chamada |
| agente 3 (julgamento) | Sonnet | aplicar regras do método exige entendimento | ~20 por chamada |

Saída de todos em formato fixo (tabela JSON por obra: id, decisão, frase transcrita, regra, estado de
acesso), gravada em arquivo por lote — nada fica só na conversa. Roteiro de cada agente = um texto fixo,
versionado, com as regras do método copiadas (§1.2, §1.2.1, §3.4) e exemplos do gabarito de ajuste.

## M4 — validação (PROPOSTA)

1. **Calibração antes de rodar:** a cadeia roda sobre um conjunto conhecido — as 28 obras de **ajuste**
   do gabarito (relevantes) + 30 obras sorteadas das excluídas na camada A (lixo conhecido). Metas:
   agente 1 **não elimina nenhuma** das 28; agente 3 marca relevante/dúvida em **>= 90%** das 28.
2. **Dupla leitura:** 10% das obras de cada lote passam por uma segunda cadeia independente; a
   concordância entra no relatório.
3. **Sua auditoria:** 30 vereditos sorteados por volta, com a frase transcrita ao lado — você confere.
4. **Teste final:** a metade de **teste** do gabarito (29) só é usada no fim, para medir a perda do
   processo inteiro.

**Decisões do Pedro (23/09) sobre M2/M3/M4:** F1 ok · **F3 e F4 trocam de lugar** — F3 (penúltima) =
keywording (a) sobre o que sobrar, com eliminação de categorias-lixo em bloco; F4 (última) = leitura
completa pela cadeia 1 -> 2 -> 3 + decisão do Pedro, e o agente 3 também atribui a categoria. Bilhete
21–50 entra no keywording; golden ticket entra na F4. · F3 antiga (leitura completa) "depende de quantas
obras sobrarem" · **M3 ok · M4 ok**. · **F2 em aberto:** a regra do três limita a *proporção* (< ~10%
com 0/30, qualquer tamanho de população), não o *número* de cajuzeiros escondidos, que cresce com o
grupo. Opções: (a) 30 fixo, (b) amostra proporcional com teto, (c) F2 só ordena. Pedro: *"leia o paper
pra gente decidir"* — leitura de Hanley & Lippman-Hand 1983 em andamento.

## F2 depois da leitura de Hanley & Lippman-Hand 1983 (Claude, nível 2 — notas em `docs/artigos/notas-hanley-lippman-hand-1983.md`)

**Resposta à pergunta do Pedro** ("são 30 obras independente do tamanho da população?"): o artigo
**não fala de tamanho de população** — o modelo é uma taxa de longo prazo (binomial). O *n* se escolhe
pela **proporção que se quer excluir**: 0/30 exclui > 10%, 0/50 > 6%, 0/100 > 3% (Tabela 2). Num grupo
finito, o limite continua valendo (é conservador), mas o número de cajuzeiros que pode sobrar é a
proporção x o tamanho do grupo. **Precedente de triagem no próprio artigo:** a "regra das 14 falhas
consecutivas" para descartar agentes de câncer.

**Opções revisadas para a F2:**

| | regra | exclui grupo com mais de | leituras por grupo | no grupo de 1.000, podem sobrar até |
|---|---|---|---|---|
| a | 0/30 elimina | 10% relevantes | 30 | ~100 |
| b | 0/100 elimina | 3% | 100 | ~30 |
| c | 0/30 só ordena (vai para o fim da fila) | — | 30 | nenhum sai |
| d | **duas etapas:** 0/30 manda para o fim da fila; eliminar só com 0/100 | 3% (para eliminar) | 30 ou 100 | ~30, só nos grupos que chegam a 0/100 |

**F2 — DECIDIDA (Pedro, 23/09), amostra por tamanho do grupo:**

| tamanho do grupo (depois da F1) | amostra | se 0 relevantes, exclui (95%) grupo com mais de |
|---|---|---|
| >= 1.000 | 0 em **50** | 6% relevantes |
| 800 a 999 | 0 em **40** | 7,5% |
| 100 a 799 (confirmado pelo Pedro) | 0 em **30** | 10% |
| 50 a 99 | **proporcional** — leitura do Claude, a confirmar: 30% do grupo (a proporção de 30 em 100); ex.: 50 -> 15, 0/15 exclui > 20% | ~3/n |
| < 50 | **ler tudo** (sem amostragem) | — |

Base: Tabela 2 de Hanley & Lippman-Hand 1983 (lida pelo Claude, nível 2). Grupo com 0 relevantes na
amostra desce inteiro — ordena, não apaga: fica no bruto com o motivo e volta se a bola de neve trouxer
algum membro dele.

**Plano fechado em 23/09.** Próximo passo: `/checkpoint` e execução da F1 (árvore de citação) em sessão nova.
