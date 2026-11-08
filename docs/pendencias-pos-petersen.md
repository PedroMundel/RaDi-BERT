# Pendências para depois da leitura do Petersen 2008

**Aberto em 22/09/2026.** Tudo que surgiu enquanto o Pedro lia o Petersen (nível 1, em andamento) e
ficou para decidir depois. **Nada aqui está decidido.** Cada item termina com a pergunta que o Pedro
responde; a resposta vai para o método (`docs/screening/metodo-screening-etapa1.md`) ou para o pool
(`docs/screening/pool-termos-etapa1.md`), e o item sai desta lista com a data.

Regra de trabalho registrada em 22/09: decisão que falta é **perguntada** ao Pedro — não preenchida e
rotulada como do Claude.

---

## A. Perguntas de pesquisa (RQs) — **FECHADO em 22/09**

- ~~**A1.**~~ **DECIDIDO:** as cinco perguntas entram no método, em **§1.4 nova** ⟨rev-28⟩, sob a
  pergunta-guarda-chuva do professor (*o que forma a minha área atualmente?*).
- ~~**A3.**~~ **DECIDIDO:** **não** separar RQ de mapa de RQ de área. Em vez disso, declarado o que
  todas têm em comum: são perguntas de **onde encontrar**, nenhuma é de **o que é verdade** — e essa
  é a linha que separa o screening da RSL (liga ao bloco M).
- ~~**A2.**~~ **DECIDIDO (Pedro, 22/09): criar o grupo `ferramentas` no pool** — emenda 2 do v0.
  6 termos com retorno medido; `MLOps` e `model deployment` foram para `uso?` (testar §1.2);
  `machine learning systems`, `benchmarking`, `toolkit` e `inference framework` ficaram fora por
  ruído medido. **Achado:** termo preciso de ferramenta devolve 0–3 — a área **documenta** suas
  ferramentas, não as pesquisa; o pilar ferramentas depende de §3 (documentação) e §4.1 (ementas)
  tanto quanto da busca. Expectativa baixa declarada no próprio pool.
- ~~**A5.**~~ **DECIDIDO (Pedro, 22/09): pesquisar ferramenta fora de survey.** Três rotas escritas:
  (1) filha `ferramentas` **sem `filtro-tipo`**, para achar paper de sistema (pool §2, emenda 3);
  (2) **ferramentas nomeadas pela fonte** viram item de extração (método §6, §7) — custo zero;
  (3) **registros de ecossistema** (HF, ONNX, **MLPerf Inference**) como descoberta **nível 3
  permanente, não citável** (§3) — o MLPerf é a fonte mais direta para o eixo de atividade.
- **A4 — FECHADO (Pedro, 22/09): sim** — método §2.1, pool §3 ⟨rev-35⟩. Pergunta original: esta emenda não se encaixa em nenhum gatilho existente — não veio de
  survey, nem de ruído no bruto, nem de lacuna no plot A. Veio do **confronto do pool com as
  perguntas de §1.4**. Ampliar a direção (b) da regra de revisão por retorno de "lacuna vista no plot
  A" para "lacuna de cobertura — plot A **ou** confronto com as perguntas de §1.4"?

## B. Definição de fundamentos do professor — **FECHADO em 22/09**

- ~~**B1.**~~ **DECIDIDO: adotar os termos dele.** *Fundamentos* passa a ser **o produto** (o que forma
  a área atualmente), com divisões, vocabulário, conceitos, ferramentas e história como partes/modo de
  construção. **Consequência:** o antigo "fundamentos" de §1.1/§6 (self-attention, KV cache, máscara
  causal) foi renomeado para **conceitos** em todo o método, e o valor `fundamentos` da coluna *pilar*
  virou `conceitos`. Motivo registrado: com a palavra antiga, a pergunta do professor "quais são os
  fundamentos da sua área?" seria respondida com a lista estreita. Método §1.4 ⟨rev-28⟩.
- ~~**B2.**~~ **DECIDIDO: opção (a)** — *"infelizmente, (a), fala dele é lei"*. Criado o **eixo de
  atividade** (§3.3 nova) + coluna `atividade` no §8. Bottom-up como as divisões: atividade entra
  quando uma fonte a **declara** (página de visão geral da ferramenta, ementa, seção de prática de
  survey); duas fontes consolidam. **Limite declarado no próprio método:** as fontes de atividade são
  mais fracas que as de divisão, e o mapeamento completo atividade x ferramenta é trabalho da Etapa 2
  — pilar fino na Etapa 1 é resultado esperado, não falha.
- ~~**B3.**~~ **DECIDIDO:** os fundamentos da **trilha** (tema v3) ficam fora da Etapa 1 e do mapa —
  limite de escopo declarado em §1.4.
- ~~**B4.**~~ **CONFIRMADO:** "atualmente" = janela 2020+ para mapa e divisões; história sem janela.

## C. Restrição por tipo de fonte × Petersen ("broad overview", sem restringir por tipo de estudo)

- **C1 — FECHADO (Pedro, 22/09): declarar.** Método §3 ⟨rev-35⟩. Pergunta original: O `filtro-tipo` (survey/review/overview/taxonomy) em toda string é uma restrição que o
  Petersen evita de propósito. Efeito: divisão sem survey ainda é invisível. Aceita por custo (um
  aluno, semanas) — **declarar por escrito** no §3 ou no método-do-método, com o trecho do Petersen
  como contraponto?
- ~~**C2.**~~ **RESOLVIDO em 22/09** (ver bloco E): a cláusula anti-viés da regra de revisão por
  retorno obriga a rodar a filha de todo termo movido — a filha `edge` é obrigatória.

## D. Exclusão por menção só na abertura do resumo (técnica do Petersen)

Protótipo em 22/09 sobre os 89 resumos do arXiv (exec. 2): dos 7 com termo só nas 2 primeiras frases,
**6 estão dentro da área** e 1 fora. Mecanismo do nosso ruído é o inverso (survey de outro assunto
com uma seção de eficiência → termo no *meio* do resumo). E o bulk do S2 não devolve resumo.
- **D1 — FECHADO (Pedro, 22/09): não adotar; protótipo registrado no método-do-método §2.** Pergunta original: Confirmar: **não adotar** a técnica. Registrar o protótipo como evidência no método-do-método?

## E. O loop keywording → busca — **FECHADO em 22/09**

- ~~**E1.**~~ **DECIDIDO:** criada a regra **"revisão por evidência de retorno"** (pool §3; método
  §2.1 ⟨rev-25⟩) — a espelho da aposentadoria: havia regra para o termo que devolve *nada*, não para
  o que devolve *demais e errado*. **Cláusula anti-viés:** o termo não é apagado nem só removido —
  é **obrigado a rodar numa string-filha**, com o bruto salvo. Vocabulário fechado junto: **versão**
  = rodada de saturação; **emenda** = ajuste por retorno dentro da versão. A emenda 1 (21/09) fica
  autorizada retroativamente, marcada como tal no pool.
- ~~**E2.**~~ **DECIDIDO:** checkpoint do nome da área antes de consolidar (método §2.3 ⟨rev-25⟩),
  **até saturar, mas só antes do v1** — palavras do Pedro: *"até saturar, mas só nos primeiros loops,
  enquanto não temos a base"*. Com o v1 no lugar, nome de área novo segue o loop normal (v2+).
- ~~**K6.**~~ **DECIDIDO:** uma regra só, **duas direções** — (a) ruído, decidido sobre o bruto;
  (b) lacuna no plot A, decidida sobre o registro.
- ~~**C2.**~~ **RESOLVIDO por consequência:** a filha `edge` **não é opcional** — a cláusula
  anti-viés de (a) obriga a rodar a filha de todo termo movido.
- ~~**E3.**~~ **DECIDIDO (Pedro, 22/09): gate de relevância + teto.** Nome de área candidato é
  **rodado sozinho antes de ganhar volta**; o gate é a ordem de aplicação de regras já existentes
  (retorno zero → aposenta; majoritariamente fora da área → filha; relevante → ganha a volta).
  **Parada:** mais da metade dos nomes da rodada já no pool. **Teto: 8 voltas**, ampliável por
  decisão dele com motivo. Voltas viram métrica de gate (§13). Método §2.3 ⟨rev-26⟩.
  **Limite registrado:** o gate mede o vocabulário dos surveys lidos, não o da área — depende da
  diversidade do conjunto inicial, o que reforça **H1** como pendência a resolver **antes da Fase 2**.

## F. Funil por voltas numeradas (proposta do Pedro, 22/09)

*"loop 1 — 3000 papers → filtragem por keywords → resumo → recomendação de grupos → decisão minha →
loop 2 — 1500 → ... até número viável para leitura."*
Compatível com o pipeline de §10 (largo → fino → filtragem → leitura); o Pedro não lê nas voltas,
decide sobre tabela. Três pontos precisam de regra:
- ~~**F1.**~~ **DECIDIDO (Pedro, 22/09): sim, com quatro salvaguardas.** *Por que o §7 proíbe
  interpretação no registro:* a cicatriz do **Agrawal** — estava em nível 3 como "incógnita", a
  triagem não pegou o mecanismo, e o mecanismo era o do tema (`## Rejected` do CLAUDE.md).
  Princípio: o registro é aquilo sobre o que o Pedro decide. O agrupamento não é entrada de registro,
  mas herda o risco se decidir o que cai — daí: (1) ordena, não apaga; (2) o grupo mostra sempre os
  membros, título e identificador; (3) artefato do Claude, datado, fora do registro, em
  `screening/fase1/<data>-volta-N-agrupamento.md`; (4) agrupamento não é divisão e morre na volta
  seguinte. Método §11.1 ⟨rev-32⟩.
- ~~**F2.**~~ **DECIDIDO (Pedro, 22/09): sim** — o filtro **ordena, não apaga**. Descartado fica no
  bruto com motivo e a volta em que caiu, e volta a ser candidato se uma rodada abrir grupo novo.
  Método §11.1 ⟨rev-31⟩.
- **F3. PARCIAL (Pedro, 22/09):** alvo provisório **~50 documentos no total**, e a parada coexiste com
  a saturação (para quando N cabe no orçamento **ou** a volta não abre grupo novo). **Não fechado:**
  falta separar N de **leitura resumida** (extração nível 3) de N de **leitura integral** (nível 2->1).
  Palavras dele: *"ainda não decidi, tenho que ver (ver, gráficos, tabelas, etc) antes de decidir"* —
  **a decisão é sobre dados das primeiras voltas, não agora.** Registrado em §11.1.
- ~~**F4.**~~ **DECIDIDO (Pedro, 22/09): opção (b)** — população = surveys da área **sem piso de
  citação**; as palavras de tipo (survey|review|overview|taxonomy) **ficam**. O piso sai da busca e
  vira critério de registro (§3.2, valor 60). Método §11 e §3.2 ⟨rev-30⟩; pool, emenda 4.
  **Medição de 22/09 (S2, string limpa, 2020+, CS):** com piso 103 · **sem piso 863** · sem palavras
  de tipo 16.821 · papers da área com >= 60 citações 793.
  **Correcão:** os 41.412 da execução 1 não eram esta população — string suja, antes da filha `edge`.
  **Resolve G3 em parte:** o número passa a ser 60 em um lugar só.
- **O loop por voltas continua** (Pedro, 22/09): 863 é só o S2; somadas as outras bases e tirada a
  duplicata, a entrada da Fase 1 fica maior. **F1, F2 e F3 seguem abertos** e definem o loop.

## G. Critérios de inclusão/exclusão — **FECHADO em 22/09** (⟨rev-34⟩; G3 em ⟨rev-30⟩)

**Decisões do Pedro (22/09)** — método §1.2.1 e §3.4:
- **G1a** survey que cobre a área em parte **entra**, como base de conhecimento (*"é necessário
  entender LLMs do treino até a inferência pro meu caso"*) · **G1b** CNN/GNN/difusão **fora** ·
  **G1c** aplicação específica **só se não houver survey geral da divisão** · **G1d** infraestrutura
  de implantação **dentro** (*"ajuda a mapear a área"*) · **G1e** hardware **divisão do mapa**
  (*"pra saber que existe, não pq vamos usar"*).
- **G2a** survey = se declara **ou** funciona como survey · **G2b** paper primário fica no bruto e
  volta como candidato a seminal · **G2c** paper de sistema -> pilar ferramentas.
- **G4 — FECHADO (Pedro, 22/09): eficiência de treino não entra.** Registrado em §1.2.1.
  Pergunta original: G1a cobre survey que trata a área *em parte*. Survey de
  eficiência de **treino pura** (sem nenhum eixo de §1.2 — ex.: "Compute-Efficient Deep Learning",
  "Dimensionality Reduced Training") continua fora por §1.2, ou a razão "base de conhecimento" o
  traz também? **Pergunta para o Pedro.**

Texto original:

- **G1.** §1.2 está escrito para *divisão*, não para *paper*. Na Fase 1 foi aplicado a surveys por
  título, por extrapolação — as 36 "borda" são o sintoma. Escrever critério de relevância por survey?
- **G2.** Não há exclusão nomeada para "não é survey" (paper primário, software) — sai implicitamente
  por §3. Nomear? (12 obras caíram aí em 21/09.)
- **G3.** O Resumo do método diz >= 100 citações; §3.2 diz "teste a 60". Fechar o número e sincronizar.

## H. Saturação depende da ordem de leitura — **FECHADO em 22/09**

- ~~**H1.**~~ **DECIDIDO:** §5.3 nova ⟨rev-27⟩ — conjunto inicial com **autores disjuntos, venues
  distintos, ≥ 1 de cada pico da distribuição de anos** e termos de origem diferente do pool;
  citação sozinha não ordena. **Detector de cluster:** divisões novas por survey deve cair; se não
  cair, é cluster perdido — volta ao conjunto inicial com sinônimos (Wohlin, lições 7–8).
  **Teste da bimodalidade marcado como instrumento nosso**, não de Wohlin (a lição 9 dele diz que a
  matriz de citação não detecta cluster independente; aqui os dois grupos já são conhecidos).
  Métrica nova em §13: divisões novas por survey lido.
- **Achado que motivou a regra (nível 3, 22/09):** os 8 mais citados das 58 são todos de 2020–21
  (citação = idade); distribuição bimodal com vale em 2022; **zero** sobreposição de autores entre os
  5 mais citados — o risco é de era, não de grupo.
- ~~**H2.**~~ **DECIDIDO por delegação** — o Pedro passou a escolha ao Claude em 22/09 (*"pra evitar
  meu viés, vou deixar você escolher"*), com a inclinação dele registrada (*"acho que divisões do mapa
  né, n sei, mas my gut tells me so"*). **Escolha: não vira divisão** — a era é **atributo de cada
  divisão** (coluna `era`, §8) e o fato "duas literaturas que se citam pouco" entra no **pilar
  história**. Motivo: divisão só existe se um survey a declarar (§9); "pré-LLM" é periodização, não
  técnica, e como divisão faria o mapa misturar dois eixos. Reversível pela regra normal de §9.
  Método §5.3 ⟨rev-28⟩. **Continua aberto:** confirmar que o teste vale o custo, na Fase 2.

## I. Rótulos "decisão/default do Claude" nos documentos

Regra nova (22/09): perguntar antes, nunca preencher e rotular como do Claude. Rótulos existentes:
método §3.2 ("default do Claude por omissão"), §6 ("definida pelo Claude por delegação"), CLAUDE.md
(bloco da definição de fundamentos, "Leitura (Claude, a confirmar)").
- **I1 — FECHADO (Pedro, 22/09): pode deixar.** Pergunta original: Reescrever esses trechos como decisão do Pedro (com a data em que ele confirmou), manter
  como delegação com as palavras dele, ou deixar?

## J. Herdado do handoff de 21/09 (ainda aberto)

- **J1 — FECHADO (Pedro, 22/09): até o mapa v1.** Pergunta original: "Fase 1 em 2 semanas" (alvo 05/10) = só a lista de candidatos (§11 Fase 1) ou até o mapa v1
  (Fases 2–3)? Anotar data-alvo no método (`## Em aberto`, item 2).
- **J2 — FECHADO (Pedro, 22/09): rodar a Fase 1 inteira de novo, conforme o método** (a execução 2 foi calibração, *"só pra ter um feeling"*). **Plano apresentado antes de executar** — ordem dele. Pergunta original: Rodar as strings-filhas (agora 7, com `edge`) e o Google Scholar (manual)?
- **J3 — FECHADO (Pedro, 22/09, delegado ao Claude):** `screening/registro-etapa1.md` + `.csv`. Pergunta original: Nome do arquivo de registro (§8; `## Em aberto`, item 1).
- **J4.** Quando terminar o Petersen: o keywording dele muda algo em §2 (esquema emergente) ou §9
  (união com consolidação)?
- **J5.** Divisão de horas (§10); Agrawal §4.3; pendências bibliográficas antigas; Glaser & Strauss
  cap. III no original; `[4]` na Fundamentação entregue.

---

*Blocos K–O: notas do Pedro em 22/09, durante a leitura (trechos do Petersen citados por ele).*

## K. Bubble plot (systematic map) — "vamos fazer? se sim, precisamos das facets"

Petersen: *"bubble plots allow to combine categories with each other and thus the relative emphasis of
research on categories is visible from the plot itself"* — e sugere variar no tempo (GapMinder).
Exige **duas facetas classificadas em toda obra incluída**, com frequência por célula.

Faceta 1 = **divisão** (emergente, §9). Faceta 2, candidatas:

| faceta 2 | o que mostra | custo | observação |
|---|---|---|---|
| família de arquitetura (encoder-only / decoder-only / enc-dec / outros) | concentração da eficiência por família | médio — nem todo survey declara | é o pilar fixo (§1.1) e a resposta do Pedro a "o que quero saber fazer"; exporia visualmente o vazio onde o tema v3 mora |
| eixo de §1.2 (inferência / memória-hardware / dado rotulado) | que custo a área ataca mais | baixo — contorno já definido | top-down, independe dos surveys |
| ano | tendência no tempo (o GapMinder do Petersen) | zero — já no bruto | descreve mercado editorial, não estrutura |
| pilar (história/fundamentos/ferramentas/vocabulário) | cobertura da Etapa 1 por divisão | zero — **coluna já existe em §8** | régua do professor; sai de graça |

- ~~**K1.**~~ **DECIDIDO (Pedro, 22/09): sim, e a faceta 3 é `arquitetura`.** Três facetas: divisão
  (Y) · pilar (semiplano esquerdo) · arquitetura (direito) — o layout de Petersen. Motivo registrado:
  arquitetura é a única candidata **ortogonal à divisão** (eixo §1.2 é quase função da divisão, como
  o teste de 22/09 mostrou: o próprio critério para classificar por eixo usa as palavras que nomeiam
  as divisões). Escrito em `docs/screening/metodo-screening-etapa1.md` §8 (coluna `arquitetura`) e §9.1 ⟨rev-23⟩.
- ~~**K2.**~~ **FEITO:** a coluna existe no §8 antes da Fase 2.
- **K3.** Ressalva de escala: Petersen contava 78–304 papers; aqui são ~58 surveys sobre ~8–12
  divisões — muitas células vazias. O vazio informa (é o argumento do tema), mas o gráfico precisa
  declarar N e a unidade (survey, não paper).
- ~~**K5.**~~ **DECIDIDO (Pedro, 22/09): sim.** Eixo §1.2 anotado por divisão no eixo Y — propriedade
  da divisão, não da obra; custo zero e não gasta semiplano. Escrito em §9.1 ⟨rev-23⟩.
- ~~**K4.**~~ **DECIDIDO (Pedro, 22/09): os dois, em momentos diferentes.** **A** (unidade = survey) a
  cada rodada, como instrumento do loop keywords ↔ busca — bolha pequena ou célula vazia vira a
  pergunta "lacuna da área ou da busca?". **B** (unidade = paper referenciado) no fim, com tudo.
  Escrito em §9.1 ⟨rev-24⟩. **Consequência aceita junto:** a extração passa a registrar a **seção
  citante** de cada referência (§6, §7) — sem isso, B exigiria reler os surveys. Bônus: refina o
  critério de seminal de §4 para "≥ 2 surveys **na mesma divisão**".
- **K6 (novo, não decidido):** A como instrumento do loop cria um **gatilho de revisão do pool** —
  lacuna vista no gráfico. É o mesmo gatilho de **E1** (calibração sobre o retorno) ou um segundo?
  Nomear os dois juntos quando E1 for decidido.

## L. Tabela "Number of Included Articles" — escala de referência

Pedro (22/09): *"o nosso objetivo inicial é apresentado no artigo, na seção"* — a tabela dos 10
mapeamentos comparados: **potencialmente relevantes** 185–5.453 → **incluídos** 10–304.
Nossa execução 2: **154 potencialmente relevantes → 58 incluídos** — dentro da faixa deles, na ponta
pequena (comparável a 185 → 10 e 353 → 173). O funil pequeno é efeito do `filtro-tipo` (bloco C) e
do piso de citação.
- **L1 — FECHADO (Pedro, 22/09): sim** — §11.1 ⟨rev-35⟩. Pergunta original: Adotar o **relato de funil com contagem por estágio** (estilo PRISMA / Tabela 5 do Petersen)
  como saída obrigatória da Fase 1? Hoje existe de fato (`2026-09-21-candidatos-*.md`), não como regra.
- **L2.** Essa faixa é a resposta parcial de **F4**: com `filtro-tipo`, o "3000 → 1500 → 500" não
  acontece — os números já nascem na casa das centenas. O loop por voltas só é necessário se a
  população mudar (F4 b/c). Confirmar qual população.

## M. Mapa não julga qualidade / mapa como precursor de revisão

Petersen: as revisões sistemáticas que eles acharam buscam **best practices a partir de evidência
empírica** — *"this is not a goal for systematic maps, and can not be since they do not study
articles in enough detail. A thematic summary leading to a map could be the first steps in a more
detailed systematic review."*
- **M1 — FECHADO pela N3** (§1.4). Pergunta original: Registrar isto como **limite declarado** do nosso screening: o mapa diz o que existe e onde
  está, **não** diz o que funciona melhor. Reforça "screening em contraposição à RSL" (professor).
- **M2 — FECHADO (Pedro, 22/09): sim** — §1.4 ⟨rev-35⟩. Pergunta original: E como **ponte**: o mapa da Etapa 1 é o primeiro passo de uma revisão mais detalhada — que
  é o que a trilha (Etapa 3 / tema v3) faria depois. Encaixa com B3 ("toda trilha tem fundamentos
  próprios"). Escrever no método ou no método-do-método?

## N. Profundidade de leitura adaptativa — **FECHADO em 22/09** (⟨rev-33⟩)

**Decisões do Pedro (22/09):**
- **N1.** A tabela vira **escada** de classificação: **abstract -> introdução -> conclusão**, sobe só
  se o degrau não bastou. E a leitura tem duas funções: *"como nosso trabalho não é só juntar os papers
  pra fazer um mapa, ler seções como taxonomia, ferramentas, e criar um glossário continua tendo
  importância"* — a extração fixa de survey fica (método §6.2).
- **N2.** **A escada é o limite** — sai o teto de 5 minutos; dúvida (§8.1) só no topo da escada.
- **N3.** **Sim** — declarado em §1.4: mapa que também extrai; não avalia qualidade de resultado.
- **N4.** **Tenta buscar o abstract (arXiv id / DOI); se falhar, sobe para a introdução.**
- **N5 — FECHADO (Pedro, 22/09): como na tabela.** §6.1. Pergunta original: A escada abstract/introdução/conclusão foi pensada para paper.
  Livro/capítulo e documentação não têm abstract — manter para eles a leitura da tabela de §6.2 como
  está, ou definir uma escada própria? **Pergunta para o Pedro.**
- **Correção de contagem (22/09):** o "103 das 154 sem resumo" abaixo contava **registros** do S2;
  37 deles vieram também no arXiv, com resumo. Sem resumo em nenhuma das duas bases: **66 obras** —
  29 com arXiv id, 36 só com DOI, 1 sem identificador.

Texto original da pendência:

Petersen: *"abstracts are often misleading and lack important information ... do not pre-specify that
only certain parts of a paper can be read. Instead, allow more detailed study of papers for which it
is not clear how they should be classified."* E, no keywording, o revisor vai à introdução/conclusão
quando o resumo é ruim.
**O nosso §6 faz o contrário: pré-especifica o que se lê por tipo de fonte.** O adaptativo existe só
como exceção — fonte que pede mais leitura vira "dúvida" (§8.1, Claude lê a seção, Pedro decide).
- **N1.** Inverter a moldura: a tabela de §6 passa a ser **piso** (o mínimo que se lê), não teto, com
  regra explícita "não classificou? leia mais fundo" — em vez de virar dúvida por padrão?
- **N2.** Se sim, o que muda em §8.1 (a dúvida deixa de ser o caminho normal e vira só o caso em que
  nem lendo mais fundo se decide) e no limite de 5 minutos de §6 (artigo científico)?
- **N3.** Petersen liga isso a um **contínuo** mapa ↔ revisão sistemática: quanto mais fundo, mais
  perto de revisão. Declarar onde o nosso screening se põe nesse contínuo? (liga a M1.)
- **N4.** Efeito prático já visto: o bulk do Semantic Scholar **não devolve resumo** — para 103 das
  154 obras da execução 2 não há nem resumo para julgar. Qualquer regra adaptativa tem de dizer o que
  fazer nesse caso (buscar o resumo por outra rota? classificar só por título e marcar o nível?).

## O. Extração de dados com justificativa por linha; esquema evolui durante a extração

Petersen: planilha com uma coluna por categoria do esquema; ao lançar o paper, o revisor escreve
**uma justificativa curta** de por que ele fica naquela categoria; o esquema **evolui durante a
extração** (categorias novas, fusões, divisões); da tabela final saem as **frequências**.
Alinhamento com o que já existe: §8 já tem as colunas `divisão`, `pilar` e **`motivo`** (uma linha) —
que é exatamente a justificativa; §9 já prevê mescla pelo Pedro; §2.3 já versiona o mapa (v2+).
- **O1 — FECHADO (Pedro, 22/09): sim** — §8 ⟨rev-35⟩. Pergunta original: Tornar explícito em §8 que **o esquema evolui durante a extração** (hoje a evolução está em
  §9/§2.3, como se fosse etapa posterior) — e que mescla/divisão de categoria gera nova versão do
  mapa com data e motivo?
- **O2 — FECHADO: sim** — §8. Pergunta original: Acrescentar **frequência por categoria** como saída da tabela (é o insumo do bubble plot, K)?
- **O3 — FECHADO: .md + planilha** — §8. Pergunta original: Formato do registro: o método diz "arquivo único com tabela" (.md). Petersen usou planilha.
  Manter .md, ou .md + .csv/.xlsx para contar e plotar? (liga a J3, nome do arquivo.)

