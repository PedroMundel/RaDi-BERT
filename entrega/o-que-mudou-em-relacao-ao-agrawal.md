# O que Mudou em Relacao ao Agrawal

## 1. O ponto de partida

No Agrawal, Ahemad & Sembium (2025), um BERT classifica o par de frases. Durante o treino, um decoder (a metade
decoder do T5 base) fica pendurado no BERT e tem de escrever a justificativa que um LLM escreveu para aquele par,
lendo apenas os vetores do BERT. A aposta é que, para o decoder conseguir escrever, o BERT precisa guardar o
raciocínio nos vetores, e isso ajudaria a classificar. No fim do treino o decoder é descartado e só o BERT é usado.

A perda do treino é a soma de duas partes: perda de classificação + 0,1 x perda de escrita.

## 2. As três formas de usar a justificativa

Repeti o treino do paper e depois testei duas formas mais simples de fazer a justificativa chegar ao encoder. A
segunda coluna é uma ideia minha; a terceira entrou como referência para a segunda.

| | Decoder (Agrawal, 2025) | Marcas de atenção | Cabeça por token |
|---|---|---|---|
| O que se aproveita da justificativa | o texto inteiro | só quais palavras do par ela usa | só quais palavras do par ela usa |
| O que o modelo é cobrado a fazer | escrever a justificativa | fazer o [CLS] prestar atenção nessas palavras | dizer, palavra por palavra, se ela é marcada ou não |
| Peça a mais no treino | um decoder inteiro, do tamanho do próprio BERT | nenhuma | uma camada linear |
| Perda | classificação + 0,1 x escrita, em três fases | classificação + 1 x atenção, desde o primeiro passo | classificação + 1 x marcação, desde o primeiro passo |
| Na inferência | o decoder é descartado | nada a descartar | a camada pode ficar, para dar o destaque |

O [CLS] é a posição especial no começo da entrada. É o vetor dela que a cabeça de classificação lê.

## 3. Um par, nas três formas

Par do RTE, rótulo "implica":

- Premissa: Coal company stocks got a lift Monday morning after an article in Barron's said the industry was
  benefiting from soaring natural gas prices and the advent of new power plants that emit less pollution.
- Hipótese: Coal stocks rise.
- Justificativa gerada pelo Qwen: "Got a lift" means increased, so coal stocks rose after the Barron's article
  reported industry benefits from gas prices and new plants.

O que cada forma faz com esse par:

- **Decoder:** tem de escrever a frase da justificativa inteira, palavra por palavra.
- **Marcas de atenção:** da justificativa sai só a lista de palavras do par que ela repete (coal, stocks, got, lift,
  article, Barron, industry, gas, prices, new, plants). A perda cobra que a atenção do [CLS], na última camada, caia
  nessas palavras.
- **Cabeça por token:** a mesma lista de palavras, mas cada palavra do par recebe uma resposta "marcada" ou "não
  marcada".

Palavras gramaticais (the, of, after) nunca são marcadas.

## 4. O controle

Para saber se um efeito vem do conteúdo da justificativa, e não só de existir uma perda a mais, rodei sempre um
terceiro treino: o mesmo das marcas, com o mesmo número de palavras marcadas em cada par, mas sorteadas. Se a marca
real ganha da sorteada, o efeito vem de quais palavras a justificativa aponta.

## 5. O tamanho do encoder

Também troquei o encoder por versões menores do BERT, para ver se um modelo mais fraco aproveita mais a justificativa.

| Encoder | Camadas | Tamanho do vetor | Parâmetros |
|---|---|---|---|
| BERT base | 12 | 768 | cerca de 110 milhões |
| BERT small | 4 | 512 | cerca de 29 milhões |
| BERT tiny | 2 | 128 | cerca de 4 milhões |

Com o decoder, os modelos menores precisam de uma camada linear no meio, que leva os vetores para o tamanho que o
decoder do T5 espera (768).

## 6. O que cada forma deu

| Forma | A nota de classificação melhora? | O modelo aprende a apontar as palavras da justificativa? |
|---|---|---|
| Decoder | não; no BERT base piora | não se aplica |
| Marcas de atenção | não; empata com o treino normal | sim |
| Cabeça por token | não; empata com o treino normal | sim, um pouco melhor que as marcas |

Os números e os testes estão nos documentos Replicacao do Agrawal no RTE e Marcas de Atencao e Destaque.

O código dos três treinos e as rodadas foram feitos com LLM (Claude). As ideias das marcas de atenção e de trocar o
encoder por um menor são minhas.
