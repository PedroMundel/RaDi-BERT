# Trilha das Semanas 9 e 10

A replicação de Agrawal, Ahemad & Sembium (2025) e o que medi sobre ela que o artigo não mediu, de 09/11 a 19/11.

## 1. A pergunta

A justificativa escrita por um LLM ajuda um modelo encoder, que não gera texto, a classificar melhor? A receita de partida é a de Agrawal, Ahemad & Sembium (2025): um BERT base classifica o par de frases e, durante o treino, a metade decoder de um T5 base fica pendurada nele e tem de escrever a justificativa do rótulo lendo só os vetores do BERT. A perda é a de classificação mais 0,1 vez a perda do decoder, com um aquecimento em duas fases em que só o decoder treina. Na entrega o decoder é descartado. As justificativas foram geradas por um LLM aberto (Qwen3.6-35B-A3B) com um prompt meu.

O ganho que o artigo relata não se repetiu. Como o resultado positivo não aparecia, resolvi medir o que o artigo não mediu, usando a receita dele como bancada. Saí com cinco medidas:

- De onde vem o ganho aparente do decoder: do calendário de treino, e não da justificativa (seção 3);
- Se o conteúdo da justificativa conta: conta, a justificativa de outro par atrapalha mais que a certa (seção 3);
- O que acontece fora do domínio de treino e em calibração, predição seletiva e pior classe: o decoder custa nota, não aparece em outra medida (seção 4);
- Por que três outros caminhos da justificativa ao encoder não sobem a nota: a atenção muda de lugar sem mudar a nota, a informação já estava no encoder, e a justificativa entrega o rótulo (seção 5);
- O que funciona no mesmo cenário: o encoder aprende a apontar as palavras que o LLM usa, e a destilação comum entre BERTs, sem LLM e sem justificativa, dá o ganho de nota (seção 6).

A resposta à pergunta, com esta receita, este LLM e este prompt, é não. O que fica são essas medidas.

Onde há um intervalo entre parênteses, a diferença é pareada por semente e o intervalo é de 95%.

## 2. O ponto de partida: o número do artigo não se repetiu

O baseline do artigo não saiu em nenhuma condição que tentei, e o decoder ficou nulo ou negativo. O artigo relata no RTE ROC-AUC de 0,4754 para o baseline (um BERT base ajustado em MS-MARCO) e 0,5873 para o método. Ele não nomeia o checkpoint nem descreve como ajustou o baseline no GLUE, e deixa vagos "50% dos dados" e "primeiros 30%"; li esses pontos de um jeito, declarado como interpretação.

Com nboost/pt-bert-base-uncased-msmarco ajustado no RTE o baseline fez 0,767; sem nenhum treino no RTE, de 0,575 a 0,620; com o encoder congelado, 0,590; com uma época, 0,635 e 0,741. Com um segundo checkpoint, Capreolus/bert-base-msmarco, 0,743. A regra escrita antes pedia uma média entre 0,44 e 0,51.

Como ler: ROC-AUC no dev do RTE (277 pares; a última linha, no dev do e-SNLI), 5 sementes; a coluna do meio é o braço sem decoder e a última é o braço com decoder menos o braço sem decoder.

| Condição | ROC-AUC sem decoder | Com decoder menos sem decoder |
|---|---|---|
| BERT base, aquecimento proporcional | 0,736 | -0,028 (-0,071 a +0,015) |
| BERT base, aquecimento da Tabela 4 do artigo | 0,711 | +0,007 (-0,031 a +0,045) |
| BERT MS-MARCO (nboost) | 0,767 | -0,049 (-0,078 a -0,021), perde 5 de 5 |
| BERT MS-MARCO (Capreolus) | 0,743 | -0,022 (-0,040 a -0,004), perde 5 de 5 |
| BERT small | 0,682 | -0,004 (-0,020 a +0,012) |
| e-SNLI, 4.000 pares, BERT base | 0,916 | -0,007 (-0,015 a +0,002) |

O ganho de 0,112 que o artigo relata no RTE ficaria visível nessas grades: o maior limite superior é +0,045. Um ganho pequeno, como o +0,005 que o artigo mostra nas tarefas com baseline forte, não seria visto com 5 sementes, e nessas tarefas os intervalos da Tabela 2 do próprio artigo se sobrepõem.

Antes de seguir, conferi se era erro meu. Com o peso da perda do decoder em 0, o braço com decoder termina com os mesmos pesos do BERT sozinho; o corte da norma do gradiente não encolhe o passo do classificador; e o BERT sem decoder com o calendário do braço com decoder fez 0,746 no RTE, então perder os passos iniciais de classificação não custava nada ali. Nenhuma das três checagens achou erro. A partir daqui a pergunta deixou de ser "o decoder ganha?" e passou a ser "o que está acontecendo quando ele treina?".

## 3. De onde vem o ganho aparente e se o conteúdo conta

Nos 16.000 pares do e-SNLI com justificativa do Qwen a receita do artigo cabe inteira (o aquecimento de 500 passos da Tabela 4 é 12,5% do treino). Avaliei no dev do e-SNLI (9.842 pares, 3 classes), BERT base, 5 sementes.

O braço com decoder passa os passos 1 a 1.200 sem nenhum passo de classificação. Por isso rodei o BERT sem decoder com esse mesmo calendário. E, para saber se o conteúdo da justificativa conta, um braço em que o decoder tem de gerar a justificativa de outro par do mesmo rótulo (troca fixa, nenhum par fica com a sua). É o controle que Agrawal, Ahemad & Sembium (2025) não rodaram.

Como ler: diferença do primeiro braço menos o segundo, semente a semente, no dev do e-SNLI; ROC-AUC e acurácia em pontos percentuais; a última coluna diz em quantas das 5 sementes o primeiro braço ficou acima, no ROC-AUC e na acurácia.

| Comparação | ROC-AUC | Acurácia (pontos) | Sementes acima (ROC-AUC; acurácia) |
|---|---|---|---|
| Com decoder menos sem decoder, treino comum | +0,003 (-0,004 a +0,010) | -0,6 (-1,1 a 0,0) | 3 de 5; 1 de 5 |
| Sem decoder com o calendário menos sem decoder, treino comum | +0,007 (+0,006 a +0,008) | +0,4 (+0,3 a +0,5) | 5 de 5; 5 de 5 |
| Com decoder menos sem decoder com o calendário | -0,004 (-0,011 a +0,003) | -0,9 (-1,6 a -0,3) | 2 de 5; 0 de 5 |
| Justificativa de outro par menos calendário | -0,020 (-0,027 a -0,013) | -3,0 (-4,2 a -1,9) | 0 de 5; 0 de 5 |
| Justificativa do par menos justificativa de outro par | +0,016 (+0,014 a +0,019) | +2,1 (+1,4 a +2,9) | 5 de 5; 5 de 5 |

- O calendário sozinho, sem decoder e sem justificativa, ajuda: +0,007 de ROC-AUC nas 5 sementes. O critério escrito antes não previa esse caso. Não testei por que ele ajuda;
- Com o mesmo calendário dos dois lados, o decoder é nulo no ROC-AUC e perde 0,9 ponto de acurácia. O +0,003 do decoder era do calendário;
- O conteúdo importa: a justificativa errada custa 3,0 pontos contra o calendário e a certa 0,9. Como a troca é dentro do rótulo, o que protege o classificador é o texto casar com o par. O gradiente do decoder tem força para mover a nota em pontos inteiros;
- A justificativa certa não ajuda: continua abaixo do calendário. Este controle também não separa "a justificativa certa ensina o motivo" de "a tarefa errada é impossível de aprender a partir do par e atrapalha como ruído".

Com 16.000 pares o decoder aprende bem mais que com 4.000 (perda nas palavras copiadas do par 2,01 por token contra 3,63) e a classificação não ganha. Então "poucos pares" deixa de explicar o nulo; essa leitura segue uma regra escrita com LLM antes da rodada, que eu ainda não confirmei. Os dois braços ainda diferem no sorteio do dropout, no corte de gradiente e no estado do otimizador ao fim da fase só do decoder.

O decoder faz a classificação arrancar na frente (15,4 pontos depois de 25 passos), mas os braços empatam no passo 1.300 e, em tempo de relógio, a vantagem não existe: a fase só do decoder custa mais que o treino inteiro sem decoder.

## 4. O decoder fora do domínio e em outras medidas

Treinei de novo os três braços nos 16.000 pares, 5 sementes, e avaliei em conjuntos que o modelo não viu. No MNLI, o conjunto que decide por ter as mesmas 3 classes, o decoder fica 1,5 ponto abaixo do calendário. Também fechei antes um painel de três medidas além da acurácia, lidas dos mesmos classificadores.

Como ler: média das 5 sementes; MNLI é acurácia de 3 classes nos 19.647 pares das duas validações; ECE é o erro de calibração (menor é melhor); predição seletiva é o ROC-AUC da confiança para separar acerto de erro (maior é melhor); pior classe é o menor F1 das três (a neutra). A última coluna é decoder menos calendário e em quantas das 5 sementes ela é positiva.

| Medida (lado bom) | Calendário | Decoder | Decoder menos calendário |
|---|---|---|---|
| Acurácia no MNLI (maior) | 65,0% | 63,5% | -1,5 ponto (-2,3 a -0,7), 0 de 5 |
| Calibração, ECE no dev (menor) | 0,142 | 0,152 | +0,010 (+0,003 a +0,017), 5 de 5 |
| Predição seletiva no dev (maior) | 0,742 | 0,737 | -0,005 (-0,029 a +0,019), 2 de 5 |
| Pior classe, menor F1 no dev (maior) | 0,799 | 0,790 | -0,009 (-0,013 a -0,005), 0 de 5 |

- Nenhuma medida melhora com o decoder: três ficam do lado ruim com o intervalo fora do zero e a predição seletiva é nula. As três pioras andam junto com a perda de acurácia;
- A perda no MNLI (-1,5) é maior que a de dentro do domínio (-0,8 nesta rodada), nos mesmos modelos; essa diferença não tem teste;
- No RTE a diferença não se distingue do zero (-0,010 de ROC-AUC, -0,022 a +0,002). O HANS ficou no piso: os três braços respondem "entailment" em 98% a 99,6% dos pares de não-entailment, então não diz nada sobre atalho;
- O ganho do calendário não aparece fora do domínio (+0,1 ponto no MNLI).

O braço com a justificativa de outro par também foi avaliado fora, mas a conferência que fixei antes não passou para ele (0,63 ponto de diferença contra o limite de 0,6), e os números ficam só descritos: no MNLI ele faz 60,6%, 2,9 pontos abaixo do braço com a justificativa do par.

Por fim variei o peso da perda do decoder, fixo em 0,1 até então, em 0, 0,05 e 0,5, com 3 sementes cada; é exploratório. Nenhum valor passa: a acurácia no dev fica entre 82,8% e 83,2% nos quatro pesos, abaixo do calendário nas 3 sementes, com os intervalos cruzando o zero. Com peso 0 o decoder só mexe no encoder até o passo 1.200, e a perda é quase a mesma. O custo parece estar na fase em que só o decoder treina o encoder; isso é leitura de 3 sementes, sem teste próprio.

## 5. Três outros caminhos e o que cada um mostrou

**Marcas na atenção do [CLS].** Ideia minha: em vez do decoder, cobrar que a atenção do [CLS] na última camada caia nas palavras do par que a justificativa repete, com um controle de palavras sorteadas. No BERT base, no RTE, a marca real ganha da sorteada (+0,055 de ROC-AUC, +0,031 a +0,078, 5 de 5) e empata com o treino sem marcas (+0,006, -0,019 a +0,031).

No BERT small, as 5 primeiras sementes davam +0,017 (5 de 5) sobre o treino sem marcas; com mais 10 sementes o ganho caiu para +0,002, e o mesmo treino, rodado duas vezes na GPU, difere em até 0,026. Fora da distribuição (BERT small treinado no RTE, teste no dev do e-SNLI, 15 sementes, critério escrito antes) a marca real fica, contra o treino sem marcas, em -0,004 (-0,011 a +0,002), e encerrei a hipótese.

A atenção muda de lugar e a nota fica igual: sem marcas, 0,285 da atenção do [CLS] cai nas palavras marcadas; com a marca real, 0,805, em pares nunca vistos. Isso não quer dizer que a atenção não pese na decisão. Tapando a atenção do [CLS] às palavras marcadas, sem treinar de novo, a decisão do modelo sem marcas muda em 18,5% dos pares na camada 3 e em 8,9% na camada 4 (com palavras sorteadas, cerca de 7% e 4%). A marca muda o caminho da decisão sem mudar a nota. Cobrar a marca em outras camadas (11 combinações) também deu nulo, com a maior diferença +0,011.

**Grupos de palavras novas no [CLS].** As palavras que a justificativa traz e que não estão no par acertam 76,4% do rótulo numa regressão (as palavras do par, 46,6%). Agrupadas, deram 1 grupo de argumentar e 28 de assunto. Uma cabeça no [CLS] do BERT small prevendo esses grupos foi nula pelo critério escrito antes: nenhum braço passa de 0,64 ponto, o maior número é +0,29. A cabeça treinou, mas uma sonda linear lê os grupos no [CLS] do BERT pré-treinado (0,765) tão bem quanto no aluno com a cabeça (0,760): a informação já estava lá, porque é sobretudo o assunto do par.

**Professor que lê a justificativa.** Um BERT base que lê o par mais a justificativa acerta 96,7% dos pares do aluno, e lendo só a justificativa faz o mesmo (96,9%); com a justificativa de um par de outro rótulo, responde o rótulo da justificativa em 94,6% dos pares. A justificativa do Qwen entrega o rótulo.

Usado como professor na destilação da seção 6, imitar o interior dele atrapalha: -2,7 pontos (-3,3 a -2,1) no conjunto de escolha, 0 de 5. Não separei a causa.

## 6. O que funciona no mesmo cenário

**O destaque.** O BERT small treinado com a marca real aprende a apontar, em pares novos, as palavras que o LLM copia: precisão média de 0,724, contra 0,555 da melhor regra sem treino e 0,260 ao acaso, nas 5 sementes (critério escrito antes). Com 2.000 pares, 0,731, com a classificação empatada. Uma cabeça por token treinada direto nas marcas faz 0,748, só 0,017 acima (o limite fixado antes era 0,05). O gabarito são as palavras que o LLM repetiu; não medi se o destaque ajuda uma pessoa.

**Destilação entre BERTs.** Esta parte não usa LLM nem justificativa: é destilação de conhecimento padrão (Hinton et al., 2015). O professor é um BERT base treinado em 4.000 pares do e-SNLI que o aluno não vê; o aluno é um BERT small nos outros 4.000. Destilar só a atenção não mudou a nota (no máximo +0,1 ponto no dev). Imitar as respostas do professor ajuda.

A versão que mais ganhou é a "sequência": o aluno passa 20 épocas imitando os embeddings, a atenção e os estados internos do professor e depois treina classificação mais as respostas. A receita segue o TinyBERT (Jiao et al., 2020), obra que não li; a leitura foi feita por LLM. O mesmo vale para o MiniLM (Wang et al., 2020), de onde saiu outro pacote de perdas que não ganhou.

Como ler: acurácia do BERT small em pontos percentuais; o conjunto de escolha (4.000 pares que ninguém viu) decide e o dev do e-SNLI confirma; diferença contra a linha indicada, com o número de sementes.

| Jeito de treinar o small | Comparado com | Escolha | Dev | Sementes |
|---|---|---|---|---|
| Respostas do professor | sem destilação | +1,6 | +1,6 | 5 |
| Controle: rótulo suavizado, sem professor | sem destilação | -0,1 | 0,0 | 5 |
| Controle: respostas trocadas entre pares do mesmo rótulo | sem destilação | -1,7 | -1,8 | 5 |
| Sequência | respostas | +0,93 (+0,70 a +1,17), 15 de 15 | +0,45 (+0,25 a +0,65), 13 de 15 | 15 |
| Controle: sequência com professor que não aprendeu a tarefa | respostas | +0,06 (-0,23 a +0,36) | -0,05 (-0,25 a +0,16) | 15 |

O ganho vem do que um professor que aprendeu a tarefa diz sobre cada par: o alvo mole sem professor não ajuda, as respostas no par errado pioram, e imitar um BERT sem a tarefa não ganha. No conjunto de escolha, com 15 sementes, o small faz 74,0% com as respostas e 74,9% com a sequência; sem destilação fazia 72,3%, média de 5 sementes (o professor faz 78,0%). Juntar tudo num treino só, em vez de em sequência, não ajudou; temperatura e um professor com o dobro de pares não subiram o ganho. É um professor de uma semente, uma tarefa, 4.000 pares.

## 7. O que o decoder gera

O BERT com decoder dos 16.000 pares gerou justificativas para 200 pares do dev, lendo só o par. Nas 50 primeiras, lidas e classificadas por LLM, 22 defendem o rótulo previsto com o fato certo, 10 com fato trocado, 2 defendem outro rótulo e 16 não argumentam. Um BERT juiz não vê diferença entre essas e as de um T5 base treinado sozinho para gerar (o T5 sozinho fica 2,0 pontos acima, de -5,0 a +9,0).

## 8. O que isso ensina sobre método

- Toda comparação com uma etapa extra de treino precisa do controle de calendário. Sem ele, o calendário sozinho (+0,007 de ROC-AUC) passou por ganho do decoder;
- O mesmo treino na GPU varia entre rodadas (até 0,026 de ROC-AUC no RTE), e 5 sementes não separam ganhos de meio ponto. O +0,017 das marcas sumiu com 10 sementes novas;
- Escrevi antes de cada rodada o que cada resultado significaria. Foi esse critério que deixou o ganho do calendário marcado como caso não previsto e o braço trocado fora do domínio só descrito.

## 9. Limites e o que não foi testado

- Um LLM (Qwen) e um prompt. A qualidade das justificativas não tem medida humana tabulada; as leituras de qualidade foram feitas por LLM;
- Um conjunto em escala: 16.000 de 549 mil pares do e-SNLI; MNLI e RTE são mudanças de domínio brandas;
- Os pontos vagos do artigo foram lidos por mim de um jeito, e os autores não foram consultados;
- Não testei se a falta de ganho vem das justificativas que gerei: nas minhas, só 21,8% das palavras são novas e elas quase só entregam o rótulo (um BERT que lê só a justificativa acerta 96,9%). Num domínio em que a justificativa traga informação ausente do par o resultado pode ser outro. As medidas estão no documento Figuras e Evidencias, seção 6. Essa hipótese não explica o ganho que o artigo relata no RTE, que é um conjunto de domínio geral;
- Custo: gerar as 16 mil justificativas levou 5h20 de GPU (1,20 s por par), e o treino com decoder leva cerca de 33 minutos por semente, contra 4,5 sem decoder com o mesmo calendário; na inferência o custo é igual;
- Não variei a duração da fase só do decoder, pesos acima de 0,5 nem a taxa de aprendizado;
- Não testei por que o calendário ajuda, nem um alvo que se aprenda a partir do par sem falar do rótulo, que separaria "ensina o motivo" de "atrapalha como ruído";
- Na destilação: pesos de perda diferentes de 1,0, professor maior que o BERT base e mais pares para o aluno ficaram de fora.

O código, as rodadas e a leitura dos resultados foram feitos com LLM. São minhas a ideia das marcas de atenção, a de trocar o encoder por um menor, a hipótese dos grupos de palavras novas, as decisões de treinar nos 16.000 pares, de rodar o controle de calendário, a justificativa embaralhada, o segundo checkpoint MS-MARCO e o teste fora do domínio, a escolha das medidas do painel, os valores de peso, a pergunta sobre o arranque, a ideia de destilar a atenção de um BERT maior, a linha do professor que lê a justificativa e as escolhas na destilação. Os desenhos, os controles e os critérios de cada rodada foram escritos com LLM antes de rodar.
