# Geracao com Modelo Local

## 1. Por que um modelo local

A politica de uso da Anthropic nao permite treinar modelos com as saidas do Claude sem autorizacao previa. Por isso
passei a gerar as justificativas com um modelo de pesos abertos, rodando no meu notebook:

- **Gerador principal:** Qwen3.5-9B (licenca Apache-2.0), arquivo GGUF Q4_K_M, inteiro na GPU (RTX 5060, 8 GB);
- **Reserva:** Qwen3.6-35B-A3B (Apache-2.0), arquivo GGUF UD-IQ4_XS, com os experts na memoria RAM.

Os dois rodam no llama.cpp (llama-server), com o modo de raciocinio desligado. A geracao nao tem custo de API.

## 2. Como rodei

- **Pares:** 45 pares do conjunto de validacao do e-SNLI, 15 por rotulo. Sao os mesmos pares da comparacao entre
  justificativas humanas e de LLM da semana anterior, entao cada versao fica ao lado do humano, do Haiku e do Sonnet;
- **Rotulo:** o modelo recebe o rotulo correto e explica por que ele vale (geracao pos-hoc);
- **Amostragem:** a recomendada no cartao do modelo (temperature 0.7, top_p 0.8, top_k 20, presence_penalty 1.5),
  com semente 42 em todas as versoes;
- **Uma coisa por vez:** cada versao do prompt muda uma parte em relacao a anterior, para saber o que causa cada
  efeito.

## 3. O prompt base

Todas as versoes usam este molde. O que muda entre elas e o bloco de cima ({definitions}) e o pedido ({ask}).

```
You are annotating a natural language inference dataset.
{definitions}
Premise: {premise}
Hypothesis: {hypothesis}
Label: {label}

{ask} Do not name the label. Write only the explanation.
```

## 4. As sete versoes

| Versao | Bloco de cima | Pedido |
|---|---|---|
| A | definicoes dos rotulos | uma ou duas frases |
| B | nada | uma ou duas frases |
| D | nada | uma frase, ate 25 palavras, o fato da premissa que decide |
| E | 12 exemplos meus | uma frase, cerca de 30 palavras, o conhecimento que liga premissa e hipotese, com uma regra por rotulo |
| E2 | 12 exemplos + 1 exemplo de implicacao quase literal | igual a E |
| E3 | 12 exemplos | E + responder curto e sem enchimento quando a hipotese so repete a premissa |
| E4 | 12 exemplos | E3 + proibido citar premissa e hipotese e usar palavras de relacao |

**Definicoes dos rotulos (versao A):**

```
Labels:
- entailment: if the premise is true, the hypothesis must be true.
- neutral: the hypothesis might be true, but the premise does not guarantee it.
- contradiction: if the premise is true, the hypothesis cannot be true (both describe the same scene).
```

**Pedido das versoes A e B:**

```
Explain in one or two sentences why this label is correct.
```

**Pedido da versao D:**

```
Explain in one sentence (at most 25 words) why this label is correct, stating the fact from the premise that
decides it.
```

**Pedido das versoes E e E2:**

```
Explain in one sentence (about 30 words at most) why this label is correct, stating the world knowledge that links
the premise to the hypothesis. For entailment, cover what the hypothesis adds; for neutral, give an alternative the
premise allows; for contradiction, say why both cannot happen in the same scene. Follow the style of the examples.
```

**Frase somada na versao E3:**

```
When the hypothesis only repeats part of the premise, answer in a few words with no filler.
```

**Frase somada na versao E4:**

```
Do not refer to the premise or the hypothesis (no "the premise says", "the hypothesis states"), and do not use
relation words such as contradicts, confirms, supports or entails.
```

**Exemplos (versoes E a E4):** os 12 exemplos do documento Exemplos da Justificativa, na versao final, intercalados
por rotulo, cada um no formato abaixo. Nenhum dos 12 pares esta entre os 45 testados.

```
Premise: ...
Hypothesis: ...
Label: ...
Explanation: ...
```

**Exemplo extra da versao E2:**

```
Premise: A man is leaning out of a window to paint some decorative iron white.
Hypothesis: A man is painting.
Label: entailment
Explanation: Painting the iron white means he is painting.
```

## 5. Resultados

Contagens nos 45 pares. Palavras em mediana. "Cita premissa ou hipotese" e "reafirma a relacao" sao contagens por
lista de expressoes. A copia e a fracao de palavras de conteudo da justificativa que ja estao no par.

| Medida | Humano | A | B | D | E | E2 | E3 | E4 | 35B (E) |
|---|---|---|---|---|---|---|---|---|---|
| Palavras (mediana / maxima) | 11 / 24 | 45 / 70 | 44 / 64 | 16 / 26 | 24 / 34 | 24 / 35 | 20 / 31 | 20 / 28 | 23 / 31 |
| Uma frase so | 44 | 6 | 2 | 45 | 45 | 44 | 45 | 45 | 45 |
| Cita premissa ou hipotese | 0 | 42 | 44 | 37 | 13 | 9 | 13 | 0 | 10 |
| Reafirma a relacao | 3 | 33 | 29 | 28 | 17 | 13 | 17 | 7 | 13 |
| Nomeia o rotulo | 0 | 7 | 11 | 14 | 6 | 4 | 8 | 0 | 8 |
| Copia do par | 0,86 | 0,31 | 0,29 | 0,67 | 0,36 | 0,40 | 0,44 | 0,33 | 0,38 |
| Segundos por par | - | 0,9 | 0,9 | 0,4 | 0,6 | 0,7 | 0,6 | 0,6 | 2,4 |

**Um par em todas as versoes (neutro).** Premissa: "A baby in an indoor pool is using an inflatable tube on it's on".
Hipotese: "The baby is swimming".

| Fonte | Justificativa |
|---|---|
| Humano | Just because the baby is in a pool does not mean it is swimming. |
| A | Using an inflatable tube in a pool does not necessarily mean the person is actively swimming, as they could simply be floating or playing while stationary. Therefore, the premise does not guarantee that the baby is swimming. |
| B | Using an inflatable tube in a pool does not necessarily mean the baby is actively swimming, as they could simply be floating or playing while supported by the tube. Therefore, we cannot definitively conclude that the hypothesis is true based solely on the premise. |
| D | The premise states the baby is using a tube, which does not confirm or deny if they are actively swimming. |
| E | Babies can float or play on inflatable tubes in pools without necessarily performing the active strokes required to be considered swimming. |
| E2 | Using an inflatable tube floats the baby on the water's surface rather than requiring the physical strokes needed to swim. |
| E3 | Using an inflatable tube floats the baby rather than swimming, as the tube provides buoyancy instead of the baby propelling themselves through water. |
| E4 | Tubes allow babies to float without swimming strokes, so floating on a tube does not prove the baby is actively swimming. |
| 35B (E) | The baby is using a tube, which suggests floating or being assisted rather than actively swimming on their own. |

Em A e B a segunda frase so repete a relacao. A D diz apenas que a premissa nao confirma. A partir da E aparece o
conhecimento que liga as duas frases: com boia se flutua sem nadar.

## 6. O que descobri

- **Tirar as definicoes dos rotulos nao mudou a forma (A -> B).** A frase final que so repete a relacao continuou,
  com outras palavras. Ela vinha do pedido "explique por que o rotulo esta correto", nao das definicoes;
- **Mudar o pedido mudou a forma (B -> D).** O texto caiu de 44 para 16 palavras e a frase vazia sumiu, mas a
  justificativa perdeu o conhecimento que liga premissa e hipotese;
- **Pedir essa ligacao e dar exemplos trouxe o conhecimento de volta (D -> E),** com cerca de 24 palavras;
- **Eco:** quando a hipotese e um pedaco da premissa, a justificativa so repete o par. Nenhuma versao resolveu (E2 e
  E3), porque nesses pares nao ha ligacao a explicar. Isso vale para cerca de 8,5% do conjunto de validacao do
  e-SNLI (implicacoes em que a hipotese nao traz nenhuma palavra nova);
- **Proibir palavras so troca por sinonimos (E4).** "Premise" virou "the description" e "contradicts" virou
  "incompatible", e apareceram erros de fato, como "a single-wheeled skateboard";
- **Rotulo errado:** no par em que o rotulo do e-SNLI esta errado, a versao E justificou o rotulo assim mesmo. Por
  isso vou marcar, e nao apagar, os pares em que o modelo discorda do rotulo;
- **O modelo maior (35B)** teve a mesma forma e raciocinou melhor nos dois casos dificeis da amostra, mas e 3,7
  vezes mais lento. Ficou como reserva.

## 7. Limites

- Sao 45 pares e uma semente. Diferencas de 2 a 4 casos ficam dentro do sorteio;
- As contagens sao por lista de expressoes e nao pegam sinonimos;
- A leitura de qualidade foi feita par a par, sem avaliacao cega.

## 8. Uso de LLM

O codigo de geracao e de medida, as rodadas e a primeira leitura dos resultados foram feitos com apoio de LLM
(Claude). A escolha das versoes, a regra por rotulo e a versao final dos 12 exemplos sao minhas.
