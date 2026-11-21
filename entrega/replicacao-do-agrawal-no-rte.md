# Replicacao do Agrawal no RTE

Tentei repetir, no conjunto RTE do GLUE, o método de Agrawal, Ahemad & Sembium (2025). O ganho que o paper reporta no RTE não se repetiu em nenhuma das condições que rodei. Este documento diz o que o paper descreve, o que ele deixa em aberto, o que eu decidi em cada ponto, os números de cada condição e o que ficou sem fazer.

A métrica é ROC-AUC (0,5 = acaso). O teste do GLUE não traz rótulo, então o conjunto de validação do RTE (277 pares) faz o papel de teste em todo o documento.

## 1. O que o paper faz

Agrawal, Ahemad & Sembium (2025) treinam um BERT base (110M de parâmetros) para classificar e, ao mesmo tempo, penduram nele a metade decoder de um T5 base como cabeça auxiliar. O decoder lê os vetores do BERT e aprende a escrever a justificativa do rótulo. A justificativa é escrita antes por um LLM professor, que recebe o par e o rótulo certo.

A perda é a soma da perda de classificação com 0,1 vez a perda auxiliar (a do decoder). O gradiente da perda auxiliar atravessa o decoder e entra no BERT. Na entrega o decoder é descartado e só o BERT com a cabeça de classificação é avaliado.

O paper descreve um aquecimento em duas fases. Primeiro o BERT fica congelado e só o decoder treina, em 50% dos dados. Depois o BERT é liberado com aquecimento linear nos primeiros 30% do treino, e nesse trecho só a perda auxiliar vale. Em seguida entra a perda completa.

No RTE o paper reporta ROC-AUC de 0,4754 para o baseline e de 0,5873 para o método. O baseline do paper é um BERT ajustado para relevância de busca (MS-MARCO).

## 2. O que o paper não diz e o que eu decidi

| O que falta no paper | O que foi feito | De quem é a decisão |
|---|---|---|
| Não há código publicado | O treino foi escrito a partir do texto do paper | decidi |
| O checkpoint do baseline (BERT com MS-MARCO) não tem nome | Rodei primeiro o bert-base-uncased comum e depois o nboost/pt-bert-base-uncased-msmarco | decidi |
| O professor aparece como Mixtral 8x7B na seção 4 e como LLaMA2/Mistral-7B no apêndice B | Usei o Qwen3.6-35B-A3B, um modelo aberto da mesma classe. É um desvio declarado | decidi |
| Não há prompt para o GLUE, e as justificativas do paper não foram publicadas | Usei um prompt meu: o modelo recebe o par e o rótulo certo e responde "por quê", com 2 rótulos e 20 exemplos de RTE | decidi |
| A tabela de hiperparâmetros pede 500 passos de aquecimento da taxa, e o treino no RTE tem 624 passos. O paper não diz se usou essa tabela no GLUE | Rodei as duas formas: a cópia (500 passos) e a proporcional (10% dos passos, 62) | decidi |
| "50% dos dados", "aquecimento linear do encoder" e "primeiros 30%" admitem mais de uma leitura | Leitura literal, declarada como interpretação: uma passada por metade dos pares só com o decoder; depois 30% dos passos do treino só com a perda auxiliar e a taxa do BERT subindo de 0 a 5e-5; depois a perda completa | decidi |
| Como o aquecimento da tabela convive com o aquecimento do encoder | Cada parte do modelo tem a própria rampa: decoder e cabeça seguem a tabela, o BERT sobe durante a segunda fase. Depois do pico a taxa cai em linha reta até zero | aceitei a recomendação do LLM |
| Taxa do decoder na primeira fase | Constante, 5e-5 | aceitei a recomendação do LLM |
| O paper testa passar ou não o vetor do [CLS] ao decoder, sem vantagem clara de nenhuma forma | O decoder recebe o [CLS] | aceitei a recomendação do LLM |
| Dropout da cabeça de classificação | 0,1 | aceitei a recomendação do LLM |
| Número de sementes | 5 por condição, as mesmas nos dois braços, com diferença pareada por semente | decidi |
| Métrica no GLUE | ROC-AUC, precisão e revocação a 0,7 (as do paper), mais acurácia e F1 | decidi |
| Quais pares o baseline vê | Os mesmos 2.470 pares do braço com decoder, para os braços diferirem só no decoder | aceitei a recomendação do LLM |

## 3. As justificativas do RTE

O RTE não traz justificativa. Gerei as justificativas dos pares de treino com o Qwen3.6-35B-A3B. Dos 2.490 pares de treino, 20 foram usados como exemplos dentro do prompt e saíram do treino. Sobraram 2.470 justificativas: 1.239 de entailment e 1.231 de not_entailment. Nenhuma saiu cortada, vazia ou repetida. A mediana é de 20 palavras, e a mais longa tem 34.

A leitura de qualidade foi feita com LLM (Claude). Eu não li o lote. É a leitura de um avaliador só, que sabia o rótulo. Os 20 exemplos do prompt também foram rascunhados com LLM (Claude) e aprovados por mim; eles não são alvo de treino.

O que a leitura achou em 30 pares sorteados (15 por rótulo):

| Resultado | Pares |
|---|---|
| Defendem o rótulo certo | 30 de 30 |
| Usam o fato certo | 27 de 30 |
| Defendem o rótulo com um fato trocado ou inventado | 2 de 30 (6,7%; intervalo de 95%: ~2% a ~21%) |
| Defendem o rótulo com uma imprecisão | 1 de 30 |

Fora da amostra, a leitura estimou que cerca de 1% do lote (~20 pares) argumenta pelo rótulo oposto ao do gabarito. A estimativa vem de 4 casos em 15 lidos, dentro dos 77 pares de entailment que têm negação ou ressalva.

Antes do treino, uma limpeza tira a abertura "The text states" (e os verbos says, notes, reports) do começo da justificativa. A primeira versão dessa limpeza quebrava pelo menos 96 frases, deixando um verbo sem sujeito. Aceitei a recomendação do LLM de estreitar a regra. Com a regra nova os cortes caíram de 450 para 347, e 536 justificativas (22%) continuam abrindo com "The text". Não há contagem de quantos cortes ainda quebram a frase.

## 4. O treino

O treino segue a tabela de hiperparâmetros do paper:

| Item | Valor |
|---|---|
| Lote | 32 |
| Taxa de aprendizado | 5e-5 |
| Épocas | 8 |
| Passos de aquecimento da taxa | 500 |
| Weight decay | 0,001 no decoder, 0 no encoder |
| Corte da norma do gradiente | 1,0 |

Com 2.470 pares e lote de 32 são 78 passos por época e 624 passos no total. As três fases ficaram assim:

| Fase | O que treina | Perda | Passos |
|---|---|---|---|
| A | só o decoder, com o BERT congelado, em metade dos pares | só a auxiliar | 39, fora dos 624 |
| B | BERT e decoder, com a taxa do BERT subindo de 0 a 5e-5 | só a auxiliar | 1 a 187 (30% de 624) |
| C | tudo | classificação + 0,1 x auxiliar | 188 a 624 |

O baseline é o mesmo encoder com a cabeça de classificação, só com a perda de classificação, nos mesmos pares e com os mesmos hiperparâmetros.

A classe positiva é entailment. O conjunto de teste é lido uma vez, no fim do treino: não há parada antecipada nem escolha de época por ele. Por causa da memória da placa (8 GB), cada lote de 32 foi processado em partes de 16 ou de 8 pares.

## 5. Resultados

Em todas as tabelas, cada célula é a média de 5 sementes, com o desvio entre sementes entre parênteses. A diferença é pareada por semente (com decoder menos sem decoder), com intervalo de 95%.

### 5.1 BERT base comum

O decoder não ajudou. Com o aquecimento de 500 passos houve empate. Com o proporcional o braço com decoder ficou abaixo nas 5 sementes, mas o intervalo cruza o zero.

| | Aquecimento de 500 passos | Aquecimento proporcional (62 passos) |
|---|---|---|
| BERT sozinho | 0,711 (desvio 0,021) | 0,736 (desvio 0,020) |
| BERT + decoder | 0,718 (desvio 0,019) | 0,707 (desvio 0,030) |
| Diferença | +0,007 (intervalo de 95%: -0,031 a +0,045) | -0,028 (intervalo de 95%: -0,071 a +0,015) |
| Decoder vence em | 2/5 | 0/5 |

O BERT sozinho com aquecimento proporcional (0,736) foi o melhor braço. Ele fica 0,26 acima do baseline do paper (0,4754) e 0,15 acima do método do paper (0,5873). Copiar os 500 passos de aquecimento custou 0,025 ao BERT sozinho. Com 277 pares de teste, 0,01 de ROC-AUC fica dentro do ruído entre sementes.

### 5.2 BERT MS-MARCO, a condição do paper

O número do paper não foi reproduzido com o checkpoint que usei (nboost/pt-bert-base-uncased-msmarco). O baseline não ficou abaixo do acaso, e o decoder piorou o resultado nas 5 sementes, com intervalo que não cruza o zero.

| | ROC-AUC | Acurácia |
|---|---|---|
| Paper: BERT (MS-MARCO) | 0,4754 | |
| Paper: com o método | 0,5873 | |
| Aqui: BERT MS-MARCO ajustado no RTE | 0,767 (desvio 0,013) | 0,721 |
| Aqui: BERT MS-MARCO + decoder | 0,718 (desvio 0,013) | 0,665 |
| Diferença | -0,049 (intervalo de 95%: -0,078 a -0,021) | -0,056 (intervalo de 95%: -0,082 a -0,031) |
| Decoder perde em | 5/5 | |
| Aqui: o mesmo checkpoint sem nenhum treino no RTE | 0,620 (hipótese como consulta) e 0,575 (premissa como consulta) | |

O baseline ficou 0,29 acima do 0,4754 do paper e 0,18 acima do método do paper. Sem nenhum ajuste no RTE, o checkpoint dá de 0,58 a 0,62. Não achei, com este checkpoint, uma condição que dê 0,4754. Esta condição rodou só com o aquecimento de 500 passos.

O pré-treino em MS-MARCO ajudou o baseline (0,767 contra 0,711 do BERT comum no mesmo aquecimento). Com o decoder essa vantagem sumiu: 0,718, o mesmo valor do BERT comum com decoder.

### 5.3 T5 v1.1 como encoder

Com o encoder do T5 v1.1 base no lugar do BERT, o braço com decoder ficou perto do acaso. A causa medida é desequilíbrio de escala entre as duas perdas, então este resultado não serve de evidência contra o método.

| | ROC-AUC | Acurácia |
|---|---|---|
| Encoder do T5 + cabeça | 0,636 (desvio 0,032) | 0,588 |
| Encoder do T5 + decoder do mesmo T5 | 0,522 (desvio 0,026) | 0,505 |
| Diferença | -0,115 (intervalo de 95%: -0,140 a -0,089) | -0,083 |
| Decoder perde em | 5/5 | |

No braço com decoder, a perda de classificação ficou em 0,695 (o valor do acaso) do passo 1 ao 600, nas 5 sementes. Pelo T5, o gradiente da perda de classificação é cerca de 10 vezes menor que pelo BERT, e mesmo com peso 0,1 a perda auxiliar domina o passo. A taxa de 5e-5 é taxa de BERT. É uma comparação de receita, não de arquitetura.

### 5.4 e-SNLI com 4 mil pares

O resultado se repetiu em outro conjunto: o decoder não acrescentou nada, e o intervalo cruza o zero.

Treinei o BERT base em 4.000 pares do e-SNLI (3 classes), com justificativas do mesmo Qwen, e avaliei na validação do e-SNLI (9.842 pares). Mesma receita, com 1.000 passos: fase A com 63 passos, fase B nos passos 1 a 300, fase C nos passos 301 a 1.000, aquecimento proporcional (100 passos).

| | ROC-AUC (um contra os outros) | Acurácia |
|---|---|---|
| BERT sozinho | 0,916 (desvio 0,005) | 0,797 (desvio 0,009) |
| BERT + decoder | 0,909 (desvio 0,003) | 0,787 (desvio 0,003) |
| Diferença | -0,007 (intervalo de 95%: -0,015 a +0,002) | -0,009 (intervalo de 95%: -0,023 a +0,005) |
| Decoder vence em | 1/5 | |

### 5.5 BERT small e BERT tiny

Com encoders menores a queda some, mas ganho não há. Troquei só o encoder: small (4 camadas, 512 dimensões, ~29M de parâmetros) e tiny (2 camadas, 128 dimensões, ~4M). Uma camada linear leva os vetores do encoder para as 768 dimensões que o decoder lê. Aquecimento proporcional, teste no RTE.

| Encoder | BERT sozinho | Com decoder | Diferença | Decoder vence em |
|---|---|---|---|---|
| small | 0,682 | 0,678 | -0,004 (intervalo de 95%: -0,020 a +0,012) | 1/5 |
| tiny | 0,622 | 0,612 | -0,010 (intervalo de 95%: -0,029 a +0,009) | 1/5 |

A camada linear a mais não explica o resultado. A perda auxiliar da última época foi 3,3 no small e 3,7 no tiny, contra 3,45 no BERT base: o decoder leu o encoder pequeno tão bem quanto lia o grande.

## 6. E erro meu?

Fiz três checagens no BERT base. Nenhuma achou erro no código.

| Checagem | O que foi medido | O que mostrou |
|---|---|---|
| Equivalência | Com o peso da perda auxiliar em 0, sem a fase B e com uma rampa só, o braço com decoder tem de terminar igual ao BERT sozinho | Termina com os mesmos pesos (diferença abaixo de 1e-7). Com o peso 0,1 os pesos saem diferentes, então o teste compara de fato. Carregar o decoder não tem efeito colateral sobre o classificador |
| Corte de gradiente | O corte da norma em 1,0 é feito sobre o modelo inteiro. Medi se o gradiente do decoder encolhe o passo do classificador | Não encolhe. A escala aplicada ao classificador é a mesma que seria sem o decoder: razão mediana 0,9998 na fase C (mínimo 0,993) e 0,977 na fase B (mínimo 0,953). Um treino por braço, uma semente |
| Controle de calendário | BERT sozinho, sem decoder, com o calendário do braço com decoder: perda de classificação desligada até o passo 187 e pico da taxa no passo 187 | 0,746 (desvio 0,021), contra 0,736 do BERT sozinho: +0,010 (intervalo de 95%: -0,020 a +0,041), vence em 3/5 |

A hipótese que caiu: o braço com decoder perderia por receber menos treino de classificação, já que nos passos 1 a 187 só a perda auxiliar vale. O controle de calendário mostra que perder esses 187 passos não custa nada ao BERT. O braço com decoder (0,707) fica 0,039 abaixo desse controle (intervalo de 95%: -0,097 a +0,020; perde em 5/5). A queda vem do que a perda auxiliar faz com o BERT, não do calendário.

A explicação que fica é de escala. A fase A existe para o decoder aprender a ler o BERT antes de o gradiente dele entrar no BERT. No RTE, "50% dos dados" são 39 passos. No primeiro passo da fase B a perda auxiliar ainda está em 7,0 por token; lendo o encoder do próprio T5 ela começa em 4,2. A perda auxiliar para em cerca de 3,0 perto do passo 300. O decoder aprende o molde da frase, e as palavras copiadas do par ficam em 4,5 por token (2,5 quando ele lê o encoder do próprio T5). De 60% a 65% do empurrão da perda auxiliar no BERT vem dessas palavras copiadas, e o cosseno entre o gradiente da perda auxiliar e o da classificação fica entre -0,05 e +0,02 o treino todo.

Essa explicação não foi testada diretamente. O teste que a derruba é uma fase A longa, com o BERT congelado até a perda das palavras copiadas parar de cair, e ele não foi rodado.

Uma pergunta continua sem resposta possível: se a minha leitura dos pontos vagos do paper é igual à implementação dos autores.

## 7. O que não foi feito

- Um checkpoint MS-MARCO só, e o paper não nomeia o dele. O Capreolus/bert-base-msmarco não foi rodado. Outro checkpoint pode se comportar de outro jeito.
- A condição MS-MARCO rodou só com o aquecimento de 500 passos.
- O paper não descreve o ajuste do baseline no GLUE (épocas, se a cabeça foi trocada, qual classe é a positiva). Não tenho como conferir se o meu ajuste é igual.
- Do que é replicável no paper (GLUE, QADSM e ESCI), rodei só o RTE. O e-SNLI não está no paper. As duas tarefas são de inferência textual.
- O professor é outro (Qwen no lugar do Mixtral) e o prompt é meu. O paper não reporta a qualidade das justificativas dele, então não há régua para comparar as minhas.
- As justificativas foram lidas só por LLM, em 30 pares, sem leitura cega. No e-SNLI, 7,8% das justificativas estão marcadas como eco e não foram filtradas.
- 5 sementes por condição e 277 pares de teste. O desvio entre sementes fica entre 0,02 e 0,03 no RTE, então um ganho de meio ponto, como os que o paper reporta nas tarefas com baseline forte, não seria visto.
- Uma receita só. O peso da perda auxiliar, a taxa e o número de pares não foram variados. No T5 v1.1 isso impede a comparação justa.
- No BERT base com decoder e aquecimento proporcional, as sementes 2 a 5 rodaram com o lote processado em partes de 8 pares, e a semente 1 em partes de 16.
- A fase A longa, que testaria a explicação da seção 6, não foi rodada.
- No e-SNLI a avaliação foi na validação; o teste não foi usado.

O código do treino, as rodadas e a leitura dos resultados foram feitos com LLM (Claude). As decisões da seção 2 são minhas ou foram aceitas por mim.
