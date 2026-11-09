# O prompt do Agrawal, generalizado: que padrões servem para o nosso (09/11/2026)

**Procedência:** o prompt foi transcrito do Apêndice C de Agrawal, Ahemad & Sembium (2025), COLING 2025 Industry,
pp. 144–145 (`docs/artigos/2025.coling-industry.12-agrawal.pdf`), sob licença **CC BY 4.0** (conferida na página da
ACL Anthology em 09/11). A generalização e a análise são do Claude (nível 2). O paper descreve o prompt em mais dois
lugares que não batem com este: §4.3 ("[Query] is [Product Title] relevant? [Relevance]. Explain why.") e Apêndice A
("Please provide reasoning for your answer."). **O prompt usado no GLUE/RTE não está publicado.**

## 1. O prompt, inteiro (Apêndice C)

```text
Given a query, a product title and their relevance label, generate a concise reasoning (1-2 sentences) for their
relevance. Focus on key semantic connections and functional similarities, rather than relying solely on exact word
matches. Consider the following aspects:
1. Identify core functionality matches between the query and product title.
2. Recognize semantic relationships between different terms that serve similar purposes.
3. Align user needs across potentially different demographics or use cases.
4. Note shared purpose indicators or common structural elements in both query and title.
5. Connect conceptually related terms that may not be identical but serve similar functions.
Emphasize how these connections demonstrate relevance despite potential differences in wording or target audiences.
Your reasoning should highlight functional similarities and shared purposes that a classification model should
learn to recognize when determining relevance between queries and product titles.
Prioritize understanding context, functionality, and user needs to generate nuanced and accurate relevance
determinations.
Query: [Query]
Product title: [Title]
Actual Relevance label: [Relevance]
Write concise reasoning for given relevance label.
```

## 2. O mesmo prompt, com marcadores genéricos

| Marcador | No original |
|---|---|
| `[A]`, `[B]` | query, product title |
| `[RELAÇÃO]` | relevance |
| `[RÓTULO]` | relevance label (Yes/No) |
| `[ATALHO]` | exact word matches |
| `[SINAL DO DOMÍNIO]` | functional similarities, shared purpose |
| `[CONTEXTO DE USO]` | user needs, demographics, use cases |
| `[CLASSIFICADOR]` | a classification model |

```text
(1) TAREFA + RÓTULO DADO + TAMANHO
Given [A], [B] and their [RÓTULO], generate a concise reasoning (1-2 sentences) for their [RELAÇÃO].
(2) FOCO + ANTI-ATALHO
Focus on [SINAL DO DOMÍNIO], rather than relying solely on [ATALHO].
(3) LISTA DE TIPOS DE LIGAÇÃO ENTRE A E B
Consider: 1. [ligação central] 2. [termos diferentes, mesma função] 3. [CONTEXTO DE USO]
          4. [marcadores comuns] 5. [conceitos relacionados, não idênticos]
(4) ROBUSTEZ À PARÁFRASE
Emphasize how these connections demonstrate [RELAÇÃO] despite differences in wording.
(5) PROPÓSITO DECLARADO
Your reasoning should highlight what [CLASSIFICADOR] should learn to recognize when determining [RELAÇÃO].
(6) PRIORIDADE
Prioritize understanding context ... to generate accurate [RELAÇÃO] determinations.
(7) ITEM, COM O RÓTULO NOMEADO
[A]: ... / [B]: ... / Actual [RÓTULO]: ...
(8) INSTRUÇÃO REPETIDA NO FIM
Write concise reasoning for given [RÓTULO].
```

## 3. Os padrões, um a um, contra a nossa F parágrafo (FP)

| # | Padrão | Na FP hoje? | Serve? | Por quê |
|---|---|---|---|---|
| 1 | Rótulo dado + tamanho curto | sim (o rótulo só escolhe a forma da pergunta; ~30 palavras) | já temos | — |
| 2 | **Anti-atalho**: nomear o atalho que a justificativa não deve tomar | não | **sim, é o mais útil** | Dá para apontar direto os dois defeitos achados nos 20 pares: inventar inferência quando o texto diz (padrão 1 da leitura) e explicar `not_entailment` por plausibilidade de mundo (padrão 2) |
| 3 | Lista de tipos de ligação | não | talvez, curta | No NLI os tipos seriam paráfrase, parte/todo, número/data, papel no evento, ausência no texto. Alonga o prompt; o Pedro já rejeitou verbosidade (A/B) |
| 4 | Robustez à paráfrase | os exemplos cobrem | não precisa | — |
| 5 | Propósito declarado ("o classificador deve aprender…") | não, de propósito | não | A F tirou o enquadramento de anotação (25/10); devolver isso desfaz a F |
| 6 | Prioridade genérica | não | não | Não instrui nada verificável |
| 7 | Rótulo nomeado no item | não, de propósito | não | Mesmo motivo do 5 |
| 8 | Instrução repetida no fim | sim (o "Answer in one sentence…" vem por último) | já temos | — |

### Duas coisas que o exercício mostrou

1. **O prompt deles é assimétrico.** Os cinco aspectos e a ênfase só servem para defender **relevância** ("similarities",
   "shared purpose", "despite differences"). Para o rótulo "No" não há orientação nenhuma. No RTE, metade dos pares é
   `not_entailment`, e é justamente nele que apareceu o padrão 2 (plausibilidade em vez de texto). Qualquer instrução
   nova tem que cobrir os dois rótulos.
2. **O nosso próprio pedido puxa os dois defeitos.** O `ASK_ANSWER` da F diz *"with the world knowledge behind the
   answer"*. No e-SNLI isso era o ponto: legendas de foto, em que o que decide é conhecimento de mundo ("andar de bicicleta
   não é subir em árvore"). No RTE, o que decide quase sempre é o **texto**: o que a passagem diz ou deixa de dizer.
   Pedir "conhecimento de mundo" explica o #16 ("apoio emocional é coisa de amigo", quando a passagem diz "his friend")
   e o #15 ("rivais não fazem negócio"). **É hipótese, a testar.**

## 4. O que testar (proposta, nada rodou)

Uma variante **FP2** = FP com o pedido trocado: em vez de "the world knowledge behind the answer", algo como
*"with what the passage says, or leaves unsaid, that decides it; use world knowledge only when the passage relies on it"*.
Mesmos 20 pares, ~5 min no PC, lado a lado com a FP.

**Cuidado:** isso se parece com a variante D do e-SNLI ("stating the fact from the premise that decides it"), que o
Pedro rejeitou em 21/10 porque a qualidade caiu. A diferença a testar é que, no RTE, o fato que decide está no texto, e
na D do e-SNLI muitas vezes não estava.
