# Método de leitura rápida: caça dirigida (01/10)

Pedido do Pedro (01/10): *"leitura mais rápida mas que ainda extrai os mesmos ganhos"*. Os **13 ganhos** da versão
detalhada (`docs/metodo-de-leitura-v1-detalhado.md`) continuam todos aqui. O que muda é o caminho: em vez de ler o
paper e depois procurar o que extrair, **você vai direto aos lugares onde cada ganho costuma estar**. São cinco paradas,
cerca de **35 minutos por obra**, contra cerca de 1h30 da versão detalhada.

## A ideia em uma linha

Todo paper põe as mesmas coisas nos mesmos lugares: a contribuição no fim da introdução, a história no começo dela, o
mecanismo na figura principal, as limitações na conclusão. **Saber onde procurar é o que economiza tempo.**

## As cinco paradas

| Parada | Onde | Tempo | O que você colhe (ganhos) |
|---|---|---|---|
| **1. Promessa** | abstract + **último parágrafo da introdução** (onde costuma estar "our contributions are…") | 5 min | **tipo** da obra (mapa, fundador, conceito, sistema) · **três frases**: problema, solução, número principal com a condição |
| **2. Origem** | **primeiros parágrafos da introdução** + primeiro parágrafo dos trabalhos relacionados | 5 min | **história** (o que havia antes, o que ela abriu) · **ligações** (as 2–3 referências que ela trata como base) · **como pensar** (o critério que motiva os autores) |
| **3. Núcleo** | **figura principal** + a seção que a explica (num survey: a figura da taxonomia, os títulos das seções e as tabelas-resumo) | 15 min | **conceitos** (o mecanismo, com as suas palavras) · **divisões** (onde mora; num survey, a árvore) · **arquitetura** (a família de modelo) · os **termos** definidos ali |
| **4. Caça por palavra** | **Ctrl+F** no PDF (lista abaixo) | 5 min | **frameworks** (software e receitas) · o resto do **vocabulário** · a **arquitetura**, se a parada 3 não deu |
| **5. Fecho** | **conclusão + limitações** (ou "future work", "discussion") | 5 min | **atualidade** (o que falta, o que vem depois) · **dúvidas** · **pré-requisitos** (o que você travou nas paradas anteriores) |

**Procedência** é o ganho que sai de graça: as paradas que você fez **são** a lista do que leu.

### As palavras da parada 4

| Para achar | Procure |
|---|---|
| framework de software | `github` · `code` · `open-source` · `implement` · `library` · `release` |
| framework conceitual (receita) | `we recommend` · `guideline` · `should` · `first` · `then` · `rule of thumb` · `in practice` |
| vocabulário | `we define` · `refer to` · `called` · `denote` · `i.e.` · `terminology` |
| arquitetura | `encoder` · `decoder` · `autoregressive` · `bidirectional` · `CNN` · `RNN` |

Para cada resultado, leia só a frase em volta. Se ela servir, anote com a página e siga.

### A parada 3 muda conforme o tipo (descoberto na parada 1)

- **Mapa (survey):** não leia os trabalhos citados. Leia **como o autor agrupa**: a figura da taxonomia, os títulos das
  seções e as tabelas que comparam métodos. O ganho principal é a árvore de divisões.
- **Fundador:** a figura do método e a seção do método. Pule provas e hiperparâmetros. Diante de uma equação, leia a frase
  de antes e a de depois.
- **Conceito:** a figura da arquitetura e o "por que" das escolhas.
- **Sistema:** a figura da arquitetura do sistema e a seção de uso (API, como rodar).

## Como escrever sem perder tempo

- **Escreva direto nos arquivos acumulados** de `docs/leituras/` (linha do tempo, mapa, glossário, frameworks). A ficha da obra
  fica só com o que é dela: as três frases, os conceitos, como pensar e as dúvidas. Assim não há etapa de "copiar depois".
- Formato curto: `• ideia (p. N)`. Página em toda linha.
- Com as suas palavras; trecho literal só curto e entre aspas.

## Quatro regras

1. **Página em toda anotação.** No gate só entra o que você leu, e a página prova isso.
2. **Não julgue se o resultado está certo.** Anote o número e a condição. O pedido é screening, não revisão sistemática.
3. **Atalho permitido: use a ficha do agente só como guia de ONDE ler, nunca de O QUE.** O campo "por onde ler" de cada
   ficha (`docs/screening/fase1/2026-09-27-lista-v2-fichas.md`) dá as páginas, e isso economiza a busca da parada 3. Não leia
   o resumo nem o veredito antes de terminar: depois, use-os para conferir.
4. **Se travar, não force.** Termo que impede de entender a contribuição: procure em até 5 minutos. Se não resolver,
   anote em "pré-requisitos" e siga para a próxima parada.

## Quando ir além das cinco paradas

Só em duas situações: **obras da sua trilha** (destilação) e **frameworks que você vai apresentar no gate**. Aí vale a
reconstrução da versão detalhada (passada 3: refazer de memória, no papel ou rodar o código).
