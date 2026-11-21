# Marcas de Atencao e Destaque

## 1. A ideia

No treino do Agrawal, Ahemad & Sembium (2025), um decoder escreve a justificativa lendo os vetores do encoder. Nas
minhas rodadas esse decoder não melhorou a nota. Pensei em tirar o decoder e entregar ao encoder, de forma direta,
aquilo que a justificativa aponta: quais palavras do par importam.

Chamei isso de marcas de atenção:

- De cada justificativa gerada pelo Qwen, pego só as palavras que ela repete do par (premissa ou hipótese). Palavras
  gramaticais ficam de fora. Essas são as palavras marcadas. No RTE, elas são cerca de 16% dos tokens de entrada, com
  mediana de 10 por par;
- No treino, além da perda de classificação, entra uma perda que cobra que a atenção do [CLS], na última camada, caia
  nas palavras marcadas. Peso 1 para cada perda, desde o primeiro passo;
- Não existe peça a mais no modelo. Na inferência nada é descartado.

Em todas as rodadas há três treinos, iguais em tudo menos na perda das marcas:

- **sem marcas:** só a classificação;
- **marca real:** as palavras que a justificativa repete;
- **marca sorteada:** o mesmo número de palavras por par, sorteadas. É o controle: se a marca real ganha da sorteada,
  o efeito vem de quais palavras a justificativa aponta, e não de existir uma perda a mais.

A nota é o ROC-AUC (0,5 é chute, 1,0 é perfeito). O dev do RTE (277 pares) faz o papel de teste. As diferenças são
pareadas por semente, com intervalo de 95%.

## 2. No BERT base: ganha da marca sorteada, empata com o treino normal

RTE inteiro (2.470 pares com justificativa), 5 sementes.

| Treino | ROC-AUC | Acurácia |
|---|---|---|
| Sem marcas | 0,739 | 0,681 |
| Marca real | 0,745 | 0,687 |
| Marca sorteada | 0,691 | 0,633 |

| Comparação | Diferença de ROC-AUC (intervalo de 95%) | Vence em |
|---|---|---|
| Marca real - marca sorteada | +0,055 (+0,031 a +0,078) | 5 de 5 |
| Marca real - sem marcas | +0,006 (-0,019 a +0,031) | 3 de 5 |
| Marca sorteada - sem marcas | -0,049 (-0,077 a -0,020) | 0 de 5 |

O conteúdo da justificativa importa: marcar as palavras que ela aponta é melhor do que marcar palavras ao acaso. Mas,
contra o treino normal, não há ganho.

## 3. Com poucos pares de treino

Testei se a marca ajuda quando há pouco dado: 500 e 1.000 pares de treino. Para ter um teste maior que o dev, usei
também os 1.470 pares de treino que nenhum dos dois tamanhos usa. Essa ideia de teste é minha.

| Comparação nos 1.470 pares | 500 pares de treino | 1.000 pares de treino |
|---|---|---|
| Marca real - sem marcas, ROC-AUC | +0,000 (-0,006 a +0,007) | -0,004 (-0,019 a +0,010) |
| Marca real - marca sorteada, ROC-AUC | +0,023 (+0,012 a +0,035), 5 de 5 | +0,007 (-0,001 a +0,014), 4 de 5 |

Com pouco dado a marca real também empata com o treino normal.

## 4. Em um encoder menor

Troquei o BERT base por modelos menores, para ver se um encoder mais fraco aproveita mais a justificativa: BERT small
(4 camadas, cerca de 29 milhões de parâmetros) e BERT tiny (2 camadas, cerca de 4 milhões).

**O ganho das 5 primeiras sementes não se confirmou.** No small, a marca real ganhou do treino normal nas 5 primeiras
sementes. Rodei mais 10 para confirmar e o ganho sumiu.

| Sementes (BERT small, RTE inteiro) | Sem marcas | Marca real | Marca sorteada | Real - sem marcas | Real - sorteada |
|---|---|---|---|---|---|
| 1 a 5 | 0,674 | 0,691 | 0,641 | +0,017 (+0,008 a +0,025), 5 de 5 | +0,049 (+0,030 a +0,069), 5 de 5 |
| 6 a 15 | 0,677 | 0,680 | 0,632 | +0,002 (-0,009 a +0,014), 6 de 10 | +0,048 (+0,038 a +0,058), 10 de 10 |
| 1 a 15 | 0,676 | 0,683 | 0,635 | +0,007 (-0,001 a +0,015), 11 de 15 | +0,048 (+0,041 a +0,056), 15 de 15 |

Nessa rodada também vi que o mesmo treino, com a mesma semente e os mesmos dados, rodado duas vezes na GPU, dá notas
que diferem em até 0,026. Um ganho de 0,017 em 5 sementes é menor que isso.

Com 1.000 pares de treino no small, o dev repete o +0,017 (5 de 5), mas o teste maior, de 1.470 pares, dá -0,022
(intervalo de -0,031 a -0,012, 0 de 5). Os dois testes discordam no sinal, e o maior é o mais confiável.

O BERT tiny fica perto do que um modelo sem treino dá (0,621 sem marcas). Nele não dá para ler nada.

## 5. Fora da distribuição

Faltava testar se a marca ajuda em pares de outro conjunto. Treinei o small no RTE e testei no dev do e-SNLI (9.842
pares), juntando "neutro" e "contradição" como "não implica". O critério foi escrito antes de rodar (documento
Criterios Escritos Antes dos Testes). 15 sementes.

| Teste | Sem marcas | Marca real | Marca sorteada | Real - sem marcas | Real - sorteada |
|---|---|---|---|---|---|
| Fora (e-SNLI), ROC-AUC | 0,759 | 0,754 | 0,712 | -0,004 (-0,011 a +0,002), 7 de 15 | +0,042 (+0,036 a +0,049), 15 de 15 |
| Dentro (dev do RTE), ROC-AUC | 0,676 | 0,683 | 0,635 | +0,007 (-0,001 a +0,016), 11 de 15 | +0,049 (+0,041 a +0,057), 15 de 15 |

Fora da distribuição a marca real também não ganha do treino normal. Pelo critério combinado, encerrei a hipótese de
que as marcas melhoram a nota.

## 6. Por que não muda a nota: a atenção muda de lugar e a nota fica igual

Medi quanto da atenção do [CLS], na última camada, cai nas palavras marcadas, em 1.470 pares que o modelo nunca viu
(1.000 pares de treino, 5 sementes).

| Modelo | Parte da atenção do [CLS] nas palavras marcadas |
|---|---|
| Atenção espalhada por igual (referência) | 0,193 |
| Antes de qualquer treino | 0,314 |
| Treinado sem marcas | 0,285 |
| Treinado com marca sorteada | 0,261 |
| Treinado com marca real | 0,805 |

Uma explicação possível para o empate era que o treino normal já levasse a atenção para essas palavras, e que por
isso a marca não acrescentasse nada. Não é o que acontece: sem marcas, a atenção fica onde estava antes do treino. A marca real leva a atenção para
as palavras da justificativa, inclusive em pares novos, e mesmo assim a nota não muda.

Nas camadas anteriores os quatro modelos são quase iguais. Na terceira camada, a atenção nas palavras marcadas fica
entre 0,36 e 0,42, contra 0,19 da referência.

Correção de 18/11. Na versão entregue na Semana 9 esta seção se chamava "a atenção muda, a decisão não" e dizia que a
explicação provável era o [CLS] já ter recolhido a informação antes da última camada. Testei isso em 16/11 e a frase
estava errada. Tapei a atenção do [CLS] às palavras marcadas, uma camada por vez, sem treinar de novo, em 470 pares
nunca vistos (BERT small, 2.000 pares de treino, 5 sementes). No modelo sem marcas a decisão muda em 18,5% dos pares
quando tapo a camada 3 e em 8,9% quando tapo a camada 4, a última; com o mesmo número de palavras de conteúdo
sorteadas, cerca de 7% e 4%. Nas camadas 1 e 2 quase nada muda. No modelo treinado com a marca real na última
camada, tapar a camada 4 muda 33,1% das decisões e tapar a camada 3 muda 8,4%. Então a decisão depende da atenção do
[CLS] nas duas últimas camadas, e a marca muda o caminho da decisão sem mudar a nota. O teste não separa palavra da
justificativa de palavra que aparece nas duas frases.

## 7. O destaque

Se a nota não muda, o que o modelo ganhou foi outra coisa: ele aprendeu a apontar as palavras que o LLM usa para
justificar. Testei se isso vale algo, com o critério escrito antes.

A medida é a precisão média: ordeno as palavras do par pela atenção do [CLS] e vejo se as marcadas vêm no topo. 1,0
significa todas no topo; ao acaso dá 0,26. A comparação é com regras simples, sem treino nenhum.

Com 1.000 pares de treino, medido nos 1.469 pares nunca vistos que têm marca, 5 sementes:

| Quem dá a nota a cada palavra | Precisão média |
|---|---|
| BERT small treinado com marca real | 0,724 |
| Melhor regra sem treino: palavra de conteúdo que aparece nas duas frases | 0,555 |
| BERT small antes do treino | 0,446 |
| Regra: palavra de conteúdo da hipótese | 0,394 |
| Regra: toda palavra de conteúdo | 0,388 |
| BERT small treinado sem marcas | 0,361 |
| BERT small treinado com marca sorteada | 0,309 |
| Ao acaso | 0,260 |

A marca real supera a melhor regra em 0,17, nas 5 sementes. Um encoder de 29 milhões de parâmetros aprende, com
1.000 pares, a apontar em pares novos as palavras que um LLM muito maior usaria, e o destaque sai da atenção que o
modelo já calcula para classificar.

**Destaque e nota juntos.** Com 2.000 pares de treino, medido nos 470 que sobram, 5 sementes:

| Treino | Precisão média do destaque | ROC-AUC no dev | ROC-AUC nos 470 pares |
|---|---|---|---|
| Cabeça por token | 0,748 | 0,670 | 0,669 |
| Marca real (atenção) | 0,731 | 0,691 | 0,659 |
| Sem marcas | 0,377 | 0,681 | 0,659 |
| Marca sorteada | 0,320 | 0,637 | 0,626 |
| Melhor regra sem treino | 0,558 | não classifica | não classifica |

- O destaque se mantém e a classificação empata com o treino normal: marca real - sem marcas dá +0,010 no dev
  (intervalo de -0,006 a +0,027) e -0,000 nos 470 pares (-0,018 a +0,018);
- A cabeça por token é um modelo treinado direto para marcar palavras, com uma camada linear sobre cada token. Entrou
  como referência. Ela supera a atenção em 0,017 de precisão média, nas 5 sementes, abaixo do limite de 0,05 fixado
  antes da rodada. A atenção entrega um destaque quase tão bom quanto o de uma cabeça dedicada.

O documento Exemplos do Destaque mostra 20 pares com as palavras coloridas.

## 8. Limites

- O gabarito do destaque são as palavras que o LLM repetiu do par. Não medi se o destaque ajuda uma pessoa;
- Não medi se o destaque explica a decisão do modelo. A marca não mudou a nota, mas a decisão depende da atenção do
  [CLS] nas duas últimas camadas (seção 6);
- O peso da perda das marcas (1) e a camada (a última) não foram variados, porque o dev é o teste;
- Palavras gramaticais nunca são marcadas, mesmo quando decidem, como a negação;
- As marcas reais não têm palavras gramaticais e as sorteadas podem ter, o que aumenta um pouco a diferença entre as
  duas no destaque;
- Uma tarefa (RTE), um conjunto de justificativas (Qwen), pares curtos em inglês;
- O e-SNLI se mostrou mais fácil que o RTE para o modelo treinado no RTE (0,759 contra 0,676), então é um teste
  brando de robustez.

O código, as rodadas e a leitura dos resultados foram feitos com LLM (Claude). São minhas a ideia das marcas de
atenção, a de trocar o encoder por um menor e a de testar nos pares de treino não usados. Os critérios dos testes
das seções 5 e 7 foram redigidos com LLM e aceitos por mim antes de cada rodada.
