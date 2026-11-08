# Método de leitura e extração (30/09)

**Status: proposta do Claude, para o Pedro ajustar.** Pedido do Pedro (30/09): *"um método pra eu extrair exatamente
essas coisas que eu preciso de cada uma das obras"*. O método é o mesmo para qualquer obra; o que muda de uma obra para
outra é **quais campos ela preenche**, e isso você descobre na primeira passada, não antes.

**Bases:**
- Keshav 2007, *How to Read a Paper* (ACM SIGCOMM CCR, doi 10.1145/1273445.1273458). Lido pelo Claude na íntegra
  (3 páginas, cópia em `docs/artigos/`). De lá vêm as três passadas.
- Levac et al. 2010 e Kitchenham & Charters 2007 §6.4 (lidos pelo Claude). De lá vem a regra de **formulário de
  extração fixo, pilotado nas primeiras obras e revisado**.
- O nosso método (§1.4): o screening **mapeia, não julga se o resultado é verdadeiro**. Por isso a pergunta
  "Correctness" do Keshav fica de fora.

## 1. Para que você está lendo: o que precisa sair no fim

Tudo o que você extrai alimenta **cinco arquivos acumulados** em `docs/leituras/`. **Eles são o produto**: depois de algumas
obras, são o material do gate.

| Arquivo | O que junta | Serve a |
|---|---|---|
| `linha-do-tempo.md` | marcos: o que veio antes, o que cada obra abriu, com ano | **história** (Etapa 1, "TEMPO") |
| `mapa-divisoes.md` | as divisões da área e onde cada obra mora | **divisões** (Etapa 1) |
| `glossario.md` | termo, definição em uma linha, obra e página | **vocabulário** (Etapa 1) |
| `frameworks.md` | framework, tipo (software ou conceitual), atividade, onde viu | **ferramentas e frameworks** (Etapas 1 e 2) |
| `fila.md` | pré-requisitos que faltaram e referências fundadoras a ler depois | a **ordem** das próximas leituras |

Cada obra também ganha a sua ficha: `docs/leituras/fichas/<ano>-<primeiro-autor>.md`, a partir de `docs/leituras/modelo-ficha.md`.

## 2. As três passadas

### Passada 1: reconhecimento (5 a 10 minutos, em toda obra)

Leia **só**: título, abstract e introdução inteiros; os títulos das seções e subseções; a conclusão; as figuras e
tabelas de relance; as referências de relance.

No fim, responda no topo da ficha **cinco perguntas**:
1. **Tipo:** mapa (survey ou tutorial), fundador (abriu uma técnica), conceito (base que outros assumem) ou sistema
   (ferramenta ou framework)?
2. **Contexto:** de que problema ela parte e com que trabalhos ela conversa?
3. **Contribuição:** o que ela traz de novo, em uma frase?
4. **Lugar no mapa:** em que divisão da área ela mora?
5. **Decisão:** vale a passada 2? E o que eu preciso saber antes (pré-requisitos)?

**O tipo decide quais campos da ficha você preenche** (tabela da §3). Se faltar pré-requisito, anote em `fila.md` e
decida: ler o pré-requisito antes ou seguir assim mesmo.

### Passada 2: extração (até 1 hora)

Leia as seções que a passada 1 apontou, com atenção às figuras. **Pule provas e detalhes de experimento.** Preencha a
ficha durante a leitura, **com página em toda anotação**. No fim, você deve conseguir explicar a obra a alguém, com os
números principais, sem olhar.

### Passada 3: reconstrução (2 a 5 horas, só quando você decidir)

Reconstrua a obra como se fosse implementá-la (Keshav). Para nós, isso pode ser literal: **rodar o framework ou o
mecanismo** (o roofline de um modelo, um vLLM local, uma destilação pequena). É a passada do **saber fazer**. Ela vale
para as obras da trilha (destilação) e para os frameworks que você vai apresentar.

## 3. O que extrair: os campos da ficha

| # | Campo | Pergunta-guia | Onde costuma estar | Preencha quando a obra é… | Vai para |
|---|---|---|---|---|---|
| 1 | **Identificação e procedência** | o que eu li, de fato, e quando? | — | sempre | ficha |
| 2 | **Em três frases** | qual o problema, qual a resposta, qual o número principal (e em que condição)? | abstract, introdução, tabela principal | sempre | ficha |
| 3 | **História** | o que existia antes, segundo os autores? O que esta obra abriu ou continua? | introdução, trabalhos relacionados | sempre | `linha-do-tempo.md` |
| 4 | **Divisões** | em que divisão ela mora? Se é mapa: **como ela divide a área?** (copie a árvore) | figura de taxonomia, sumário | mapa (obrigatório); outras (só o lugar) | `mapa-divisoes.md` |
| 5 | **Conceitos** | que mecanismos ela explica? Reescreva cada um com as suas palavras | seção de método ou de fundamentos | fundador, conceito, mapa | ficha |
| 6 | **Vocabulário** | que termos eu não conhecia? Defina cada um em uma linha | fundamentos, notação, primeira vez que o termo aparece | sempre | `glossario.md` |
| 7 | **Frameworks** | **software:** que ferramenta ela usa, propõe ou libera, e para qual atividade? **Conceitual:** que diretriz ela prescreve ("se X, faça Y"; "primeiro A, depois B")? | método, implementação, discussão, código liberado | sistema (obrigatório); outras (quando houver) | `frameworks.md` |
| 8 | **Arquitetura** | trata encoder, decoder ou encoder-decoder (ou CNN e RNN)? O que muda com a família? | método, experimentos | sempre que o texto distinguir | ficha |
| 9 | **Atualidade** | a própria obra diz o que ainda falta ou o que vem depois? | conclusão, limitações, trabalhos futuros | sempre | ficha |
| 10 | **Pré-requisitos** | o que tive de procurar para entender? | — | sempre | `fila.md` |
| 11 | **Ligações** | que referências a obra trata como fundadoras? Com quais obras da lista ela conversa? | introdução, trabalhos relacionados | sempre | `fila.md` (as fundadoras) |
| 12 | **Como pensar** | que forma de raciocinar do autor vale copiar? (uma ou duas linhas; o seu saber ser) | discussão, motivação | quando houver | ficha |
| 13 | **Dúvidas** | o que não entendi? | — | sempre | ficha |

## 4. Regras

1. **Página em toda anotação.** É a procedência: no termo de entrega só entra o que você leu (regra do projeto), e a
   página prova isso.
2. **Com as suas palavras.** Citação literal só entre aspas, curta, com página.
3. **Não julgue se o resultado é verdadeiro.** Anote o número e a condição ("4× menor, em AlexNet, sem perda de
   acurácia"), não a validade. Julgar é revisão sistemática, e o professor pediu screening.
4. **Os arquivos acumulados crescem a cada obra.** Um termo entra no glossário uma vez; se reaparece, acrescente a
   nova fonte. Um framework visto em duas obras ganha duas fontes.
5. **Revise o modelo depois das duas primeiras obras** (Levac 2010: o formulário é iterativo e se pilota nas primeiras
   obras). Campo que nunca se preenche sai; o que faltou entra. Anote a revisão no topo do modelo, com a data.
6. **Ficha do agente só depois.** As fichas dos agentes (`docs/screening/fase1/2026-09-27-lista-v2-fichas.md`) existem para
   cada obra. Leia a do agente **só depois de terminar a sua**, para não ser levado por ela. Onde as duas
   discordarem, anote: ou você achou algo que o agente perdeu, ou o contrário.
7. **Tempo:** passada 1 em até 10 minutos; passada 2 em até 1 hora; passada 3 só quando você decidir. Se a passada 2
   travar (Keshav: termos novos demais), volte para `fila.md` e leia o pré-requisito antes.
