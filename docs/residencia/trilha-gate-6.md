# Trilha até o gate 6 (terça 13/10, 15h30 → quarta 14/10, 12h)

**Para que serve:** chegar no gate com uma semana que conta como trabalho, não só com uma definição.
A semana tem três peças: **vocabulário** (definição apoiada em duas leituras), **um resultado** (o teste
dos dados do e-SNLI) e **uma decisão** (a tarefa). O termo descreve as três.

**Procedência:** trilha escrita pelo Claude em 13/10. Os passos de código trazem **esqueleto e dicas**. As linhas
que respondem à pergunta são suas. Os nomes de arquivo, colunas e bibliotecas foram conferidos em 13/10:

| Item | Conferido |
|---|---|
| Cabeçalho real do `esnli_dev.csv` | 19 colunas, entre elas `gold_label`, `Sentence1`, `Sentence2` e `Explanation_1` a `_3` |
| Tamanho do arquivo | 7,5 MB |
| Ambiente local | pandas 3.0.2 e scikit-learn 1.8.0 no py311; nltk **não** está instalado, então a trilha não usa |
| PDFs | arXiv 2301.08912 e 2102.12060 abrem |

---

## Calendário

**Revisão 13/10, 16h30:** o teste (passo 2) passou para antes da leitura. Ele é o que faz a semana valer:
planejamento com coleta que produz resultado, e não só planejamento (conversa de 13/10). Se a noite apertar, quem
encolhe é a leitura, nunca o teste.

| Quando | Passo | Tempo | Se apertar |
|---|---|---|---|
| Ter 16h30 | **0. Decidir a tarefa** | 15 min | Não corta: sem ela o Planejamento fica vazio |
| Ter 16h45 | **2. Teste dos dados** | ~2h30 | Corta o 2.7 (destaques). **Não cortam:** o 2.3 (olhar), o 2.5 (controle) e o 2.9 (registro) |
| Ter 19h15 | Pausa | — | — |
| Ter 20h | **1. Leitura dirigida:** Wiegreffe, depois Gurrapu | ~2h | Lê só o Wiegreffe (mais claro sobre os tipos) e o Gurrapu fica para a semana |
| Ter 22h | **3. O que adaptar na D** | 30 min | Vira uma linha no Planejamento |
| Qua 8h | **4. Termo:** eu redijo, você adapta | 1h | — |
| Qua 9h30 | **5. Ensaio da arguição** | 30 min | Pelo menos a definição em voz alta |
| Qua 12h | **Entrega** | — | — |

---

## Passo 0. Decidir a tarefa (15 min)

A comparação está na conversa de 13/10 e em `docs/datasets-nli-verificacao.md`. Resumindo:

- **e-SNLI (inglês):** racionalização humana pronta, sem custo de API; 3 rótulos, contradição incluída. Perde o
  argumento do pt-BR, que era de novidade.
- **ASSIN2 (pt-BR):** sem racionalização, que teria de ser gerada com LLM local em 8 GB; 2 rótulos; fatos simples
  por construção.

**Escreva em uma ou duas frases:** qual escolheu e por quê. Essa frase vai direto para o termo.

O passo 2 usa o e-SNLI de qualquer jeito. Se você escolher ASSIN2, ele continua valendo como estudo do que uma
racionalização humana carrega, e o termo diz isso.

---

## Passo 1. Leitura dirigida (~2h)

**Objetivo:** apoiar a definição em fontes que **você** leu, e saber nomear os tipos.

| Obra | PDF |
|---|---|
| Wiegreffe & Marasović (2021), *Teach Me to Explain*, NeurIPS | https://arxiv.org/pdf/2102.12060 |
| Gurrapu et al. (2023), *Rationalization for Explainable NLP: A Survey*, Frontiers in AI | https://arxiv.org/pdf/2301.08912 |

**Como ler:** caça dirigida (`docs/metodo-de-leitura.md`): promessa (abstract) → origem (introdução) → núcleo →
Ctrl+F → fecho. Pule tudo que não seja definição e tipos.

**Ordem:** o Wiegreffe primeiro. Ele é a referência dos tipos, e o Gurrapu fica mais fácil depois.

**O que caçar (§7 da `docs/leituras/explicacao-racionalizacao.md`):**

1. **A definição de cada um**, com página. A sua (§1 da explicação, corrigida por você em 13/10) bate com a deles?
   Onde diverge?
2. **Os tipos com os nomes exatos.** O Wiegreffe deve trazer *highlights*, *free-text* e *structured*, mas
   **confira**. O Gurrapu fala em extrativa × abstrativa: é a mesma divisão com outro nome?
3. **Ctrl+F:** `faithful`, `plausib`, `post-hoc`, `e-SNLI`.
   - O que o Wiegreffe diz do e-SNLI é ouro para o passo 2: se ele comenta que as explicações seguem um template
     ou repetem a entrada, o seu teste mede isso. Como o teste já terá rodado, acrescente a observação ao
     `resultado.md`, dizendo se confirma ou contradiz o seu número.
4. **Algum dos dois trata racionalização como sinal de treino**, ou só como explicação para pessoas? Se só como
   explicação, isso mostra a diferença do seu tema (§6 da explicação).

**Registro:** no formato do `Leituras Semana 5`: Questionamento, Núcleo, conclusão, com as suas palavras e página
em cada anotação. Depois, uma entrada em `docs/leituras/glossario.md`: a sua definição, com a fonte.

---

## Passo 2. Teste dos dados do e-SNLI (~2h30)

### 2.1 A pergunta, em uma frase

> **Quanto de uma racionalização humana do e-SNLI já está escrito na premissa e na hipótese?**

**Por que importa:** o Wadhwa (2024), que você leu, mostra que embaralhar os tokens da racionalização não derruba o
ganho. Se as racionalizações são, em boa parte, **cópia de palavras do input**, o sinal que transferem pode ser
"quais palavras do input importam" (perto de uma racionalização extrativa disfarçada), e não raciocínio. Se trazem
muita palavra nova, carregam conhecimento que não está no input, como o "pé" do seu exemplo.

### 2.2 Baixar o arquivo

```bash
mkdir -p "/c/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial/dados/esnli"
```

```bash
curl -L -o "/c/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial/dados/esnli/esnli_dev.csv" "https://raw.githubusercontent.com/OanaMariaCamburu/e-SNLI/master/dataset/esnli_dev.csv"
```

É o conjunto de validação, com uns 10 mil pares e **3 racionalizações por par** (3 anotadores), o que dá umas 30 mil
racionalizações. O treino não é necessário.

### 2.3 Olhar antes de contar (30 min, sem pular)

Todo praticante olha os dados antes de medir. É aqui que você descobre o que o número vai esconder.

```python
import pandas as pd

CSV = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial\dados\esnli\esnli_dev.csv"
df = pd.read_csv(CSV)
pd.set_option("display.max_colwidth", None)

print(df.shape)
print(df["gold_label"].value_counts())
print(df.sample(15, random_state=1)[["gold_label", "Sentence1", "Sentence2", "Explanation_1"]])
```

Leia umas 50 linhas, 15 de cada vez, trocando o `random_state`. **Anote à mão o que você vê:**

- As explicações de contradição têm um molde? (algo como "X cannot Y and Z at the same time")
- As de implicação repetem a hipótese? ("A man is a person")
- Quantas trazem conhecimento de mundo que não está no texto?

Essas anotações valem tanto quanto o número. São a parte qualitativa do resultado.

### 2.4 As decisões de medida (suas; anote cada uma)

| Decisão | Sugestão | Por quê |
|---|---|---|
| O que é "palavra" | Minúsculas, só letras: `re.findall(r"[a-z]+", texto.lower())` | Simples e explicável em uma frase |
| Palavras vazias (the, a, is…) | Tirar, com `ENGLISH_STOP_WORDS` do sklearn | Sem tirar, "the" e "is" inflam a cópia |
| Plural e conjugação (hug/hugging) | **Não** tratar | Mais simples; fica declarado como limitação: subestima a cópia |
| Contar repetição? | Não: conjunto de palavras | "Que fração das palavras distintas da explicação está no input" |
| Entrada | Premissa + hipótese juntas | É o que o modelo vê |

### 2.5 O controle (não corte)

Um número sozinho não diz nada. Se 60% das palavras da explicação estão no input, isso é muito ou pouco? O SNLI é
cheio de "man", "woman", "people", que aparecem em qualquer par.

**Controle:** medir a mesma coisa contra o input de **outro par, sorteado**. A diferença entre o próprio par e o par
sorteado é a **cópia de verdade**.

É o mesmo raciocínio do controle do DHRD, que você leu: trocar pela racionalização de outro exemplo. E é o
instrumento "ruído / linha de base" do `docs/pesquisa/mapa-do-terreno.md`.

### 2.6 O esqueleto (você completa os TODO)

Arquivo sugerido: `src/radibert/copia.py`

```python
import re
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

CSV = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial\dados\esnli\esnli_dev.csv"
df = pd.read_csv(CSV)

# uma linha por racionalização: Explanation_1..3 viram uma coluna só
longo = df.melt(
    id_vars=["pairID", "gold_label", "Sentence1", "Sentence2"],
    value_vars=["Explanation_1", "Explanation_2", "Explanation_3"],
    var_name="anotador",
    value_name="explicacao",
).dropna(subset=["explicacao"])


def palavras(texto):
    """Conjunto de palavras de conteúdo: minúsculas, só letras, sem stopwords."""
    return {p for p in re.findall(r"[a-z]+", str(texto).lower()) if p not in ENGLISH_STOP_WORDS}


def fracao_copiada(explicacao, entrada):
    """Fração das palavras de conteúdo da explicação que aparecem na entrada."""
    # TODO 1: monte os dois conjuntos com palavras()
    # TODO 2: se a explicação não tiver nenhuma palavra de conteúdo, devolva None
    #         (senão você divide por zero)
    # TODO 3: devolva len(interseção) / len(palavras da explicação)
    ...


# --- medida no PRÓPRIO par ---
# TODO 4: coluna longo["copia_propria"], aplicando fracao_copiada linha a linha.
#   dica: a entrada é Sentence1 + " " + Sentence2;
#   uma forma é: [fracao_copiada(e, s1 + " " + s2) for e, s1, s2 in zip(...)]

# --- controle: entrada de OUTRO par, sorteado ---
# TODO 5: coluna longo["copia_outro"].
#   dica: embaralhado = longo.sample(frac=1, random_state=0)
#   pegue Sentence1/Sentence2 dele com .to_numpy(). Sem o .to_numpy(), o pandas
#   realinha pelo índice e você mede contra o próprio par sem perceber.
#   (Pense: um par sorteado pode cair nele mesmo? Com ~30 mil linhas, o efeito é desprezível,
#   mas saiba responder se perguntarem.)

# --- resultado ---
# TODO 6: média de copia_propria e copia_outro, no geral e por gold_label.
#   dica: longo.groupby("gold_label")[["copia_propria", "copia_outro"]].mean()
# TODO 7: quantas explicações viraram None (sem palavra de conteúdo)?
```

**Conferência rápida antes de confiar no número:** escolha 3 linhas, faça a conta à mão e compare com o que o script
deu. Se não bater, o erro é do script, não da sua conta.

### 2.7 Opcional, só se sobrar tempo: os destaques

O e-SNLI também tem racionalização **extrativa**: os anotadores marcaram palavras com `*` em `Sentence1_marked_1` e
`Sentence2_marked_1`. Pergunta extra: **as palavras destacadas aparecem na explicação em texto livre?** Se quase
sempre aparecem, a explicação em texto livre "contém" a extrativa, o que liga direto aos tipos do passo 1.

Dica: `re.findall(r"\*(\w+)", texto)` pega as palavras marcadas.

### 2.8 Como ler o resultado

**Os cortes são decisão sua.** Escreva-os **antes** de rodar, senão você ajusta a história ao número.

| Se der… | Leitura possível |
|---|---|
| Próprio ≫ outro, e a cópia é alta | As racionalizações repetem muito do input. O sinal pode ser em boa parte "quais palavras importam", o que é compatível com o Wadhwa (embaralhar não derruba) |
| Próprio ≫ outro, e a cópia é moderada | Elas misturam cópia e palavra nova. Vale olhar o que são as palavras novas: conhecimento de mundo ou molde ("cannot", "same time")? |
| Próprio ≈ outro | A "cópia" é só vocabulário comum do SNLI. A medida não separa nada, e isso também é resultado |
| Muita diferença entre os rótulos | O sinal muda por rótulo; contradição provavelmente é a mais moldada. Isso pesa na hora de escolher a loss |

### 2.9 Registrar (15 min)

Em `resultados/s6-copia-esnli/resultado.md`, com as suas palavras:

- a pergunta (2.1);
- as decisões de medida (2.4);
- os números (próprio, outro, por rótulo);
- as anotações à mão (2.3);
- **limitações:** só validação; cópia lexical, não de sentido; sem tratar plural e conjugação; **racionalização
  humana, não de LLM.** O tema usa racionalização de LLM, então o resultado vale para o e-SNLI e é uma pista, não
  uma prova, para o caso do LLM.

---

## Passo 3. O que adaptar na D (30 min)

Você disse em 12/10 que queria adaptar coisas na D antes de começar. Escreva:

- o que muda e por quê, em uma lista curta;
- se o resultado do passo 2 muda alguma coisa, por exemplo "a racionalização do e-SNLI é muito moldada, então…".

Isso vira o **Planejamento** do termo.

---

## Passo 4. Termo (quarta, 8h)

Quando você pedir, eu rodo a skill `termogate` e redijo a partir de:

- passo 0 (decisão);
- passo 1 (registro da leitura);
- passo 2 (resultado.md);
- passo 3.

Você adapta, e não cola. **Declarado no termo:** o esqueleto do script veio de LLM, e as linhas da medida e a
leitura dos dados são suas.

**Entregáveis prováveis (.docx):** o registro das duas leituras e o resultado do teste. Eu gero a partir dos .md.

---

## Passo 5. Ensaio da arguição (quarta, 30 min)

Diga **em voz alta**, sem ler:

| Pergunta | Onde está |
|---|---|
| O que é racionalização? | Sua definição + fonte do passo 1 |
| Quais os tipos? | Passo 1 |
| Qual a diferença para o CoT? | §3 da explicação |
| Se o encoder não gera texto, como usa a racionalização? | §6 da explicação |
| O que fica no encoder quando a cabeça sai? | §6: os pesos mudados pelo gradiente |
| Por que e-SNLI (ou ASSIN2)? | Passo 0 |
| O que o seu teste mostrou, e o que ele **não** mostra? | Passo 2.9, incluindo as limitações |
| Por que o controle com outro par? | Passo 2.5 |

A última linha é a que mais impressiona um arguidor: **saber dizer o que o próprio resultado não prova.**
