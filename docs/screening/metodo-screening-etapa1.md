# Método de screening — Etapa 1 da especialização

**Autor das decisões:** Pedro, 15/09/2026, ditadas em resposta a
`docs/formulario-metodo-screening.md`. Consolidado pelo Claude.
**Versão:** v3.8 (23/09) — ⟨rev-36⟩ bilhete por tamanho de técnica (golden ticket <= 20 obras; penúltima filtragem 21–50), §11.1. v3.7 (22/09) — ⟨rev-35⟩ fechamento das pendências pós-Petersen: livro e documentação seguem a tabela (§6.1); restrição do `filtro-tipo` declarada (§3); lacuna do pool também pelas perguntas de §1.4 (§2.1); relato de funil por volta (§11.1); mapa como primeiro passo de revisão mais funda (§1.4); esquema evolui na extração, frequência por categoria, registro em .md + planilha (§8); data-alvo 05/10 = até o mapa v1 (Em aberto). v3.6 (22/09) — ⟨rev-34⟩ critério de pertencimento **por survey** (§1.2.1: parcial entra como base; CNN/GNN/difusão fora; aplicação específica só sem survey geral; infraestrutura de implantação dentro; hardware como divisão para saber que existe) e exclusão nomeada **não é survey** (§3.4). v3.5 (22/09) — ⟨rev-33⟩ a leitura de classificação vira **escada** (abstract -> introdução -> conclusão; a escada é o limite, sem teto de tempo) e a extração de survey continua fixa (§6); a dúvida só nasce no topo da escada (§8.1); abstract ausente é buscado por arXiv id ou DOI antes de subir o degrau (§6.1); o screening se declara no contínuo mapa <-> RSL (§1.4). v3.4 (22/09) — ⟨rev-32⟩ proposta de agrupamento por volta, com as quatro salvaguardas que a separam do registro (§11.1). ⟨rev-31⟩ §11.1 nova: o loop por voltas, com o filtro que **ordena e não apaga** e o alvo provisório de ~50 documentos. ⟨rev-30⟩ população = surveys **sem piso de citação** (863 no S2, opção b); o piso sai da busca e vira critério de registro em §3.2, com valor 60 (§11, §3.2, Resumo). ⟨rev-29⟩ o pilar ferramentas ganha rotas de descoberta fora de survey: filha `ferramentas` **sem `filtro-tipo`** (pool §2), ferramentas nomeadas pela fonte na extração (§6, §7) e registros de ecossistema como descoberta nível 3 não citável (§3). ⟨rev-28⟩ os termos passam a ser os do professor: *fundamentos* é o produto
e o antigo "fundamentos" de §1.1/§6 vira **conceitos**; §1.4 nova (hierarquia + as cinco perguntas
do screening + limites de escopo); §3.3 nova (**eixo de atividade**); colunas `atividade` e `era`
em §8; era como atributo, não divisão (§5.3). ⟨rev-27⟩ conjunto inicial com diversidade obrigatória, detector de cluster
e teste da bimodalidade (§5.3, §13). ⟨rev-26⟩ gate de relevância e teto de 8 voltas no checkpoint (§2.3, §13).
⟨rev-25⟩ revisão do pool por evidência de retorno, duas direções (§2.1,
pool §3), e checkpoint do nome da área antes de consolidar (§2.3). ⟨rev-23⟩ facetas do mapa e bubble plot (§8, §9.1) e ⟨rev-24⟩ dois momentos
do plot (A por rodada, B no fim) com a seção citante nas referências (§4, §6, §7, §9.1), decididos
pelo Pedro em 22/09 depois de ler o Petersen. Demais pendências da leitura em `docs/pendencias-pos-petersen.md`.
v2.4 (17/09) — **FECHADO**, com a §2 reescrita em 17/09 (pool de termos versionado; strings são composições dele). v1 revisada contra dois critérios do Pedro (sem lacuna de
conhecimento; documento robusto); os 21 achados estão em `docs/revisao-metodo-screening-2026-09-15.md`.
Toda inserção da revisão está marcada `⟨rev-N⟩` e foi decidida pelo Pedro em 16/09 (ou adotada por
omissão, onde indicado). O texto sem marcador é decisão original do Pedro. Restam só os três itens
operacionais do fim.

**Especialização:** eficiência de modelos para implantação.
**Etapa 1 (professor):** história, fundamentos, ferramentas — divisões e vocabulário da área.
**Tipo de busca (professor):** *screening*, em contraposição à Revisão Sistemática — "encontrar
artigos relevantes e que suportem o início da Etapa 1".
**O que este método cobre:** o screening (nível 3) e a passagem para a leitura (2 → 1). A leitura da
Etapa 1 em si — como se lê um seminal, como se escreve a nota — terá regra própria quando começar.
**Como este método foi construído:** `docs/metodo-de-construcao-do-metodo.md` — as dez decisões são os
componentes-padrão de protocolo de revisão (Kitchenham; Arksey & O'Malley; Petersen; Wohlin),
adaptados ao screening; trilha datada de quem decidiu o quê.

---

## 1. Objeto do screening

A unidade de busca é a **área**: eficiência de modelos para implantação. As **arquiteturas**
(encoder, decoder, encoder-decoder) entram como **pilar fixo, definido a priori** — é o que o Pedro
declarou querer aprender neste ciclo. Os demais pilares **não são fixados agora**: emergem "conforme
formos descobrindo ao ler os documentos". Top-down na área e no pilar de arquiteturas; bottom-up no
resto.

### 1.1 Conceitos a priori do pilar arquiteturas ⟨rev-2⟩ ⟨rev-28⟩ — fechado pelo Pedro em 16/09

Top-down exige conteúdo. O pilar só fecha quando **cada item tem uma fonte em nível 1** no registro.

**O que "profundidade" significa aqui** (critério acordado): *plena* = saber onde está o custo do
componente em FLOPs e em memória, e por que as três famílias diferem nele — **não** é derivar
gradiente. *Média* = entender o componente pelo gancho de implantação nomeado. *Leve* = uma frase
certa. **Critério que separou os níveis:** o componente aparece como variável de custo ou como alvo
de algum termo do pool de §2? Se sim, média ou plena.

| Nível | Itens | Gancho de implantação |
|---|---|---|
| **plena** | self-attention | centro de custo: O(n²) no comprimento; é o que o KV cache guarda, o que FlashAttention otimiza, o que atenção linear tenta substituir |
| **plena** | máscara causal · cross-attention | **são a diferença entre as três famílias** — encoder sem máscara, decoder com, encoder-decoder com cross-attention. É onde mora "o que cada família absorve" |
| **plena** | FFN/MLP | ~2/3 dos parâmetros; alvo de poda, MoE e quantização |
| **média** | multi-head | via MQA/GQA — redução de KV cache presente em todo modelo servido hoje |
| **média** | tokenização por subpalavras | define quantos tokens um texto custa (pt-BR gasta ~1,5–2× em tokenizador centrado em inglês); vocabulário = matriz de embedding, ~23M dos 110M do BERT-base, 30%+ em SLMs |
| **média** | codificação posicional | RoPE é o que permite estender contexto sem retreinar; comprimento de contexto é custo de KV cache |
| **leve, com gancho** | normalização de camada | *outliers* de ativação que dificultam quantização (o problema de LLM.int8 / SmoothQuant) aparecem associados a ela |
| **leve, com gancho** | conexões residuais | é o que faz *early exiting* e poda de camadas funcionarem — o fluxo residual mantém representações intermediárias legíveis |
| **leve** | linhagem atenção Bahdanau/Luong → *scaled dot-product* | base, não mecanismo em uso |

- **As três famílias e seus objetivos de pré-treino — tudo:** encoder-only (MLM — BERT) ·
  decoder-only (CLM — GPT) · encoder-decoder (*span corruption* / seq2seq — T5, BART). O que cada
  objetivo faz a representação aprender, e por que encoder rotula e decoder gera.
- **Inferência — mantido (Pedro, 16/09):** decodificação autorregressiva · KV cache · *prefill* ×
  *decode* · *memory-bound* × *compute-bound* · precisão numérica (FP32/FP16/BF16/INT8/INT4) · custo
  em FLOPs e bytes por token. Motivo registrado: gestão de memória, continuous batching, early
  exiting e a quantização inteira são ilegíveis sem este bloco; sem ele o pilar seria "arquitetura
  de transformer" em geral, não "arquitetura *para implantação*".
- **Escala — curto:** leis de escala, só o suficiente para ler um survey de compressão.
- **Base pré-transformer — plena, por §1.3:** RNN · LSTM · seq2seq · atenção neural (Bahdanau
  2014). Entra como conceito, não só como história.

### 1.2 Critério de pertencimento à área ⟨rev-5⟩ — decidido pelo Pedro em 16/09

Uma divisão candidata **pertence à área** se reduz custo de implantação em pelo menos um de três
eixos: **(i) inferência** — latência ou throughput; **(ii) memória/hardware** — cabe onde não cabia;
**(iii) dado rotulado** — mesma capacidade com menos rótulo. Os três são os da proposta de tema
(rev. 2). **PEFT/LoRA entram** (Pedro, 16/09) — pelo eixo de implantação: *serving* de múltiplos
adaptadores sobre uma base. Consequência registrada: a fronteira é o **efeito na implantação**, não
o momento em que a técnica age; eficiência de *treino* pura (sem efeito no modelo servido) fica fora.
Consequência aceita pelo Pedro em 16/09.

### 1.2.1 Pertencimento de survey ⟨rev-34⟩ — decidido pelo Pedro em 22/09

§1.2 decide **divisão**; esta regra decide **survey**. Motivo: na Fase 1 (21/09) §1.2 foi aplicado a
surveys por título, por extrapolação, e 36 obras ficaram em "borda" — cinco tipos recorrentes, uma
regra por tipo:

| caso | regra | motivo do Pedro |
|---|---|---|
| **(a) cobre a área em parte** — uma seção de inferência num survey de LLM, treino + inferência, fine-tuning com PEFT dentro | **entra**, inteiro, como **base de conhecimento** | *"é necessário entender LLMs do treino até a inferência pro meu caso, queremos criar uma base na área"* |
| **(b) técnica da área sobre modelo fora de §1.3** — CNN, GNN, difusão | **fora** | — |
| **(c) aplicação específica** — compressão para YOLOv5, biometria, imagem médica | **entra só se nenhum survey geral cobrir a divisão**; até haver divisões, fica ordenado no bruto, não apagado (§11.1) | — |
| **(d) infraestrutura de implantação** — edge/nuvem, serverless, serving de agentes | **dentro** | *"ajuda a mapear a área"* |
| **(e) hardware** — aceleradores, FPGA | **dentro, como divisão do mapa** | *"pra saber que existe, não pq vamos usar"* — presença no mapa, não alvo de estudo |

**Eficiência de treino pura continua fora** (Pedro, 22/09, G4): a razão "base de conhecimento" de (a) vale para survey que cobre a área **em parte**, não para survey sem nenhum eixo de §1.2.

Consequência de (d): a fronteira de §1.2 — **efeito na implantação** — inclui onde e como o modelo
roda, não só mudanças no modelo.

### 1.3 Escopo de "modelos" ⟨rev-6⟩ — decidido pelo Pedro em 16/09

**Transformers e a base dos transformers** — RNN, LSTM, seq2seq, atenção neural — para conceitos
e ferramentas. A base pré-transformer entra como **conceito** (é de onde o transformer vem), não
só como história. CNNs continuam só em **história** (poda e quantização nasceram nelas; ver §2.4).

### 1.4 Os termos do professor e as perguntas do screening ⟨rev-28⟩ — decidido pelo Pedro em 22/09

**Os termos são os dele.** Da definição transmitida em 22/09 (*"os FUNDAMENTOS de qualquer Área é
construído ao longo do TEMPO (história), reunindo FERRAMENTAS que auxiliam na execução de toda e
qualquer ATIVIDADE que seja necessária dentro de uma TRILHA... Um especialista conhece 'o que forma'
a sua área ATUALMENTE"*), **fundamentos não é um pilar ao lado dos outros: é o produto**, e os
demais são as suas partes e o seu modo de construção:

```
FUNDAMENTOS = o que forma a area ATUALMENTE        <- o produto
   |- divisoes ...... as partes
   |- vocabulario ... os nomes das partes
   |- conceitos ..... o que os nomes nomeiam (o antigo "fundamentos" de 1.1)
   |- ferramentas ... com o que se executa cada atividade (3.3)
   \- historia ...... como as partes vieram a ser (atravessa todas)
```

**Consequência de nomenclatura (a razão da mudança):** o que este método chamava de "fundamentos"
em §1.1 e §6 — self-attention, KV cache, máscara causal — são **conceitos**, não os fundamentos no
sentido do professor. Mantida a palavra antiga, a pergunta dele *"quais são os fundamentos da sua
área?"* seria respondida com a lista estreita, quando a resposta esperada é divisões + vocabulário +
ferramentas + história. Renomeado em todo o método ⟨rev-28⟩; o valor `fundamentos` da coluna *pilar*
(§8) passa a ser `conceitos`.

**As perguntas do screening.** A pergunta-guarda-chuva é a do professor — *o que forma a minha área
atualmente?* — e as cinco abaixo são as suas componentes:

| | pergunta | componente |
|---|---|---|
| **Q1** | quais são as divisões da área e como os surveys as nomeiam e agrupam? | as partes |
| **Q2** | qual é o vocabulário da área, e quanto o meu de partida coincide com ele? | os nomes |
| **Q3** | que trabalho abriu cada divisão, e qual survey conta essa história? | o tempo |
| **Q4** | que conceitos os surveys assumem que o leitor já sabe? | o que os nomes nomeiam |
| **Q5** | que ferramentas a área usa para executar cada atividade, e quais têm paper? | com o que se executa |

**O que as cinco têm em comum, e é a fronteira do método:** todas são perguntas de **onde
encontrar**; nenhuma é pergunta de **o que é verdade**. Nenhuma pergunta "qual técnica funciona
melhor" — isso exigiria julgar evidência empírica, que é trabalho de revisão sistemática e está
**fora** deste screening (Petersen et al. 2008: mapas "não estudam os artigos em profundidade
suficiente" para isso). É esta linha que separa o screening da RSL, como o professor pediu.
*(Decisão do Pedro em 22/09: não separar "perguntas sobre o mapa" de "perguntas sobre a área" —
declarar o que todas são.)*

⟨rev-33⟩ **Onde este screening fica no contínuo mapa <-> revisão sistemática** (Pedro, 22/09).
Petersen et al. 2008 põem os dois num contínuo: quanto mais fundo se lê, mais perto da revisão.
Este screening **é um mapa que também extrai** — taxonomia, ferramentas, referências e vocabulário
para o glossário, porque o trabalho não é só juntar papers para fazer um mapa: é o insumo da Etapa 1.
Extrair vocabulário não é julgar evidência; **não avalia a qualidade de nenhum resultado**. Por isso
continua do lado do mapa, mesmo lendo mais fundo que um mapa puro.

⟨rev-35⟩ **O mapa como primeiro passo** (Pedro, 22/09, M2). Petersen et al. 2008: um resumo temático
que leva a um mapa pode ser o primeiro passo de uma revisão sistemática mais detalhada. Aqui, essa
revisão mais funda é trabalho da **trilha** (Etapa 3; o tema v3 é uma), não deste screening.

**Trilha tem fundamentos próprios.** "Toda Trilha também tem seus próprios fundamentos" — logo os
fundamentos da trilha (o tema v3: inferência textual, destilação de racionalização, datasets)
**não são objeto da Etapa 1** e não entram no mapa. Limite de escopo declarado.
**Janela:** "atualmente" confirma §11 — surveys 2020+ para mapa e divisões; história sem janela.

## 2. Divisões da área — bottom-up, com pool de termos (reescrita em 17/09)

**Decisão original (P2, 15/09): híbrido.** Reinterpretada pelo Pedro em 17/09: *"minhas escolhas são
muito vagas para colocar como top-down literal; foram só palavras que vieram na minha cabeça, e eu
não conheço da área — por isso quero me especializar."* Consequência: a lista a priori **não é
rascunho de taxonomia** — seria o mapa confirmando a ignorância de partida em vez de corrigi-la.
O híbrido passa a ser: **top-down no contorno, bottom-up no conteúdo.**

- **Top-down (fixado antes da busca):** o que é a área e o que pertence a ela (§1.2); o pilar de
  arquiteturas e seus conceitos (§1.1); o escopo de modelos (§1.3).
- **Bottom-up (vem dos surveys):** as divisões, subdivisões e nomes da área — construídos por união
  com consolidação (§9). Nenhuma divisão existe no mapa antes de um survey aprovado a trazer.

### 2.1 O pool de termos — vocabulário versionado (decidido pelo Pedro em 17/09)

O vocabulário do screening vive em **`docs/screening/pool-termos-etapa1.md`**: uma tabela, uma linha por termo, com
variantes, grupo, **origem** (`pedro` · `claude 15/09` · `survey:<id>`), status e retorno.
**As strings de busca são composições do pool** — string-mãe (grupo `área` + `filtro-tipo`) e uma
string-filha por grupo — traduzidas por base, com os filtros de §3.2 e §11 embutidos onde a base
permite. Nenhuma string é decretada à parte do pool; mudou o pool, regeneram-se as strings.

*Trilha da decisão (17/09):* a lista de 10 termos de 15/09 foi julgada pelo próprio Pedro "muito
vaga para top-down literal — só palavras que vieram na cabeça, e eu não conheço da área". Passou por
"string-mãe v0, alterável" e chegou em **pool de termos**, que é o que a string-mãe deveria ser desde
o início: o vocabulário separado da sua forma de uso. A seção de string de busca de
`docs/pesquisa/metodo-busca-artigos.md`, descartada em 09/09 para a busca de fronteira, **é reaberta aqui pelo
Pedro** para outro propósito (mapa da área, não fronteira) — registrado em `CLAUDE.md`.

**O que o pool é, e o que não é:**
- É **vocabulário e registro do ponto de partida**. Os termos do Pedro estão nele com origem
  marcada — o confronto antes/depois (abaixo) filtra por origem.
- **Não** é divisão, pilar nem taxonomia. Termo do pool não entra no mapa por si; só um survey
  aprovado cria divisão (§9).

**Regras de entrada e saída** (detalhadas no arquivo do pool): entra como semente no v0, ou como
nome de divisão/seção na taxonomia de um survey aprovado do v1 em diante; aposenta com retorno zero
*e* nenhum survey usando — riscado com motivo, nunca apagado; **v0** = sementes, **v1** = após
saturação do mapa, com os termos que os surveys trouxeram e as strings regeneradas.

**Confronto antes/depois (entregável):** no mapa v1, cada termo de origem `pedro` recebe um veredito
— **encontrou divisão / virou subdivisão / ficou fora da área (§1.2) / não existe com esse nome** —
e o mesmo para os de origem `claude`, separados. É o que o screening ensinou, visível.
⟨rev-22⟩ **Quando se revê o veredito — decidido pelo Pedro em 21/09: a cada rodada de saturação.**
Isto é, no v1 (saturação do mapa, §5.1) **e** a cada saturação de divisão (§5.2, v2+). Cada versão
do pool corresponde a uma rodada; o veredito de cada termo é reescrito na versão, com o que mudou e
por quê. Alinha o método ao termo de entrega da Semana 2 ("revisão ... após cada rodada"). O registro
(§8) ganha, por rodada, uma coluna `veredito-vN` por termo.

⟨rev-25⟩ **O pool também muda por evidência de retorno — decidido pelo Pedro em 22/09.** Além da via
"survey aprovado traz termo", o pool tem uma regra com **duas direções** (detalhe e tabela no arquivo
do pool, §3): **(a) ruído** — termo cujo retorno bruto é majoritariamente fora da área sai da string
que polui e passa a rodar numa **string-filha própria**, nunca apagado nem só removido, com o bruto
salvo; **(b) lacuna** — célula vazia no bubble plot A (§9.1) **ou pergunta de §1.4 sem termo que a cubra** (⟨rev-35⟩, Pedro, 22/09, A4) levanta "lacuna da área ou da busca?", e
se for da busca, o pool ganha termo. A cláusula de (a) é anti-viés: termo que só sai encolhe a área
para o que já se acreditava. Consequência: **a filha de um termo movido é obrigatória**.
Vocabulário: **versão** = rodada de saturação; **emenda** = ajuste por retorno dentro da versão.

**Definição a priori (opcional, recomendado):** uma linha por termo de origem `pedro`, escrita
*antes* de ler qualquer survey — "o que eu acho que isso é". Sem consultar nada; errar é o ponto.
Preenche-se em `screening-etapa1.md`, seção "ponto de partida", e não se edita depois.

### 2.2 Sementes do Claude — mesmo status, origem separada

O pool v0 tem 8 termos de origem `claude 15/09` — os que o Pedro desconhece ou não lembraria de
listar — ao lado dos 34 do Pedro. Status idêntico: termo de busca, não divisão. São conhecimento prévio do Claude,
**não verificados** contra survey nenhum — nível 3 por definição — e serão julgados pelo mesmo
confronto. "Prompt engineering" está no grupo `uso?`, a testar contra §1.2 no confronto — "prompt
compression" pode ser a variante que pertence.

### 2.3 Ciclo de vida do mapa

- **v0** = não existe mapa. Existem o pool v0 (§2.1, §2.2) e o contorno (§1).
- **Fase 1–2** (§11): surveys da área entram; cada taxonomia é extraída (§7) e vai para a união (§9).
- **v1** = mapa após **saturação do mapa** (§5.1): divisões consolidadas (≥ 2 surveys ou decisão do
  Pedro com motivo), singulares marcadas, confronto do pool (§2.1) feito.
- **v2+** = revisões durante o screening por divisão (§5.2), quando um survey de divisão traz
  subdivisão nova. Toda versão fica no arquivo `mapa-divisoes-etapa1.md`, com data e o que mudou.

⟨rev-25⟩ **Checkpoint do nome da área, antes de consolidar — decidido pelo Pedro em 22/09.** Depois
da extração e **antes** de consolidar o mapa (§9), comparar os nomes que os surveys dão à **área
inteira** com o grupo `área` do pool. Critério para distinguir: é nome de área se descreve o **escopo
inteiro** do survey (título, frase de escopo do resumo); é nome de divisão se nomeia uma **seção**
dele — a extração de §7 já entrega os dois. Apareceu nome de área que o pool não tem: o termo entra,
a **string-mãe é regenerada e roda de novo**, e só então se consolida.
**Até saturar, mas só antes do v1** (palavras do Pedro: *"até saturar, mas só nos primeiros loops,
enquanto não temos a base"*): repete-se enquanto a volta trouxer nome de área novo, e esse regime
vale apenas **enquanto não existe mapa**. Com o v1 no lugar, nome de área novo segue o loop normal
(v2+). Motivo: antes do v1 a população inteira ainda está enviesada pelo vocabulário de partida do
Pedro, e consolidar sobre ela fixaria o viés na estrutura; depois do v1 existe base para julgar.
Cada volta é uma **emenda** do pool (não uma versão) e leva motivo, data e o bruto.

⟨rev-26⟩ **Gate de relevância do checkpoint — decidido pelo Pedro em 22/09.** "Até saturar" não é
"até parar de aparecer nome novo": um nome de área candidato **é rodado sozinho antes de ganhar uma
volta**, e o que decide é o retorno dele. O gate não é mecanismo novo — é a ordem de aplicação de
três regras que já existem:

| o candidato, rodado sozinho, devolve… | regra | efeito |
|---|---|---|
| praticamente nada | aposentadoria por retorno zero (pool §3) | não ganha volta |
| muito, mas majoritariamente fora da área (§1.2) | revisão por retorno, direção (a) | não ganha volta; roda na filha |
| retorno relevante, dentro de §1.2 | — | **ganha a volta**: a mãe é regenerada |

"Majoritariamente fora da área" fica **qualitativo**, julgado pelo Pedro sobre o bruto — o mesmo
critério da emenda 1, sem percentual novo.

- **Parada:** o checkpoint fecha quando **mais da metade** dos nomes de área da rodada já estão no
  pool (Pedro, 22/09). Os poucos novos que sobrarem seguem para o v1 pelo loop normal.
- **Teto: 8 voltas** (Pedro, 22/09), **podendo aumentar se for necessário** — aumento é decisão dele,
  com motivo e data na linha. O número de voltas é **métrica de gate** (§13).
- **Limite conhecido do gate:** repetição de conceito mede o vocabulário **dos surveys lidos**, não o
  da área. Primeiras fontes homogêneas (mesmo subcampo, mesmos anos) se repetem rápido e fecham o
  gate cedo, com uma visão só. O gate vale o que valer a diversidade do conjunto inicial — é o mesmo
  problema do start set (§5, em aberto), e é argumento para resolvê-lo **antes** da Fase 2.

### 2.4 Regra do pilar história ⟨rev-3⟩ — confirmada pelo Pedro em 16/09

História de cada divisão = **o paper que a abriu** (primeiro seminal, sem janela temporal) + **a
narrativa de um survey** (introdução/seção de *background*). Pré-transformer e CNN entram **só no
pilar história** — LeCun 1990 (*Optimal Brain Damage*) e Han 2015 (*Deep Compression*) para poda e
quantização. **Exceção por §1.3:** a linhagem RNN/LSTM/atenção neural (Bahdanau 2014) é *base do
transformer* e entra também em conceitos. Confirmado pelo Pedro em 16/09.

## 3. Tipos de fonte

Aceitos, para todos os pilares, sem mapeamento fixo pilar × tipo:
**survey · livro ou capítulo · paper seminal · artigo científico.**

**Documentação de ferramenta** entra **só no pilar ferramentas**, com precedência: se a ferramenta
tem paper, o paper é a fonte e a documentação é apoio; se não tem (llama.cpp, TensorRT-LLM, Optimum,
ONNX Runtime), a documentação é a fonte — só a página de visão geral. Tutorial e API ficam para a
Etapa 2. Motivo: a Etapa 1 do professor inclui "ferramentas" explicitamente, e várias ferramentas
centrais de implantação não têm artigo.

⟨rev-29⟩ **Registros de ecossistema como fonte de descoberta — decidido pelo Pedro em 22/09.**
Catálogos do ecossistema (Hugging Face, ONNX, **MLPerf Inference**) entram para **descobrir nome de
ferramenta e nome de atividade** (§3.3) — o MLPerf enumera as pilhas de serving *e* as tarefas que
elas executam, e é a fonte mais direta que existe para o eixo de atividade. **São nível 3
permanente e não são citáveis**: consórcio industrial e documentação de projeto, não literatura.
Servem para saber que a ferramenta existe; a fonte dela continua sendo o paper de sistema ou a
página de visão geral, pela precedência acima.

Fora: tutorial de conferência, curso de referência (como fonte — ver §4).

⟨rev-35⟩ **Restrição declarada: o `filtro-tipo`** (Pedro, 22/09, C1). Toda string de mapa carrega
`survey | review | overview | taxonomy`. Petersen et al. 2008 evitam de propósito restringir por
tipo de estudo — o mapa deles quer visão ampla. Aqui a restrição é **aceita por custo** (um aluno,
semanas; sem ela a população vai de 863 para 16.821 no S2, ⟨rev-30⟩) e tem efeito conhecido:
**divisão que ainda não tem survey é invisível** para a string-mãe. Mitigações já no método: filhas
por grupo, filha `ferramentas` sem `filtro-tipo` (⟨rev-29⟩), bola de neve pelas referências.

### 3.1 Ferramenta × técnica ⟨rev-7⟩

**Ferramenta** = software que se instala e usa. **Técnica** = método, vai para a divisão. Um paper de
sistema (vLLM/PagedAttention, FlashAttention) gera **duas linhas** no registro: a técnica na divisão
correspondente; a ferramenta no pilar ferramentas.

### 3.2 Filtro de qualidade para survey ⟨rev-13⟩ — default do Claude por omissão (16/09)

Um survey entra no screening se satisfaz **pelo menos um**: (a) venue com revisão por pares
(periódico, conferência, workshop com anais); (b) **≥ 100 citações** no Semantic Scholar; (c) citado
por **≥ 2** surveys já registrados. Survey de arXiv sem nenhum dos três é registrado como "não entra —
sem filtro de qualidade", não descartado silenciosamente.
⟨rev-30⟩ **O piso de citação NÃO é parâmetro de busca — decidido pelo Pedro em 22/09.** A busca
roda **sem piso**; o piso vive só aqui, como critério de **registro**, aplicado depois da relevância.
Ordem correta: buscar largo -> classificar por relevância (§1.2) -> filtrar por qualidade (§3.2).
Motivo medido em 22/09: o piso seleciona **idade disfarçada de qualidade** — os 8 surveys mais citados
das 58 da Fase 1 são todos de 2020-21 (§5.3), e um piso na busca tornaria invisíveis os surveys de
2024-25 que ainda não acumularam citação. Consequência prática: a perna (c) — citado por >= 2 surveys
registrados — deixa de ser letra morta, porque passa a existir populacão para ela resgatar.
**Valor do piso quando aplicado no registro: 60** (Pedro, 21/09; era 100 até então).

*Pedro (16/09): "não sei qual é o melhor".* **Default do Claude, adotado por omissão:** os três em
OU, com 100 e 2. Motivo de cada perna: revisão por pares sozinha exclui surveys bons que só existem
no arXiv (comuns nesta área); citação sozinha exclui os recentes; a citação cruzada entre surveys é o
que resgata os recentes bons. Os números são calibráveis: se a Fase 1 devolver < 3 surveys por
divisão, baixar para 50; se devolver > 10, subir para 200.
*Calibração 1 (Pedro, 21/09, sobre o bruto da execução 1 da string-mãe):* piso da perna (b) em
**teste a 60** na execução 2 (o bruto a 100 era dominado por 2020–21, com 19 papers de 2025). O
ruído do bruto não era de qualidade, era de **relevância** — termos largos (`resource-constrained`,
`on-device`) puxando IoT/quântica/fotônica; esses termos saíram da string-mãe para uma filha `edge`
(pool, emenda 1). §3.2 não filtra relevância: isso é §1.2, julgado por título em nível 3 na Fase 1
e confirmado pelo Pedro na Fase 3.

### 3.3 Atividade — o eixo das ferramentas ⟨rev-28⟩ — decidido pelo Pedro em 22/09

Pela definição do professor, **ferramenta serve a uma atividade** ("ferramentas que auxiliam na
execução de toda e qualquer atividade necessária dentro de uma trilha"). O método passa a ter um
**eixo de atividade**, e não só ferramenta -> divisão (§3.1).

- **Coluna `atividade`** no registro (§8), preenchida para fontes do tipo ferramenta e para qualquer
  fonte que **declare** a atividade que a ferramenta executa.
- **Bottom-up, como as divisões.** Não há lista de atividades a priori — seria a taxonomia decretada
  que o método recusa (§2). Uma atividade entra quando uma fonte a **declara**: página de visão geral
  da ferramenta ("usado para servir modelos", "converte para ONNX"), ementa de curso de §4.1, ou
  seção de prática de um survey. Duas fontes consolidam; uma só fica marcada *singular*, como em §9.
- **Limite conhecido, declarado:** as fontes de atividade são mais fracas que as de divisão —
  documentação e ementa, não survey. A Etapa 1 registra o que for declarado; o mapeamento completo
  atividade x ferramenta é trabalho da **Etapa 2** do professor ("frameworks de apoio"), e este eixo
  é a semente dela. Pilar de atividade fino na Etapa 1 é resultado esperado, não falha.

### 3.4 Exclusão nomeada: não é survey ⟨rev-34⟩ — decidido pelo Pedro em 22/09

Na Fase 1 a população é de surveys (⟨rev-30⟩). **Conta como survey** a fonte que **se declara**
survey, review, overview ou taxonomy (título ou abstract) **ou** que **funciona** como survey —
revisa literatura e a organiza. O que não é survey sai da Fase 1 com motivo **"não é survey"**, e o
destino depende do que ela é:

- **paper primário da área** (ex.: VecQ, quantização) — fica no bruto com o motivo, pela regra
  *ordena, não apaga* (§11.1); **volta como candidato a seminal** se survey registrado o citar (§4);
- **paper de sistema** (ex.: LightSeq) — vai para o pilar ferramentas pela filha `ferramentas`
  (⟨rev-29⟩, §3.1), não para o mapa;
- **fora da área e não survey** — fica no bruto com os dois motivos.

## 4. Identificação do seminal de cada divisão

Seminal é o que **os surveys da divisão citam em comum** e/ou o que **cursos de referência usam**.
O curso não é lido — a ementa aponta o paper. A Fase 2B de `docs/pesquisa/metodo-busca-artigos.md` (interseção
das referências dos surveys), descartada em 09/09, **volta** como esse critério.

⟨rev-24⟩ **A seção citante refina (b)** (efeito da decisão do Pedro em 22/09, §9.1): com a seção
registrada, "citado por ≥ 2 surveys" pode ser lido como "citado por ≥ 2 surveys **na mesma
divisão**" — critério mais forte, porque um paper citado de passagem na introdução de dois surveys
não é seminal da divisão. Usar a versão por divisão quando a seção estiver disponível.

⟨rev-10⟩ **Limiar de (b):** citado por **≥ 2 dos ≥ 3 surveys** da divisão que passaram em §3.2.
*Pedro (16/09): "também não sei".* **Default do Claude, adotado por omissão:** 2 de 3. Motivo: com 1
de 3 tudo vira seminal; com 3 de 3 um survey ruim veta. Se uma divisão tiver ≥ 5 surveys, subir para
"metade ou mais".

**Cláusula de inclusão forçada:** se um paper é, para a divisão, tão relevante quanto o "Attention
is All You Need" — citação massiva —, ele entra *também*, mesmo que não saia pelos dois critérios.
*"Infelizmente tem que entrar."* Contagem de citação não é critério de busca; é só esse gatilho.
⟨rev-11⟩ **Gatilho operacional:** está entre os **3 mais citados da divisão** (Semantic Scholar,
busca pelo nome da divisão) e não saiu por (b)/(c). **Default do Claude, adotado por omissão:** 3.
Um paper nessa posição que não foi citado por 2 surveys é raro, e a raridade é o sinal.

### 4.1 Cursos de referência ⟨rev-14⟩

Lista inicial, verificada em 15/09 (página existe e título confere — nível 3; ementas ainda não
lidas). O Pedro adiciona ou remove.

| Curso | Instituição / responsável | Cobre | URL |
|---|---|---|---|
| 6.5940 *TinyML and Efficient Deep Learning Computing* | MIT, Song Han | compressão, quantização, poda, destilação, inferência eficiente | hanlab.mit.edu/courses/2024-fall-65940 |
| CS336 *Language Modeling from Scratch* | Stanford | arquitetura transformer, treino e inferência de LM, escala | cs336.stanford.edu/spring2025 |
| 11-868 *Large Language Model Systems* | CMU | serving, batching, memória, kernels | llmsystem.github.io/llmsystem2025spring |

## 5. Regra de parada — saturação em dois níveis ⟨rev-8⟩ ⟨rev-9⟩

Decisão original: **saturação**. A revisão separou o que o v1 misturava:

1. **Saturação do mapa** (nível da área): um survey *da área* novo não traz **divisão nova**. Satura
   primeiro; produz o mapa v1 (§2.3) por união (§9).
2. **Saturação da divisão:** um survey *da divisão* novo não traz **seminal novo** (critério de §4)
   nem **conceito assumido novo** (§6, regra transversal).

**Mínimo:** **3 surveys** lidos (em nível de screening) antes de declarar saturação em qualquer
nível — com um só, "o próximo não trouxe nada" é indistinguível de "não li o suficiente".
Sem teto de tempo por divisão; o orçamento é global (§10).

### 5.3 Conjunto inicial e detecção de cluster ⟨rev-27⟩ — decidido pelo Pedro em 22/09

**O problema.** A saturação depende da **ordem de leitura**: fontes iniciais parecidas entre si
saturam umas com as outras e fecham o mapa com uma visão só. Wohlin 2014 nomeia os dois sinais
idênticos — referências muito repetidas significam **ou** que a área foi capturada **ou** que se está
dentro de um cluster e existem outros — e declara "identificar um bom start set" **problema em
aberto**, sem bala de prata. *(Procedência: Claude leu o texto completo em 19/09;
`docs/artigos/notas-wohlin-2014.md`. Pedro não leu — não citar em texto assinado sem a leitura dele.)*

**Medição que motivou a regra (22/09, nível 3, sobre as 58 obras que entraram na Fase 1):** os **8
mais citados são todos de 2020–2021** — citação é, em boa medida, idade. Um conjunto inicial "os 3
mais citados" daria três surveys **pré-LLM**, e divisões nascidas com os LLMs (serving, KV cache,
decodificação especulativa) ficariam fora do conjunto que decide a saturação. A distribuição por ano
é **bimodal** — 2020: 11 · 2021: 7 · **2022: 3** · 2023: 5 · 2024: 18 · 2025: 7 — com vale em 2022.
Sobreposição de autores entre os 5 mais citados: **nenhuma** — o risco aqui é de **era**, não de grupo.

**(b) Composição do conjunto inicial — a regra.** Os ≥ 3 surveys que abrem a saturação (do mapa ou de
uma divisão) devem ter:
- **autores disjuntos** entre si;
- **venues distintos**;
- **≥ 1 de cada pico da distribuição de anos do próprio retorno** — a distribuição é olhada no bruto
  antes de escolher; a regra é genérica, não presa a 2020/2024;
- termos de origem diferentes do pool quando possível (o ponto dos **sinônimos** em Wohlin §3.1:
  não capturar uma terminologia só).

Citação sozinha **não** ordena o conjunto inicial. *(Origem: a lista de Wohlin §3.1 — comunidades
diferentes, diversidade de editoras/anos/autores, sinônimos — aplicada aos nossos dados. O próprio
Wohlin registra que o start set da replicação dele tinha os 3 papers com um autor em comum e estava
"longe de perfeito".)*

**O detector de cluster.** Registrar, a cada survey lido, **quantas divisões novas ele trouxe**. Com
conjunto inicial bom, a curva **cai**. Se **não cair**, a hipótese não é "área larga": é **cluster
perdido** — volta-se ao conjunto inicial e busca-se de novo com sinônimos do pool, antes de declarar
saturação. *(Lições 7 e 8 de Wohlin 2014, licenciadas; a lição 9 dele **não** serve aqui — ele avisa
que a matriz de citação não detecta cluster independente.)*

**Teste da bimodalidade — instrumento nosso, não de Wohlin ⟨rev-27⟩.** Hipótese a testar na Fase 2:
*a área tem duas literaturas — compressão pré-LLM, herdeira de visão/CNN, e inferência/serving de
LLM — que se citam pouco.* Teste: verificar, pela API de referências do Semantic Scholar, **se os
surveys de 2023–2025 citam os de 2020–2021**. A ressalva de Wohlin (matriz não detecta cluster) é
sobre cluster **desconhecido**; aqui os dois grupos já estão no registro, e a pergunta é a relação
entre dois conjuntos conhecidos — por isso o teste vale, **mas é nosso, e não se apresenta como
método de Wohlin**. Enquanto não for testada, é **suspeita com evidência fraca** (distribuição de
anos em nível 3), não achado — e não entra no mapa como divisão.

⟨rev-28⟩ **Onde o resultado do teste entra, se der positivo — escolha delegada pelo Pedro ao Claude
em 22/09** (*"pra evitar meu viés, vou deixar você escolher"*): **não vira divisão.** A era entra como
**atributo de cada divisão** (coluna `era` em §8: o ano do seminal que a abriu) e o fato "duas
literaturas que se citam pouco" entra no **pilar história**, que é onde mora como a área veio a ser.
Motivo: divisão só existe se um survey aprovado a declarar (§9), e nenhum survey declara "pré-LLM"
como divisão — como divisão, seria taxonomia nossa entrando pela porta dos fundos, e o mapa passaria
a misturar dois eixos (técnica e era). Como atributo, a informação é a mesma e o eixo do mapa
continua único. Reversível: se surveys passarem a declarar divisão por era, a regra normal de §9 a
promove.

## 6. Profundidade de leitura no screening ⟨rev-33⟩

A leitura tem **duas funções**, com regras diferentes (Pedro, 22/09):

- **Classificar** — entra / não entra, em que divisão. Regra: a **escada** de §6.1 — sobe um degrau
  só quando o de baixo não bastou.
- **Extrair** — taxonomia, ferramentas, referências, termos. Não serve para decidir: é o que a fonte
  entrega à Etapa 1. Regra: a **tabela fixa** de §6.2, lida **inteira em toda fonte que entrou**,
  qualquer que tenha sido o degrau em que ela foi classificada.

Motivo da mudança: Petersen et al. 2008 — resumos enganam; não pré-especificar que só certas partes
do paper podem ser lidas; ler mais fundo quando não der para classificar. A versão anterior deste §6
fazia o contrário: a tabela era **teto** e o que passasse dela virava "dúvida".

### 6.1 Escada de classificação ⟨rev-33⟩ — decidida pelo Pedro em 22/09

**abstract -> introdução -> conclusão.** Vale para **paper** (survey, seminal, artigo); livro/capítulo e documentação não têm abstract e seguem a leitura da tabela de §6.2 (Pedro, 22/09, N5). Para no primeiro degrau que decide. **A escada é o limite:**
não há teto de tempo (o antigo "se não decidir em 5 minutos, não entra" saiu). Chegou ao topo e não
decidiu -> **dúvida** (§8.1). O registro anota o degrau em que a fonte foi classificada.

**Abstract ausente** (na execução 2, 66 das 154 obras ficaram sem abstract — a busca não pedia o
campo; o bulk do S2 o devolve quando pedido, mas não para toda obra): primeiro **buscar o abstract** por outra rota — arXiv
id (29 das 66) ou DOI (36 das 66); só se a busca falhar, **subir para a introdução**. Classificar só
pelo título não é degrau.

### 6.2 Extração fixa por tipo de fonte

Definida pelo Claude por delegação do Pedro, com o objetivo da Etapa 1 e as regras anteriores em
mente (os surveys corrigem o mapa; a saturação precisa detectar "novo"; a Fase 2B precisa das
referências).

| Tipo | O que se extrai de toda fonte que entrou | Por quê |
|---|---|---|
| **Survey** | resumo · introdução · **seção/figura de taxonomia** · títulos de todas as seções · conclusão / *future directions* · **referências extraídas em forma estruturada, com a seção em que cada uma foi citada** ⟨rev-16⟩ ⟨rev-24⟩ · **ferramentas nomeadas pela fonte** ⟨rev-29⟩ | a taxonomia corrige §2 e dispara §5; introdução e conclusão carregam história e problemas abertos; as referências alimentam a Fase 2B |
| **Livro / capítulo** | sumário · prefácio · introdução do capítulo | decide se cobre a divisão; prefácio costuma ser a melhor fonte de história |
| **Paper seminal** | resumo · introdução (contribuições declaradas) · figura principal do método · tabela principal | o bastante para posicioná-lo e extrair o vocabulário que ele introduziu; **leitura integral é Etapa 1** |
| **Artigo científico** (não seminal; inclui paper de sistema) | título · resumo · figura 1 · conclusão | posicioná-lo e extrair o vocabulário |
| **Documentação** (só ferramentas) | página de visão geral | §3 |

Regras transversais:
- Nada lido em nível de screening conta como conceito aprendido.
- ⟨rev-33⟩ Fonte que chega ao topo da escada (§6.1) sem decisão vira **"dúvida"** no registro (resolução em §8.1).
- ⟨rev-1⟩ **Conceitos assumidos:** toda fonte screenada produz a lista dos termos que ela **usa sem
  definir**. Cada termo vira candidato a conceito. Um conceito está **coberto** quando tem fonte
  própria (seminal ou livro/capítulo) no registro; **descoberto** enquanto não tiver. É o teste
  "self-attention": se o alvo é transformer e self-attention aparece assumido em toda fonte, ele
  precisa de linha própria. A lista de §1.1 é o ponto de partida; esta regra é o que a completa.

## 7. Procedência — 3 → 2 → 1, sem degrau novo

- **Nível 3 = o screening.** Um agente faz a leitura de §6 e devolve o registro. É triagem: decide o
  que entra, não ensina nada, nunca cita.
- **Nível 2 = Claude lê o texto completo** do que entrou e produz notas.
- **Nível 1 = Pedro lê o original.** Só isso conta como conceito aprendido e só isso é citável em
  texto assinado por ele.

O screening inteiro roda em nível 3 e é delegável. A subida 3 → 2 → 1 é a Etapa 1 propriamente dita.

⟨rev-15⟩ **O que "versão simples" do nível 3 significa — extração, não interpretação.** O agente
devolve, para cada fonte: seção de taxonomia **transcrita**; títulos de seções; contribuições
declaradas **verbatim** (o parágrafo "our contributions are…"); lista de referências estruturada
(§8, identificador) **com a seção citante** ⟨rev-24⟩; conceitos assumidos (§6); ⟨rev-29⟩ **ferramentas nomeadas pela fonte** — transcritas como aparecem, com a atividade que a fonte declarar para cada uma (§3.3). É a rota de descoberta mais barata do pilar ferramentas: os surveys de serving nomeiam as pilhas que a área usa, e a extração já os lê. **O agente não julga relevância** e não resume o
método com as próprias palavras — foi assim que o Agrawal passou como "incógnita" no nível 3 e o
mecanismo dele só apareceu no nível 2. A filtragem (§10) é do Pedro, sobre extração.
**Falha de extração:** se `pdftotext` falhar ou sair ilegível, tentar outra rota (URL do publisher,
versão HTML, arXiv) **antes** de registrar "ilegível" — e "ilegível" nunca vira registro permanente
sem uma segunda tentativa documentada.

## 8. Registro

Um **arquivo único com tabela** (o screening) **+ um arquivo de notas por fonte lida em nível 1**.

- ⟨rev-35⟩ Tabela: **`screening/registro-etapa1.md` + `screening/registro-etapa1.csv`** (Pedro, 22/09: .md + planilha, O3; nome escolhido pelo Claude por delegação dele, J3). O .md é o que se lê; o .csv é o que se conta e plota (abre no Excel) — mesmas linhas, o .csv é gerado do .md. Colunas — as originais do Pedro e as adicionadas
  pela revisão ⟨rev-4⟩ ⟨rev-16⟩ ⟨rev-19⟩:

| Coluna | Origem | Conteúdo |
|---|---|---|
| divisão | original | conforme mapa de §9 (ou "mapa" para surveys da área) |
| pilar | original | história · divisões · **conceitos** · vocabulário · ferramentas ⟨rev-28⟩ (era "fundamentos"; ver §1.4) |
| tipo de fonte | original | §3 |
| referência | original | autores, título, ano |
| **identificador** | rev-16 | DOI ou arXiv id; sem identificador não entra na Fase 2B |
| **venue** | rev-19 | regra já em vigor: *Comments* do arXiv ou página do publisher; rodapé de PDF não é venue |
| como foi achada | original | busca por título · ementa de curso · interseção de surveys (Fase 2B) · inclusão forçada · bola de neve |
| **fonte de origem** | rev-19 | qual survey/curso levou até ela — a bola de neve visível |
| nível de procedência | original | 3 / 2 / 1 |
| decisão | original | entra / não entra / dúvida |
| motivo | original | uma linha |
| **termos** | rev-4 | introduzidos pela fonte + assumidos por ela (alimenta o glossário) |
| **data** | rev-19 | quando foi screenada |
| **origem** | rev-20 | `etapa-1` ou `etapa-3` (ver §12) |
| **atividade** | rev-28 | o que a ferramenta executa (§3.3), **só quando a fonte declara**: servir, quantizar, converter formato, medir latência, compilar kernel... Vazio para fonte que não é ferramenta e não declara atividade |
| **era** | rev-28 | para linhas de divisão: ano do seminal que a abriu — atributo da divisão, **não** divisão (§5.3) |
| **arquitetura** | rev-23 | faceta do mapa (§9.1): `encoder-only` · `decoder-only` · `encoder-decoder` · `transformer (família não declarada)` · `pré-transformer/CNN` · `indeterminado`. **Só o que a fonte declara** (título, escopo, seção, frase do tipo "we focus on"); não declarou, é `indeterminado` — inferir é interpretação, proibida no nível 3 (§7). Mais de uma família na mesma fonte: registrar todas, separadas por `+` |

- ⟨rev-35⟩ **O esquema evolui durante a extração** (Pedro, 22/09, O1; Petersen et al. 2008): categoria
  nova, fusão ou divisão de categoria acontecem enquanto se extrai, não numa etapa posterior. Cada
  mudança gera **nova versão do mapa** (§2.3), com data e motivo, e as linhas já lançadas são
  reclassificadas.
- ⟨rev-35⟩ **Frequência por categoria** (O2): a tabela produz, a cada volta, a contagem por divisão x
  pilar x arquitetura — é o insumo do bubble plot (§9.1).
- ⟨rev-23⟩ **As três facetas do mapa** (Pedro, 22/09) são colunas desta tabela e existem antes da
  Fase 2, porque é a extração que as preenche: **divisão** (emergente, §9) · **pilar** (história ·
  divisões · conceitos · vocabulário · ferramentas) · **arquitetura** (acima). Ver §9.1.
- Notas: `docs/artigos/notas-<autor>-<ano>.md`, padrão já em uso; nível 2 e nível 1 marcados item a
  item, como em `docs/pesquisa/secao-dsbs-cabeca-auxiliar.md`.
- ⟨rev-4⟩ **Glossário:** `glossario-etapa1.md`, alimentado pela coluna *termos*. Cada termo: definição
  em uma linha, fonte onde foi definido (não onde foi assumido), divisão. É o pilar vocabulário
  materializado.

### 8.1 Resolução de "dúvida" ⟨rev-17⟩

⟨rev-33⟩ Com a escada de §6.1, a dúvida deixa de ser o caminho normal de quem pede mais leitura:
nasce só quando **abstract, introdução e conclusão foram lidos e ainda assim não se decidiu**.
Dúvida não fica para a Etapa 1 (que só lê o que entrou). Regra: o Claude lê **a seção em questão**
(nível 2 parcial, limitado à seção) e devolve o fato; o Pedro decide entra/não entra. Prazo: antes
de declarar a divisão saturada.

## 9. Saída do screening

**Lista de fontes por divisão + mapa das divisões da área (uma página).** Sem trilha ordenada de
leitura — a ordem se decide no início da Etapa 1, com a lista e o mapa na mão.

⟨rev-18⟩ **Reconciliação de taxonomias — refeita em 16/09.** A proposta "espinha dorsal = survey
mais recente" foi **derrubada pelo Pedro**: *"às vezes um paper mais recente oferece uma abordagem
não tão boa quanto o antigo, e o contrário também; e o antigo tem mais citações por ser antigo"* —
nem recência nem citação decidem. **Regra nova — união com consolidação** (proposta do Claude,
aprovada pelo Pedro em 16/09 "se for a melhor opção"; avaliação registrada abaixo): o mapa não adota
a taxonomia de nenhum survey. É construído por **união**: cada divisão que aparece em qualquer survey
aprovado entra no mapa com a lista dos surveys que a usam. Divisão que só aparece em **1** survey é
marcada *singular* e só se consolida quando um segundo a confirma (ou o Pedro a mantém com motivo).
Sobreposições e nomes diferentes para a mesma coisa são **mescladas pelo Pedro**, com o motivo na
linha. Os termos do pool (§2.1) são confrontados com a união, item a item, por origem: encontra
divisão / vira subdivisão / fora da área por §1.2 / não existe com esse nome. O mapa é do Pedro; os surveys são
evidência, não autoridade.

*Por que união e não as alternativas:* (a) survey mais recente manda — derrubado pelo Pedro; (b) mais
citado manda — envelhece pelo mesmo motivo; (c) interseção (só divisão em que ≥ 2 surveys concordam)
— perde as divisões recentes, que só um survey ainda cobre, e nesta área o recente é o serving; (d)
união com consolidação — é (c) sem perder o recente, e a única que não elege autoridade. Fraqueza
conhecida: surveys cortam em granularidades diferentes (um trata "quantização" como divisão; outro
separa PTQ e QAT), o que obriga mesclagem manual — e a mesclagem manual é o exercício de aprender as
divisões da área, que é o que a Etapa 1 pede.

### 9.1 Mapa visual — bubble plot ⟨rev-23⟩ — decidido pelo Pedro em 22/09

Saída visual do mapa, no formato de Petersen et al. 2008 (*systematic map bubble plot*): **divisão no
eixo Y**, uma faceta no **semiplano esquerdo** e outra no **direito**, bolha proporcional à frequência.

- Semiplano esquerdo: **pilar**. Mostra a cobertura da Etapa 1 por divisão — é a régua do professor.
- Semiplano direito: **arquitetura** (Pedro, 22/09). Escolhida por ser a única das candidatas
  **ortogonal à divisão**: eixo (i/ii/iii) de §1.2 é quase função da divisão (quantização → ii,
  decodificação especulativa → i), então repetiria no semiplano o que o eixo Y já diz; família de
  arquitetura não é derivável do nome da técnica — a diferença entre (quantização, encoder) e
  (quantização, decoder) é informação nova. É também o pilar fixo de §1.1 e o que o Pedro declarou
  querer aprender neste ciclo.
- **Eixo de §1.2 anotado no eixo Y** (Pedro, 22/09): cada divisão leva o eixo que a faz pertencer à
  área — (i) inferência · (ii) memória/hardware · (iii) dado rotulado, ou combinação. Não é faceta:
  é propriedade da divisão, não da obra, então sai sem custo de extração e sem gastar semiplano.
  Dá de brinde o teste do próprio §1.2 — se toda divisão cair em (ii), o critério não parte a área.
- **`indeterminado` é categoria visível no gráfico**, nunca omitida. Medição por título em 22/09
  (nível 3, aproximação para estimar custo): das 58 obras que entraram na Fase 1, **30 não declaram
  família no título** — um vazio de encoder pode ser artefato de não-declaração, e o gráfico tem de
  deixar isso ver.
- Todo gráfico declara **N**, a **unidade** (survey, não paper) e a **data**.
- O mapa continua sendo o de §9 (uma página, união com consolidação); o bubble plot é a sua
  visualização, não o substitui.

**Dois momentos, duas unidades ⟨rev-24⟩ — decidido pelo Pedro em 22/09:**

| | **A — durante** | **B — no fim** |
|---|---|---|
| unidade da bolha | **survey registrado** | **paper referenciado** pelos surveys |
| quando | a cada rodada de saturação (v1, v2+), junto com a versão do pool | uma vez, com o screening concluído (§13) |
| para que serve | **instrumento do loop** (§2.1, pool §3): célula vazia ou bolha de 1 levanta a pergunta "é lacuna da **área** ou lacuna da **busca**?" — se for da busca, o pool ganha termo e a rodada seguinte roda de novo | entregável: o mapa da área com o volume por trás de cada divisão |
| custo | zero — pivô da tabela de §8 | zero de leitura nova, **desde que** a extração tenha guardado a seção citante (⟨rev-24⟩ em §6 e §7): o paper citado na seção X herda a divisão X, sem ninguém classificar paper por paper |
| o que afirma | "dos surveys que li, tantos cobrem X na família Y" | "a literatura que os surveys da divisão X citam se distribui assim" |

**Precondição de B, registrada como tal:** sem a seção citante, B exigiria reler os surveys. É por isso
que ⟨rev-24⟩ entra em §6 e §7 **antes** da Fase 2. Em B, `pilar` e `arquitetura` só existem para os
papers que subirem de nível; para o resto, o semiplano correspondente fica `indeterminado` — o
gráfico declara isso.

## 10. Orçamento de tempo e pipeline

- **16–24 horas semanais.**
- **Prazo:** o professor não deu e "provavelmente nem vai dar". Sem prazo externo, o marcador é a
  cadência dos gates (semanal): a cada gate, planejado × feito (métricas em §13).
- **Pipeline (palavras do Pedro):** **screening geral → screening do screening → filtragem → leitura
  completa.** Lido contra §7: as duas primeiras fases são nível 3 (agente, largo e depois fino
  sobre os candidatos); a filtragem é a decisão do Pedro sobre a tabela de §8; a leitura completa é
  a subida 2 → 1. A divisão de horas entre as fases não foi fixada.

## 11. Procedimento ⟨rev-12⟩ ⟨rev-21⟩

O pipeline de §10, com entrada e saída por fase. Bases e janela confirmadas pelo Pedro em 16/09
("perfeito").

**Bases:** arXiv · ACL Anthology · Semantic Scholar (também para contagem de citação) · Google
Scholar (conferência) · livros via ementas dos cursos de §4.1 e via referências dos surveys.
**Bases na execução 3** (Pedro, 22/09): **Semantic Scholar e arXiv**; a ACL Anthology entra **pelo S2**
(que indexa os venues da ACL — a Anthology não tem API de busca); **Google Scholar fora por ora**
("talvez depois") — é manual e bloqueia automação.
**Janela:** surveys **2020+** para mapa e divisões (a área mudou de forma com os LLMs); **sem
janela** para seminais e história. **Língua:** inglês.

⟨rev-30⟩ **População do screening — decidida pelo Pedro em 22/09.** A população é **os surveys da
área, sem piso de citação** (opção "b"): as palavras de tipo (`survey | review | overview | taxonomy`)
ficam na string; o piso sai. Medição de 22/09 no Semantic Scholar, com a string-mãe da execução 2
(2020+, Computer Science):

| população | palavras de tipo | piso | total |
|---|---|---|---|
| o que rodou na execução 2 | sim | >= 60 | 103 |
| **adotada** | **sim** | **—** | **863** |
| Petersen puro (sem palavras de tipo) | não | — | 16.821 |
| (recurso lateral: papers mais citados da área) | não | >= 60 | 793 |

**Por que não o Petersen puro:** 16.821 é mapping study de verdade — mudaria §2, §6 e §7 inteiros, e
o mapa passaria a vir de keywording de papers primários em vez de taxonomia de survey. Fica fora por
orçamento, e a restrição é declarada (pendência C1).
**Correcão de registro:** o número 41.412 da execução 1 **não** era esta população — foi medido com a
string suja, antes de `resource-efficient`/`on-device` saírem para a filha `edge`. A população real
sem piso é **863**, e não dezenas de milhares.
**Imprecisão conhecida:** o `query` do Semantic Scholar procura em título **e resumo**, então um paper
que escreve "we survey related work" no resumo entra nos 863 sem ser survey. Some na triagem por
título; infla o número de partida.
**As outras bases somam:** 863 é só o S2. arXiv, ACL Anthology e Google Scholar acrescentam, com
sobreposição alta — o total após dedup é a entrada real da Fase 1.
**O recurso lateral (793):** não é população do mapa; é onde moram os **seminais**, e serve à cláusula
"top-3 mais citados da divisão" de §4, quando as divisões existirem.

**Fase 1 — screening geral** (nível 3, agente). *Entrada:* o pool v0 (`docs/screening/pool-termos-etapa1.md`) e as strings compostas dele.
*Como:* (1) **string-mãe** nas bases (mapa da área), depois **strings-filhas** por grupo — todas
geradas do pool, com os filtros de §3.2/§11 embutidos; (2) ementas dos cursos de §4.1; (3) referências dos surveys encontrados (bola de
neve, uma rodada). Aplicar §3.2. *Saída:* lista de surveys candidatos, registrados com decisão
"entra" ou "não entra — sem filtro de qualidade".

**Fase 2 — screening do screening** (nível 3, agente). *Entrada:* surveys que entraram. *Como:*
leitura de §6 por tipo, extração de §7, conceitos assumidos, referências estruturadas. Rodar a Fase
2B (interseção) por divisão assim que houver ≥ 3 surveys dela. *Saída:* tabela de §8 preenchida com
surveys, seminais candidatos (b, c, forçados), conceitos candidatos, ferramentas e atividades candidatas.

**Fase 3 — filtragem** (Pedro). *Entrada:* a tabela. *Como:* decisão linha a linha (entra / não entra
/ dúvida), com motivo; dúvidas por §8.1; saturação por §5, primeiro do mapa, depois por divisão;
mapa por §9. *Saída:* screening da divisão fechado; mapa das divisões.

**Fase 4 — leitura completa** (Claude nível 2 → Pedro nível 1). *Entrada:* o que entrou. *Como:* notas
em `docs/artigos/`; glossário atualizado; conceitos de §1.1 e §6 marcados cobertos. *Saída:* Etapa
1 — o que, por regra própria, ainda será escrito.

### 11.1 O loop por voltas ⟨rev-31⟩ — decidido pelo Pedro em 22/09

A Fase 1 não é uma passada: é um **funil por voltas numeradas**, cada uma terminando numa **decisão
do Pedro**. Motivo dele, em 22/09: a população de 863 é só do Semantic Scholar — somadas as outras
bases e tirada a duplicata, a entrada real é maior do que cabe numa triagem só.

**Forma de uma volta:** bruto (todas as bases, sem piso) -> dedup -> triagem em nível 3 pela escada de §6.1
(relevância por §1.2 e §1.2.1) -> **proposta de agrupamento** (ver abaixo) -> **decisão do Pedro** -> entrada da
volta seguinte. O piso de §3.2 só entra no **registro**, nunca na busca (⟨rev-30⟩).

⟨rev-35⟩ **Relato de funil por volta — obrigatório** (Pedro, 22/09, L1): toda volta termina com a
contagem por estágio (bruto por base -> após dedup -> por decisão de triagem -> por grupo), no estilo
da tabela de artigos incluídos de Petersen et al. 2008. É o número que mostra o processo.

**Pastas** (Pedro, 22/09): `docs/screening/papers/volta-N/` recebe os papers baixados em cada volta; depois
dos clusters, eles são **movidos** para `docs/screening/papers/<cluster>/`. Apagar qualquer coisa só com
pedido explícito dele — e ao fim de cada volta o Claude lista o que virou lixo e pergunta.

⟨rev-36⟩ **Bilhete por tamanho de técnica** (Pedro, 23/09): técnica (termo do pool) com **até 20 obras**
na população filtrada -> as obras dela recebem **golden ticket** e vão **direto para a última fase**,
sem amostragem nem filtragem intermediária; técnica com **21 a 50 obras** -> as obras dela pulam para a
**penúltima filtragem**. Motivo dele: categoria pequena não precisa de mais filtragem — amostrar custa
o mesmo que ler tudo e arrisca perder o pouco que existe. Primeira aplicação (camada C da execução 3,
14.901 obras): golden ticket = *reasoning distillation* (3 obras); penúltima = *early exiting* (42),
*KV cache compression* (38), *continuous batching* (48) — 125 obras. Obra que casa técnica pequena **e** técnica
grande: **vale o bilhete mais favorável** (Pedro, 23/09). Em aberto: o que são exatamente a
"última fase" e a "penúltima filtragem" no desenho dos agentes, ainda por fazer.

**O filtro de cada volta ORDENA, não APAGA** (Pedro, 22/09). Nenhum item é eliminado por não formar
grupo: o descartado fica no bruto com o motivo e a volta em que caiu, e **volta a ser candidato** se
uma rodada posterior abrir grupo novo. Motivo: divisão pequena não forma grupo na volta 1 e sumiria —
seria o viés de confirmação entrando pela porta do orçamento.

**Parada por número, além da saturação.** As voltas param quando o número cabe no orçamento **ou**
quando a volta não abre grupo novo (§5). **Alvo provisório: ~50 documentos no total** (Pedro, 22/09:
*"em volta de 50 documentos totais, mas ainda não decidi, tenho que ver (ver, gráficos, tabelas, etc)
antes de decidir"*). **Não está fechado** — falta separar quantos vão para **leitura resumida**
(extração nível 3, Fase 2) e quantos para **leitura integral** (nível 2 -> 1), e a decisão dele é
sobre dados: ele quer ver os gráficos e as tabelas das primeiras voltas antes de fixar. Âncora para
calibrar: a saturação de §5 implica ~3 surveys para o mapa + ~3 por divisão.

**Proposta de agrupamento ⟨rev-32⟩ — decidido pelo Pedro em 22/09.** A cada volta, o Claude agrupa os
candidatos por tema e entrega a proposta ao Pedro, que decide a prioridade da volta seguinte.

*Por que isto não viola §7.* O §7 proíbe **interpretação no registro** — a regra nasceu do **Agrawal**,
que passou pelo nível 3 como "incógnita" porque a extração não pegou o mecanismo, e o mecanismo era o
do tema. O princípio: **o registro é aquilo sobre o que o Pedro decide**; se contém interpretação do
Claude, ele decide sobre o Claude e não sobre a fonte. O agrupamento **não é entrada de registro** —
não é o que uma fonte diz, é proposta de como organizar candidatos — mas herda o mesmo risco se
chegar a **decidir o que cai**. Daí as quatro salvaguardas:

1. **Ordena, não apaga** (regra da volta, acima) — agrupamento nenhum elimina item.
2. **O grupo mostra sempre os membros**, título e identificador, nunca só o rótulo: a decisão do Pedro
   é sobre os itens, com o rótulo como índice.
3. **Artefato do Claude, datado, fora do registro** — arquivo próprio por volta,
   `screening/fase1/<AAAA-MM-DD>-volta-N-agrupamento.md`, aberto com "proposta do Claude, nível 3,
   não é taxonomia de fonte". Precedente: as sementes do Claude no pool têm origem separada (§2.2).
4. **Agrupamento não é divisão** — só survey aprovado cria divisão (§9). O agrupamento **morre na
   volta seguinte**; a divisão persiste. Nome de grupo nunca entra no mapa nem no pool por si.

## 12. Reaproveitamento da Etapa 3 ⟨rev-20⟩ — confirmado pelo Pedro em 16/09

`docs/pesquisa/artigos-verificados.md` já tem ~50 artigos verificados na fonte para a divisão *destilação de
raciocínio* (a do tema v3), e quatro em nível 2 com notas. Eles **entram no registro novo** com o
nível de procedência que já têm e `origem: etapa-3`. Não se refaz o que já foi feito; mas a divisão
ainda passa por §5 (saturação) como as outras, porque aquela busca foi de fronteira, não de mapa.

## 13. Critérios de conclusão e métricas de gate ⟨rev-21⟩

**Screening de uma divisão concluído:** saturação por §5 · seminais identificados por §4 · nenhuma
"dúvida" aberta · conceitos assumidos listados (cobertos ou marcados descobertos).
**Screening concluído:** mapa saturado (§5.1) · toda divisão do mapa com screening concluído ·
pilar arquiteturas com todos os itens de §1.1 com fonte no registro · mapa de §9 escrito.
**Etapa 1 concluída** (fora deste método, mas o alvo): todo conceito coberto tem fonte em nível 1;
todo seminal em nível 1; glossário fechado.

**Métricas de gate (planejado × feito, semanal):** divisões saturadas / total do mapa · fontes
registradas · fontes em nível 2 · fontes em nível 1 · conceitos cobertos / listados ·
⟨rev-26⟩ **voltas do checkpoint do nome da área** (§2.3), contra o teto de 8 ·
⟨rev-27⟩ **divisões novas por survey lido** (§5.3) — a curva do detector de cluster.

---

## Em aberto

1. ~~Nome do arquivo da tabela de registro~~ — decidido em 22/09 (§8).
2. ~~Data-alvo~~ ⟨rev-35⟩ **05/10 = Fases 1–3 até o mapa v1** (Pedro, 22/09, J1) — não só a lista de candidatos. Data-alvo da Etapa 1 inteira segue aberta.
3. Divisão de horas entre as quatro fases do pipeline (§10).
4. ~~Decisões da revisão~~ — todas fechadas em 16/09. Os defaults de §3.2 e §4 valem por omissão,
   com regra de calibração escrita, até o Pedro mandar mudar.

## Relação com o que já existe

- `docs/screening/pool-termos-etapa1.md` — o vocabulário versionado (v0) e as strings compostas dele, como texto.
- `docs/formulario-metodo-screening.md` — as dez perguntas com opções, porquês e efeitos de errar.
- `docs/revisao-metodo-screening-2026-09-15.md` — os 21 achados da revisão e o que cada `⟨rev-N⟩`
  corrige.
- `docs/pesquisa/metodo-busca-artigos.md` (09/09) — método de busca de **fronteira** para o tema; serve à Etapa 3.
  A Fase 2B dele volta aqui como critério de seminal (§4).
- `docs/pesquisa/artigos-verificados.md` e `docs/residencia/triagem-bibliografica.md` — resultado daquela busca; entram por §12.
- Procedência (§7) é a mesma regra permanente do `CLAUDE.md`.

---

## Resumo — critérios de aceite e de rejeição

Consolidação do que as seções acima decidem, para consulta rápida durante a filtragem (Fase 3). Cada
linha aponta a seção que a fundamenta; em conflito, vale a seção.

### Critérios de aceite

**Uma divisão entra no mapa se:**
- reduz custo de implantação em pelo menos um eixo — inferência, memória/hardware ou dado rotulado (§1.2);
- foi trazida como divisão por **≥ 2 surveys aprovados**, ou por 1 survey **e** decisão do Pedro com motivo na linha (§9);
- para PEFT/LoRA e casos análogos: o efeito na implantação existe, mesmo que a técnica aja no treino (§1.2).

**Um survey pertence à área se** (§1.2.1): cobre ao menos em parte um eixo de §1.2 (entra inteiro, como base) · trata infraestrutura de implantação ou hardware · é de aplicação específica e não há survey geral da divisão.

**Um survey entra no screening se satisfaz pelo menos um** (§3.2):
- venue com revisão por pares; ou
- **≥ 60 citações** no Semantic Scholar ⟨rev-30⟩ (era 100; o piso **não** é parâmetro de busca — só de registro); ou
- citado por ≥ 2 surveys já registrados.
E, para contar no mapa e nas divisões: publicado em **2020+** (§11). Para história: sem janela.

**Um paper é seminal da divisão se** (§4):
- é citado por ≥ 2 dos ≥ 3 surveys aprovados da divisão; ou
- consta na ementa de um curso de referência da lista de §4.1; ou
- está entre os 3 mais citados da divisão (inclusão forçada), mesmo sem os dois anteriores.

**Um artigo científico (não seminal) entra se** (§6):
- ⟨rev-33⟩ a decisão sai da escada de §6.1 (abstract -> introdução -> conclusão), sem teto de tempo; e
- serve de apoio a um pilar nomeado (história, divisões, conceitos, vocabulário, ferramentas).

**Um livro/capítulo entra se** (§6): o sumário + prefácio + introdução mostram que cobre uma divisão do mapa ou um conceito de §1.1.

**Uma ferramenta entra no pilar ferramentas se** (§3, §3.1):
- é software instalável (não técnica); e
- tem paper de sistema (fonte primária) **ou**, na ausência, documentação com página de visão geral.

**Um conceito está coberto se** (§1.1, §6): tem fonte própria (seminal ou livro/capítulo) no registro, na profundidade definida na tabela de §1.1 — plena, média ou leve.

**Uma fonte sobe de nível se** (§7): 3 → 2 quando o Claude lê o texto completo e produz nota; 2 → 1 quando o Pedro lê o original. Só nível 1 é citável.

**Uma divisão está screenada se** (§5.2, §13): ≥ 3 surveys lidos; survey novo não traz seminal nem conceito assumido novo; nenhuma dúvida aberta; seminais identificados; conceitos assumidos listados.

**O mapa está saturado se** (§5.1): ≥ 3 surveys da área lidos e o próximo não traz divisão nova.

**O screening está concluído se** (§13): mapa saturado; toda divisão screenada; todo item de §1.1 com fonte no registro; mapa de §9 escrito; confronto do pool (§2.1) feito.

### Critérios de rejeição

**Uma divisão candidata fica fora se:**
- não reduz custo em nenhum dos três eixos de §1.2 — ex.: eficiência de treino pura, sem efeito no modelo servido; "prompt engineering" será testado por esta regra;
- só aparece em 1 survey e o Pedro não a manteve com motivo — fica *singular*, não entra (§9);
- é nome alternativo de divisão já existente — mescla, com motivo, não entra em duplicata (§9).

**Um survey fica fora se:**
- não satisfaz nenhuma das três pernas de §3.2 — registrado como "não entra — sem filtro de qualidade", nunca descartado em silêncio;
- é anterior a 2020 e o uso pretendido é mapa/divisões (§11);
- ⟨rev-34⟩ aplica técnica da área a modelo fora do escopo de §1.3 — CNN, GNN, difusão (§1.2.1 b); a história de CNN vem dos seminais (§2.4), não de survey;
- ⟨rev-34⟩ é de aplicação específica e já existe survey geral da divisão (§1.2.1 c);
- ⟨rev-34⟩ não é survey (§3.4) — fica no bruto com o motivo e o destino de §3.4.

**Um paper fica fora como seminal se:** só tem contagem de citação a seu favor e não está no top-3 da divisão (§4) — citação não é critério de busca.

**Uma fonte fica fora do screening se:**
- é tutorial de conferência ou curso de referência usado *como fonte* (§3) — cursos só apontam seminais (§4);
- é documentação de ferramenta fora do pilar ferramentas, ou é tutorial/API em vez de visão geral (§3);
- está em outra língua que não inglês (§11);
- não tem identificador (DOI/arXiv id) resolvível — não entra na Fase 2B até ter (§8);
- ⟨rev-33⟩ a escada de §6.1 chegou ao topo (abstract, introdução, conclusão) sem decisão — vira **dúvida**, resolvida por §8.1 antes da saturação da divisão; não entra "por via das dúvidas".

**Uma extração de nível 3 é rejeitada se** (§7):
- contém interpretação do agente em vez de transcrição (taxonomia parafraseada, contribuições resumidas com palavras próprias, juízo de relevância);
- registra "ilegível" sem segunda tentativa documentada por outra rota.

**Uma citação é rejeitada em texto assinado pelo Pedro se** (§7, `CLAUDE.md`): a fonte não está em nível 1.

**Um venue é rejeitado se** (§8): a única evidência é o rodapé do PDF — vale o campo *Comments* do arXiv ou a página do publisher.

**Um termo do pool não vira divisão se** (§2.1): nenhum survey aprovado o traz como divisão — fica com veredito "sem retorno" ou "não existe com esse nome" no confronto, e é aposentado se além disso nenhum survey o usa; é dado, não erro.

