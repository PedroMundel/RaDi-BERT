# Plano: último teste das marcas, fora da distribuição (10/11/2026)

**Procedência:** plano escrito pelo Claude a pedido do Pedro ("planeja esse último teste"). **Nada rodou e nenhum
código foi escrito.** As decisões marcadas com (D) são do Pedro; a coluna "recomendação" é do Claude. A afirmação de
que a literatura acha ganho fora da distribuição vem de `docs/pesquisa/2026-11-10-combinar-sinais-racionalizacao-
encoder.md`, que é nível 3 (agente leu só resumos): serve para escolher o teste, não para citar.

## 1. A pergunta

Todos os testes até aqui mediram o modelo em pares do próprio RTE, e a marca real empata com o treino normal
(`resultados/rte-pequenos/leitura-grade.md`). A pergunta que falta: **um modelo treinado no RTE com a marca real
acerta mais em pares de outro conjunto do que o mesmo modelo treinado sem marcas?**

A ideia por trás: o treino normal pode aprender atalhos que só valem no RTE. Se a marca puxa a atenção para as
palavras que a justificativa usa, o modelo dependeria menos desses atalhos e se sairia melhor em texto diferente.

## 2. O teste, por extenso

| Item | Escolha |
|---|---|
| Treino | RTE inteiro (2.470 pares), igual às grades de hoje. Nada muda no treino |
| Modelo | BERT small (`google/bert_uncased_L-4_H-512_A-8`) |
| Braços | sem marcas · marca real · marca aleatória |
| Sementes | 1 a 15 (45 treinos) |
| Teste de dentro | dev do RTE (277 pares), como sempre |
| **Teste de fora (principal)** | **dev do e-SNLI: 9.842 pares** (contados hoje), já no disco das duas máquinas |
| Rótulo no teste de fora | entailment = 1; neutral e contradiction = 0 (o RTE só tem "entailment" e "não entailment") |
| Medida principal | ROC-AUC no teste de fora, marca real − sem marcas, pareado por semente, intervalo t de 95% |
| Medidas secundárias | acurácia no teste de fora; real − aleatória; as mesmas no dev do RTE |

O e-SNLI é texto de outro tipo (legendas de imagem, frases curtas), então é mudança de distribuição de verdade. O
modelo nunca treinou nele: as rodadas de e-SNLI de 10/11 foram outros modelos, e os pesos não são salvos.

## 3. Regra de parada, escrita antes de rodar

Uma análise só, com as 15 sementes, sem olhar no meio.

| Resultado na medida principal | Conclusão |
|---|---|
| Intervalo inteiro acima de zero **e** real − aleatória também acima de zero | **Ganho.** Confirma-se uma vez com as sementes 16 a 25. Se repetir, o tema continua como "a justificativa melhora a robustez, não a nota". Se não repetir, é falso positivo e vale a linha de baixo |
| Intervalo cruza o zero, ou fica abaixo | **Hipótese encerrada.** Nenhuma variação nova das marcas (peso, camada, outro conjunto) é rodada depois |
| Baseline sem marcas abaixo de 0,55 de ROC-AUC no teste de fora | **Teste não informa** (o modelo está no piso, como o tiny). Não conta como nulo nem como ganho; a decisão de rodar ou não no BERT base é do Pedro |

Por que 15 sementes e uma análise só: hoje duas rodadas idênticas diferiram em até 0,026 numa semente, e o +0,017 de
5 sementes sumiu em 10 novas. Com 9.842 pares de teste o ruído da medida é pequeno; sobra o ruído do treino, e é
ele que as 15 sementes cobrem.

## 4. Contrato da etapa

- **Entrada:** código de hoje (encoder `marcas-small`), justificativas FA do RTE, dev do e-SNLI.
- **Saída:** `resultados/rte-marcas-small-fora/resultados.csv` com 45 linhas e as colunas novas do teste de fora;
  uma seção nova em `resultados/rte-pequenos/leitura-grade.md`.
- **Custo:** código ~30 min do Claude (seção 5); rodada ~25 min no PC (45 treinos de ~30 s, mais a avaliação em
  9.842 pares por treino). Usa menos de 1 GB de VRAM, então roda junto com o `llama-server` do Pedro.
- **Chance de ganho (palpite do Claude, não medida):** baixa a moderada. O mais provável é empate.
- **Parada:** a tabela da seção 3.

## 5. O que muda no código

Só avaliação; o treino não é tocado.

1. `rte_treino.py`: opção `--fora` que (a) carrega o dev do e-SNLI com o rótulo em duas classes, (b) avalia cada
   treino nele e grava `fora_roc_auc`, `fora_accuracy`, `n_fora` na linha do resultado, (c) grava numa pasta
   própria (`<pasta>-fora`), como o `--pares` já faz, porque as colunas do CSV mudam.
2. `esnli_dados.py`: função que devolve o dev com o rótulo em duas classes.
3. Teste: o rótulo em duas classes (3.329 pares com 1, 6.513 com 0) e a pasta própria.
4. Fumaça na CPU, `scp`, MD5, lançamento com vigia, como hoje.

Comando da rodada, no PC:

```bash
ssh pc 'cd D:\RaDi-BERT; uv run --frozen python -m radibert.rte_treino --grade --encoder marcas-small --warmups prop --seeds 15 --fora'
```

## 6. Decisões do Pedro

| # | Decisão | Opções | Recomendação do Claude |
|---|---|---|---|
| D1 | Conjunto de fora | ver tabela abaixo | dev do e-SNLI |
| D2 | Modelo | small · small e BERT base (+ ~30 min) | só o small; o base entra se o small ficar no piso |
| D3 | O decoder entra? | não · sim (+ ~45 min, 10 treinos de ~3 min por tamanho) | não: a pergunta é sobre as marcas |
| D4 | A regra de parada da seção 3 | aceita · muda | aceitar como está |

**D1, candidatos (existência conferida no Hub em 10/11; números de desempenho não conferidos):**

| Conjunto | Tamanho | Rótulos | No disco? | Risco | Licença |
|---|---|---|---|---|---|
| **dev do e-SNLI** (recomendado) | 9.842 | 3, viram 2 | sim, nas duas máquinas | juntar neutral e contradiction é escolha nossa | a do projeto, já em uso |
| `jhu-cogsci/hans` | não conferido | 2, iguais aos do RTE | não (download pede OK) | feito para derrubar atalhos; um modelo pequeno treinado em 2,5 mil pares deve ficar no piso | "unknown" no cartão |
| `allenai/scitail` | não conferido | 2 (entails, neutral) | não (download pede OK) | texto de ciência; piso possível | sem licença no cartão |

O e-SNLI ganha por estar no disco, ser grande e ter menos risco de piso. O HANS é o teste clássico de atalho e seria
o segundo a tentar, mas só se o primeiro der sinal.

## 7. Limites que já se sabe

- Um conjunto de fora só. Ganho nele não prova robustez em geral.
- O peso da marca (1,0) e a camada (última) continuam sem varredura.
- Se o dev do RTE for olhado junto, ele já foi visto: só o teste de fora é novo.

## 8. Teste do destaque (acrescentado em 10/11, 21h30, antes de rodar)

**Procedência:** ideia do Claude depois da medida de redundância, a pedido do Pedro ("não consegue pensar num cenário
que isso poderia ser útil?"; "pode rodar ele agora"). É uma leitura feita depois de ver os dados, por isso o critério
vai escrito antes do teste. Não busca ganho de nota: a hipótese das marcas para acerto segue encerrada (seção 3).

**Pergunta:** o BERT small treinado com a marca real serve de destaque de evidência, isto é, as palavras em que o
`[CLS]` mais presta atenção são as que a justificativa do LLM copia, em pares nunca treinados, e melhor do que uma
regra simples sem treino?

| Item | Escolha |
|---|---|
| Pares | os 1.470 pares do RTE nunca treinados (recorte do `--pares 1000`), só os que têm ao menos uma marca |
| Gabarito | as marcas reais (palavras do par que a justificativa do Qwen copia) |
| Nota de cada token | atenção do `[CLS]` na última camada, média das cabeças; só tokens do par (sem `[CLS]` e `[SEP]`) |
| Medida principal | precisão média (AP) por par, média dos pares |
| Medida secundária | AUROC por par, média dos pares |
| Modelos | marca real, sem marcas, marca aleatória (5 sementes cada) e o modelo antes do treino |
| Regras sem treino | (a) toda palavra de conteúdo; (b) palavra de conteúdo da hipótese; (c) palavra de conteúdo que aparece nas duas frases; (d) nota ao acaso. "Palavra de conteúdo" = a mesma definição das marcas (fora as gramaticais) |

**Critério, uma análise só:**

| Resultado | Conclusão |
|---|---|
| AP da marca real supera a **melhor** regra em 0,05 ou mais, nas 5 sementes, e supera o modelo sem marcas | **O destaque aprendido vale algo.** Vira candidato a cenário; o passo seguinte (outra tarefa, texto longo) é decisão do Pedro |
| AP da marca real fica a menos de 0,05 da melhor regra, ou abaixo | **Trivial.** Uma regra sem treino faz o mesmo; o cenário é encerrado |

Limite já sabido: o gabarito é o que o LLM copia, não o que um humano marcaria nem o que o modelo usa para decidir.

## 9. Cabeça por token como referência do destaque (acrescentado em 10/11, 23h, antes de rodar)

**Procedência:** pedido do Pedro ("roda aquela cabeça por token"). Lacuna do item 6 da leitura do destaque.

**Pergunta:** o destaque tirado da atenção do `[CLS]` (AP 0,731 com 2.000 pares) chega perto do que um modelo
treinado direto para marcar palavras consegue?

| Item | Escolha |
|---|---|
| Braço novo | BERT small com uma camada linear sobre o vetor de cada token (última camada), treinada com entropia cruzada binária contra as marcas reais; perda total = classificação + 1,0 × marcação, desde o passo 1, como nas marcas de atenção |
| Nota de cada token | a probabilidade que a cabeça dá |
| Comparação | na mesma rodada: marca real (atenção), sem marcas, marca aleatória, cabeça por token; 2.000 pares de treino, 470 de teste, 5 sementes |
| Medida | AP do destaque (principal); ROC-AUC de classificação no dev e nos 470 pares (relatado) |

**Leitura combinada antes:**

| Resultado | Conclusão |
|---|---|
| Cabeça supera a atenção em 0,05 de AP ou mais, nas 5 sementes | Para o destaque, a cabeça dedicada é o mecanismo melhor; o cenário continua, com uma camada linear a mais |
| Diferença menor que 0,05, ou atenção acima | A atenção entrega um destaque tão bom quanto o de uma cabeça dedicada |

A classificação é relatada, mas **diferença de nota com 5 sementes abaixo de ~0,03 não é lida como ganho** (regra do
`## Rejected`), e a regra de parada das marcas continua valendo: esta rodada não busca nota.

## 10. Atenção nas outras camadas: (a) intervenção sem treino e (b) treino com a marca por camada (acrescentado em 16/11, antes de rodar)

**Procedência:** decisão do Pedro (16/11): "testar se mexer nas outras camadas de atenção muda alguma coisa
(ablação) e depois testar o d"; "os dois: (a) sem treinar primeiro, (b) treinos com as marcas". Reabre só a parte
"camada" da regra de parada da seção 3; peso da marca e outro conjunto de teste continuam fora. O desenho abaixo é
proposta do Claude, **confirmada pelo Pedro em 16/11 com uma mudança** ("só muda uma coisa, coloca interpolação de
camadas também": as 11 combinações de 10.1; se valem também para os treinos de 10.2 está em aberto com ele). O
sorteio entre palavras de conteúdo pode coincidir com marcas reais: é sorteio entre as palavras em que uma marca
poderia cair, e a coincidência média é relatada. **Nenhuma escolha de método foi conferida na literatura**:
bloquear ligações de atenção é uma técnica que existe em trabalhos de interpretabilidade, mas nenhum foi lido aqui e
nenhum é citado.

**O que já está medido (seção de atenção da `leitura-grade.md`, `atencao.csv`):** fração da atenção do `[CLS]` nas
palavras marcadas, por camada, no BERT small sem marcas: 0,18 · 0,23 · 0,41 · 0,29 (uniforme = 0,19). Isso diz para
onde ele olha, não se a decisão depende disso. É o que (a) mede.

### 10.1 (a) Intervenção na atenção, sem treino novo

**Pergunta:** no modelo já treinado, em qual camada a atenção às palavras que a justificativa copia pesa na decisão?

| Item | Escolha |
|---|---|
| Modelos | BERT small, 2.000 pares de treino, 5 sementes, braço sem marcas (principal) e braço marca real na camada 4 (o que já existe) |
| Pares medidos | os 470 pares do RTE nunca treinados (recorte do `--pares 2000`), só os que têm ao menos uma marca |
| Onde se mexe | 11 combinações (mudança do Pedro, 16/11): cada camada sozinha (1, 2, 3, 4), cada par (1 e 2, 1 e 3, 1 e 4, 2 e 3, 2 e 4, 3 e 4) e as quatro juntas |
| Operação **bloquear** | na camada escolhida, o `[CLS]` fica impedido de olhar para um conjunto de posições; a atenção se redistribui pelo resto |
| Operação **só estas** | na camada escolhida, o `[CLS]` só pode olhar para o conjunto (e para si mesmo) |
| Conjuntos de posições | (1) palavras que a justificativa copia (marca real); (2) mesmo número de posições sorteadas no par (a coluna `random` que já existe); (3) mesmo número sorteado só entre palavras de conteúdo; (4) um segundo sorteio de (3), com outra semente |
| Linhas mexidas | principal: só a linha do `[CLS]` (é a que a perda das marcas cobra). Relatado ao lado: todas as linhas (nenhum token olha para o conjunto), porque nas camadas 1 a 3 todos os tokens alimentam a camada seguinte |
| Medida principal | fração dos pares em que a classe prevista muda em relação ao modelo sem intervenção |
| Medidas ao lado | queda média da probabilidade da classe que o modelo tinha escolhido; ROC-AUC nos mesmos pares |

**Como a intervenção é feita:** antes do cálculo de atenção da camada escolhida, soma-se um valor muito negativo às
posições proibidas na máscara de atenção, do mesmo jeito que o BERT já ignora o preenchimento. Os pesos do modelo
não mudam. Um teste confere que, sem posição proibida, a saída é idêntica à do modelo normal.

**Por que os conjuntos (3) e (4):** as marcas reais nunca são palavras gramaticais e o sorteio (2) pode ser; (3)
tira essa vantagem. A diferença entre (3) e (4), dois sorteios do mesmo tipo, é o tamanho do acaso desta medida.

**Leitura combinada antes:**

| Resultado, por camada e operação | Conclusão |
|---|---|
| Bloquear a marca real muda mais decisões que bloquear (3), com o mesmo sinal nas 5 sementes e diferença média maior que a maior diferença entre (3) e (4) em qualquer semente | Naquela camada a decisão **depende** da atenção do `[CLS]` às palavras da justificativa mais do que a outras palavras de conteúdo |
| Diferença dentro do tamanho do acaso, ou sinal que troca entre sementes | Naquela camada **não se distingue** a marca real de outras palavras de conteúdo |
| Nenhum bloqueio (real ou sorteado) muda mais de 1% das decisões numa camada | A atenção do `[CLS]` naquela camada **não pesa** na decisão por esse caminho |

**Limites já sabidos:** bloquear atenção cria uma situação que o modelo nunca viu no treino; o controle sorteado mede
o efeito disso. O `[CLS]` também recebe informação pelo caminho direto entre camadas, que a intervenção não toca. O
gabarito é o que o LLM copiou. 470 pares, 5 sementes, um modelo, uma tarefa. O resultado de (a) **não decide** quais
camadas entram em (b): (b) roda as três de qualquer forma, e (a) fica como previsão escrita antes.

### 10.2 (b) Treino com a marca cobrada em outra camada

**Pergunta:** cobrar a atenção do `[CLS]` nas palavras da justificativa na camada 1, 2 ou 3, em vez da 4, muda a
classificação?

| Item | Escolha |
|---|---|
| Braços | marca real e marca sorteada (coluna `random`) nas mesmas 11 combinações de camadas de 10.1 (Pedro, 16/11: "As 11"); sem marcas. Com mais de uma camada, a perda é a soma da perda de cada camada, para cada camada ser puxada com a mesma força de quando está sozinha (escolha do Claude) |
| Perda | a mesma `mark_loss` (linha do `[CLS]`, média das cabeças), peso 1,0, desde o passo 1; muda só a camada lida |
| Treino | BERT small, 2.000 pares, calendário `prop`, 5 sementes por braço |
| Medida | ROC-AUC no dev do RTE (277, já visto muitas vezes) e nos 470 pares nunca treinados |

**Leitura combinada antes:**

| Resultado | Conclusão |
|---|---|
| Algum braço de marca real supera o sem marcas **e** a marca sorteada da mesma camada em 0,03 ou mais de ROC-AUC, nos dois conjuntos | **Candidato.** Roda 10 sementes novas só desse braço e dos dois controles; só se o intervalo das 15 não cruzar o zero conta como ganho |
| Abaixo de 0,03, ou só num conjunto, ou só contra um dos controles | **Nulo.** A camada volta para a regra de parada; nenhuma variação nova de camada |

O 0,03 vem da regra do `## Rejected` de 10/11 (o mesmo treino na GPU varia até 0,026 entre rodadas).

## 11. Destilar a atenção do BERT base no BERT small (acrescentado em 16/11, antes de rodar; ESPERA A CONFIRMAÇÃO DO PEDRO)

**Procedência:** ideia do Pedro (16/11): "às vezes a gente deveria estar destilando a atenção do BERT-large"; "vamos
fazer com o base primeiro". Ele mesmo apontou que o que rodou até aqui não é destilação: as marcas são as palavras
que a justificativa do LLM cita, não a atenção de um modelo. **O sinal aqui deixa de vir da justificativa do LLM.**

**Fontes (nível 3: páginas do ar5iv resumidas por modelo, em 16/11; ninguém leu os artigos inteiros):**

| | MiniLM (Wang et al., 2020, arXiv:2002.10957) | TinyBERT (Jiao et al., 2020, arXiv:1909.10351) |
|---|---|---|
| O que o aluno imita | a atenção da **última** camada do professor (seção 3.1) | a atenção de várias camadas, uma do professor para cada uma do aluno |
| Conta | divergência KL entre as distribuições de atenção, por cabeça, todas as linhas (eq. 6) | erro quadrático entre as notas de atenção **antes** do softmax, por cabeça (eq. 7) |
| Casamento de camadas | não precisa | uniforme: camada m do aluno aprende da camada 3m do professor, no aluno de 4 camadas (seção 4.2) |
| Quando | no pré-treino, em texto geral | em duas etapas; na da tarefa, o professor é o BERT **ajustado na tarefa**, com dados aumentados |
| Cabeças | aluno com 12 cabeças, como o professor | aluno com 12 cabeças, como o professor |
| Efeito relatado | aluno 6x384: MNLI 82,2 contra 84,5 do professor (tabelas 2 e 3) | sem a parte de atenção, o aluno de 4 camadas cai de 82,8 para 79,9 no MNLI (tabela 3) |

**O que é diferente no nosso caso, e nenhuma das duas fontes cobre:** o aluno é o BERT small do Google, já
pré-treinado, com **8 cabeças** contra 12 do professor; a destilação seria só na tarefa, com 4.000 pares, sem dados
aumentados e sem a etapa geral.

### 11.1 Desenho proposto (escolhas do Claude, a confirmar)

| Item | Escolha | De onde vem |
|---|---|---|
| Dados | os 4.000 pares do e-SNLI de `esnli_dados`; nota no dev do e-SNLI (acurácia) | no e-SNLI as sementes variam 0,4 ponto e o base está 5,8 pontos acima do small (medido em 16/11) |
| Professor | BERT base ajustado nesses 4.000 pares, uma semente, pesos parados; a nota dele é registrada | TinyBERT, etapa da tarefa |
| Aluno | BERT small, mesma receita de treino de hoje, 5 sementes | rodadas de 16/11 |
| Cabeças | média das cabeças dos dois lados antes de comparar (12 no professor, 8 no aluno) | escolha do Claude; é o que a perda das marcas já faz |
| Linhas | todas as linhas de atenção, média sobre os tokens reais | as duas fontes |
| Conta | divergência KL entre a atenção do professor e a do aluno | MiniLM, eq. 6 |
| Braço U (última) | última camada do professor -> última do aluno | MiniLM |
| Braço T (todas) | camadas 3, 6, 9 e 12 do professor -> 1, 2, 3 e 4 do aluno, soma das quatro | TinyBERT, casamento uniforme |
| Peso | perda de classificação + 1,0 x perda de atenção, desde o passo 1 | o mesmo das marcas |
| Controle 1 | small sem destilação | já rodado: 73,9% |
| Controle 2 | mesma destilação com o BERT base **sem ajuste na tarefa** como professor | separa "atenção de quem aprendeu a tarefa" de "atenção de qualquer BERT maior" |
| Referência (opcional) | destilação clássica das saídas do professor (Hinton et al., 2015), sem atenção | diz se este professor ajuda o small por algum caminho |

### 11.2 Leitura combinada antes

| Resultado, na acurácia do dev do e-SNLI | Conclusão |
|---|---|
| Braço U ou T supera o small sem destilação em 1,0 ponto ou mais, nas 5 sementes, **e** supera o controle 2 em 1,0 ponto ou mais | A atenção do professor ajustado na tarefa ajuda o small |
| Supera o sem destilação em 1,0 ponto ou mais, mas não o controle 2 | Imitar a atenção de um BERT maior ajuda, e não depende de ele ter aprendido a tarefa |
| Menos de 1,0 ponto, ou sinal que troca entre sementes | Nulo neste desenho |

O 1,0 ponto é 2,5 vezes o desvio entre sementes do small no e-SNLI (0,4 ponto), escolha do Claude.

**Limites já sabidos:** um professor, um aluno, uma tarefa, 4.000 pares; a média das cabeças joga fora o que cada
cabeça faz; as fontes destilam também outras coisas (estados internos, relações de valor) que aqui ficam de fora.

**Confirmado pelo Pedro em 16/11 ("Confirmo"), com a referência opcional. Rodado: nulo** (nenhum braço passa de
+0,1 ponto; `resultados/rte-pequenos/leitura-grade.md`).

### 11.3 Professor que não viu os pares do aluno (acrescentado em 16/11, antes de rodar)

**Procedência:** hipótese do Claude para o nulo de 11.2, inclusive o da destilação das saídas: o professor foi
treinado nos mesmos 4.000 pares em que o aluno destila, decorou-os, e ali a saída dele é quase o rótulo certo.
Pedro (16/11): "vamos por esse caminho então". O desenho abaixo é a leitura do Claude desse pedido.

| Item | Escolha |
|---|---|
| O que muda em relação a 11.1 | **só o professor**: BERT base treinado em outros 4.000 pares do mesmo lote do e-SNLI, sem nenhum par em comum com os 4.000 do aluno (sorteio fixo entre os 12.000 restantes) |
| O que não muda | o aluno: mesmos 4.000 pares, mesmos rótulos, mesmos 1.000 passos, mesmas 5 sementes, mesma perda |
| Braços | sem destilação; atenção da última camada; atenção das 4 camadas; saídas do professor |
| Conferência da premissa | para os dois professores (o de 11.1 e o novo): acurácia e certeza média (probabilidade da classe escolhida) **nos 4.000 pares do aluno**. A hipótese prevê perto de 100% para o professor de 11.1 e perto da nota do dev para o novo |

**Leitura combinada antes:**

| Resultado, na acurácia do dev do e-SNLI | Conclusão |
|---|---|
| A premissa não se confirma (o professor de 11.1 não está perto de 100% nos pares do aluno) | A hipótese cai antes do teste: o nulo de 11.2 não vem de o professor ter decorado |
| Premissa confirmada **e** algum braço supera o sem destilação em 1,0 ponto ou mais nas 5 sementes | A hipótese se sustenta: o professor precisa não ter decorado os pares para passar algo ao aluno |
| Premissa confirmada e nenhum braço chega a 1,0 ponto | A hipótese cai: mesmo sem decorar, este professor não passa nada ao small neste desenho |

**Limites já sabidos:** os dois professores diferem também nos pares em que foram treinados, não só em terem visto
ou não os do aluno; um professor de cada, uma semente; o mesmo limite de 1,0 ponto.

**Rodado em 16/11:** premissa confirmada (professor de 11.1: 100,0% e certeza 99,9% nos pares do aluno); imitar as
respostas do professor que não viu os pares dá +1,6 ponto (pior semente +1,3), passa; atenção continua nula.

### 11.4 Subir o ganho das respostas, e de onde ele vem (acrescentado em 16/11, antes de rodar)

**Procedência:** Pedro (16/11): "se é o que deu certo, vamos ver se dá pra subir mais". As alavancas e os controles
abaixo são escolha do Claude; ele não escolheu quais. Temperatura e o fator T² vêm de Hinton et al. (2015), lido
pelo Pedro; a fórmula está escrita **de memória** pelo Claude, não conferida no artigo. Suavização de rótulo com
0,1: valor usual, **de memória**.

**Regra para não escolher por sorte:** o dev do e-SNLI não escolhe nada. Um conjunto de escolha novo, 4.000 pares do
mesmo lote que nem o aluno nem nenhum professor viu, decide qual variação é a melhor; o dev só é lido para
confirmar a escolhida (os números do dev de todos os braços ficam no arquivo, mas não entram na escolha).

| Braço | O que é | Para que serve |
|---|---|---|
| sem destilação | o small sozinho | base |
| respostas, T=1 | o que passou em 11.3 (professor A: 4.000 pares que o aluno não viu) | referência a bater |
| respostas, T=2 e T=4 | as probabilidades do professor A mais espalhadas (temperatura), perda multiplicada por T² | alavanca 1 |
| professor maior, T=1 e T=2 | professor B: BERT base treinado em 8.000 pares que o aluno não viu | alavanca 2 |
| rótulo suavizado | sem professor: alvo = 90% na classe certa, 5% em cada outra | controle: o ganho é só de o alvo ser mole? |
| respostas trocadas | as respostas do professor A, mas cada par recebe as de outro par do mesmo rótulo | controle: o ganho depende do que o professor diz sobre **aquele** par? |

Aluno sempre igual: BERT small, os mesmos 4.000 pares, 1.000 passos, 5 sementes, classificação + 1,0 x perda do alvo.

**Leitura combinada antes (acurácia no conjunto de escolha, diferenças pareadas por semente):**

| Resultado | Conclusão |
|---|---|
| Uma variação (T=2, T=4 ou professor maior) supera "respostas, T=1" em 0,5 ponto ou mais, nas 5 sementes, **e** no dev a mesma variação também fica 0,5 ponto ou mais acima | Subiu. Essa é a configuração melhor |
| Nenhuma chega a 0,5 no conjunto de escolha, ou o dev não confirma | Não subiu com estas alavancas |
| "Rótulo suavizado" fica a menos de 0,5 ponto de "respostas, T=1" | O ganho de 11.3 é explicado por o alvo ser mole; o professor não é necessário |
| "Respostas trocadas" fica a menos de 0,5 ponto de "respostas, T=1" | O ganho não depende do que o professor diz sobre cada par |
| Os dois controles ficam 0,5 ponto ou mais abaixo | O ganho vem do que o professor sabe sobre cada par |

O 0,5 ponto é pouco mais que o desvio entre sementes no dev (0,4); escolha do Claude. **Limites:** um professor de
cada tipo, uma semente deles; o conjunto de escolha vem do mesmo lote do treino; peso fixo em 1,0.

### 11.5 Juntar a atenção com a destilação das respostas (acrescentado em 16/11 com 3 jeitos; revisto em 17/11: jeito 3 retirado pelo Pedro, MiniLM e TinyBERT lidos, desenho final confirmado por ele no fim da seção)

**Procedência:** Pedro (16/11): "pense na arquitetura de um transformer, e só então deduza como as duas podem
ajudar"; depois, "vamos rodar as 3". Os três jeitos foram deduzidos pelo Claude; os braços, os controles, os pesos e
o critério abaixo são escolha do Claude, **a confirmar**. Nada foi codado nem rodado. **Pedro (17/11): "Sem jeito 3
então. Lê o MiniLM. Não sei como decidir a 2 e 3, sem saber como cada mudança afeta."**

**Pergunta:** somar algum sinal de atenção à destilação das respostas faz o small passar do que as respostas
sozinhas já dão?

**O que já está medido e serve de ponto de partida (não é previsão):**

- Respostas do professor A sozinhas: +1,6 ponto sobre o small sem destilação, no conjunto de escolha e no dev.
- Atenção do professor A sozinha: +0,1 (última camada) e +0,3 (4 camadas), nulo.
**Fontes:** MiniLM (Wang et al., 2020, arXiv:2002.10957): **nível 2**, lido pelo Claude em 17/11 (seções 1 a 5.1
inteiras; notas em `docs/artigos/notas-minilm-wang-2020.md`). TinyBERT (Jiao et al., 2020, arXiv:1909.10351):
**nível 2**, lido pelo Claude em 17/11 (seções 1 a 4.6 e apêndices A a C; notas em
`docs/artigos/notas-tinybert-jiao-2020.md`). MiniLMv2 (Wang et al., 2020, arXiv:2012.15828): só o resumo no arXiv, que diz não
exigir o mesmo número de cabeças; o mecanismo não foi lido.

**O que o MiniLM diz e muda este desenho:**

- Ele destila **sem tarefa** (texto geral, 400 mil passos) e o aluno é ajustado na tarefa depois, do jeito comum.
  **Não junta nada com as respostas do professor na tarefa, em nenhuma ordem.** Nenhum dos braços abaixo repete uma
  condição do artigo; os números dele dizem para que lado cada peça empurrou lá, não aqui.
- Só a última camada. Camada a camada, com casamento uniforme, foi **pior** no aluno de 4 camadas: 79,9 contra 80,3
  no MNLI (tabela 7).
- Atenção + relação entre valores, pesos iguais. Sem a relação entre valores: 79,0 contra 80,3 (tabela 5). Com erro
  quadrático sobre os valores e matriz de projeção no lugar: 80,1 contra 80,3 (tabela 6). Relação entre **estados
  internos**: "instável" entre professores (seção 4.4).
- O aluno deles foi montado com 12 cabeças, como o professor. 8 contra 12 não é tratado.

**O que o TinyBERT diz e muda este desenho:**

- Na tarefa ele faz duas fases seguidas: a interna (embeddings + atenção + estados internos, 4 camadas) por **20
  épocas** (10 nas tarefas grandes) e depois só as respostas do professor por **3 épocas**, tudo em dados da tarefa
  aumentados 21 vezes. A fase interna imita atenção **e** estados internos juntos: o jeito 1 daqui (só atenção, depois
  respostas) e o pacote TinyBERT do jeito 2 (tudo junto num treino) são, cada um, metade do que o artigo faz.
- **Apêndice C, o caso mais perto do nosso:** aluno pequeno pré-treinado direto (sem a etapa geral deles), sem
  dados aumentados. A destilação na tarefa ajuda no MNLI (75,9 para 79,2) e **não ajuda nas tarefas pequenas** (MRPC
  83,2 para 82,9; CoLA 19,5 para 12,4). O nosso aluno é um BERT pequeno pré-treinado direto e o conjunto tem 4.000
  pares.
- Atenção deles: erro quadrático antes do softmax, por cabeça, aluno com 12 cabeças. A nossa: KL depois do softmax,
  média das cabeças.
- Sem atenção: 79,9 contra 82,8 no MNLI; sem estados internos: 81,7; sem embeddings: 82,3 (tabela 3).

**O que é igual em todos os braços:** aluno BERT small, os mesmos 4.000 pares do e-SNLI, 5 sementes, lote de 32,
mesma taxa de aprendizado; professor A (BERT base treinado em 4.000 pares que o aluno não viu, 79,2% no dev), parado,
carregado de `destilacao-professor-fora-4000.pt`; respostas do professor com T=1 e peso 1,0; cabeças de atenção
comparadas pela média (12 no professor, 8 no aluno), como em 11.1.

**Braços de referência, rodados de novo no mesmo script para comparar semente a semente:**

| Braço | O que é |
|---|---|
| sem destilação | o small sozinho |
| respostas | classificação + respostas do professor A (o que passou em 11.3); **é a referência a bater** |

**Jeito 3 (atenção como guia): retirado pelo Pedro em 17/11.** Não roda em nenhuma das duas versões (marcas do LLM
ou linha do `[CLS]` do professor). A regra de parada das marcas (`CLAUDE.md`, `## Rejected`) fica como estava.

**Jeito 1, em sequência.** Dois treinos seguidos no mesmo aluno. Fase 1: 1.000 passos **só** de atenção (4 camadas,
casamento uniforme, todas as linhas, a mesma conta de 11.1), sem classificação e sem respostas. Fase 2: os 1.000
passos de sempre, classificação + respostas, com otimizador e calendário de taxa novos. O tamanho da fase 1 (igual ao
da fase 2) é escolha do Claude; o TinyBERT usa uma fase interna mais longa que a das respostas (nível 3).

| Braço | Fase 1 | Para que serve |
|---|---|---|
| sequência | imita a atenção do professor A | o jeito 1 |
| controle, professor sem tarefa | imita a atenção de um BERT base **não** treinado na tarefa | se "sequência" passar: vem de o professor saber a tarefa ou de qualquer fase de imitação? |
| soma simples (**extra, não pedido**) | não há fase 1: classificação + respostas + atenção das 4 camadas desde o passo 1, 1.000 passos | se "sequência" passar: vem da ordem ou só de ter os dois sinais? |

**Jeito 2, atenção mais conteúdo.** Um treino só, 1.000 passos: classificação + respostas + atenção das 4 camadas +
uma perda de conteúdo. "Conteúdo" tem duas formas nas fontes, e cada uma vem com a sua escolha de camadas:

| | Pacote MiniLM (nível 2) | Pacote TinyBERT (nível 2) |
|---|---|---|
| Camadas | só a última do professor para a última do aluno | 4 camadas, casamento uniforme (3, 6, 9, 12 para 1, 2, 3, 4) |
| Conteúdo que o aluno imita | relação entre valores: para cada par de tokens, o quanto os vetores de valor se parecem (KL, eq. 7 a 9) | estados internos: o vetor de cada token na saída da camada (erro quadrático) |
| Tamanhos diferentes (512 x 768) | não entra: a comparação é token com token | uma camada linear treinada junto leva 512 a 768 e é descartada no fim |
| Cabeças diferentes (8 x 12) | **sem fonte**: o artigo usa 12 e 12. **Pedro (17/11): média das cabeças**, como na atenção | não entra no conteúdo; entra na atenção, como já entra hoje |
| O que a fonte mediu | tirar a relação entre valores custa 1,3 ponto no MNLI; lá, sem tarefa | o pacote inteiro, refeito pelo MiniLM: 79,2 contra 80,3 no MNLI; a peça dos estados internos nunca isolada |
| Código que falta | pouco: o valor é a camada `value` do BERT aplicada ao estado da camada anterior | pouco: o BERT já devolve os estados internos; mais a camada de projeção no otimizador |
| Risco conhecido | a saída para as cabeças é invenção nossa | erro quadrático tem outra escala que as demais perdas e pode dominar o gradiente |

Como ler: cada coluna é um jeito de copiar "o que passa pela atenção"; as linhas são o que muda de um para o outro.
**A recomendação anterior do Claude (estados internos, "menos código") caiu:** a diferença de código não existe, e
a única comparação lida favorece a relação entre valores, numa condição que não é a nossa. Rodar os dois pacotes
custa dois braços a mais (cerca de 7 minutos cada).

| Braço | O que soma à classificação + respostas | Para que serve |
|---|---|---|
| atenção + conteúdo | atenção + conteúdo, nas camadas do pacote escolhido | o jeito 2 |
| controle, só conteúdo | o mesmo conteúdo, sem atenção | se "atenção + conteúdo" passar: a atenção fez falta? |

Na fumaça, o valor de cada perda no passo 1 e no último é impresso, para ver se alguma domina. **O peso não é
ajustado depois de ver a nota.**

**Leitura combinada antes (acurácia; diferença semente a semente contra o braço "respostas"):**

| Resultado | Conclusão |
|---|---|
| Um braço dos 2 jeitos fica 0,5 ponto ou mais acima de "respostas" nas 5 sementes no conjunto de escolha, **e** 0,5 ponto ou mais acima na média do dev | **Candidato.** Rodam 10 sementes novas desse braço, de "respostas" e do controle dele; só conta como ganho se o intervalo da diferença nas 15 sementes não cruzar o zero |
| Candidato confirmado e o controle dele fica a menos de 0,5 ponto dele | Houve ganho, mas não vem do sinal de atenção que o braço diz usar |
| Menos de 0,5 ponto, ou sinal que troca entre sementes, ou o dev não confirma | **Juntar não ajudou neste desenho**, para aquele jeito |
| Um braço fica 0,5 ponto ou mais **abaixo** de "respostas" nas 5 sementes | Aquele sinal de atenção atrapalha a destilação das respostas |

O 0,5 ponto e o conjunto de escolha decidindo são os de 11.4. As 10 sementes novas entram porque aqui são 5 braços
(7 se os dois pacotes do jeito 2 rodarem) comparados com a mesma referência: a chance de um passar por sorte é maior que em 11.4.

**Custo previsto (conta, não medida):** 7 braços x 5 sementes (9 braços com os dois pacotes). Um aluno leva ~45 s
sem professor e ~75 s com (medido em 16/11); os dois braços com fase 1 levam cerca do dobro. Total perto de 50
minutos (1h05 com os dois pacotes), em duas rodadas (uma por jeito), cada uma acima de 10 minutos:
`training-auditor` antes e `train-watch` para lançar.

**Limites já sabidos:** um professor, uma semente dele; um aluno, uma tarefa, 4.000 pares; pesos fixos em 1,0 e soma
das camadas; média das cabeças; tamanho da fase 1 sem fonte; o conjunto de escolha vem do mesmo lote do treino; nenhuma
fonte lida junta imitação interna com respostas na tarefa; se nenhum braço passar, isso vale para estes pesos e estas camadas, não para "juntar" em geral.

**A confirmar pelo Pedro antes de codar:**

1. ~~Jeito 3 com marcas~~: respondido em 17/11, o jeito 3 saiu inteiro.
2. Conteúdo do jeito 2: pacote MiniLM, pacote TinyBERT, ou os dois. **Respondido (Pedro, 17/11): "Os dois
   pacotes".** O jeito 2 roda 4 braços: atenção + conteúdo e só conteúdo, em cada pacote.
3. O braço "soma simples" entra? **Respondido (Pedro, 17/11): "Entra sempre".**
4. Fase 1 do jeito 1. **Respondido (Pedro, 17/11): "Como no TinyBERT"**, depois de o Claude ler o artigo.
5. Cabeças no pacote MiniLM: **respondido (Pedro, 17/11): média das cabeças.**

**Desenho final depois das respostas de 17/11 (vale no lugar do que estiver diferente acima):**

| Braço | Treino | Fonte |
|---|---|---|
| sem destilação | 1.000 passos, só classificação | referência |
| respostas | 1.000 passos, classificação + respostas do professor A | referência a bater (11.3) |
| sequência | fase 1: 2.500 passos (20 épocas) só de imitação interna do professor A: embeddings + atenção e estados internos das 4 camadas, sem classificação e sem respostas; fase 2: igual ao braço "respostas" | TinyBERT, seção 4.2 |
| controle da sequência | a mesma fase 1, com um BERT base não treinado na tarefa como professor; fase 2 igual | escolha do Claude |
| soma simples | 1.000 passos, classificação + respostas + atenção das 4 camadas | Pedro: "Entra sempre" |
| pacote TinyBERT junto | 1.000 passos, classificação + respostas + embeddings + atenção e estados internos das 4 camadas | TinyBERT, as mesmas perdas, sem fases |
| pacote TinyBERT sem atenção | o mesmo, sem a perda de atenção | controle |
| pacote MiniLM junto | 1.000 passos, classificação + respostas + atenção e relação entre valores da última camada | MiniLM, eq. 6 a 10 |
| pacote MiniLM sem atenção | o mesmo, sem a perda de atenção | controle |

**O que continua diferente do TinyBERT, declarado:** sem dados aumentados; aluno pré-treinado direto (a condição do
apêndice C); atenção por KL depois do softmax com média das cabeças (o artigo: erro quadrático antes do softmax, por
cabeça, 12 e 12); a fase 2 usa o rótulo certo mais as respostas (o artigo: só as respostas), para ser idêntica ao
braço "respostas"; 20 épocas de fase 1 contra 8 de fase 2 (o artigo: 20 contra 3). Uma matriz de projeção para os
embeddings e uma para os estados internos, a segunda compartilhada pelas 4 camadas: leitura do Claude das eq. 8 e 9,
o código deles não foi lido.

**Acréscimo de 17/11, antes de rodar: atenção lida antes do dropout.** A auditoria de código e o brute-test
(`docs/claude/brute-test-juntar.md`) mostraram que a atenção que o BERT devolve em treino já passou pelo dropout
(10% das entradas zeradas, linhas que não somam 1), e é sobre ela que a perda de atenção e a das marcas são
calculadas desde 10/11. **Pedro (17/11): "Rodar dos dois jeitos".** Os cinco braços com perda de atenção (soma
simples, pacote TinyBERT junto, pacote MiniLM junto, sequência e controle da sequência) rodam também numa versão
`_clean`, em que a atenção do aluno é recalculada antes do dropout; nas duas fases, no caso da sequência. São 14
braços. Leitura combinada antes, para este acréscimo: se algum braço `_clean` ficar 0,5 ponto ou mais acima do seu
par nas 5 sementes no conjunto de escolha, o ruído do dropout pesava, e os nulos de atenção de 16/11 ficam em
aberto; se nenhum ficar, o ruído não explica aqueles nulos **neste desenho** (não foram rodados de novo).

**Pedro (17/11): "Pode escrever"** o código, depois da explicação. Código em `src/radibert/rte_destilacao.py` e
`resultados/rte-pequenos/medir_juntar.py`.

**Custo previsto (conta, não medida):** 14 braços x 5 sementes, perto de 2h20; os quatro braços com fase 1 são
mais da metade disso. Critério: o mesmo escrito acima (0,5 ponto sobre "respostas" nas 5 sementes no conjunto de escolha, dev
confirmando, e 10 sementes novas para o candidato).

**Rodado em 17/11** (`resultados/rte-pequenos/leitura-grade.md`, seção "Juntar o interior do professor com as
respostas"): só a sequência virou candidata; com as 10 sementes novas, +0,93 ponto sobre "respostas" no conjunto de
escolha (intervalo de 95% de +0,70 a +1,17, acima nas 15 sementes) e +0,45 no dev (+0,25 a +0,65). O controle não
ganha. Juntar tudo num treino só não ajudou. Nenhum braço "antes do dropout" ficou 0,5 ponto acima do seu par.

### 11.6 Quanto as palavras novas da justificativa dizem sobre o rótulo (acrescentado em 17/11, antes de rodar)

**Procedência:** hipótese do Pedro (17/11): pegar as palavras novas da justificativa e levá-las ao `[CLS]` num treino
novo, junto com a destilação. Antes de gastar GPU, o Claude sugeriu esta checagem e o Pedro respondeu "pode rodar".
Desenho, faixas e nomes abaixo são escolha do Claude.

**Pergunta:** só com as palavras novas da justificativa (grupo N de `rte_gradientes.word_groups`: palavra que não
está no par, não é gramatical e não é expressão de rótulo), dá para adivinhar o rótulo?

| Item | Escolha |
|---|---|
| Dados | os 4.000 pares de treino do e-SNLI (`esnli_dados.training_pairs`) com as justificativas F do Qwen 35B |
| Modelo | regressão logística sobre presença de palavra (cada palavra que aparece em 2 pares ou mais vira uma coluna 0/1) |
| Nota | acurácia em validação cruzada de 5 partes; chute pela classe mais comum = cerca de 34% |
| Conjuntos de palavras, um modelo para cada | N (novas); S (expressões de rótulo); C (copiadas do par); F (gramaticais); a justificativa inteira; e as palavras do próprio par (premissa e hipótese), como referência do que já está na entrada |

**Leitura combinada antes, para o conjunto N:**

| Acurácia só com as palavras novas | Conclusão |
|---|---|
| 90% ou mais | As palavras novas são, na prática, o rótulo dito de outro jeito: prever essas palavras ensina o que o rótulo já ensina |
| 40% ou menos | As palavras novas não falam da decisão: como alvo, seriam ruído para a classificação |
| Entre 40% e 90% | Caso do meio: carregam parte da decisão sem serem o rótulo; é onde pode haver algo. A comparação com "palavras do par" diz quanto disso já está na entrada |

**Limites já sabidos:** presença de palavra ignora ordem e negação com alcance; as expressões de rótulo (S) são
tiradas dos próprios pares, então o grupo N já exclui as mais reveladoras por construção; isto mede informação
sobre o rótulo, **não prevê** se um treino com esse alvo dá ganho.

### 11.7 Agrupar as palavras novas com HDBSCAN: molde de argumentar ou conteúdo? (acrescentado em 17/11, antes de rodar)

**Procedência:** ideia do Pedro (17/11): "e HDBSCAN pra medir essas palavras novas?"; "pode instalar o UMAP e rodar".
Ele não escolheu de onde vêm os vetores; a escolha abaixo e os parâmetros são do Claude. É uma leitura
exploratória: não há critério de ganho.

**Pergunta:** os 76,4% da seção 11.6 vêm de palavras de argumentar do LLM ou de palavras de assunto?

| Item | Escolha |
|---|---|
| Palavras | as 2.323 palavras novas (grupo N) que aparecem em 2 pares ou mais, nos 4.000 pares de treino do e-SNLI |
| Vetor de cada palavra | BERT base como veio do pré-treino (sem ajuste na tarefa), última camada, lendo a justificativa inteira; média dos pedaços da palavra e depois média de todas as ocorrências dela. Não exige instalar nem baixar modelo |
| Redução | UMAP para 10 dimensões (15 vizinhos, distância do cosseno, semente 0); `umap-learn` usado só nesta execução (`uv run --with`), sem entrar nas dependências do projeto |
| Agrupamento | HDBSCAN do scikit-learn, grupo mínimo de 15 palavras |
| Por grupo, relatado | número de palavras; em quantos pares aparece; as palavras mais frequentes; como os pares que têm o grupo se dividem entre as 3 classes; acurácia da regressão da 11.6 vendo só as palavras do grupo |

**Leitura combinada antes:**

| Resultado | Conclusão |
|---|---|
| Mais da metade das palavras fica sem grupo, ou saem menos de 5 grupos | O agrupamento não organizou as palavras; nenhuma conclusão sobre molde e conteúdo |
| Caso contrário | A tabela é mostrada ao Pedro. Chamar um grupo de "molde" ou de "conteúdo" é leitura do Claude sobre a lista de palavras, marcada como tal; o número objetivo é a divisão entre classes e a acurácia de cada grupo |

**Limites já sabidos:** o HDBSCAN agrupa por vizinhança de vetor, não por função na frase; UMAP e HDBSCAN dependem
de parâmetros que não foram varridos; vetor médio mistura os sentidos de uma palavra; uma semente.

### 11.8 Levar os grupos de palavras novas ao `[CLS]` (acrescentado em 17/11, antes de codar; etapas com parada)

**Procedência:** hipótese do Pedro (17/11): pegar as palavras novas da justificativa e levá-las ao `[CLS]` num treino
novo. Ele pediu um plano e apontou uma falha das rodadas anteriores: "não pensar antes de implementar como esse
sinal pode ajudar o aluno ou o professor a melhorar as respostas, mexendo no que for necessário na arquitetura". O
mecanismo, o desenho, as etapas e os critérios abaixo são do Claude; o Pedro respondeu "sim pra todos" (o desenho é
o que ele tinha em mente; escrever esta seção; rodar a etapa 1).

**Mecanismo, escrito antes do código:**

- As palavras novas nomeiam o conceito que liga as duas frases: no neutro, o que a hipótese acrescenta e a premissa
  não garante; na contradição, o eixo em que divergem (leitura do Claude da seção 11.7, não testada).
- Para isso ajudar a resposta, o vetor do `[CLS]`, que é o que a cabeça de classificação lê, tem de carregar esse
  conceito. Um alvo que obrigue o `[CLS]` a dizer quais grupos de palavras aparecem na justificativa força o
  encoder a calcular o conceito a partir do par.
- Diferença para o decoder: lá a maior parte da perda vai para palavras gramaticais e copiadas, e o decoder lê
  todos os tokens, então nada obriga a informação a passar pelo `[CLS]`.
- **Armadilha:** o alvo acompanha o rótulo (76,4%, seção 11.6). O modelo pode aprender só "se é neutro, palavras de
  relação", o que não ensina nada além do rótulo.

**Desenho:**

| Item | Escolha |
|---|---|
| Alvo | para cada par, quais dos 29 grupos do HDBSCAN (seção 11.7; as palavras sem grupo ficam de fora) aparecem na justificativa: 29 alvos de sim ou não |
| Onde entra | uma camada linear sobre o mesmo vetor do `[CLS]` que o classificador lê, descartada na inferência |
| Contra a armadilha | a camada tem um viés próprio para cada rótulo certo: o que o rótulo sozinho explica fica no viés, e o gradiente que chega ao encoder é do que depende do par |
| Controle | os grupos de cada par trocados com os de outro par do mesmo rótulo (como as "respostas trocadas" da 11.4): se o trocado ganhar igual, o ganho era só rótulo |
| Gradiente por grupo | medido dentro do treino da etapa 2, sem rodada extra: o cosseno entre o gradiente de cada grupo e o da classificação. O tamanho do gradiente não ordena nada (grupo raro tem perda alta). Ranking só descritivo; escolher grupos e treinar de novo exige ler a nota no conjunto de escolha |

**Aviso registrado:** parece com "decoder fraco com gargalo no `[CLS]`", rejeitado pelo Pedro em 10/11 por ser
suposição sem evidência (`CLAUDE.md`, `## Rejected`). O que há de novo são duas medidas: as palavras novas carregam
70,4% do rótulo sem o grupo de argumentar (11.7), e o aluno aproveitou informação por par (respostas trocadas: −1,7).

**Etapa 1, CPU, sem BERT: o alvo depende do par, ou só do rótulo?**

| Item | Escolha |
|---|---|
| Dados | os 4.000 pares de treino e os grupos de `grupos-palavras-novas-palavras.csv` |
| Para cada um dos 29 grupos | duas regressões logísticas prevendo se o grupo aparece na justificativa do par: (a) vendo só o rótulo certo; (b) vendo o rótulo certo e as palavras do par (presença de palavra) |
| Nota | área sob a curva ROC em validação cruzada de 5 partes (0,5 = acaso; 1,0 = perfeito) |

| Resultado | Conclusão |
|---|---|
| A média dos 29 grupos sobe menos de 0,02 de (a) para (b) | O alvo é o rótulo disfarçado. **Parada: a etapa 2 não roda** |
| Sobe 0,02 ou mais | O alvo depende do par além do rótulo; a etapa 2 pode rodar. **Não prova utilidade:** prever o assunto do par (par sobre cães, grupo de animais) também faz a nota subir |

**Etapa 2, GPU, cerca de 20 minutos, só se a etapa 1 passar:** BERT small, 4.000 pares, 5 sementes, seis braços: sem
nada, com a cabeça de grupos, com os grupos trocados; e os mesmos três com as respostas do professor A. Peso 1,0.
Critério da 11.5: 0,5 ponto ou mais sobre o braço de referência (sem nada, ou "respostas") nas 5 sementes no
conjunto de escolha, com o dev confirmando; candidato roda 10 sementes novas e só conta se o intervalo das 15 não
cruzar o zero; e precisa ficar 0,5 ponto acima do controle trocado para o ganho ser do par e não do rótulo.

**Etapa 3, só se a etapa 2 passar:** treinar o BERT base com a mesma cabeça e ver se ele próprio melhora; se
melhorar, usá-lo como professor na sequência da 11.5. Um professor que **lê** a justificativa fica de fora: ela
entrega 94,7% do rótulo, e a 11.3 mostrou que professor que já sabe a resposta não passa nada pelas respostas.

**Limites já sabidos:** grupos de uma única rodada de UMAP e HDBSCAN; um gerador (Qwen 35B, prompt F); uma tarefa;
4.000 pares; o viés por rótulo tira o efeito médio do rótulo, não as combinações de rótulo com assunto.

**Etapa 1 rodada em 17/11:** média dos 29 grupos 0,595 (só rótulo) para 0,753 (rótulo e par): passa na regra de
parada. "Só o par" dá 0,729: quase tudo é o assunto do par (`leitura-grade.md`, "Etapa 1 da seção 11.8").

**Decisão do Pedro para a etapa 2 (17/11), antes de codar:** "acho que vale rodar (e as duas já que o custo é
baixo), mas tirar um baseline nesses 1300 pares antes, e depois comparar o resultado com ele, e não com o score
geral do modelo". Consequências no desenho, escritas pelo Claude e **a confirmar por ele**:

| Item | Escolha |
|---|---|
| Dois alvos | (T) todos os 29 grupos; (R) só os grupos em que o rótulo acrescenta 0,04 ou mais de ROC ao que as palavras do par já dão na etapa 1 |
| Grupos de (R), pela regra de 0,04 | 21 lazer e emoções (+0,075), 2 "different, distinct" (+0,068), 3 relações entre pessoas (+0,065), 14 eventos (+0,052), 20 "active, passive, quickly" (+0,047), 16 fotografia (+0,045). **Correção:** a lista dada ao Pedro em conversa incluía "gênero e idade" (+0,037, fica de fora pela regra) e omitia o grupo 20 |
| Onde se mede | o conjunto de escolha tem justificativa do Qwen (vem do mesmo lote), o dev não. "Os pares dos grupos" = pares do conjunto de escolha cuja justificativa tem alguma palavra dos grupos de (R), pela tabela palavra -> grupo montada no treino. O dev continua só como nota geral |
| Baseline antes | os braços "sem nada" e "respostas" rodam primeiro, 5 sementes, gravando acerto par a par; deles sai a acurácia nesses pares e a variação entre sementes nesse recorte |
| Critério | escrito **depois** do baseline e **antes** dos braços com a cabeça de grupos, usando a variação medida no recorte (o 0,5 ponto da 11.5 valia para 4.000 pares; o recorte é cerca de um terço disso) |
| Também relatado | a mesma diferença nos pares **fora** do recorte, para ver se o que ganha de um lado perde do outro; e a nota geral |
| Braços depois do baseline | cabeça com alvo (T), cabeça com alvo (R), e cada uma com os grupos trocados dentro do rótulo; os quatro com e sem as respostas do professor A |

**Rediscussão com o Pedro (17/11, noite), antes de codar. O que ele decidiu:**

| Ponto | Decisão do Pedro |
|---|---|
| Alvo restrito (R) | "Seis mais gênero e idade": grupos 21, 2, 3, 14, 20, 16 e 4. Ele perguntou se valia descer a regra para 0,03 ou 0,035; medido com 5 divisões da validação cruzada, os dois limiares dão a mesma lista (os seis mais 4 e 12), o grupo 4 fica entre +0,033 e +0,039 em todas e o 12 (limpeza e conserto) só passa de 0,031 numa delas. O grupo 12 fica de fora |
| Tamanho do recorte | com os seis grupos, 1.007 pares no treino e 1.014 no conjunto de escolha; com os oito, 1.297 e 1.292 (era o "1300" dele). Com os sete: contado ao ler o baseline |
| Dev | "concordo com (b)": as justificativas do dev (9.842 pares, 3h20 a 4h30 de GPU pela velocidade de 27/10) só são geradas se algum braço passar no conjunto de escolha |
| Braços | "sim, todos os 10": os 2 do baseline e os 8 com a cabeça de grupos |
| Baseline | "pode tirar esse baseline": braços "sem nada" e "respostas", 5 sementes, acerto gravado par a par no conjunto de escolha e no dev (`medir_grupos_cls.py`, saída `grupos-cls-acertos-esnli-4000.csv`; leitura por `medir_recorte.py`) |

**O que o baseline tem de entregar, escrito antes de rodar:** para cada braço, a acurácia no recorte, fora dele e
geral, por semente; o desvio entre as 5 sementes em cada um; e a diferença "respostas" menos "sem nada" no recorte,
por semente. O critério dos braços com a cabeça é escrito a partir desses números, **depois** do baseline e **antes**
de qualquer braço com a cabeça rodar. **Depois de ler o baseline de 5 sementes (ruído de ±0,64 ponto no recorte), o
Pedro escolheu "Mais sementes antes"; o número é escolha do Claude: sementes 6 a 15 nos dois braços, fechando 15,
como na 11.5.**

**Critério dos braços com a cabeça de grupos (17/11, noite; escrito depois do baseline de 15 sementes e antes de
qualquer braço com a cabeça existir em código). O Pedro escolheu "5 e depois 10"; os números vêm do baseline:**

| Item | Regra |
|---|---|
| Onde se lê | o recorte: os 1.249 pares do conjunto de escolha com palavra dos sete grupos na justificativa do Qwen |
| Referência | "sem nada" para os braços sem professor; "respostas" para os braços com as respostas do professor A. As 15 sementes das duas já estão em `grupos-cls-acertos-esnli-4000.csv` |
| Primeira rodada | 8 braços, sementes 1 a 5 |
| Vira candidato | o braço com a cabeça cuja média, semente a semente, fica mais de 0,64 ponto acima da referência **e** mais de 0,64 ponto acima do seu controle com grupos trocados (0,64 = metade do intervalo de 95% de uma diferença entre braços com 5 sementes, medida no baseline) |
| Candidato | roda as sementes 6 a 15, ele e o seu controle trocado; só conta se, com as 15, o intervalo de 95% das duas diferenças não cruzar o zero |
| Também relatado, sem decidir | a mesma diferença fora do recorte e no geral; o dev como nota geral |
| Nenhum candidato | nulo; a etapa 3 não roda e as justificativas do dev não são geradas |

**Exceção ao critério, decidida pelo Pedro em 18/11 depois de ver as 5 sementes ("sim, roda as 10 sementes"):** o
braço dos sete grupos sem professor não virou candidato (+0,14 sobre "sem nada", +0,29 sobre o controle trocado,
linha em 0,64), mas é o único positivo nas duas comparações. Rodam as sementes 6 a 15 dele e do controle trocado.
Regra de leitura, escrita antes de rodar e igual à do candidato: com as 15 sementes, só conta se o intervalo de 95%
das **duas** diferenças (sobre "sem nada" e sobre o controle trocado) não cruzar o zero, no recorte. Fica declarado
que o braço foi escolhido depois de olhar oito comparações, e que os dois testes de 18/11 mostraram o alvo de 29
grupos já presente no `[CLS]`.

**Mudanças no código em relação ao desenho, antes de rodar (17/11, noite; o Pedro disse "Pode escrever" e pediu o
brute-test antes):** (1) a auditoria de treino mostrou que o viés por rótulo, nascendo em zero e treinado na taxa
das cabeças, não sairia do lugar; ele passa a nascer no logit da taxa de cada grupo em cada rótulo, calculada nos
alvos do próprio braço (escolha do Claude para cumprir o item "Contra a armadilha"). (2) O cosseno do gradiente é
medido antes e depois do treino, não em três momentos. (3) O sorteio do controle trocado é um só para todas as
sementes; no alvo restrito, 51% dos pares ficam com a linha igual, porque 69% não têm nenhum dos sete grupos
(`docs/claude/brute-test-grupos-cls.md`).

Limite já sabido: o recorte é definido pelo que o Qwen escreveu (o par entra
se a justificativa dele tem palavra dos sete grupos), então o resultado vale para "pares em que o Qwen citou esses
conceitos".

### 11.9 Os pares difíceis no dev: o padrão do olhar exploratório se repete? (acrescentado em 18/11, antes de ler qualquer número do dev por subconjunto)

**Procedência:** pedido do Pedro em 18/11 ("escreve o critério e lê os pares no dev"). O olhar exploratório de 18/11
(`leitura-grade.md`) viu, no conjunto de escolha, o ganho do braço dos sete grupos concentrado nos pares difíceis
(+0,26 ponto em 782 pares) e na contradição (+0,20 em 1.313), em 24 comparações sem critério prévio. O dev não
entrou naquele olhar: dele só foi lida a nota geral (74,04% com a cabeça, 73,99% com o controle, 73,98% sem nada).
Esta seção é a única leitura confirmatória; **é uma exceção à regra de 17/11** ("dev só se algum braço passar"),
decidida pelo Pedro. Nenhum treino novo: os acertos par a par do dev das 15 sementes já estão em
`grupos-cls-acertos-esnli-4000.csv` (conferido: `none`, `answers`, `head_cut` e `head_cut_swapped`, sementes 1 a
15, 9.842 pares).

| Item | Regra |
|---|---|
| Onde se lê | o dev do e-SNLI (9.842 pares), que não escolheu nada no treino nem entrou no olhar exploratório |
| Dificuldade de um par | em quantos dos 15 alunos do braço "respostas" ele é acertado **no dev** (mesma definição do olhar exploratório; o braço "respostas" não é nenhum dos comparados) |
| Faixas | as mesmas: difíceis 0 a 2, médios 3 a 12, fáceis 13 a 15 |
| Comparações | sete grupos sem professor (`head_cut`) menos "sem nada" (`none`), e menos o controle trocado (`head_cut_swapped`); semente a semente, 15 sementes, intervalo de 95% pela t |
| Teste principal | os pares difíceis. **Passa** se o intervalo das **duas** diferenças ficar inteiro acima de zero |
| Teste secundário | os pares de rótulo contradição, mesma regra. Sozinho não sustenta "ajuda nos difíceis" |
| Só descrito, sem decidir | fáceis, médios, entailment, neutral e o geral |
| Fora | "contradição dentro do recorte": o recorte depende da justificativa do Qwen, que não existe para o dev |

**Leitura combinada antes:**

- **Principal passa:** o padrão se repete em dado independente. Sustenta "neste braço, neste aluno, o pequeno ganho
  fica nos pares que o aluno com as respostas quase nunca acerta", com o tamanho que der. Não sustenta "a
  justificativa ajuda rótulos difíceis" em geral (um alvo, um aluno, um conjunto), nem diz por quê.
- **Principal não passa:** o olhar exploratório fica registrado como acaso de 24 comparações e a pergunta fecha
  para este braço. Não se troca a faixa, o braço de dificuldade nem o subconjunto para procurar de novo.
- **Só o secundário passa:** fica como observação sobre a contradição, sem conclusão sobre dificuldade.

**Limites já sabidos:** (1) se o efeito real for o +0,26 do conjunto de escolha, a conta de pares diz que o dev
tem cerca de 2,5 vezes mais pares e o intervalo deve ser mais estreito que o ±0,21 de lá, mas o quanto não foi
medido; um intervalo que cruza o zero com média positiva não prova ausência. (2) "Difícil" inclui pares de rótulo
discutível, que nenhum treino deveria acertar; não foi medido quantos. (3) O braço foi escolhido depois de olhar
oito comparações no conjunto de escolha; o dev não participou dessa escolha.
