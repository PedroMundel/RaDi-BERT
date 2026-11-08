# Racionalização: explicação de apoio

**Procedência:** texto do Claude escrito em 12/10/2026 com base no que ele já sabia. **Nenhuma fonte foi conferida
nesta sessão.** Serve de **mapa para a leitura** do Gurrapu et al. (2023) e do Wiegreffe & Marasović (2021). Não serve
para citar. Onde o texto diz "conferir", a confirmação sai da leitura do Pedro.

---

## 1. A definição em uma linha

**Racionalização é o texto que liga a entrada à resposta e mostra por que a resposta é aquela.** Pode vir **antes**
da resposta, guiando-a (o CoT produz esse tipo), ou **depois**, justificando-a.

(Correção de 13/10, apontada pelo Pedro: a versão anterior, "explicação de por que uma resposta está certa", puxava
para o caso "depois" e para respostas certas. A racionalização existe nos dois lugares e também para respostas
erradas.)

- Pergunta: qual membro serve para chutar uma bola?
- Resposta (rótulo): pé.
- Racionalização: *"para chutar se usa o pé."*

Em inglês, o texto se chama **rationale** e o ato de produzi-lo se chama *rationalization*. Na literatura de NLP o
mais comum é encontrar *rationale*.

## 2. A imagem: o gabarito comentado

| Gabarito comentado | Destilação de racionalização |
|---|---|
| "B" | Rótulo |
| "B, porque se chuta com o pé" | Racionalização |
| O aluno estuda com o comentário | O modelo treina com a racionalização |
| Na prova, o aluno só marca a letra | Na inferência, o modelo só dá o rótulo |
| O aluno que só sabe marcar X, nunca escrever | O encoder |
| O caderno onde ele treina escrever o comentário | A cabeça auxiliar, que é descartada |

## 3. O que racionalização NÃO é

| Termo | O que é | Diferença |
|---|---|---|
| **Racionalização** | Um **texto**: a justificativa da resposta | — |
| **CoT (chain-of-thought)** | Uma **técnica**: o modelo escreve o raciocínio **na inferência, antes** de responder | O CoT é **uma das formas de gerar** racionalização. No DSbS, o PaLM gera as racionalizações por CoT |
| **Destilação de racionalização** | Um **método de treino**: o aluno aprende com a racionalização do professor | É o que se **faz** com a racionalização, não a racionalização em si |
| **Explicação (XAI)** | Qualquer coisa que torne a decisão de um modelo compreensível | Categoria maior: a racionalização é um tipo de explicação |

O erro do gate 5 foi tomar a técnica (CoT) pelo texto (racionalização).

## 4. Os três tipos de racionalização

É a divisão que se costuma atribuir ao Wiegreffe & Marasović (2021). **Conferir na leitura** os nomes exatos e se o
Gurrapu (2023) divide do mesmo jeito: o resumo dele fala em extrativa × abstrativa.

| Tipo | Forma | Exemplo com o pé | Onde aparece |
|---|---|---|---|
| **Extrativa (highlights)** | Um pedaço do **próprio input**, marcado | Na pergunta, as palavras "chutar" e "membro" destacadas | Destaques do e-SNLI; ERASER (DeYoung et al., 2020) |
| **Texto livre (abstrativa)** | Uma frase **nova**, escrita | "Para chutar se usa o pé" | Explicações do e-SNLI; DSbS; Wadhwa; Chen |
| **Estruturada** | Um formato fixo, como uma cadeia de fatos ou um template | "chutar → ação do pé; pé → membro" | Conferir os exemplos na leitura |

**O seu tema usa a de texto livre.**

## 5. Dois eixos que cortam os três tipos

**Fiel × plausível** (a referência mais citada é Jacovi & Goldberg, 2020; **conferir**)

- **Fiel:** mostra como o modelo **de fato** decidiu.
- **Plausível:** convence uma pessoa, mas pode não ter sido o que causou a decisão.
- Uma racionalização pode ser plausível e infiel. É esse o sentido psicológico da palavra: uma justificativa
  construída depois.

**Antes × depois da resposta**

- **Antes:** a racionalização guia a resposta. É o caso do CoT. Ela pode ser fiel, mas não é garantido.
- **Depois:** a racionalização justifica uma resposta que já foi dada.
- As suas leituras da Semana 5 (Wadhwa 2024; Chen 2025) mostram que, **na destilação**, colocar a racionalização
  depois do rótulo funciona melhor.

## 6. Onde o seu tema entra

| Pergunta | Resposta no tema v3 |
|---|---|
| Que tipo? | Texto livre |
| Quem escreve? | O LLM professor. Ou uma pessoa, no caso do e-SNLI |
| Quando é usada? | Só no treino |
| Como o encoder aproveita, se não gera texto? | Uma cabeça decodificadora auxiliar aprende a gerar a racionalização a partir das representações do encoder. O erro dela volta pelo gradiente e muda os pesos do encoder. Na inferência a cabeça sai, e **os pesos mudados ficam** (mesmo mecanismo do Agrawal et al., 2025) |
| Ela é fiel? | **A pergunta não se aplica ao aluno.** A racionalização é do professor, não explica a decisão do encoder. É sinal de treino, não explicação para o usuário |

O último ponto merece atenção. No seu tema, a racionalização **não é XAI**: ninguém vai lê-la na inferência. Isso
separa o seu trabalho da maior parte da literatura de racionalização, que se preocupa com explicar.

## 7. O que procurar na leitura

**No Gurrapu et al. (2023):**
- a definição dele de racionalização, com página;
- extrativa × abstrativa: é a mesma divisão da seção 4?
- ele trata racionalização como sinal de treino (destilação) ou só como explicação?

**No Wiegreffe & Marasović (2021):**
- os nomes exatos dos tipos;
- a diferença entre *explanation* e *rationale*, se eles fazem;
- o que dizem do e-SNLI, que está na sua lista.

**Nos dois:** Ctrl+F em "faithful", "plausib", "post-hoc", "chain".

## 8. Perguntas de arguição

| Pergunta | Onde está a resposta |
|---|---|
| O que é racionalização? | §1, com a fonte que você leu |
| Qual a diferença para o CoT? | §3 |
| Se o encoder não gera texto, como usa a racionalização? | §6 |
| Se a cabeça é descartada, o que fica no encoder? | §6: os pesos mudados pelo gradiente |
| A racionalização explica o seu modelo? | §6: não. É sinal de treino |
| Por que depois do rótulo funciona melhor? | Wadhwa; Chen. **Em aberto:** que sinal ela transfere |
