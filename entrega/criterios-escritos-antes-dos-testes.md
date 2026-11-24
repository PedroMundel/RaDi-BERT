# Criterios Escritos Antes dos Testes

## 1. Por que passei a escrever o critério antes

No BERT small, a marca de atenção ganhou do treino normal nas 5 primeiras sementes: +0,017 de ROC-AUC, 5 de 5.
Rodei mais 10 sementes para confirmar e o ganho sumiu: +0,002, 6 de 10.

Também vi que o mesmo treino, com a mesma semente e os mesmos dados, rodado duas vezes na GPU, dá notas que diferem
em até 0,026. Um ganho de 0,017 em 5 sementes é menor que essa variação.

A partir daí, cada teste teve o critério escrito antes de rodar: o que conta como ganho, o que conta como empate e o
que eu faço em cada caso. Os três testes abaixo seguiram essa regra. Os critérios foram redigidos com LLM (Claude) e
aceitos por mim antes de cada rodada.

## 2. Teste fora da distribuição

**Pergunta:** um modelo treinado no RTE com a marca real acerta mais em pares de outro conjunto do que o mesmo modelo
treinado sem marcas?

**Combinado antes:**

| Resultado | Conclusão |
|---|---|
| Intervalo de 95% da diferença inteiro acima de zero, e marca real também acima da sorteada | ganho; confirmo uma vez com 10 sementes novas |
| Intervalo cruza o zero, ou fica abaixo | hipótese encerrada; não rodo variação nova das marcas para ganhar nota |
| Treino normal abaixo de 0,55 no conjunto de fora | o teste não informa (modelo no piso) |

**O teste:** BERT small treinado no RTE, 15 sementes, testado nos 9.842 pares do dev do e-SNLI.

**O que deu:** treino normal 0,759; marca real 0,754; diferença de -0,004, com intervalo de -0,011 a +0,002.

**Conclusão pelo critério:** o intervalo cruza o zero. A hipótese de que as marcas melhoram a nota foi encerrada.

## 3. Teste do destaque

**Pergunta:** as palavras em que o modelo mais presta atenção são as que a justificativa do LLM usa, em pares que ele
nunca viu, e melhor do que uma regra simples sem treino?

**Combinado antes:**

| Resultado | Conclusão |
|---|---|
| Precisão média da marca real supera a melhor regra em 0,05 ou mais, nas 5 sementes, e supera o treino normal | o destaque aprendido vale algo |
| Fica a menos de 0,05 da melhor regra, ou abaixo | trivial; uma regra sem treino faz o mesmo |

**O teste:** 1.000 pares de treino, medida nos 1.469 pares do RTE que o modelo nunca viu. Quatro regras sem treino
como referência; a melhor é "palavra de conteúdo que aparece nas duas frases".

**O que deu:** marca real 0,724; melhor regra 0,555; treino normal 0,361.

**Conclusão pelo critério:** supera a melhor regra em 0,17, nas 5 sementes. O destaque aprendido vale algo.

## 4. Cabeça por token como referência

**Pergunta:** o destaque tirado da atenção chega perto do que um modelo treinado direto para marcar palavras
consegue?

**Combinado antes:**

| Resultado | Conclusão |
|---|---|
| A cabeça supera a atenção em 0,05 de precisão média ou mais, nas 5 sementes | a cabeça dedicada é o mecanismo melhor para o destaque |
| Diferença menor que 0,05, ou atenção acima | a atenção entrega um destaque tão bom quanto o de uma cabeça dedicada |

**O teste:** 2.000 pares de treino, 470 de teste, 5 sementes, todos os treinos na mesma rodada.

**O que deu:** cabeça por token 0,748; marca de atenção 0,731; diferença de +0,017.

**Conclusão pelo critério:** a diferença é menor que 0,05. A atenção entrega um destaque quase tão bom quanto o da
cabeça dedicada.

## 5. O que os critérios não cobrem

- O gabarito do destaque são as palavras que o LLM usou, e não as que uma pessoa marcaria.
- Um conjunto de fora (e-SNLI), que se mostrou mais fácil que o próprio RTE.
- Os valores 0,05 e 0,55 dos critérios foram escolhidos antes dos testes, sem base em medida anterior.
