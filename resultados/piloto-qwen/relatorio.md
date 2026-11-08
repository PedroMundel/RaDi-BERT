# Piloto Qwen3.5-9B: 45 justificativas do e-SNLI (20/10/2026)

**Procedência:** os 45 textos foram gerados nesta máquina e lidos inteiros pelo Claude (nível 2). O Pedro ainda não leu.
A leitura lado a lado está em `lado-a-lado.md`, e os números brutos em `resultados.csv` e `vazao.md`.

## O que foi feito

- **Modelo:** `Qwen/Qwen3.5-9B`, GGUF Q4_K_M de `unsloth/Qwen3.5-9B-GGUF`, SHA256 conferido com o do Hugging Face.
- **Servidor:** `llama-server` do llama.cpp b11770 (CUDA 13.4, SHA256 conferido com o do release) em
  `C:\Users\Pedro\Documents\Projects\tools`.
- **Configuração:** tudo na GPU (VRAM de 1,7 para 7,1 GB de 8), raciocínio desligado, amostragem do cartão do modelo,
  semente 42.
- **Amostra:** 45 pares (15 por rótulo) tirados da amostra do piloto do Claude, com **o mesmo prompt**. O modelo é a
  única diferença entre os professores.

## O que se descobriu

| Medida | Humano | Haiku | Sonnet | **Qwen** |
|---|---|---|---|---|
| Palavras (mediana) | 11 | 50 | 46 | **45** |
| Nomeia o rótulo (entail-/contradict-/neutral) | 0/45 | 3/45 | 0/45 | **7/45** |
| Frase de molde ("guarantees the truth of the hypothesis", "mutually exclusive"...) | 0/45 | 11/45 | 1/45 | **30/45** |
| Leitura errada do par | — | 0 | 0 | **2** (abaixo) |

1. **Velocidade não é problema.** 45 pares em 41 s, num fluxo só: 58 tok/s, ~0,9 s por par, sem cortes e sem sobra de
   `<think>`. Nesse ritmo, 100 mil pares levam ~25 h sem lote. Com `--parallel` deve cair bastante, mas isso **não
   foi medido**.
2. **O Qwen escreve como o Claude no tamanho, não no conteúdo.** A primeira frase quase sempre traz o fato que
   decide ("concrete and dirt", "brown × black", "baby × son"). A segunda, em 30 de 45, é molde que repete a definição
   do rótulo do prompt ("the truth of the premise guarantees the truth of the hypothesis"). Pela conta da
   `docs/2026-10-20-perdas-o-que-e-I-gradiente.md` §1.3, essa segunda frase é parte redundante: I(R; X | Y) ≈ 0 nela.
   É o braço com mais molde dos quatro, e é o caso em que tirar as definições do prompt (variante B) mais deve mudar.
3. **Duas leituras erradas:**
   - **#391:** a hipótese diz "causal" (erro de digitação de "casual"). O Qwen leu "cautious" e justificou sobre
     cautela e segurança, que não estão no par. Haiku e Sonnet leram "casual".
   - **#9:** rótulo-ouro "entailment" para "pessoas na fila do ponto" → "o ônibus já tem gente esperando nele". O
     rótulo está errado, e os três modelos recusaram justificá-lo. Haiku e Sonnet disseram que o certo seria neutro.
     O Qwen disse **contradição**, que também está errado, e nomeou o rótulo.
4. **Rótulo ruidoso: o Qwen também não força a justificativa, mas discorda para o lado errado.** É um caso só; não dá
   para dizer taxa. É o cenário da coluna `professor_concorda` (`docs/2026-10-20-pos-hoc-filtro-e-volume.md`, P3).

## Limites

- 45 pares, um prompt, uma semente. Serve para ver o tipo de texto, não para estimar taxas.
- A contagem de "molde" e de "nomeia o rótulo" é por expressão regular, só descritiva (a régua de vazamento foi
  questionada em 20/10).
- Nenhuma checagem de qualidade fora a leitura do Claude. A avaliação cega do Pedro (§6 de
  `docs/2026-10-20-professores-abertos.md`) não foi feita.

## Variante B: sem as definições de rótulo (20/10, pedido do Pedro)

Mesmos 45 pares, mesma semente e amostragem. O prompt B é o A sem o bloco `Labels:`. Textos em `lado-a-lado-B.md`,
números em `resultados-B.csv` e `vazao-B.md`. Também 40 s, sem cortes nem `<think>`.

| Medida | Qwen A | Qwen B | Humano | Haiku | Sonnet |
|---|---|---|---|---|---|
| Palavras (mediana) | 45 | 44 | 11 | 50 | 46 |
| Duas frases ou mais | 39/45 | 43/45 | — | — | — |
| Frase de molde pela lista de expressões | 30/45 | 22/45 | 0 | 11 | 1 |
| Nomeia o rótulo | 7/45 | **11/45** | 0 | 3 | 0 |
| **Última frase sem nenhuma palavra do par** | **22/45** | **26/45** | 1 | 13 | 14 |

A última linha é a medida mais limpa das cinco: não depende de adivinhar quais expressões são molde. Uma frase final que
não usa nenhuma palavra de conteúdo da premissa nem da hipótese só pode estar falando da relação em abstrato.
Palavras vazias e termos como "premise" e "true" foram excluídos da conta.

**O que mudou com a B:**
1. **O molde não sumiu, trocou de palavras.** A lista de expressões caiu de 30 para 22, mas só porque a frase final
   deixou de copiar a definição do prompt. A última frase vazia **subiu** de 22 para 26. No lugar de "the truth of the
   premise guarantees the truth of the hypothesis" vieram "the relationship is neutral", "cannot be determined as true
   or false" e "the hypothesis directly contradicts the premise". Por isso nomear o rótulo subiu de 7 para 11.
2. **A causa não é a definição, é o pedido.** "Explain in one or two sentences why this label is correct" leva o
   modelo a fechar com uma frase que reafirma a relação. Na contradição, o molde até subiu (11 → 13 pela lista):
   "mutually exclusive" é do próprio modelo, não do prompt.
3. **A primeira frase quase não muda.** Em muitos pares ela sai igual ou quase (#126, #195, #847, #948, #986). O fato
   que decide já estava ali na A.
4. **Os dois erros da A melhoraram:**
   - #391: a B leu "casual" e não "cautious". Mas inventou que ser casual "contradiz a agitação" de vender comida.
   - #9: a B não diz mais "contradição". Diz que a premissa não sustenta a hipótese, o que é a leitura de neutro. Segue
     não justificando o rótulo-ouro, que está errado.
5. **Comparação com o Claude:** o Haiku (13) e o Sonnet (14) também fecham com frase vazia em ~30% dos casos, e o Qwen
   em ~50–60%. A diferença é de grau, não de tipo.

**Leitura (Claude):** tirar as definições não resolve o molde e aumenta o vazamento literal. Se o objetivo é uma
justificativa só com a parte informativa, o próximo teste é a variante D, "uma frase: o fato da premissa que decide".
Ela ataca o pedido que gera a frase final. A outra opção é cortar a última frase por script quando ela não tiver
palavra do par: é barato, mas mexe no texto do professor depois de gerado.

## Variante D: uma frase, o fato da premissa que decide (20/10, pedido do Pedro)

Prompt D = B + o pedido trocado por *"Explain in one sentence (at most 25 words) why this label is correct, stating the
fact from the premise that decides it."* **Sem os exemplos escolhidos pelo Pedro** da variante C original do protocolo
(`docs/2026-10-19-geracao-dataset-prompt-e-licenca.md` §1.4): não há exemplos escolhidos ainda. Textos em
`lado-a-lado-D.md`. Tempo de 18 s, 911 tokens de saída contra 2.386 da A (2,6× menos), sem cortes nem `<think>`.

| Medida | Humano | Haiku | Sonnet | Qwen A | Qwen B | **Qwen D** |
|---|---|---|---|---|---|---|
| Palavras (mediana / máx.) | 11 / 24 | 50 / 64 | 46 / 63 | 45 / 70 | 44 / 64 | **16 / 26** |
| Uma frase só | 44 | 1 | 1 | 6 | 2 | **45** |
| Acima de 25 palavras | 0 | 45 | 45 | 45 | 45 | **1** (26) |
| Nomeia o rótulo | 0 | 3 | 0 | 7 | 11 | **14** |
| Última frase sem palavra do par | 1 | 13 | 14 | 22 | 26 | **0** |

**O que mudou com a D:**
1. **A frase vazia sumiu, e o texto ficou perto do tamanho humano.** São 16 palavras contra 11 do humano e 45 da A. O
   fato que decide continua lá ("concrete × dirt", "a baby, sem dizer a relação", "the bookbag is brown"). Tudo o que
   saiu era a parte de molde.
2. **O molde encolheu para uma oração.** O padrão virou "<fato da premissa>, which contradicts/confirms/supports the
   hypothesis". Os 14 casos de "nomeia o rótulo" são 14 das 15 contradições, todas com o verbo "contradicts". Na
   implicação e no neutro, nenhum. Pela conta das perdas (`docs/2026-10-20-perdas-o-que-e-I-gradiente.md` §3.4),
   esses tokens puxam junto com a L_cls. São redundância barata, não conflito.
   - Agora a última linha da tabela é trivial: com uma frase só, ela não tem frase final separada. O molde que sobra
     está na oração "which contradicts the hypothesis...", e essa medida não o pega.
3. **Implicação trivial vira quase eco**, como no humano: "The premise explicitly states that the woman is
   gray-haired, which confirms the hypothesis" (#126, também #195, #296, #197). Quando o par é cópia, não há fato além
   da cópia.
4. **Os dois casos difíceis:**
   - #391: lê "casual" certo, sem o argumento inventado da B.
   - #9: volta a argumentar contra o rótulo-ouro ("cannot already be inside the bus"), como na A, mas sem dizer
     "contradição". O rótulo está errado, então qualquer justificativa fiel a ele seria falsa.

**Leitura (Claude):** a D é a melhor das três para o propósito do H2. Dá a mesma informação nova (o fato que decide)
sem a frase vazia, com 2,6× menos tokens de saída, e portanto mais volume por hora de GPU e alvos mais curtos para o
decoder auxiliar nos 8 GB. O custo é o "contradicts" literal nas contradições, que pela álgebra não prejudica. Tudo
isso sobre 45 pares e uma semente, lidos pelo Claude: o Pedro precisa ler antes de valer como escolha.

## Depois da D: o meio-termo e as referências (21/10)

**O Pedro (21/10):** A e B são verbosas demais, mas na D a qualidade caiu. O ideal é um meio-termo puxando para a D.

**Hipótese do Claude sobre o que caiu na D, a confirmar com o Pedro.** Não foi só tamanho. A D cortou a **ponte de
conhecimento**, o fato do mundo que liga premissa e hipótese, e ficou com "a premissa diz X":
- neutro #531: A diz que a boia permite **flutuar sem nadar**; D diz só que a premissa "does not confirm or deny";
- neutro #359, #407, #409: D vira lista do que a premissa **não menciona**, sem o porquê;
- implicação #195, #296, #126, #197: D vira eco ("states X, which confirms the hypothesis").

Na rubrica do Wiegreffe 2022 (abaixo), isso é queda em **informação nova**, não em gramática.

### Referências para a forma (o que existe de obra)

| Obra | O que dá | Procedência |
|---|---|---|
| **Wiegreffe et al. (2022)**, *Reframing Human-AI Collaboration for Generating Free-Text Explanations*, NAACL 2022 (arXiv:2112.08674) | **A melhor referência.** A Tab. 2 traz exemplos de prompt **escritos pelos autores** para o e-SNLI: 1–2 frases, ~10–25 palavras, sem nomear o rótulo, e cada um é uma ponte de conhecimento (ex.: "Horse riding is an activity almost always done outdoors."). A Tab. 4 mostra que exemplos assim vencem os do crowd do e-SNLI (42,4% × 30,8%, 26,8% empate). A §2.3 traz 7 atributos, entre eles **"Amount info" (pouca, suficiente, demais)**, que é o eixo verboso × seco | N3-txt (HTML, 21/10); Tab. 4 já conferida pelo Claude em 19/10. Está na sua lista base (`docs/leituras/2026-10-20-base-para-decidir-justificativas.md`, item 3) |
| **Camburu et al. (2018)**, e-SNLI, §3 | **Regra de cobertura por rótulo**: na implicação, justificar cada parte da hipótese que não está na premissa; no neutro e na contradição, um elemento basta. Focar no "não óbvio" e não repetir o que é idêntico nos dois. Assim o tamanho se adapta ao par em vez de ser um teto fixo | N3-txt (pesquisa de 19/10, §2.2) |
| **Dhaini et al. (2025)**, arXiv:2508.09776 | Prompt "Provide exactly one sentence that directly connects the premise to the hypothesis." É uma frase, mas pede a **ligação**, não o fato | N3-txt (v1) |
| **Wadhwa et al. (2024)** | Os 15 tokens de maior atribuição igualam a racionalização inteira (~36 tokens), mas só se carregarem sinal novo | N3-txt; você leu na Semana 5 |
| ~~arXiv:2505.22823, "~21 palavras"~~ | Errado no doc de 20/10: a Tab. 9 mede a entrada, não a explicação. Corrigido em `docs/2026-10-20-professores-abertos.md` | conferido 21/10 |

### Proposta: variante E (a montar, nada rodou)

A rodada A/B/D mostrou que **o pedido manda na forma**, e o Wiegreffe mostra que **o exemplo manda mais que a
instrução**. A proposta junta os dois:
1. **Instrução:** a da D sem o teto rígido, trocando "o fato da premissa" por **"o fato ou o raciocínio que liga a
   premissa à hipótese"** (a ligação do Dhaini). Mais a regra do Camburu: na implicação, cobrir o que a hipótese
   acrescenta; no neutro e na contradição, um elemento basta. Limite brando de ~30 palavras.
2. **Exemplos:** 6 (2 por rótulo), no formato da Tab. 2 do Wiegreffe: ponte de conhecimento, 10–25 palavras, sem
   nomear o rótulo. **Quem escolhe ou escreve os exemplos é você.** Eles definem o tom do dataset inteiro.
3. **Mesmos 45 pares**, comparando com A e D pela leitura cega e pela tabela de sempre.

Com o bloco fixo de exemplos e o cache de prompt do `llama-server`, o custo de tempo fica perto do da D.

## Variante E: a ponte de conhecimento com os 12 exemplos do Pedro (21/10)

**Procedência:** os 45 textos foram lidos inteiros pelo Claude (nível 2). O Pedro ainda não leu. Os textos estão em
`lado-a-lado-E.md`, os números em `resultados-E.csv` e `vazao-E.md`, e a tabela abaixo saiu de um script de medida do
scratchpad.

**Prompt E:**
- os **12 exemplos** de `candidatos-exemplos.md`, na versão final do Pedro, intercalados por rótulo. Antes eram 6; o
  Pedro escolheu os 12. Nenhum dos pares de exemplo está na amostra;
- a instrução: "one sentence (about 30 words at most)", "the world knowledge that links the premise to the
  hypothesis", a regra por rótulo e "follow the style of the examples";
- sem as definições de rótulo. Mesma semente, amostragem e modelo das outras variantes.

**Vazão:** 45 pares em 29 s, 1.234 tokens de saída (mediana 27), sem cortes e sem `<think>`. O prompt tem ~600
palavras a mais, e mesmo assim fica perto de 0,65 s por par.

| Medida | Humano | Haiku | Sonnet | Qwen A | Qwen D | **Qwen E** |
|---|---|---|---|---|---|---|
| Palavras (mediana / máx.) | 11 / 24 | 50 / 64 | 46 / 63 | 45 / 70 | 16 / 26 | **24 / 34** |
| Uma frase só | 44 | 1 | 1 | 6 | 45 | **45** |
| Acima de 30 palavras | 0 | 45 | 41 | 45 | 0 | **1** |
| Nomeia o rótulo | 0 | 3 | 0 | 7 | 14 | **6** |
| Oração que reafirma a relação (lista de expressões) | 3 | 8 | 11 | 33 | 28 | **17** |
| Fala de "premise"/"hypothesis" | 0 | 44 | 45 | 42 | 37 | **13** |
| Cópia do par (mediana, `copia.py`) | 0,86 | 0,42 | 0,55 | 0,31 | 0,67 | **0,36** |

Os números desta tabela foram recontados pelo mesmo script para todas as colunas, então a contagem de "nomeia o
rótulo" pode diferir em um ou dois da tabela da D.

**O que mudou com a E:**
1. **A ponte de conhecimento voltou, que era o que a D tinha perdido.**
   - neutro: alternativas concretas no lugar de "a premissa não menciona": #643 (sobrinho, filho do vizinho), #407
     (troféu, caridade), #529 (estranhos), #630 (se refrescar), #409 (parkour), #531 (boiar sem nadar), #545 (bola);
   - contradição: o molde do Pedro, choque de lugar e ação no mesmo momento, aparece sozinho em #692 (parado × pulando),
     #740 (bicicleta × skate), #724 (terra firme × água), #676 (deserto × lago) e #932 (em movimento × dormindo);
   - a cópia caiu de 0,67 (D) para 0,36: a E põe palavras novas, e não só repete o par.
2. **A forma ficou no meio-termo pedido:** 24 palavras, entre a D (16) e a A (45), sempre uma frase.
3. **"Premise"/"hypothesis" caiu de 37 para 13, e a oração que reafirma a relação de 28 para 17.**

**O que não resolveu:**
1. **Implicação trivial ainda vira eco com metalinguagem**, quando o par é quase cópia: #195, #296, #197, #126, #265
   e #73 ("The premise describes..., which directly confirms..."). Às vezes vem com rabo de enchimento ("without adding
   unrelated details", "without requiring any external assumptions"). Nenhum exemplo do Pedro cobre implicação por
   cópia quase literal, e é aí que o Qwen volta ao molde.
2. **"Contradicts" literal em 5 contradições** (#862, #948, #878, #864, #742) e **"entails" em #281**. Pela álgebra é
   redundância, não dano.
3. **Rótulo errado (#9) agora é forçado.** A D recusava justificar o rótulo-ouro errado ("cannot already be inside the
   bus"). A E inventa ("passengers must already be inside or boarding it"). **É o risco da justificativa forçada em
   rótulo ruidoso** (`docs/2026-10-20-pos-hoc-filtro-e-volume.md`): exemplos que puxam para "explique sempre" puxam
   também para obedecer ao rótulo errado. A coluna `professor_concorda` (P3) passa a ser mais necessária, não menos.
4. **#976 discorda do ouro pelo outro lado:** chama a contradição de "alternativa não relacionada", que é a leitura de
   neutro. É a convenção do SNLI de mesma cena que o Qwen não aplica sempre.
5. **Enchimento em alguns:** #309 ("while hiking or exploring scenic areas"), #211 ("specifically designed").

**Leitura (Claude):** a E é a melhor das quatro para o H2. Tem o tamanho do meio, a ponte de volta e menos
metalinguagem. Os buracos são localizados: falta exemplo de implicação por cópia, e a obediência ao rótulo errado
precisa ser marcada, não filtrada. Duas correções baratas para uma E2, se o Pedro quiser:
1. um exemplo de implicação **quase literal** com resposta curta (por exemplo, "Gray-haired means having gray hair.");
2. nenhuma mudança contra o #9 no prompt: o caso é da coluna `professor_concorda`, não do texto.

Tudo isso sobre 45 pares e uma semente. O Pedro precisa ler o `lado-a-lado-E.md` antes de a E valer como escolha.

## Variante E2: E + um exemplo de implicação quase literal (21/10, pedido do Pedro)

**Procedência:** os 45 textos foram lidos inteiros pelo Claude (nível 2). Os textos estão em `lado-a-lado-E2.md`, e os
números em `resultados-E2.csv` e `vazao-E2.md`.

**O 13º exemplo.** O Pedro propôs "Gray-haired means having gray hair.", mas essa frase é a resposta do par #126, que
está na amostra: o teste ficaria contaminado. Entrou um par do dev fora da amostra, com a mesma forma:
- P: "A man is leaning out of a window to paint some decorative iron white."
- H: "A man is painting."
- Explicação: "Painting the iron white means he is painting."

O exemplo foi posto depois do primeiro trio. Vazão: 30 s, sem cortes.

| Medida | Qwen E | **Qwen E2** |
|---|---|---|
| Palavras (mediana / máx.) | 24 / 34 | 24 / 35 |
| Uma frase só | 45 | 44 |
| Acima de 30 palavras | 1 | 2 |
| Nomeia o rótulo | 6 | 4 |
| Oração que reafirma a relação | 17 | 13 |
| Fala de "premise"/"hypothesis" | 13 | 9 |
| Cópia do par (mediana) | 0,36 | 0,40 |
| Palavras na implicação (mediana) | 24 | 24 |

**O que se descobriu:**
1. **A correção mirada não funcionou.** As implicações quase literais seguem em eco com metalinguagem: #126 ("The
   premise explicitly describes a gray-haired woman, which directly confirms..."), #296, #197, e #265 igual à E. A
   mediana da implicação continua em 24 palavras. O Qwen não copiou o tamanho do exemplo curto.
2. **O resto mexeu pouco, e para os dois lados.**
   - Melhoraram: #948, #847 e #986 (cor, material e forma do chapéu como ponte), #281 (sem "entails") e #195 ("still a
     baby").
   - Pioraram: #724 perdeu o molde de lugar ("takes place on water"), #932 voltou a "contradicts", e #653 passou a ter
     duas frases (36 palavras).
   - Com temperatura 0,7, mudar um exemplo sorteia todos os textos de novo. Diferenças de 2 a 4 casos em 45 estão
     dentro desse ruído e não são sinal.
3. **#9 segue forçado** ("passengers are already on the bus").

**Leitura (Claude):** a E2 empata com a E. Faz sentido pela conta das perdas: quando a hipótese é um pedaço da
premissa, **não existe ponte para dizer**, e I(R; X | Y) é baixo para qualquer explicação. O humano também só copia
nesses casos (cópia de 0,86). O que dá para cortar ali é só o enchimento ("without requiring any external
assumptions"), e ele custa tokens, não informação. Correr atrás disso no prompt não compensa. Fica a E, mais simples.

## Variante E3: E + uma linha contra o enchimento (21/10, pedido do Pedro)

**Procedência:** os 45 textos foram lidos inteiros pelo Claude (nível 2). Estão em `lado-a-lado-E3.md`, e os números em
`resultados-E3.csv` e `vazao-E3.md`.

**O prompt:** é a E com esta frase no fim do pedido: *"When the hypothesis only repeats part of the premise, answer in a
few words with no filler."* Os exemplos são os mesmos 12. Vazão: 27 s, 1.111 tokens de saída (−10% contra a E), sem
cortes.

| Medida | Qwen E | Qwen E2 | **Qwen E3** |
|---|---|---|---|
| Palavras (mediana / máx.) | 24 / 34 | 24 / 35 | **20 / 31** |
| Palavras por rótulo (impl. / neutro / contr.) | 24 / 23 / 23 | 24 / 26 / 21 | **22 / 19 / 20** |
| Nomeia o rótulo | 6 | 4 | 8 |
| Oração que reafirma a relação | 17 | 13 | 17 |
| Fala de "premise"/"hypothesis" | 13 | 9 | 13 |
| Cópia do par (mediana) | 0,36 | 0,40 | 0,44 |

**O que se descobriu:**
1. **A linha encurtou tudo, menos o que mirava.** O texto caiu ~10% nos três rótulos, e saiu enchimento como "while
   hiking or exploring scenic areas" (#309) e "specifically designed" (#211). As implicações quase literais seguem em
   eco: #126 trocou um enchimento por outro ("without adding any new or conflicting information"), e #296 e #197
   ficaram iguais. A metalinguagem na implicação **subiu** de 7 para 9.
2. **Duas melhoras em contradição:** #976 aplica a convenção de mesma cena ("cannot simultaneously define the same
   scene"), e #864 e #793 dizem o choque "at the same time".
3. **Uma perda em contradição:** o molde do Pedro ("X requires A, while Y means B") voltou a "which contradicts" em
   #692, #948 e #742.
4. **#9 segue forçado** ("the bus has arrived").
5. **Uma semente, temperatura 0,7:** diferenças de 2 a 4 casos em 45 são ruído.

**Leitura (Claude):** três tentativas, o exemplo (E2) e a instrução (E3), não mexeram no eco da implicação quase literal.
Isso confirma a leitura da E2: ali não há ponte a dizer, e o prompt não cria uma. E e E3 empatam em qualidade. A E3
custa ~10% menos tokens, mas perdeu o molde em algumas contradições. Com 45 pares e uma semente, só a leitura cega do
Pedro ou uma amostra maior separa as duas.

## Variante E4: E3 + proibir metalinguagem e palavras de relação (21/10, pedido do Pedro)

**Procedência:** os 45 textos foram lidos inteiros pelo Claude (nível 2). Estão em `lado-a-lado-E4.md`, e os números em
`resultados-E4.csv` e `vazao-E4.md`.

**O prompt:** a E3 com esta frase no fim do pedido: *'Do not refer to the premise or the hypothesis (no "the premise
says", "the hypothesis states"), and do not use relation words such as contradicts, confirms, supports or entails.'*
Vazão: 27 s, 1.076 tokens de saída, sem cortes.

| Medida | Qwen E | Qwen E3 | **Qwen E4** |
|---|---|---|---|
| Palavras (mediana / máx.) | 24 / 34 | 20 / 31 | **20 / 28** |
| Nomeia o rótulo | 6 | 8 | **0** |
| Oração que reafirma a relação (lista) | 17 | 17 | **7** |
| Fala de "premise"/"hypothesis" | 13 | 13 | **0** |
| Cópia do par (mediana) | 0,36 | 0,44 | **0,33** |
| Usou palavra proibida | — | — | 5 de 45 ("confirm-" em #73, #211, #265, #643 e #529) |

**O que se descobriu:**
1. **Nas medidas de superfície, a E4 é a mais limpa de todas.** Metalinguagem e rótulo nomeado foram a zero, e a oração
   que reafirma a relação caiu de 17 para 7.
2. **O neutro ganhou pontes melhores:** #359 ("Acoustic guitars are used for many genres besides country music"), #630
   ("Dogs often walk through water for reasons other than fishing"), #409 (vôlei, trampolim) e #460, mais curto.
3. **Mas a redundância trocou de palavra, como na B.** A palavra proibida virou sinônimo:
   - "premise" virou "the description of a gray-haired woman" (#126) e "the scene description" (#529);
   - "contradicts" virou "mutually exclusive", "incompatible", "prevents" e "cannot ... simultaneously in the same scene"
     (#692, #724, #878, #948, #963, #976).

   A lista de expressões não pega os sinônimos, então **parte da melhora na tabela é a medida sendo enganada**: é a lei
   de Goodhart que a conta das perdas previa.
4. **Apareceram erros de fato que E e E3 não tinham:**
   - #740: "a single-wheeled skateboard" (skate tem quatro rodas);
   - #407: "insurance payouts" (pink slip, nesse contexto, é o documento do veículo apostado na corrida);
   - #643: "could be a father, grandfather, uncle... rather than the son" (frase trocada);
   - #197 e #296 ficaram vazias de outro jeito ("is a specific type of building where people can stand in front").

   Inferência do Claude: com mais proibições, o modelo gasta capacidade obedecendo à forma e erra mais o conteúdo.
5. **#9 deixou de forçar** ("the vehicle is present but empty of passengers"), o que vai contra o rótulo-ouro errado.
   Num caso só, não dá para dizer se é efeito ou sorteio.

**Leitura (Claude):** a E4 limpa a superfície, mas troca palavras por sinônimos e acrescenta três erros de fato. Para o
H2, um fato falso no alvo é pior que um "contradicts" redundante: a álgebra diz que o rótulo repetido não atrapalha,
enquanto conhecimento de mundo errado ensina o aluno a errar. A recomendação fica na **E** (ou na E3, pelo custo). Se o
Pedro preferir a E4, o próximo passo seria a mesma leitura num lote maior, para medir a taxa de erros de fato.

## Professor maior: `Qwen3.6-35B-A3B` com a variante E (21/10, pedido do Pedro)

**Procedência:** os 45 textos foram lidos inteiros pelo Claude (nível 2). Estão em `lado-a-lado-E-35B.md`, e os números
em `resultados-E-35B.csv` e `vazao-E-35B.md`.

**Modelo:** `unsloth/Qwen3.6-35B-A3B-GGUF`, arquivo `UD-IQ4_XS` (17,73 GB), SHA256 conferido com o do Hugging Face.
Servido pelo mesmo `llama-server` com `-ngl 999 --cpu-moe -c 8192`, ou seja, todos os experts na RAM. Usou 4,1 GB de
VRAM, e havia 19,4 GB de RAM livres na carga. O prompt E, a semente e a amostragem são os do 9B: o modelo é a única
diferença.

**Vazão:** 106 s para 45 pares (~2,4 s por par, 11,6 tok/s de ponta a ponta), **3,7× mais lento que o 9B**. Sem cortes e
sem `<think>`. Não foi testado pôr parte dos experts na GPU (`--n-cpu-moe N`), embora sobrassem ~4 GB de VRAM.

| Medida | 9B E | **35B E** |
|---|---|---|
| Palavras (mediana / máx.) | 24 / 34 | 23 / 31 |
| Nomeia o rótulo | 6 | 8 |
| Oração que reafirma a relação | 17 | 13 |
| Fala de "premise"/"hypothesis" | 13 | 10 |
| Cópia do par (mediana) | 0,36 | 0,38 |
| Segundos por par | ~0,65 | ~2,4 |

**O que se descobriu:**
1. **Na forma, os dois empatam.** Tamanho, metalinguagem e cópia ficam na mesma faixa. O eco da implicação quase literal
   continua igual (#126, #296, #265): reforça que ele vem do par, não do modelo.
2. **No raciocínio, o 35B acertou os dois casos difíceis em que o 9B errou:**
   - #9 (rótulo-ouro errado): o 35B não força a justificativa, e argumenta contra o rótulo ("they are not waiting for
     that specific bus"), como Haiku e Sonnet. O 9B na E inventava que os passageiros já estavam no ônibus;
   - #976: o 35B aplica a convenção de mesma cena ("impossible for both scenes to be the same event"). O 9B na E chamava
     o caso de "alternativa não relacionada", que é a leitura de neutro.
3. **Pontes de implicação um pouco melhores:** "A baseball cap is a type of hat" (#57), "Sand dunes are composed of sand"
   (#211), "a group constitutes several" (#75). Nenhum erro de fato encontrado na leitura.
4. **Na contradição, o molde do Pedro aparece menos.** Domina "making it impossible ... simultaneously" e "mutually
   exclusive", que é redundância, não erro.

**Leitura (Claude):** o 35B ganha onde o modelo importa, que é o raciocínio sobre o par, e empata onde o prompt
manda, que é a forma. A evidência é pequena: dois casos difíceis em 45, com uma semente. O custo é 3,7× o tempo:
~66 h contra ~18 h para 100 mil pares num fluxo só (conta, não medida). O lote escala no 9B e quase não escala com os
experts na RAM. A escolha é qualidade contra tempo, e é do Pedro. Antes de fechar, valem dois testes baratos:
1. `--n-cpu-moe` com parte dos experts na GPU, para medir quanto a vazão do 35B sobe;
2. ler os dois professores num lote maior, para ver se a vantagem no raciocínio passa de dois casos.

**Decisão do Pedro (21/10):** o 35B fica como **fallback**. O professor principal segue sendo o 9B.

## Variante F: perguntar "por quê" em vez de pedir justificativa (25/10, pedido do Pedro)

**Procedência:** os 45 textos foram lidos inteiros pelo Claude (nível 2), ao lado dos da E. O Pedro ainda não leu.
Os textos estão em `lado-a-lado-F.md`, e os números em `resultados-F.csv` e `vazao-F.md`.

**A ideia do Pedro:** o eco vem de pedir que o modelo **defenda um rótulo**. Então a F troca a moldura:
- o par vira uma pergunta sobre a cena, como "por que um homem andando de moto não pode estar subindo numa árvore?";
- o prompt não traz o rótulo nem as palavras "premise" e "hypothesis";
- o "You are annotating a natural language inference dataset" também saiu.

**Como ficou o prompt:**
- O rótulo-ouro só escolhe o molde da pergunta:
  - implicação: *"If {P}, why does that mean {H}?"*;
  - neutro: *"If {P}, why does that not necessarily mean {H}?"*;
  - contradição: *"If {P}, why can't it also be that {H}, in the same place and moment?"*.
- Os 12 exemplos são os da E, **com as mesmas respostas do Pedro**, cada uma sob a pergunta do seu par.
- Pedido: *"Answer in one sentence (about 30 words at most) with the world knowledge behind the answer. Follow the
  style of the examples. Write only the answer."*
- A pergunta é montada por molde, não reescrita: P e H entram quase literais (sem o ponto final e com a primeira letra
  minúscula). A pergunta do Pedro ("um homem *que está andando de moto*") funde as duas frases, e para isso seria
  preciso um passo de reescrita. Nos fragmentos do e-SNLI o molde sai truncado ("If a man sleeping on the ground in a
  subway, why...").
- O que muda contra a E é só a moldura: o cabeçalho, o formato do item e o pedido. Os exemplos são os mesmos, e a
  semente, a amostragem e o modelo também.

**Vazão:** 30 s para os 45 pares, 1.212 tokens de saída (mediana 27), sem cortes e sem `<think>`. É o mesmo custo da E.

| Medida | Humano | Qwen E | Qwen E3 | **Qwen F** |
|---|---|---|---|---|
| Palavras (mediana / máx.) | 11 / 24 | 24 / 34 | 20 / 31 | **23 / 30** |
| Palavras por rótulo (impl. / neutro / contr.) | 9 / 14 / 11 | 24 / 23 / 23 | 22 / 19 / 20 | **23 / 22 / 23** |
| Nomeia o rótulo | 0 | 6 | 8 | **1** |
| Palavra de relação (lista abaixo) | 8 | 25 | 23 | **12** |
| Fala de "premise"/"hypothesis" | 0 | 13 | 13 | **0** |
| Texto sobre o texto ("describes", "stated", "mentions") | 0 | 12 | 7 | **5** |
| Diz "simultaneamente" ou "no mesmo lugar/momento" | 2 | 3 | 5 | **6** |
| Cópia do par (mediana, `copia.py`) | 0,86 | 0,36 | 0,44 | **0,36** |

Esta tabela sai de `python medir.py E E3 F` (nesta pasta), que reconta todas as colunas. O script da E não ficou no
projeto, e a lista de "palavra de relação" foi refeita: contradict-, confirm-, support-, entail-, satisf-, guarantee-, imply,
"consistent with", "mutually exclusive", incompatible, directly, explicitly, "which means", therefore, thus. Por isso
os números da E aqui diferem dos da tabela da E (17 → 25).

**O que se descobriu:**
1. **A metalinguagem caiu sem proibir nada.** "premise"/"hypothesis" foi a 0 e a palavra de relação caiu à metade (25 →
   12). Na E4, a proibição tinha trocado as palavras por sinônimos e criado erros; aqui não há o que substituir,
   porque o prompt não fala de premissa nem de rótulo.
2. **O eco da implicação quase literal caiu pela metade.** Nos 6 casos que nenhuma variante tinha resolvido:
   - **três saíram do eco:**
     - #195: "A baby wearing a hat and sunglasses is still a baby";
     - #265: "A guy is a person, and playing the guitar means performing that action on an instrument";
     - #73: o corpo apoiado no chão, sem "confirms";
   - **três seguem vazios**, agora com "described"/"stated" no lugar de "premise":
     - #126: "is described as having gray hair because her appearance explicitly states...";
     - #296: "is explicitly stated to be playing";
     - #197: "the standard meaning when described as being located there".

   A leitura da E2 continua de pé: quando H é um pedaço de P, não existe ponte a dizer. A F mostra que parte do eco
   vinha da moldura de anotação, mas não todo.
3. **O tamanho não mudou** (23 palavras, contra 24 na E). Quem controla o tamanho são os exemplos, não a moldura.
4. **A contradição passou a repetir a pergunta.** "Simultaneously" e "in the same place" aparecem em 6 textos, porque
   o molde da pergunta traz "in the same place and moment". É redundância que a própria pergunta pôs ali.
5. **Erros e desvios novos:**
   - **#948, erro de fato:** "having two different colored bags on their back is physically impossible". Dá para
     carregar duas mochilas; o choque é que a mesma mochila não tem duas cores, como a E dizia.
   - **#742, discorda do ouro:** "a man working alone does not exclude the possibility that a woman is also present".
     A pergunta "por que não pode?" deixou o modelo responder "pode". É a convenção de mesma cena do SNLI que ele não
     aplica. Para a coluna `professor_concorda` isso é sinal útil, não erro de texto.
   - **#740, menor:** "rather than jumping high obstacles", mas skate também salta.
6. **#9 segue forçado** ("passengers are boarding an existing vehicle"). Tirar o rótulo da vista não basta, porque
   a pergunta "why does that mean..." já pressupõe que a implicação vale.
7. **O neutro ficou igual ou um pouco melhor.** As alternativas são concretas, e sem "the premise does not confirm":
   #359 (solo, sem plateia), #630, #514, #409.

**Leitura (Claude):** a F resolve pela moldura o que a E4 tentou resolver por proibição, e sem os erros que a proibição
trouxe. A superfície ficou mais limpa que a da E, e metade do eco da implicação quase literal sumiu. Duas ressalvas:
apareceu um erro de fato (#948) que a E não tinha, e a contradição herdou a frase da pergunta. É uma semente e 45
pares, e diferenças de 2 a 4 casos são ruído. A queda de 13 → 0 em "premise"/"hypothesis" e de 25 → 12 em palavra de
relação passa desse ruído; um erro de fato a mais não passa.

**Próximos ajustes possíveis, todos baratos (< 1 min cada no 9B):**
1. **F2:** a contradição sem "in the same place and moment" na pergunta, para ver se o "simultaneously" some e se a
   convenção de mesma cena se perde (#742, #976).
2. **F com reescrita:** um passo antes, em que o próprio Qwen funde P e H numa pergunta natural, como a do Pedro.
   Dobra as chamadas (~1,3 s por par) e abre um ponto de falha novo: a pergunta reescrita pode mudar o sentido do par.
3. **Medir erro de fato num lote maior** (200 pares, E e F), porque com 45 pares um erro a mais não separa as duas.

## Variante FR: a F com a pergunta reescrita pelo Qwen (26/10, pedido do Pedro)

**Procedência:** as 45 perguntas e as 45 respostas foram lidas inteiras pelo Claude (nível 2), ao lado da F. O Pedro
ainda não leu. Os textos estão em `lado-a-lado-FR.md`, com a pergunta de cada par e as 12 perguntas dos exemplos no
topo. Os números estão em `resultados-FR.csv` (coluna `pergunta`), `vazao-FR.md` e `python medir.py E F FR`.

**Como funciona:** duas chamadas ao 9B por par.
1. **Reescrita.** O Qwen funde P e H numa pergunta "por quê" curta e natural, no molde do rótulo:
   - implicação: "Why does ... mean ...?";
   - neutro: "Why is ... not necessarily ...?";
   - contradição: "Why can't ... be ...?".

   O prompt traz 3 exemplos tirados dos pares de exemplo, um por rótulo. O da contradição é a sua pergunta, ajustada ao
   par do ciclista: "Why can't a biker jumping over dirt hills be climbing a tree?". Os outros dois foram escritos
   pelo Claude no mesmo molde. O rótulo não aparece em nenhuma das duas chamadas.
2. **Resposta.** É o prompt da F, com a pergunta reescrita no lugar da pergunta de molde. As 12 perguntas dos exemplos
   também passam pela reescrita, e as respostas continuam sendo as suas.

**Diferença da F além da reescrita:** a pergunta de contradição perdeu o "in the same place and moment", porque a sua
pergunta não tinha isso. Então a FR mistura a reescrita com o que seria a F2.

**Vazão:** 57 s para 45 pares (mediana 1,14 s por par, contra ~0,65 s na F), sem cortes. O tempo dobra, como previsto.

| Medida | Humano | Qwen E | Qwen F | **Qwen FR** |
|---|---|---|---|---|
| Palavras (mediana / máx.) | 11 / 24 | 24 / 34 | 23 / 30 | **22 / 31** |
| Palavras por rótulo (impl. / neutro / contr.) | 9 / 14 / 11 | 24 / 23 / 23 | 23 / 22 / 23 | **25 / 23 / 21** |
| Nomeia o rótulo | 0 | 6 | 1 | **2** |
| Palavra de relação (lista) | 8 | 25 | 12 | **10** |
| Fala de "premise"/"hypothesis" | 0 | 13 | 0 | **0** |
| Texto sobre o texto ("describes", "stated", "mentions") | 0 | 12 | 5 | **2** |
| Diz "simultaneamente" ou "no mesmo lugar/momento" | 2 | 3 | 6 | **4** |
| Cópia do par (mediana) | 0,86 | 0,36 | 0,36 | **0,30** |

**O que se descobriu:**
1. **As perguntas saem naturais, como a sua**, por exemplo "Why can't a child sitting on a slide be jumping on a
   trampoline?". Os fragmentos do e-SNLI deixam de truncar a pergunta, como acontecia na F ("If a man sleeping...").
2. **Mas a reescrita é um ponto de falha novo: 2 das 45 perguntas mudaram o par.**
   - **#126, rótulo invertido:** P = mulher grisalha de óculos escuros, H = ela tem cabelo grisalho, implicação. A
     pergunta saiu *"Why does a woman wearing sunglasses **not necessarily** mean she has gray hair?"*, com o molde
     do neutro e sem o "gray-haired". A resposta argumenta contra o rótulo-ouro. Como alvo de treino, isso é veneno.
   - **#195, detalhe perdido:** a reescrita tirou o chapéu e os óculos, e a pergunta virou tautologia ("Why does a baby
     looking at the camera while being held mean a baby looks at the camera?"). A resposta voltou ao eco ("directly
     implies"), pior que na F.
   - Nos exemplos, "men in fatigues" virou "a group of men". A sua resposta ("Soldiers from the same unit...")
     depende da farda, que sumiu da pergunta.
   - O desvio do #126 é fácil de pegar: das 45, só ele sai do molde do seu rótulo (conferido por regex).
3. **O eco da implicação quase literal ficou igual à F, só redistribuído.** #296 e #197 perderam o "explicitly stated" e
   o "described". #195 piorou, e #126 deixou de ser eco para virar erro.
4. **A convenção de mesma cena voltou no #742:** "a man is male and a woman is female, so they cannot be the same
   person". Na F, o modelo discordava do ouro aqui.
5. **Os erros de fato da F continuam, então vêm da forma de pergunta, não do molde:**
   - #948: "a person can carry only one bag at a time". A pergunta "por que não pode ter uma mochila preta?" puxa
     para "não pode ter duas", e não para "a mesma mochila não tem duas cores";
   - #740: "skateboarding... cannot perform that specific jump safely", mas skatista salta escada;
   - #878 ficou mais fraco: "being indoors usually restricts movement and prevents carrying large objects". O fato
     que decide (o campo fica do lado de fora) sumiu.
6. **#9 segue forçado, mas com outra invenção** ("the bus is full or delayed, causing passengers to queue outside").
7. **O neutro empata com a F**, com alternativas concretas: #407 (colete é exigência de segurança em qualquer barco),
   #653 (Lego vira carro ou robô), #409.

**Leitura (Claude):** a reescrita entrega o que prometia na forma. A pergunta fica natural, e a metalinguagem cai mais
um pouco (texto sobre o texto 5 → 2, cópia 0,36 → 0,30). Em troca, abre um ponto de falha que a F não tinha: 1 rótulo
invertido em 45 (#126). Num dataset de 100 mil pares, ~2% de alvo contra o ouro não pode passar sem filtro. Os erros
de fato da F (#948, #740) não vieram do molde e continuam aqui. Na superfície, F e FR ficam perto, e as diferenças de
2 a 3 casos são ruído com uma semente.

**Se a FR seguir, ela precisa de uma guarda barata na reescrita:**
- conferir por regex se a pergunta mantém o molde do rótulo (pegaria o #126);
- quando sair do molde, cair para a pergunta de molde da F ou reescrever de novo.

Detalhe perdido, como o do #195, a regex não pega: precisaria conferir se as palavras de H estão na pergunta.

## Variante FRG: a FR com a guarda de molde (26/10, pedido do Pedro)

**Procedência:** as 45 respostas foram lidas inteiras pelo Claude (nível 2). Estão em `lado-a-lado-FRG.md`, e os
números em `resultados-FRG.csv` (colunas `pergunta` e `guarda`), `vazao-FRG.md` e `python medir.py E F FR FRG`.

**A guarda:** depois da reescrita, uma regex confere se a pergunta mantém o molde do rótulo:
- implicação: "Why does/do ... mean", sem "not necessarily";
- neutro: "Why ... not necessarily";
- contradição: "Why can't".

Se a pergunta sair do molde, entra a pergunta de molde da F. O resto é a FR, sem mudança. Vazão: 58 s, sem cortes.

**A guarda funcionou como previsto:**
- foi acionada só no #126, e nenhum dos 12 exemplos saiu do molde;
- os prompts da FR e da FRG são iguais em 44 dos 45 pares (conferido por script); só o #126 muda;
- o #126 deixou de inverter o rótulo, mas voltou ao eco, e com uma ponte estranha: *"The description explicitly
  states she is gray-haired, and wearing sunglasses on a bench suggests it is daytime when hair color can be
  observed."* A guarda tira o erro de rótulo, mas não cria a ponte que o par não tem.

**Achado mais importante desta rodada: o servidor não reproduz a mesma saída entre rodadas.** Com os prompts iguais
em 44 pares, **34 respostas saíram diferentes das da FR.** A mesma chamada repetida em seguida devolve o mesmo
texto, mas entre rodadas o resultado muda com o estado do servidor (cache de prompt), mesmo com a semente fixa. Então
FR × FRG é, sem querer, uma **medida do ruído de uma rodada para outra com o prompt idêntico**:

| Medida | Qwen E | Qwen F | Qwen FR | **Qwen FRG** | Ruído (FR × FRG) |
|---|---|---|---|---|---|
| Palavras (mediana / máx.) | 24 / 34 | 23 / 30 | 22 / 31 | **23 / 29** | ±1 |
| Nomeia o rótulo | 6 | 1 | 2 | **2** | 0 |
| Palavra de relação (lista) | 25 | 12 | 10 | **16** | **6** |
| Fala de "premise"/"hypothesis" | 13 | 0 | 0 | **0** | 0 |
| Texto sobre o texto | 12 | 5 | 2 | **4** | 2 |
| "Simultaneamente" / mesmo lugar | 3 | 6 | 4 | **4** | 0 |
| Cópia do par (mediana) | 0,36 | 0,36 | 0,30 | **0,27** | 0,03 |

**O que o ruído muda na leitura das variantes:**
1. **E → F passa do ruído:** "premise"/"hypothesis" vai de 13 a 0, e a palavra de relação de 25 a 12, uma queda de 13
   contra um ruído de 6. A troca de moldura tem efeito.
2. **F → FR não passa:** as diferenças (relação 12 → 10, texto sobre o texto 5 → 2, cópia 0,36 → 0,30) são do tamanho
   do ruído. **A vantagem da FR na superfície não está demonstrada.** O que ela tem de real é a pergunta natural e a
   convenção de mesma cena no #742.
3. **Os casos individuais também oscilam.** O #878 estava certo na F, fraco na FR e certo de novo na FRG
   ("staying inside a building"). Um caso bom ou ruim numa rodada não é sinal. O que se repete em todas as rodadas
   é sinal:
   - **#948 em F, FR e FRG:** "só se carrega uma mochila por vez";
   - **#9 forçado em todas:** na FRG, "a stop would be empty if no one were already aboard", que não faz sentido.
4. A leitura antiga "com temperatura 0,7, mudar um exemplo sorteia todos os textos" (E2) estava incompleta: **nem é
   preciso mudar o prompt** para sortear de novo.

**Leitura (Claude):** a guarda faz o que devia. Tira a inversão de rótulo da FR por uma regex, sem custo. Mas a
medida de ruído pesa mais que a guarda. Com 45 pares e uma rodada, só diferenças grandes valem: E → F vale, F → FR
não. Entre F e FRG, a escolha é de gosto e de custo, não de número. A F é metade do tempo e não tem o ponto de falha
da reescrita. A FRG tem a pergunta natural que você desenhou, e a guarda cobre a falha que apareceu. Para separar as
duas de verdade, seriam preciso 3 rodadas de cada, ou um lote de ~200 pares lido para erro de fato.

## F e FRG no `Qwen3.6-35B-A3B` (26/10, pedido do Pedro)

**Procedência:** as 90 respostas foram lidas inteiras pelo Claude (nível 2), ao lado das do 9B. Estão em
`lado-a-lado-F-35B.md` e `lado-a-lado-FRG-35B.md`, e os números em `resultados-F-35B.csv`,
`resultados-FRG-35B.csv`, `vazao-*-35B.md` e `python medir.py E-35B F F-35B FRG FRG-35B`. O Pedro ainda não leu.

**Como rodou:** mesmo servidor da E-35B (`-ngl 999 --cpu-moe -c 8192`, experts na RAM, ~4 GB de VRAM), mesmos
prompts, semente e amostragem do 9B. Na FRG, a reescrita também é do 35B. Comando:
`QWEN_MODEL=Qwen3.6-35B-A3B QWEN_TAG=35B python gerar.py gerar F` (e `FRG`).

| Medida | 9B F | **35B F** | 9B FRG | **35B FRG** |
|---|---|---|---|---|
| Palavras (mediana / máx.) | 23 / 30 | **21 / 30** | 23 / 29 | **22 / 30** |
| Nomeia o rótulo | 1 | **0** | 2 | **2** |
| Palavra de relação (lista) | 12 | **21** | 16 | **17** |
| Fala de "premise"/"hypothesis" | 0 | **2** | 0 | **0** |
| Texto sobre o texto | 5 | **4** | 4 | **4** |
| "Simultaneamente" / mesmo lugar | 6 | **11** | 4 | **5** |
| Cópia do par (mediana) | 0,36 | **0,31** | 0,27 | **0,25** |
| Tempo (45 pares) | 30 s | **142 s** | 58 s | **229 s** |
| Guarda acionada | — | — | #126 | **nenhuma** |

**O que se descobriu:**
1. **Os dois erros que o 9B repetia em toda rodada somem no 35B, nas duas variantes:**
   - #948 (mochila marrom × preta): o 9B dizia "só se carrega uma mochila por vez". O 35B diz que a mesma mochila não
     pode ter as duas cores (F: *"having one color precludes having the other as the same object"*);
   - #9 (rótulo-ouro errado): o 35B não força a ponte e argumenta contra o rótulo, como já tinha feito na E-35B. São
     três rodadas seguidas, então é sinal, não sorte.
2. **O 35B tem erros próprios, que mudam de uma variante para outra** (o padrão do ruído):
   - #460 na F: leu o erro de digitação da hipótese ("but" por "buy") ao pé da letra e respondeu que os homens "não
     são vendidos como produto". Na FRG a reescrita corrigiu o erro e a resposta saiu certa;
   - #742 na F e #976 na FRG: raciocínio de neutro ("a presença de um não implica a do outro"; "músicos não são
     necessariamente palhaços") num par de contradição. No outro lado, cada um saiu certo;
   - deslizes menores na FRG: #531 ("stationary or dry" para um bebê na piscina) e #75 (carregar cruz na Páscoa).
3. **Na forma, empata com o 9B.** Cópia, tamanho e metalinguagem ficam dentro do ruído (±6 na palavra de relação).
   A exceção é a F do 35B: 21 palavras de relação contra 12, quase tudo "implies" e "mutually exclusive", e 11 casos
   de "simultaneamente". É redundância, não erro, e fica no limite do ruído.
4. **A reescrita do 35B nunca saiu do molde** (guarda zerada, inclusive nos 12 exemplos), mas condensa menos: as
   perguntas mantêm quase todo o detalhe do par (#126, #296, #75). Fica mais perto da pergunta de molde da F.
5. **O eco da implicação quase literal continua igual** (#126, #296: *"explicitly states"*). Vem do par, não do
   modelo, como já se tinha visto na E-35B.
6. **Custo:** 3,2 s por par na F e 5,1 s na FRG, contra 0,7 s e 1,3 s no 9B (4,7× e 3,9×).

**Leitura (Claude):** a troca de modelo resolve o que a troca de prompt não resolvia. Os erros que se repetiam no
9B eram do modelo, não do prompt nem do sorteio. O 35B ainda erra por item, mas o erro dele muda de rodada para
rodada, o que é o perfil de algo que uma segunda geração ou um juiz pode filtrar. O custo é ~4–5× o tempo. Na F e na
FRG do 35B, a contagem de erros fica igual (2 na F, 2 na FRG, mais 2 deslizes menores); a FRG custa 60% a mais e
a reescrita condensa pouco. A decisão do 21/10 (35B como fallback) tem agora um argumento novo, os dois erros fixos
do 9B, e continua sendo do Pedro.

## Vazão do 35B com experts na GPU, e F/FRG em 90 pares nos dois modelos (26/10, pedido do Pedro)

**Procedência:** as 360 respostas (90 pares × F e FRG × 9B e 35B) foram lidas inteiras pelo Claude (nível 2). Estão em
`lado-a-lado-{F,FRG}-{9B,35B}-90.md`; os números em `resultados-*-90.csv`, `vazao-*-90.md` e
`python medir.py F-9B-90 F-35B-90 FRG-9B-90 FRG-35B-90`. **A contagem de erros abaixo é leitura do Claude, sem
gabarito do Pedro.** O Pedro ainda não leu.

**Amostra de 90:** os 45 pares antigos + 45 novos (15 por rótulo), sorteados com a mesma semente entre os 1.000 pares do
piloto do Claude, fora os 45 antigos e os 12 pares dos exemplos. Todos têm Humano, Haiku e Sonnet ao lado.
`python gerar.py amostra90` → `amostra-90.csv`; a geração roda com `QWEN_SAMPLE=amostra-90.csv`.

### Vazão: `--n-cpu-moe`

`--n-cpu-moe N` deixa na RAM os experts das N primeiras camadas e põe o resto na GPU. `llama-bench` (512 tokens de
prompt, 128 de geração, 2 repetições):

| `--n-cpu-moe` | Geração (tok/s) | Observação |
|---|---|---|
| todos (`--cpu-moe`) | 28,1 | configuração da E-35B e da F-35B |
| 36 | 30,7 | |
| 32 | 31,1 | |
| 28 | 35,1 | |
| **27** | **38,4** | escolhido; servidor usa 7,7 de 8,15 GB de VRAM |
| 26 | 36,6 | |
| 24 | 13,9 | VRAM estoura e a geração despenca |

O prefill (pp512) oscilou demais entre repetições (± 40–80 tok/s) para ser comparado.

**Na geração real (90 pares, um fluxo):**

| | 9B | 35B, todos na RAM (45 pares) | **35B, `--n-cpu-moe 27`** |
|---|---|---|---|
| F, segundos por par | 0,64 | 3,2 | **2,0** |
| FRG, segundos por par | 1,24 | 5,1 | **3,8** |

O ganho é de ~36% na F. O que sobra é prefill: o log do servidor mostra, por pedido, ~270–490 tokens de prompt
reprocessados (~1 s) e ~25 tokens gerados a ~36 tok/s (~0,7 s). O cache reaproveita só parte do bloco fixo de
exemplos. **Conta, não medida:** 100 mil pares na F levariam ~57 h no 35B e ~18 h no 9B, num fluxo só. O lote
(`--parallel`) continua sem medir.

### Superfície

| Medida | Humano | 9B F | **35B F** | 9B FRG | **35B FRG** |
|---|---|---|---|---|---|
| Palavras (mediana / máx.) | 11 / 39 | 23 / 33 | 22 / 29 | 22 / 35 | 21 / 29 |
| Nomeia o rótulo | 0 | 4 | 4 | 4 | 1 |
| Palavra de relação (lista) | 13 | 28 | 38 | 30 | 35 |
| Fala de "premise"/"hypothesis" | 0 | 0 | 6 | 0 | 5 |
| Texto sobre o texto | 2 | 7 | 13 | 8 | 10 |
| "Simultaneamente" / mesmo lugar | 6 | 15 | 23 | 13 | 17 |
| Cópia do par (mediana) | 0,83 | 0,33 | 0,30 | 0,29 | 0,28 |
| Guarda acionada | — | — | — | #126 | nenhuma |

O 35B fala mais de "premise", "mutually exclusive" e "simultaneously", embora o prompt nunca use "premise": ele
reconhece sozinho que é tarefa de NLI. É redundância, não erro.

### Erros (leitura do Claude)

| | 9B F | **35B F** | 9B FRG | 35B FRG |
|---|---|---|---|---|
| 45 antigos | 3 (#948, #9, #742) | 2 (#742, #460) | 2 (#948, #9) | 0 |
| 45 novos | ~7 | **~1–2** | ~6 | ~4 |
| **Total em 90** | **~10** | **~3–4** | **~8** | **~4** |

Contei como erro: fato errado sobre o mundo, raciocínio de outro rótulo (resposta contra o ouro, salvo quando o ouro
está errado, como o #9) e lógica embaralhada. Não contei o eco da implicação quase literal.

### Padrões que os 90 pares mostraram

1. **A reescrita perde o detalhe que decide o rótulo, e a guarda não vê.** A guarda confere o molde, não o conteúdo.
   - No 9B, em 4 das 15 implicações novas: #218 vira "por que construir uma casa de gengibre quer dizer que ela tem
     cabelo castanho?", e a resposta passa a argumentar contra o ouro; #291, #121 e #27 perdem o fato e a resposta
     inventa uma ponte ("abrir os braços mostra que estão sorrindo").
   - No 35B, uma vez: #745 perde o "maiô", e a resposta sai fraca.
   - O 9B também produz perguntas com gramática quebrada que passam na regex (#934, #584, #455).
   
   É o padrão que mais pesa contra FR/FRG.
2. **O 35B argumenta contra rótulo-ouro fraco.** O #9 de novo e, na FRG, o #221 (cachorro espirrando água → "se
   divertindo": "também espirram fugindo de predador"). Para treino, a justificativa contra o rótulo é ruído. Como
   sinal, aponta rótulo-ouro suspeito: é o tipo de caso que um juiz ou uma lista de revisão deveria pegar.
3. **Contradição entre pessoas diferentes vira raciocínio de neutro** (#742 na F do 35B, de novo; #956 na F do 35B):
   "um homem e uma mulher são pessoas distintas, a presença de um não implica a do outro". Falta à resposta a
   convenção do e-SNLI de que as duas frases descrevem a mesma cena. Nenhum dos 12 exemplos cobre troca de pessoa.
   Quando acerta, o 35B diz direto: "Women are not men" (#747).
4. **A F do 35B lê o erro de digitação ao pé da letra** (#460, "but" por "buy", nas duas rodadas). A reescrita
   corrige isso, e é o único caso em que ela ajudou.
5. **Os erros do 9B se concentram em contradições com duas ações** (#733, #850, #860): ele embaralha quem faz o quê
   ("um homem não pode puxar a corda enquanto outro o observa"). E em fatos inventados (#517: "corredores são de casas
   ou escritórios, não de hotéis"; #623: "trenó é para neve").
6. **Atributo trocado (cor, roupa, cabelo) os dois resolvem bem** (#773, #846, #917, #948 no 35B).
7. **O eco da implicação quase literal segue igual nos dois** (#126, #296, #218, #228): "explicitly states". Vem do par.

### Correção sobre o ruído entre rodadas

A F do 9B, rodada de novo num servidor recém-ligado, **reproduziu os 45 textos antigos, palavra por palavra (45/45)**.
A FRG do 9B repetiu 27 de 45. O 35B com outra divisão GPU/RAM repetiu 27 de 45 na F e 9 de 45 na FRG. Então a frase da
seção FRG ("o servidor não reproduz entre rodadas") vale para a FR/FRG, não para a F do 9B.

**Hipótese, não medida:** na F todo pedido começa com o mesmo bloco de exemplos, e o reaproveitamento de cache é sempre
igual. Na FR/FRG, os pedidos de reescrita se intercalam e mudam o que o cache reaproveita, o que muda as contas em
ponto flutuante. No 35B, mudar a divisão entre GPU e RAM também muda as contas. O ruído de ±6 medido em FR × FRG
continua sendo a régua para comparar rodadas da FR/FRG.

**Leitura (Claude):** a vazão subiu ~36% com `--n-cpu-moe 27`, mas o 35B segue ~3× mais lento que o 9B na F. Nos 90
pares, a **F do 35B foi a que menos errou (~3–4 contra ~10 da F do 9B)**, e é também a variante mais barata do 35B. A
FRG não se pagou em nenhum dos dois modelos: custa ~2× a F, e a reescrita introduz a falha nova do padrão 1, que a
guarda não pega. Dois ajustes baratos ficam visíveis: um exemplo de contradição com troca de pessoa (padrão 3) e uma
lista de revisão para respostas contra o ouro (padrão 2).

## Vazão com pedidos simultâneos (`--parallel`), variante F (27/10, pedido do Pedro)

**Procedência:** medição do Claude. Tempos de parede do `gerar.py` com `QWEN_WORKERS=N` (pedidos em paralelo) e logs
do servidor. Arquivos em `vazao-paralelo/` (`vazao-*.md`, `resultados-*.csv`, `server-*.log`). Só a F foi medida; a
FRG em paralelo ficou sem medir.

### 9B (90 pares, segundos por par)

| Servidor | 1 pedido | 2 | 4 | 8 |
|---|---|---|---|---|
| `-np 8 -kvu -c 16384` (micro-lote padrão, 512) | 0,63 | 0,50 | 0,42 | 0,41 |
| **`-np 8 -kvu -c 16384 -cms 0 -ub 128`** | 0,52 | 0,38 | 0,31 | **0,28** |

O ganho do paralelo puro é pequeno (0,63 → 0,41) porque o que pesa é o prompt reprocessado: o log mostra ~500 dos ~800
tokens refeitos a cada pedido, quase todos do bloco fixo de 12 exemplos. O Qwen3.5 é híbrido (camadas recorrentes), e
o servidor só volta a um ponto salvo do cache (checkpoint), que fica a ~1 micro-lote do fim do prompt anterior. Com
`-ub 128` e `-cms 0` (checkpoints sem espaçamento mínimo), a mediana reprocessada cai de 503 para 121 tokens. `-ub 64`
reprocessa 79, mas fica igual ou pior (0,33 com 4 pedidos). VRAM: ~7,0 GB.

**Queda do servidor:** com `-np 8` sem `-kvu` (cache separado por vaga, 2.048 tokens cada), o servidor caiu sem
mensagem no meio da rodada com 2 pedidos (código de saída 127). Com `-kvu` rodou tudo. Não investiguei a causa.

### 35B (30 pares, `--n-cpu-moe 30`, segundos por par)

| Servidor | 1 pedido | 2 | 4 |
|---|---|---|---|
| `-c 8192` (micro-lote padrão) | 2,22 | 1,82 | 1,83 |
| **`-c 8192 -np 4 -kvu -cms 0 -ub 128`** | 1,89 | 1,74 | **1,66** |

O paralelo ajuda pouco no 35B (2,22 → 1,66): os experts das 30 camadas na RAM rodam na CPU, e cada sequência do lote
ativa experts diferentes, então o trabalho da CPU cresce com o lote.

**Por que `--n-cpu-moe 30` e não 27:** hoje, com 27, o 35B fez **6,1 s/par com 1 pedido** (ontem, 1,9), gerando a
~17 tok/s e com prompt a ~125 tok/s (ontem, 36 e ~390). O `llama-bench` com 27, rodado logo depois, deu 39,4 tok/s,
normal. Com 30, o servidor ocupa ~7,0 GB e voltou a 2,2 s/par. **Hipótese mais provável, não comprovada (não li o
contador de memória compartilhada da GPU):** com 27 o servidor fica em ~7,7 de 8,15 GB, e hoje outros programas já
seguravam ~0,5 GB com a GPU parada. No limite, o Windows passa parte da VRAM para a RAM, a mesma queda vista com
`--n-cpu-moe 24`. O 27 só vale com a GPU livre; o 30 dá folga.

### O paralelo muda as respostas?

| Comparação com a rodada de ontem | Textos iguais |
|---|---|
| Mesmo servidor, 1 pedido (9B, 90 pares) | 90/90 |
| Mesmo servidor, 1 pedido (35B, `--n-cpu-moe 27`, 30 pares) | 30/30 |
| Qualquer mudança: 2–8 pedidos, `-ub`, `--n-cpu-moe` | 11–22 de 90 (9B); 1–16 de 30 e 14 de 90 (35B) |

O texto exato depende da configuração: com a mesma configuração, a rodada se repete palavra por palavra; trocar o lote
ou a divisão GPU/RAM muda a maioria dos textos. A superfície não muda (`python medir.py` com os .csv de
`vazao-paralelo/`):

| Medida | 9B 1 pedido | 9B 8 pedidos, `-ub 128` | 35B ontem | 35B 4 pedidos, `-ub 128` |
|---|---|---|---|---|
| Palavras (mediana) | 23 | 23 | 23 | 22 |
| Palavra de relação | 28 de 90 | 21 de 90 | 11 de 30 | 10 de 30 |
| Nomeia o rótulo | 4 | 4 | 0 | 0 |
| Cópia do par (mediana) | 0,33 | 0,31 | 0,30 | 0,33 |
| Cortes / `<think>` | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

Não li as respostas em paralelo uma a uma, então os erros não foram contados de novo.

**Consequência para o dataset:** a reprodução palavra por palavra só existe com a configuração congelada. O dataset é
o arquivo gerado, e a configuração do servidor entra no registro dele (comando, `QWEN_WORKERS`, semente).

### Conta, não medida: horas de geração

| | s/par | 10 mil pares | 100 mil pares |
|---|---|---|---|
| 9B, 8 pedidos, `-ub 128` | 0,28 | ~47 min | ~7,8 h |
| 35B, 4 pedidos, `-ub 128` | 1,66 | ~4,6 h | ~46 h |

O 35B passou de ~3× para ~6× mais lento que o 9B, porque só o 9B aproveita o lote. A amostra do 35B tem 30 pares;
a do 9B, 90.

## Primeiro lote no treino: 35B, variante F (27/10, pedido do Pedro)

**Decisão do Pedro (27/10):** 35B com a F, até as 8h, alvo de 16 mil pares. **Baixado com autorização dele:** o
treino do e-SNLI (`dados/esnli/esnli_train_1.csv` e `_2.csv`, 90 e 99 MB, do repositório oficial
`OanaMariaCamburu/e-SNLI`). Até então só o dev estava no disco, e todos os pilotos saíram do dev.

- **Amostra:** `resultados/lote-35B/amostra-treino.csv` = o treino inteiro (549.367 pares, menos 28 sem hipótese
  ou sem justificativa humana) embaralhado com semente 42. O lote segue essa ordem, então qualquer começo dele é uma
  amostra aleatória do treino, e a curva de aprendizado pode ser cortada do que saiu.
- **Código:** `src/radibert/lote.py` (prompt da F tirado do `gerar.py`, 4 pedidos simultâneos, grava cada par
  ao terminar e retoma de onde parou) e `rodar.sh` (sobe o servidor do 35B com os parâmetros medidos acima, refaz até 3
  vezes se ele cair, desliga no fim).
- **Saída:** `resultados/lote-35B/racionalizacoes-F-35B.csv`, com o horário de cada par. O progresso fica em
  `progresso.txt` e `run/train.log`.
- **Parada:** às 7h50 ou aos 16 mil pares, o que vier primeiro. **Conta:** a 1,49 s/par dos primeiros 100, ~6h40 dão
  ~16 mil, no limite do alvo.
- **Resultado (27/10, 6h24):** bateu o alvo antes do prazo. **16.000 pares** em 5h20 (15.992 nesta rodada, mais 8 do
  teste com a mesma configuração), **1,20 s/par**, primeira tentativa, sem queda do servidor (`tentativa-1.err` vazio),
  servidor desligado no fim. Os 16 mil são exatamente os 16 mil primeiros da amostra, sem par repetido. Rótulos:
  5.406 neutro, 5.320 implicação, 5.274 contradição. Todos terminaram por `stop` (nenhum corte por tamanho).
  Superfície: 22 palavras na mediana, 37 no máximo, 165 acima de 30. Pelo regex do `medir.py`, 583 (3,6%) contêm uma
  palavra de rótulo (entail, neutral, contradict) e 434 (2,7%) falam "premise" ou "hypothesis". Ninguém leu os textos.
  O 1,20 s/par é mais rápido que o 1,66 da medição. **Hipótese, não medida:** de madrugada nada mais ocupava a VRAM.
- **Marca de eco (28/10, pedido do Pedro):** `src/radibert/eco.py` grava `marcas.csv` (pairID,
  `novas_hipotese`, `eco`) ao lado do lote, sem mexer no arquivo do lote. A regra é a de 21/10: implicação cuja
  hipótese não tem nenhuma palavra de conteúdo fora da premissa (palavras do `copia.py`, sem lematização, então o eco
  sai **subestimado**). No dev, a regra reproduz a contagem de 21/10 casa por casa (847 pares, 8,6%; 25,4% das
  implicações). **No lote: 1.252 pares de eco, 7,8% do total e 23,5% das implicações.** Com até 1 palavra nova, o teto
  sobe para 62,3% das implicações. Nos pares de eco, o Qwen copia menos do par que o humano (mediana de 0,38 das
  palavras de conteúdo, contra 0,83) e traz ~6 palavras novas, contra 1. Parte delas é recheio ("explicitly
  stated", "directly confirms"), e a contagem léxica não separa recheio de ponte; quem separa é a leitura. A marca de
  discordância não foi feita: precisa de horas de GPU, e o PC estava instável.

## Decisões que ficam com o Pedro

0. ~~Confirmar ou corrigir a hipótese do que caiu na D, e escolher ou escrever os exemplos da variante E.~~ Feito em
   21/10: os 12 exemplos, e a E rodou. Falta ler o `lado-a-lado-E.md` e decidir entre E e E2 (com um exemplo de
   implicação quase literal).
1. Ler os três lado a lado (`lado-a-lado.md`, `-B.md`, `-D.md`) e dizer se o Qwen serve como professor, e com qual
   prompt.
2. ~~Rodar sem as definições de rótulo (variante B).~~ Feito em 20/10: o molde não some.
3. ~~Rodar a variante D.~~ Feito em 20/10: a frase vazia some, ~16 palavras.
4. Exemplos no prompt (a variante C original): escolher 4–6 justificativas de que você goste, do treino do e-SNLI ou
   destas, se quiser testar se tiram o "which contradicts the hypothesis".
5. ~~Medir a vazão com lote (`--parallel 4/8`) antes de falar em volume.~~ Feito em 27/10: 9B 0,28 s/par, 35B
   1,66 s/par na F (seção da vazão com pedidos simultâneos).
6. (25/10) Ler o `lado-a-lado-F.md` e decidir se a F substitui a E, e se vale rodar a F2 ou a F com reescrita.
   (26/10) A FR rodou; ver a seção FR. Decidir entre F e FR, e se a FR ganha a guarda de molde.
   (26/10) A FRG rodou: a guarda pega o #126, e FR × FRG mediu o ruído entre rodadas. Decidir entre F e FRG.
   (26/10) F e FRG rodaram no 35B: o 35B corrige #948 e #9, que o 9B errava em toda rodada, a ~4–5× o tempo.
   Decidir se o 35B sai de fallback.
   (26/10) Com `--n-cpu-moe 27` o 35B faz a F em 2,0 s/par; em 90 pares a F do 35B errou ~3–4 contra ~10 da F do 9B
   (leitura do Claude), e a reescrita perde o detalhe que decide. Decidir modelo (9B × 35B) e variante (F × FRG), e se
   entram o exemplo de troca de pessoa e a lista de respostas contra o ouro.
   (27/10) Com pedidos simultâneos: 9B 0,28 s/par (~8 h para 100 mil) e 35B 1,66 s/par (~46 h), na F. Decidir modelo e
   variante com esse custo.

## Para subir o servidor de novo

```
C:\Users\Pedro\Documents\Projects\tools\llama.cpp-b11770\llama-server.exe -m C:\Users\Pedro\Documents\Projects\tools\models\Qwen3.5-9B-Q4_K_M.gguf -ngl 999 -c 8192 --jinja --host 127.0.0.1 --port 8080
```

O 35B, com a divisão GPU/RAM medida em 26/10:

```
C:\Users\Pedro\Documents\Projects\tools\llama.cpp-b11770\llama-server.exe -m C:\Users\Pedro\Documents\Projects\tools\models\Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 27 -c 8192 --jinja --host 127.0.0.1 --port 8080
```

Para gerar em volume (medido em 27/10), com `QWEN_WORKERS=8` no 9B e `QWEN_WORKERS=4` no 35B:

```
C:\Users\Pedro\Documents\Projects\tools\llama.cpp-b11770\llama-server.exe -m C:\Users\Pedro\Documents\Projects\tools\models\Qwen3.5-9B-Q4_K_M.gguf -ngl 999 -c 16384 -np 8 -kvu -cms 0 -ub 128 --jinja --host 127.0.0.1 --port 8080
C:\Users\Pedro\Documents\Projects\tools\llama.cpp-b11770\llama-server.exe -m C:\Users\Pedro\Documents\Projects\tools\models\Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 30 -c 8192 -np 4 -kvu -cms 0 -ub 128 --jinja --host 127.0.0.1 --port 8080
```

A variante E rodou com `-c 8192`. O prompt com os 12 exemplos tem ~850 tokens, e o servidor divide o contexto entre 4
vagas: com `-c 4096` sobram 1.024 por vaga, no limite.
