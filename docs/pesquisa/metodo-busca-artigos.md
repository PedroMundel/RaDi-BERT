# Método de busca de artigos — tema v2 (09/09/2026)

Substitui o plano de leitura da Fase 4 (os 8 esqueletos em `docs/residencia/semana-1-topicos/artigos/` foram
montados para a config C2 e não servem ao tema v2). Método reutilizável, não específico deste tema.

## Princípio: dois conjuntos, não um

| Conjunto | Para quê | Critério de corte |
|---|---|---|
| **CITAR** | Related work, posicionamento, defesa na banca | Autoridade e cobertura: surveys, papers canônicos, trabalhos em pt-BR |
| **COPIAR** | Método, código, hiperparâmetro que você vai executar | **Tem repositório?** Roda em 8GB? Reprodutível? |

O conjunto COPIAR é menor, mais recente, e é o que decide se o trabalho termina. Um paper
excelente sem código vale menos, na prática, que um mediano com repo que roda.

## Funil: largo em cima, estreito embaixo

O teto é de **leitura**, não de coleta. Coletar é barato (é script); ler é caro (é você).

| Etapa | Volume | Quem faz |
|---|---|---|
| Varredura por string | **1000+ candidatos** | Script |
| Deduplicação + filtros mecânicos (ano, idioma, tipo) | ~300 | Script |
| Ranqueamento (citação, co-citação, código) | ~100 no topo | Script |
| Passe de título | ~40 sobrevivem | Você, 10s cada |
| Passe de abstract | ~20 | Você, 2min cada |
| **Leitura real** | **8** | Você |
| **Execução/reimplementação** | **3** | Você |

Recall alto em cima é o que garante não perder o paper certo; precisão embaixo é o que garante
terminar. Passar de 8 leituras profundas é procrastinação disfarçada de rigor.

## Fase 0 — Perguntas, não palavras-chave

Buscar respostas, não tópicos. Para o tema v2, as quatro perguntas:

- **P1** Como se funde adaptadores/modelos? Quais métodos existem e o que cada um assume?
- **P2** Por que a fusão degrada (interferência entre tarefas) e o que mitiga?
- **P3** Eficiência de dados em fine-tuning: quanto dado basta, e o que curadoria economiza?
- **P4** SLMs em português: que modelos e que benchmarks existem?

Cada pergunta terá suas próprias sementes e sua própria saturação. P4 é a que provavelmente tem
menos material — e por isso é onde mora o ineditismo.

## Fase 1 — Sementes (5 a 10 papers)

Por pergunta: 1 survey recente + 1–2 papers de método canônico. Critério de semente: aparece
citado em quase tudo que você já leu sobre aquilo, OU é o survey mais recente com boa cobertura.

Regra: semente é ponto de partida, não leitura obrigatória. Algumas serão descartadas na Fase 3.

## Fase 1B — Varredura ampla: strings de busca

Montagem por **blocos de sinônimos**: cada bloco é um conceito, dentro do bloco tudo é OR, entre
blocos é AND. Isso é o que dá recall alto sem virar lixo.

**P1 — fusão de adaptadores e modelos**

```
("model merging" OR "model fusion" OR "weight averaging" OR "parameter averaging"
 OR "task arithmetic" OR "model soup" OR "weight interpolation" OR "adapter merging")
AND
("adapter" OR "LoRA" OR "low-rank adaptation" OR "parameter-efficient fine-tuning" OR "PEFT")
```

**P2 — interferência e reparo**

```
("model merging" OR "multi-task" OR "task arithmetic" OR "adapter composition")
AND
("interference" OR "catastrophic forgetting" OR "negative transfer" OR "task conflict"
 OR "capability loss")
AND
("mitigation" OR "repair" OR "recovery" OR "replay" OR "rehearsal" OR "healing")
```

**P3 — eficiência de dados em ajuste fino**

```
("data efficiency" OR "sample efficiency" OR "learning curve" OR "scaling law"
 OR "how much data" OR "data scaling")
AND
("fine-tuning" OR "instruction tuning" OR "supervised fine-tuning" OR "adapter tuning")
AND
("data selection" OR "data curation" OR "data pruning" OR "coreset" OR "deduplication"
 OR "quality filtering")
```

**P4 — SLM em português** (o bloco mais estreito, e por isso o mais promissor)

```
("small language model" OR "compact language model" OR "efficient language model"
 OR "on-device language model" OR "sub-billion" OR "1B" OR "3B")
AND
("Portuguese" OR "Brazilian Portuguese" OR "pt-BR" OR "low-resource language" OR "multilingual")
```

**Adaptação por base** (a sintaxe muda, os blocos não):

- **arXiv API** — prefixos de campo (`all:`, `ti:`, `abs:`), operadores `AND`/`OR`/`ANDNOT`, aspas
  para frase. Cobre preprint, que é onde o campo vive; não cobre venue formal.
- **Semantic Scholar / OpenAlex** — busca full-text com boolean mais simples; a força delas é o
  grafo de citação, não a string. Use string para semear, grafo para expandir.
- **Scopus / Web of Science / IEEE / ACM** — boolean rico (`TITLE-ABS-KEY(...)`, proximidade,
  truncamento com `*`). **Verifique seu acesso pelo Portal de Periódicos da CAPES via UFG** — se
  tiver, é o que permite uma revisão com cara de sistemática, e muda a qualidade do related work.
- **Google Scholar** — sem API, sem boolean decente, mas insubstituível para o passe de "quem
  citou isso". Manual e só no fim.

**Truncamento útil:** `merg*` pega merging/merged/merger; `adapt*` pega adapter/adaptation. Use nas
bases que suportam, evite onde vira ruído.

## Fase 2 — Bola de neve automatizada (o coração do método)

Busca por palavra-chave é ruim em área que se move rápido: a terminologia muda e você acha o que
já sabia procurar. Citação não mente. Duas direções, ambas automatizáveis por API:

**Para trás (fundação):** pegue as referências de TODAS as sementes e conte quantas sementes citam
cada trabalho. Citado por 4+ sementes = fundacional, você precisa conhecer mesmo que seja antigo.

**Para frente (fronteira):** pegue tudo que CITA as sementes e conte quantas sementes cada um cita.
Cita 3+ sementes = está exatamente na sua interseção, mesmo que ninguém tenha citado ele ainda.

Essa segunda direção é a que acha o trabalho de 3 meses atrás que é o mais relevante de todos e
que nenhuma busca por citação bruta encontraria.

**APIs candidatas (verificar antes de escrever o script):** OpenAlex e Semantic Scholar Graph API
— ambas gratuitas, com dados de referência e citação. arXiv API para metadados e PDF.

## Fase 2B — Achar os fundacionais (o "Attention is all you need" do seu tema)

Paper fundacional não se acha por busca — ele **emerge da contagem**. Com o corpus de 1000 na mão,
o fundacional é o que quase todo mundo cita mesmo escrevendo sobre coisas diferentes.

**Critério mecânico (roda no script):** para cada trabalho referenciado pelo corpus, conte em
quantos dos 1000 ele aparece na lista de referências. Ordene por essa contagem, não por citações
globais. Quem é citado por 20%+ do seu corpus é fundacional **do seu tema** — que é diferente de
ser famoso em geral.

**Três camadas que vão aparecer, e cada uma tem um papel diferente:**

| Camada | Como reconhecer | O que fazer com ela |
|---|---|---|
| Fundacional da área ampla | Citado por quase 100% do corpus, anterior a tudo (arquitetura base, mecanismo básico) | Ler uma vez na vida, citar sempre, não gastar tempo |
| **Fundacional do seu nicho** | Citado por 20–60% do corpus, é o primeiro a fazer aquilo, todo método novo se compara a ele | **É aqui que mora o seu trabalho.** Ler a fundo, reimplementar, usar de baseline |
| Método corrente | Citado por 5–20%, recente, compete com os outros | Escolher 2–3 para comparar |

**Teste humano de confirmação:** se você não consegue explicar o seu método sem mencionar aquele
trabalho, ele é fundacional pra você. Se consegue, é related work.

**Sinal de alerta:** se nenhum trabalho passa de 20% de co-citação, ou o corpus está mal montado
(string errada, muito ruído), ou seu tema cruza duas comunidades que não se citam — e cruzar duas
comunidades que se ignoram é, por si só, um achado que vale parágrafo no artigo.

## Fase 3 — Filtros de corte

Aplicar nesta ordem, o mais barato primeiro:

1. **Janela temporal por pergunta.** Fusão de modelos e SLM: nada anterior a ~2023 sobrevive como
   método (só como fundação). Eficiência de dados: aceita mais antigo.
2. **Velocidade de citação, não total.** Citações ÷ anos desde a publicação. Sem isso, papers de
   2019 enterram os de 2025 que são os que importam.
3. **Tem código?** Filtro decisivo para o conjunto COPIAR. Repositório ativo > repositório morto >
   sem repositório.
4. **Roda em 8GB?** Se o paper só existe em escala de 70B, o método pode não transferir — e isso
   precisa ser sabido ANTES de investir leitura.
5. **Tem pt-BR ou multilíngue?** Não é eliminatório, mas sobe a prioridade (é o seu ineditismo).

## Fase 4 — Triagem em três passes

- **Passe 1 (título + venue):** 10 segundos. Sobrevive ~50%.
- **Passe 2 (abstract + figura principal):** 2 minutos. Pergunta única: "isso responde P1–P4?"
  Sobrevive ~40%.
- **Passe 3 (leitura real):** só os que passaram, e só as seções que respondem a pergunta.

Ninguém lê paper inteiro. Método, resultados e limitações — nessa ordem.

## Fase 5 — Regra de parada (a que faltava)

**Saturação:** pare quando 3 papers novos seguidos não trouxerem nenhuma referência ou método que
você já não tenha visto. Isso é critério de revisão sistemática, não preguiça — e é o que impede
a busca de virar hobby.

Segundo gatilho de parada: **o orçamento acabou** (Fase 0). O que vier depois entra em "trabalhos
futuros", não na leitura.

## Fase 6 — Registro

**Não** criar um .md por paper antes de ler (foi o erro do plano anterior: 8 esqueletos escritos,
nenhum usado). Em vez disso:

- **Uma tabela única** — `mapa-de-leitura.md`: id, título, ano, pergunta que responde (P1–P4),
  conjunto (CITAR/COPIAR), tem código, velocidade de citação, status de triagem.
- Nota individual **só** para os que passaram no passe 3 — e a nota é escrita DEPOIS de ler,
  não antes.

## Automação

O que dá pra script (e vale, porque é reutilizável em todo projeto futuro):

1. Recebe DOIs/IDs das sementes.
2. Puxa referências e citações via API.
3. Conta co-citação (para trás) e acoplamento (para frente).
4. Calcula velocidade de citação.
5. Marca quem tem link de código nos metadados.
6. Cospe a tabela da Fase 6 ordenada.

Fases 3 (filtros 4 e 5), 4 e 5 continuam humanas — são julgamento, não contagem.
