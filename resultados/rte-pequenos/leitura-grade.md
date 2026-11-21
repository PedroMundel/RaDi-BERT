# Encoders pequenos no RTE: marcas e decoder (10/11/2026)

**Procedência:** números calculados pelo Claude a partir dos `resultados.csv` das pastas citadas (cópias em
`<pasta>/pc/`). Ninguém além do Claude leu esta leitura. Ideia do experimento: Pedro (10/11, "trocar o BERT por um
modelo bem menos capaz").

## O que foi rodado

Mesmo treino das grades anteriores (Tabela 4 do Agrawal 2025: taxa 5e-5, 8 épocas, lote 32, aquecimento `prop`),
trocando só o encoder:

- **small** = `google/bert_uncased_L-4_H-512_A-8` (4 camadas, 512 dimensões, ~29 M de parâmetros);
- **tiny** = `google/bert_uncased_L-2_H-128_A-2` (2 camadas, 128 dimensões, ~4 M).

Os dois têm o vocabulário e os ids do BERT base (conferido). Com o decoder T5 base, uma camada linear (ponte) leva
os vetores do encoder de 512 ou 128 para 768 dimensões. Teste = dev do RTE (277 pares), lido uma vez no fim.
Diferenças pareadas por semente, intervalo t de 95%.

| Pasta | O quê | Treinos |
|---|---|---|
| `resultados/rte-marcas-small/` | marcas no small, sementes 1 a 15 | 45 |
| `resultados/rte-marcas-tiny/` | marcas no tiny, sementes 1 a 5 | 15 |
| `resultados/rte-marcas-small-1000/` | marcas no small com 1.000 pares de treino, sementes 1 a 5 | 15 |
| `resultados/rte-small/`, `resultados/rte-tiny/` | BERT sozinho e BERT + decoder, sementes 1 a 5 | 10 + 10 |

## Decoder: nulo nos dois tamanhos

| ROC-AUC | BERT sozinho | com decoder | diferença (IC 95%) | vence em |
|---|---|---|---|---|
| small | 0,682 | 0,678 | −0,004 (−0,020 a +0,012) | 1/5 |
| tiny | 0,622 | 0,612 | −0,010 (−0,029 a +0,009) | 1/5 |

- No BERT base o decoder piorava (−0,028). No encoder pequeno a queda some, mas ganho não há.
- A ponte não explica o nulo: a L_aux da última época é 3,3 no small e 3,7 no tiny, contra 3,45 no BERT base. O
  decoder aprendeu a ler o encoder pequeno tão bem quanto lia o grande.

## Marcas: o ganho das 5 primeiras sementes não se confirmou

**Small, treino inteiro (2.470 pares), ROC-AUC no dev:**

| Sementes | sem marcas | real | aleatória | real − sem marcas | real − aleatória |
|---|---|---|---|---|---|
| 1 a 5 (primeira rodada) | 0,674 | 0,691 | 0,641 | +0,017 (+0,008 a +0,025), 5/5 | +0,049 (+0,030 a +0,069), 5/5 |
| **6 a 15 (confirmação)** | 0,677 | 0,680 | 0,632 | **+0,002 (−0,009 a +0,014), 6/10** | **+0,048 (+0,038 a +0,058), 10/10** |
| 1 a 15 (todas) | 0,676 | 0,683 | 0,635 | +0,007 (−0,001 a +0,015), 11/15 | +0,048 (+0,041 a +0,056), 15/15 |

Em acurácia, com as 15 sementes: real − sem marcas +0,007 (−0,007 a +0,021), 8/15.

**Small, 1.000 pares de treino (5 sementes):**

| Teste | sem marcas | real | aleatória | real − sem marcas | real − aleatória |
|---|---|---|---|---|---|
| dev (277 pares) | 0,642 | 0,659 | 0,574 | +0,017 (+0,004 a +0,030), 5/5 | +0,086 (+0,073 a +0,098), 5/5 |
| **1.470 pares de treino não usados** | 0,646 | 0,625 | 0,610 | **−0,022 (−0,031 a −0,012), 0/5** | +0,014 (+0,002 a +0,027), 5/5 |

**Tiny (5 sementes):** sem marcas 0,621 · real 0,599 · aleatória 0,574. Real − sem marcas −0,023 (−0,053 a +0,008),
1/5. O baseline está perto do que um modelo sem treino dá; a taxa e as épocas do paper são pouco para ele.

## Como ler

1. **A marca real não ganha do BERT pequeno sem marcas.** O +0,017 das sementes 1 a 5 caiu para +0,002 nas dez
   sementes novas. Com 1.000 pares, o dev repete +0,017, mas o teste maior (1.470 pares, intervalo mais estreito) dá
   −0,022 em 5/5. Os dois testes discordam no sinal; o maior é o mais confiável.
2. **A marca real ganha da aleatória sempre.** 15/15 no treino inteiro (+0,048), 5/5 com 1.000 pares nos dois
   testes. O conteúdo da justificativa importa: marcar as palavras que ela copia é melhor que marcar palavras ao
   acaso.
3. **Marcar ao acaso atrapalha** (−0,041, 0/15). Então o item 2 pode ser lido de dois jeitos: a marca real "ajuda",
   ou a perda de atenção custa algo e a marca real só custa menos. Contra o baseline, a segunda leitura é a que os
   números sustentam.
4. **O decoder não chega ao classificador em nenhum tamanho de encoder testado** (base, MS-MARCO, T5, small, tiny).

## Limites

- **O treino na GPU não se repete bit a bit.** O braço `bert` de `rte-small` e o `marks_none` de `rte-marcas-small`
  são o mesmo modelo, com a mesma semente e os mesmos dados, e diferem em até 0,026 de ROC-AUC numa semente (médias
  0,682 e 0,674). Diferença menor que isso entre dois braços, em 5 sementes, não é sinal. Foi o que aconteceu com o
  +0,017.
- Peso da marca (1,0), camada (última) e definição da marca não foram varridos: o dev é o teste.
- Uma tarefa (RTE), um conjunto de justificativas (Qwen 35B, variante FA).
- O vazamento pequeno continua: as expressões de rótulo são calculadas com os 1.470 pares reservados.

## Decisões que ficam com o Pedro

- O que levar ao gate de 11/11: o nulo vem agora com o controle da marca aleatória, a tentativa de repetir o paper e
  uma confirmação em sementes novas que derrubou um falso positivo.
- Se vale varrer o peso da marca ou a camada num conjunto de validação separado (os 1.470 pares permitem isso sem
  tocar no dev).

## Teste fora da distribuição (10/11, 20h): hipótese das marcas encerrada

Plano e regra de parada, escritos antes de rodar: `docs/2026-11-10-plano-teste-fora-da-distribuicao.md`. BERT small
treinado no RTE inteiro, 15 sementes, testado no dev do e-SNLI (9.842 pares; entailment = 1, neutral e contradiction
= 0). Resultados em `resultados/rte-marcas-small-fora/pc/resultados.csv` (45 linhas).

| Teste | sem marcas | real | aleatória | real − sem marcas (IC 95%) | real − aleatória (IC 95%) |
|---|---|---|---|---|---|
| **Fora: ROC-AUC (medida principal)** | 0,759 | 0,754 | 0,712 | **−0,004 (−0,011 a +0,002), 7/15** | +0,042 (+0,036 a +0,049), 15/15 |
| Fora: acurácia | 0,695 | 0,688 | 0,649 | −0,007 (−0,016 a +0,001), 5/15 | +0,039 (+0,026 a +0,051), 15/15 |
| Dentro: ROC-AUC no dev do RTE | 0,676 | 0,683 | 0,635 | +0,007 (−0,001 a +0,016), 11/15 | +0,049 (+0,041 a +0,057), 15/15 |

**Pela regra de parada:** o baseline está em 0,759, longe do piso de 0,55, então o teste informa. O intervalo da
medida principal cruza o zero. **A hipótese das marcas está encerrada**: nenhuma variação nova (peso, camada, outro
conjunto) é rodada depois.

O que o teste acrescenta:

1. Fora da distribuição a marca real também não ganha do treino normal; o sinal da diferença é negativo.
2. O contraste real × aleatória se repete fora (+0,042, 15/15), e marcar ao acaso atrapalha de novo (−0,047, 0/15).
3. O dev do RTE desta rodada repete o das 15 sementes anteriores (+0,007 nas duas), então as duas rodadas concordam.
4. O modelo treinado no RTE acerta mais no e-SNLI (0,759) do que no próprio RTE (0,676): o e-SNLI é mais fácil.
   Como teste de robustez ele é brando; um conjunto feito para derrubar atalhos (HANS) seria mais duro, mas a regra
   de parada fecha essa porta.

## Medida de redundância (10/11, 21h): o modelo sem marcas NÃO olha para as palavras marcadas

Pergunta: o empate das marcas acontece porque o BERT small, treinando só com os rótulos, já põe a atenção do `[CLS]`
nas palavras que a justificativa copia? Script `resultados/rte-pequenos/medir_atencao.py`, números em
`atencao.csv` (128 linhas). Mesmo recorte do `--pares 1000`: 1.000 pares treinam, a medida abaixo é nos 1.470 pares
nunca treinados, 5 sementes por braço. "Massa" = parte da atenção do `[CLS]` (média das cabeças) que cai nas
posições marcadas, média dos pares.

| Última camada (a que a perda de marca usa) | Massa nas palavras marcadas |
|---|---|
| Atenção espalhada por igual (referência) | 0,193 |
| Modelo antes de qualquer treino | 0,314 |
| **Treinado sem marcas** | **0,285** (0,240 a 0,310 entre sementes) |
| Treinado com marca aleatória | 0,261 |
| **Treinado com marca real** | **0,805** (0,803 a 0,807) |

Nas camadas 1 a 3 os quatro modelos são quase iguais (na 3: 0,36 a 0,42 nas palavras marcadas, contra 0,19 da
referência).

Como ler:

1. **A hipótese da redundância não se sustenta.** Treinar sem marcas não leva a atenção da última camada para as
   palavras marcadas: ela fica em 0,285, perto do que já era antes do treino (0,314).
2. **A marca real funciona como treino de atenção.** Em pares que o modelo nunca viu, 80% da atenção do `[CLS]` vai
   para as palavras que a justificativa copiaria. O modelo aprendeu a prever quais são. Com a marca aleatória isso
   não acontece (nos pares de treino ele decora as posições sorteadas, 0,52; nos novos volta a 0,21).
3. **E mesmo assim a nota não muda.** Mudar para onde o `[CLS]` olha na última camada, de 0,29 para 0,80, não
   melhora a classificação dentro nem fora da distribuição. A atenção do `[CLS]` na última camada não é o que
   limita o modelo nesta tarefa.

Limites: a medida é da atenção do `[CLS]` de uma camada; o modelo pode levar a informação por outros caminhos (na
camada 3 a massa já é 0,41 em todos os braços). As marcas reais excluem palavras gramaticais e as aleatórias não,
então "real maior que aleatória" na massa mistura as duas coisas. Uma tarefa, um modelo.

Consequência para trocar de tarefa: esta medida não dá o motivo que se procurava. O argumento "numa tarefa de texto
longo o modelo não acharia as palavras sozinho" pressupunha que no RTE ele achava; ele não acha, a marca o faz achar,
e não adianta.

## Teste do destaque (10/11, 22h): passa no critério escrito antes

Critério e desenho: `docs/2026-11-10-plano-teste-fora-da-distribuicao.md`, seção 8, escrita antes de rodar. Script
`resultados/rte-pequenos/medir_destaque.py`, números em `destaque.csv` (20 linhas). Pergunta: as palavras em que o
`[CLS]` do BERT small mais presta atenção coincidem com as que a justificativa do LLM copia, em pares nunca
treinados, e melhor do que uma regra sem treino? 1.469 pares com marca (dos 1.470 reservados), 1.000 pares de
treino, 5 sementes por braço. AP = precisão média por par, média dos pares (1,0 = as palavras marcadas vêm todas no
topo da lista).

| Quem dá a nota a cada token | AP (medida principal) | AUROC |
|---|---|---|
| **BERT small treinado com marca real** | **0,724** (0,722 a 0,727 entre sementes) | **0,902** |
| Melhor regra sem treino: palavra de conteúdo que aparece nas duas frases | 0,555 | 0,761 |
| Regra: toda palavra de conteúdo | 0,388 | 0,799 |
| Regra: palavra de conteúdo da hipótese | 0,394 | 0,667 |
| BERT small antes do treino | 0,446 | 0,686 |
| BERT small treinado sem marcas | 0,361 (0,314 a 0,393) | 0,626 |
| BERT small treinado com marca aleatória | 0,309 | 0,561 |
| Nota ao acaso | 0,260 | 0,500 |

**Pelo critério:** a marca real supera a melhor regra em 0,17 de AP nas 5 sementes (o critério pedia 0,05) e supera
o modelo sem marcas (0,361). **O destaque aprendido vale algo**: não é reproduzido por regra simples de palavras.

O que isso diz e o que não diz:

1. Um encoder de 29 M de parâmetros aprende, com 1.000 pares, a apontar em pares novos as palavras que um LLM de
   35 B usaria para justificar o rótulo. O destaque sai da atenção que o modelo já calcula para classificar: custo
   zero a mais na inferência.
2. Treinar só para classificar não produz esse destaque (0,361, abaixo até do modelo antes do treino, 0,446).
3. **Não diz que o destaque é útil para uma pessoa**: o gabarito é o que o LLM copia, não o que um humano marcaria.
4. **Não diz que o destaque explica a decisão do modelo**: mudar a atenção não mudou a nota (seção anterior).
5. **A classificação nesta configuração (1.000 pares) não saiu de graça**: nos mesmos 1.470 pares a marca real
   perdeu 0,022 de ROC-AUC para o treino sem marcas (0/5). Com o treino inteiro há empate (+0,007 no dev, −0,004
   fora). "Sem perder acerto" só vale, por enquanto, para o treino inteiro, onde o destaque não foi medido.
6. Faltam duas referências mais fortes: uma cabeça de classificação por token treinada nas mesmas marcas (o jeito
   direto de aprender o destaque) e regras combinadas. O critério comparou só com as quatro regras listadas.

## Destaque e nota na mesma rodada, com 2.000 pares de treino (10/11, 22h30)

Fecha a lacuna do item 5 acima. `medir_destaque.py --pares 2000`: treina nos 2.000 primeiros pares do embaralhamento
fixo, mede o destaque nos 470 restantes e a classificação no dev do RTE e nesses 470. 5 sementes por braço.
Números em `destaque-2000.csv`.

| Braço | AP do destaque (470 pares) | ROC-AUC no dev | ROC-AUC nos 470 pares |
|---|---|---|---|
| **Marca real** | **0,731** (0,728 a 0,734) | 0,691 | 0,658 |
| Sem marcas | 0,377 | 0,681 | 0,658 |
| Marca aleatória | 0,320 | 0,636 | 0,626 |
| Melhor regra sem treino | 0,558 | não classifica | não classifica |

Classificação, marca real − sem marcas: +0,010 no dev (IC −0,006 a +0,027), 4/5; −0,000 nos 470 pares (IC −0,018 a
+0,018), 2/5.

Como ler: com 2.000 pares de treino o destaque se mantém (0,731, contra 0,724 com 1.000) e **a classificação empata
com o treino normal nos dois testes**. O custo de 0,022 visto com 1.000 pares não aparece aqui. Com 5 sementes e 470
pares o intervalo é largo (±0,018): cabe um custo pequeno que esta rodada não enxerga.

Exemplos: `destaque-exemplos.html` (gerado por `pagina_destaque.py`), os 20 primeiros dos 470 pares, semente 1. Nesses
20 pares o LLM marcou 193 palavras; das apontadas pelo modelo, coincidem 131 (68%) com marca real e 62 (32%) sem
marcas. Ninguém além do Claude leu os exemplos ainda.

## Cabeça por token como referência do destaque (10/11, 23h30)

Fecha a lacuna do item 6 da seção do destaque. Critério escrito antes: plano, seção 9. Braço novo: BERT small com uma
camada linear sobre o vetor de cada token, treinada direto contra as marcas reais (`RationaleBert.with_token_head`).
`medir_destaque.py --pares 2000 --cabeca`, mesma rodada para todos os braços, 5 sementes, 470 pares de teste.
Números em `destaque-2000-cabeca.csv` (25 linhas).

| Braço | AP do destaque | AUROC | ROC-AUC no dev | ROC-AUC nos 470 pares |
|---|---|---|---|---|
| **Cabeça por token** | **0,748** (0,744 a 0,751) | 0,920 | 0,670 | 0,669 |
| **Marca real (atenção do `[CLS]`)** | **0,731** (0,728 a 0,733) | 0,901 | 0,691 | 0,659 |
| Sem marcas | 0,377 | 0,617 | 0,681 | 0,659 |
| Marca aleatória | 0,320 | 0,586 | 0,637 | 0,626 |
| Melhor regra sem treino | 0,558 | 0,762 | não classifica | não classifica |

Cabeça − atenção, AP: +0,017 (IC +0,013 a +0,020), 5/5.

**Pelo critério** (a cabeça precisava superar a atenção em 0,05): a diferença é 0,017. **A atenção entrega um
destaque praticamente tão bom quanto o de uma cabeça treinada só para isso.** A cabeça é um pouco melhor, de forma
consistente, mas abaixo do limite combinado.

Classificação: cabeça − sem marcas dá −0,011 no dev (IC −0,027 a +0,005) e +0,010 nos 470 pares (IC −0,009 a
+0,029). Sinais opostos, dentro do ruído: nada a ler, e esta rodada não buscava nota.

Os braços repetidos reproduzem a rodada anterior de 2.000 pares (marca real 0,731 nas duas; sem marcas 0,377 nas
duas).

Limites: peso da perda (1,0) e taxa (5e-5, a do paper) não varridos, para os dois mecanismos; a cabeça parte de uma
camada nova e pode render mais com outra taxa. Um conjunto, um modelo, 5 sementes.

## Intervenção na atenção por camada, sem treino novo (16/11): critério da seção 10.1 do plano

**Procedência:** ablação pedida pelo Pedro (16/11). Desenho e critério escritos antes de rodar (plano, seção 10.1).
Script `medir_intervencao.py`, saída `intervencao-2000.csv` (1.760 linhas). BERT small, 2.000 pares de treino, 5
sementes, 470 pares nunca treinados (todos têm marca; 11,1 posições marcadas por par em 68,2, fração 0,196).
ROC-AUC sem intervenção nesses 470 pares: 0,658 nos dois braços.

**Conferido:** a rodada é a do código com MD5 igual nas duas máquinas; na camada 4, cortar só a linha do `[CLS]` e
cortar todas as linhas dão o mesmo número (0,089 e 0,089; 0,331 e 0,331), como tem de ser, porque a cabeça só lê o
`[CLS]`: o corte funciona na GPU. **Não conferido:** nenhum método foi comparado com a literatura; nenhum controle
separa "palavra da justificativa" de "palavra que aparece nas duas frases".

### Modelo sem marcas, linha do `[CLS]`, operação bloquear (medida principal)

Fração dos pares em que a classe prevista muda. "Acaso" = maior diferença entre os dois sorteios de conteúdo em
qualquer semente.

| Camadas | Marca real | Sorteio qualquer | Conteúdo (1) | Conteúdo (2) | Real − conteúdo | Sementes no mesmo sinal | Acaso | Critério |
|---|---|---|---|---|---|---|---|---|
| 1 | 0,006 | 0,005 | 0,008 | 0,006 | −0,002 | 4 de 5 | 0,006 | não se distingue (média abaixo de 1%) |
| 2 | 0,028 | 0,019 | 0,023 | 0,026 | +0,005 | 4 de 5 | 0,009 | não se distingue |
| 3 | 0,185 | 0,045 | 0,069 | 0,071 | +0,116 | 5 de 5 | 0,019 | **depende** |
| 4 | 0,089 | 0,029 | 0,037 | 0,040 | +0,051 | 5 de 5 | 0,015 | **depende** |
| 1 e 2 | 0,032 | 0,020 | 0,023 | 0,026 | +0,009 | 4 de 5 | 0,011 | não se distingue |
| 1 e 3 | 0,195 | 0,043 | 0,074 | 0,073 | +0,121 | 5 de 5 | 0,013 | **depende** |
| 1 e 4 | 0,092 | 0,030 | 0,043 | 0,042 | +0,049 | 5 de 5 | 0,021 | **depende** |
| 2 e 3 | 0,204 | 0,053 | 0,079 | 0,080 | +0,125 | 5 de 5 | 0,026 | **depende** |
| 2 e 4 | 0,097 | 0,038 | 0,050 | 0,053 | +0,047 | 5 de 5 | 0,017 | **depende** |
| 3 e 4 | 0,297 | 0,060 | 0,103 | 0,105 | +0,194 | 5 de 5 | 0,013 | **depende** |
| 1, 2, 3 e 4 | 0,320 | 0,068 | 0,122 | 0,123 | +0,197 | 5 de 5 | 0,017 | **depende** |

O ROC-AUC acompanha: bloquear a marca real na camada 3 leva de 0,658 para 0,607 (conteúdo sorteado: 0,650); nas
camadas 3 e 4 juntas, para 0,568 (conteúdo: 0,637).

### O resto, em resumo (tudo em `intervencao-2000.csv`)

- **Só estas, linha do `[CLS]`, sem marcas:** deixar o `[CLS]` olhar só para as palavras da justificativa muda menos
  decisões do que deixá-lo olhar só para palavras de conteúdo sorteadas na camada 3 (0,116 contra 0,163; 5 de 5) e
  nas combinações com a 3. Na camada 4 sozinha não se distingue (0,116 contra 0,124).
- **Todas as linhas, sem marcas:** impedir todos os tokens de olhar para as palavras da justificativa muda 40% das
  decisões na camada 1 e 42% na 2 (conteúdo sorteado: 23%), contra 0,6% e 2,8% quando só o `[CLS]` é impedido. Nas
  camadas 1 e 2 o que pesa é a atenção entre os tokens, não a do `[CLS]`.
- **Modelo treinado com a marca real na camada 4:** a dependência muda de lugar. Bloquear a marca real na camada 4
  muda 33,1% das decisões (sem marcas: 8,9%) e na camada 3 muda 8,4% (sem marcas: 18,5%). O ROC-AUC sem intervenção
  é o mesmo nos dois braços (0,658).

### O que isso permite dizer e o que não permite

1. No BERT small treinado sem marcas, a decisão depende da atenção do `[CLS]` às posições marcadas nas camadas 3 e
   4, mais do que da atenção ao mesmo número de palavras de conteúdo sorteadas; nas camadas 1 e 2 a linha do `[CLS]`
   quase não pesa. Vale para este modelo, esta tarefa, estes 470 pares.
2. Treinar com a marca na camada 4 muda onde a decisão depende da atenção do `[CLS]`, sem mudar a nota. A frase de
   10/11, "a atenção muda, a decisão não", fica mais estreita ainda: a nota não muda, mas o caminho da decisão muda.
3. **Não permite dizer que o modelo usa "a evidência que a justificativa aponta".** As posições marcadas diferem do
   sorteio de conteúdo em mais do que virem da justificativa: 58,6% delas estão em palavra que aparece nas duas
   frases (sorteio de conteúdo: 34,4%) e 39,9% estão na hipótese (sorteio: 23,7%). Um modelo que decide por
   sobreposição de palavras entre as frases daria o mesmo quadro. Falta um controle sorteado só entre palavras
   presentes nas duas frases.

**Limites:** o modelo é fraco nesses pares (ROC-AUC 0,658), então muitas decisões estão perto de 0,5 e mudam com
pouco. O sorteio de conteúdo coincide com a marca real em 40% das posições, o que encolhe a diferença medida. Cortar
atenção cria uma entrada que o modelo nunca viu. Um modelo, uma tarefa, 5 sementes.

**Tempo:** cada treino levou cerca de 23 s na 5060 (504 passos).

## Treino com a marca cobrada em outras camadas (16/11): nulo pelo critério da seção 10.2 do plano

**Procedência:** ablação pedida pelo Pedro (16/11), 11 combinações de camadas a pedido dele ("As 11"). Desenho e
critério escritos antes de rodar (plano, seção 10.2). Script `medir_camadas.py`, saída `camadas-2000.csv` (115
treinos: 5 sem marcas; marca real e marca sorteada em cada uma das 11 combinações, 5 sementes cada). BERT small,
2.000 pares de treino. Auditoria de treino antes de lançar: sem falha. Rodada de 46 minutos, sem queda.

**Conferido:** 115 linhas, 5 por braço; código com MD5 igual nas duas máquinas; critério aplicado como escrito.
**Não conferido:** nenhuma comparação com a literatura; o peso da marca (1,0) não foi variado.

**Como ler a tabela:** cada linha é um jeito de treinar, dizendo em que camadas a atenção do `[CLS]` foi puxada para
as palavras que a justificativa copia. A nota é o ROC-AUC de classificação (0,5 = chute, 1,0 = perfeito, maior é
melhor), média de 5 sementes, em dois conjuntos: o dev do RTE (277 pares) e os 470 pares de treino nunca usados. As
colunas "diferença" são a nota desse treino menos a nota do modelo treinado sem marcas (dev 0,681; 470 pares 0,659):
positivo quer dizer que a marca ajudou. A última coluna é a mesma diferença quando as palavras marcadas são
sorteadas em vez de vir da justificativa.

| Camadas em que a marca foi cobrada | Nota no dev, marca real | Diferença para sem marcas, no dev | Nota nos 470 pares, marca real | Diferença para sem marcas, nos 470 | Diferença da marca sorteada para sem marcas, nos 470 |
|---|---|---|---|---|---|
| 1 | 0,678 | −0,002 | 0,659 | +0,001 | 0,000 |
| 2 | 0,676 | −0,004 | 0,651 | −0,007 | −0,001 |
| 3 | 0,682 | +0,002 | 0,666 | +0,007 | −0,026 |
| 4 (a que já existia) | 0,692 | +0,011 | 0,658 | −0,001 | −0,033 |
| 1 e 2 | 0,666 | −0,014 | 0,642 | −0,016 | 0,000 |
| 1 e 3 | 0,678 | −0,002 | 0,664 | +0,005 | −0,025 |
| 1 e 4 | 0,685 | +0,004 | 0,662 | +0,003 | −0,033 |
| 2 e 3 | 0,687 | +0,006 | 0,651 | −0,008 | −0,030 |
| 2 e 4 | 0,681 | +0,001 | 0,641 | −0,017 | −0,035 |
| 3 e 4 | 0,685 | +0,005 | 0,659 | 0,000 | −0,060 |
| 1, 2, 3 e 4 | 0,682 | +0,001 | 0,640 | −0,019 | −0,062 |

**Critério (escrito antes):** candidato é o braço de marca real que supera o sem marcas **e** a marca sorteada da
mesma camada em 0,03 ou mais, nos dois conjuntos. **Nenhum braço chega perto contra o modelo sem marcas:** a maior
diferença é +0,011 no dev (camada 4) e +0,007 nos 470 pares (camada 3). **Resultado: nulo.** Pela regra combinada, a
camada volta para a regra de parada: nenhuma variação nova de camada.

**O que mais os números mostram:**

- A marca **sorteada** derruba a nota quando é cobrada na camada 3 ou na 4 (de −0,025 a −0,062 nos 470 pares) e não
  derruba nas camadas 1 e 2 (0,000 e −0,001). Bate com a intervenção sem treino: é nas camadas 3 e 4 que o olhar do
  `[CLS]` pesa na decisão; nas camadas 1 e 2, puxá-lo para qualquer lugar não muda a nota.
- A marca **real** nas camadas 3 e 4 não derruba e não levanta: forçar o `[CLS]` a olhar para as palavras da
  justificativa onde isso importa deixa a nota onde estava.

**Limites:** um nulo com este tamanho diz "não há ganho de 0,03 ou mais", não "não há efeito": ganho menor que o
ruído entre rodadas (até 0,026) não é visível com 5 sementes. Peso da marca fixo em 1,0; com mais de uma camada a
perda é a soma das camadas. O dev do RTE já foi olhado muitas vezes. Um modelo, uma tarefa.

## O mesmo treino no e-SNLI (16/11): a marca não melhora em nenhuma combinação de camadas

**Procedência:** pedido do Pedro (16/11): "testa esse treino que a gente fez agora com o small mas no e-snli como
dataset pra eu ver uma coisa". **Nenhum critério foi escrito antes desta rodada**: é observação, não teste com
regra de decisão. Script `medir_camadas.py --tarefa esnli`, saída `camadas-esnli-4000.csv` (115 treinos, 5 sementes
por braço). BERT small, 4.000 pares de treino do e-SNLI com as justificativas F do Qwen 35B, 1.000 passos por
treino. Auditoria de treino antes de lançar: sem falha. Rodada de 1h24, sem queda.

**Conferido:** 115 linhas, 5 por braço; código com MD5 igual e o mesmo sorteio de 4.000 pares nas duas máquinas.
**Não conferido:** o BERT base não foi rodado de novo hoje (o número dele é da rodada de 10/11).

**O small contra o base, sem marcas:** acurácia no dev do e-SNLI (9.842 pares, 3 classes; chute = 33%) de 73,9%
no small (sementes entre 73,4% e 74,4%) contra 79,7% no BERT base (`resultados/esnli-treino/leitura-grade.md`).
Diferença de 5,8 pontos. ROC-AUC 0,890 contra 0,916.

**Como ler a tabela:** cada linha é um jeito de treinar o small, dizendo em que camadas a atenção do `[CLS]` foi
puxada para as palavras que a justificativa copia. As notas são acurácia no dev do e-SNLI, média de 5 sementes,
maior é melhor. A coluna "diferença" é a acurácia desse treino menos a do small treinado sem marcas (73,9%), em
pontos percentuais: negativo quer dizer que a marca atrapalhou. "Sementes em que ganhou" conta em quantas das 5 a
marca real ficou acima do sem marcas. A última coluna é a mesma diferença com palavras sorteadas no lugar das da
justificativa.

| Camadas em que a marca foi cobrada | Acurácia com a marca real | Diferença para sem marcas (pontos) | Sementes em que ganhou | Diferença da marca sorteada para sem marcas (pontos) |
|---|---|---|---|---|
| 1 | 73,9% | 0,0 | 2 de 5 | +0,1 |
| 2 | 73,7% | −0,2 | 1 de 5 | −0,2 |
| 3 | 73,7% | −0,2 | 2 de 5 | −0,6 |
| 4 | 73,7% | −0,2 | 2 de 5 | −0,9 |
| 1 e 2 | 73,7% | −0,2 | 0 de 5 | −0,1 |
| 1 e 3 | 73,8% | −0,1 | 2 de 5 | −0,6 |
| 1 e 4 | 73,6% | −0,3 | 2 de 5 | −0,9 |
| 2 e 3 | 73,5% | −0,4 | 2 de 5 | −0,7 |
| 2 e 4 | 72,8% | −1,1 | 0 de 5 | −1,1 |
| 3 e 4 | 72,6% | −1,3 | 0 de 5 | −2,1 |
| 1, 2, 3 e 4 | 72,0% | −1,9 | 0 de 5 | −2,3 |

**O que os números mostram:**

1. **Nenhuma combinação melhora.** Com uma camada só, a marca real fica a 0,2 ponto ou menos do sem marcas, dentro
   da variação entre sementes (desvio de 0,4 ponto). Nenhum braço ganha em mais de 2 das 5 sementes.
2. **Cobrar em duas camadas que incluem a 4, ou nas quatro, atrapalha:** −1,1 a −1,9 ponto, perdendo nas 5 sementes.
3. **A marca sorteada atrapalha mais que a real nas camadas 3 e 4**, como no RTE, mas a diferença entre as duas é
   pequena (até 0,8 ponto).
4. A distância do small para o BERT base (5,8 pontos) não diminui com a marca em nenhuma camada.

**Limites:** sem critério escrito antes. No e-SNLI o número de marcas acompanha o rótulo (entailment 5,9 por par,
neutro 3,4; aviso da auditoria), então marca contra sem marcas não é comparação limpa; a marca sorteada usa as
mesmas contagens. 104 dos 4.000 pares não têm marca. Peso da marca 1,0, soma das camadas. Um modelo, 5 sementes.

## Destilação da atenção do BERT base no small, e-SNLI (16/11): nulo pelo critério da seção 11 do plano

**Procedência:** ideia do Pedro (16/11: "às vezes a gente deveria estar destilando a atenção do BERT-large"; "vamos
fazer com o base primeiro"). Desenho e critério escritos antes de rodar e confirmados por ele (plano, seção 11).
Método tirado de MiniLM (Wang et al., 2020) e TinyBERT (Jiao et al., 2020), **nível 3** (páginas resumidas, artigos
não lidos). Script `medir_destilacao.py`, saída `destilacao-esnli-4000.csv` (30 alunos: 6 braços, 5 sementes).
Código novo em `src/radibert/rte_destilacao.py`. Auditoria de treino antes de lançar: sem falha. Rodada de 38 min.

**Conferido:** 30 linhas, 5 por braço; código com MD5 igual nas duas máquinas; o braço sem destilação reproduz a
rodada anterior do e-SNLI (73,9%); o critério é o escrito antes. **Não conferido:** nenhum artigo lido inteiro; só
um professor, de uma semente.

**O professor:** BERT base treinado nos mesmos 4.000 pares, 80,2% de acurácia no dev do e-SNLI (ROC-AUC 0,920).
O small sem destilação faz 73,9%: 6,3 pontos abaixo.

**Como ler a tabela:** cada linha é um jeito de treinar o BERT small. A nota é a acurácia no dev do e-SNLI (9.842
pares, 3 classes, chute = 33%), média de 5 sementes, maior é melhor. "Diferença" é a acurácia desse treino menos a
do small sem destilação, em pontos percentuais. "Sementes em que ganhou" conta em quantas das 5 o braço ficou acima
do sem destilação. A última coluna mostra o quanto a atenção (ou a saída) do aluno ainda difere da do professor no
fim do treino: quanto menor, mais o aluno imitou (o piso é cerca de 0,07 por camada, por causa do dropout).

| Jeito de treinar o small | Acurácia | Diferença para sem destilação (pontos) | Sementes em que ganhou | Distância para o professor no fim do treino |
|---|---|---|---|---|
| Sem destilação | 73,9% | — | — | — |
| Imita a atenção da última camada do professor treinado na tarefa | 74,0% | +0,1 | 3 de 5 | 0,19 (1 camada) |
| Imita a atenção de 4 camadas do professor treinado na tarefa | 73,9% | 0,0 | 3 de 5 | 0,59 (soma de 4 camadas) |
| Controle: imita a última camada de um BERT base **não** treinado na tarefa | 73,7% | −0,2 | 1 de 5 | 0,14 (1 camada) |
| Controle: imita 4 camadas de um BERT base **não** treinado na tarefa | 73,1% | −0,8 | 1 de 5 | 0,50 (soma de 4 camadas) |
| Referência: imita as saídas (probabilidades das classes) do professor treinado | 73,9% | 0,0 | 3 de 5 | 0,11 |

**Critério (escrito antes):** ajuda se um braço superar o sem destilação em 1,0 ponto ou mais nas 5 sementes.
**Nenhum braço chega a 0,1 ponto de média. Resultado: nulo neste desenho.**

**O que mais os números mostram:**

1. **O aluno imitou a atenção e a nota não mudou.** A distância para a atenção da última camada do professor cai a
   0,19, perto do piso de 0,07. É o mesmo quadro das marcas: a atenção vai para onde se manda e a decisão não
   melhora.
2. **Nem a destilação clássica das saídas ajudou** (0,0). Então, neste desenho, o professor não passou nada ao
   small por nenhum dos dois caminhos; o nulo não é específico da atenção.
3. **Imitar um BERT base que não aprendeu a tarefa atrapalha um pouco** (−0,2 e −0,8), e imitar o que aprendeu
   não atrapalha. A atenção do professor treinado é melhor alvo que a do não treinado, mas só o bastante para não
   piorar.

**Hipótese do Claude para o item 2, não testada:** a destilação foi feita nos mesmos 4.000 pares em que o professor
foi treinado. O BERT base decora o treino (na rodada de 10/11 a perda de classificação nos pares de treino chega a
0,003), então nesses pares a saída dele é quase igual ao rótulo certo e não traz informação nova. As duas fontes
destilam em texto que o professor não decorou (o MiniLM no pré-treino, o TinyBERT com dados aumentados). O teste que
derrubaria a hipótese: destilar em pares que o professor não viu.

**Limites:** um professor, uma semente dele; peso 1,0; média das cabeças (12 no professor, 8 no aluno), que nenhuma
fonte cobre; saídas destiladas sem temperatura; 4.000 pares; um conjunto de teste.

## Professor que não viu os pares do aluno (16/11): as saídas passam no critério da seção 11.3, a atenção não

**Procedência:** hipótese do Claude para o nulo acima; Pedro (16/11): "vamos por esse caminho então". Desenho e
critério escritos antes de rodar (plano, seção 11.3). Script `medir_destilacao.py --professor-fora`, saída
`destilacao-esnli-fora-4000.csv` (20 alunos: 4 braços, 5 sementes). Só o professor muda: BERT base treinado em
outros 4.000 pares do mesmo lote, nenhum em comum com os do aluno. Auditoria antes de lançar: sem falha. 25 min.

**Conferido:** 20 linhas, 5 por braço; os pares do professor não repetem nenhum par do aluno nem do dev, por
identificador e por texto; o braço sem destilação dá os mesmos números das duas rodadas anteriores; critério
aplicado como escrito. **Não conferido:** se o ganho vem do que o professor sabe ou só de o alvo ser "mole" (ver
limites); um professor só, de uma semente.

**A premissa, medida:** como cada professor se sai **nos 4.000 pares em que o aluno treina**.

| Professor | Acurácia no dev do e-SNLI | Acurácia nos pares do aluno | Certeza média na classe que escolhe, nos pares do aluno |
|---|---|---|---|
| Treinado nos mesmos pares do aluno (rodada anterior) | 80,2% | 100,0% | 99,9% |
| Treinado em outros pares (esta rodada) | 79,2% | 79,1% | 97,6% |

O primeiro decorou os pares do aluno: ali a resposta dele é o rótulo certo. O segundo erra 1 em cada 5.

**Como ler a tabela:** cada linha é um jeito de treinar o BERT small, sempre nos mesmos 4.000 pares. A nota é a
acurácia no dev do e-SNLI (9.842 pares, 3 classes, chute = 33%), média de 5 sementes, maior é melhor. "Diferença" é
essa acurácia menos a do small sem destilação, em pontos percentuais; "pior semente" é a menor diferença entre as 5.
As duas últimas colunas repetem a diferença da rodada anterior, em que o professor tinha visto os pares.

| Jeito de treinar o small | Acurácia | Diferença para sem destilação (pontos) | Pior semente (pontos) | Sementes em que ganhou | Mesma diferença com o professor que viu os pares |
|---|---|---|---|---|---|
| Sem destilação | 73,9% | — | — | — | — |
| Imita a atenção da última camada do professor | 74,0% | +0,1 | −0,1 | 3 de 5 | +0,1 |
| Imita a atenção de 4 camadas do professor | 74,2% | +0,3 | −0,7 | 4 de 5 | 0,0 |
| Imita as respostas do professor (probabilidade de cada classe) | 75,5% | **+1,6** | **+1,3** | 5 de 5 | 0,0 |

**Critério (escrito antes):** premissa confirmada e algum braço 1,0 ponto ou mais acima do sem destilação nas 5
sementes -> a hipótese se sustenta. **Passou, para as respostas do professor** (+1,6 ponto, pior semente +1,3; o
desvio entre sementes é 0,4). **Para a atenção continua nulo** (+0,1 e +0,3).

**O que isso permite dizer:**

1. O nulo da destilação das respostas na rodada anterior vinha de o professor ter decorado os pares. Com um
   professor que não os viu, o small ganha 1,6 ponto, fechando cerca de um quarto da distância para o BERT base
   (5,3 pontos até o professor desta rodada).
2. **Imitar a atenção não ajuda em nenhum dos dois casos.** O aluno imita (a distância para a atenção do professor
   cai a 0,19) e a nota não muda. Até aqui, toda forma de mexer na atenção do small, por marcas do LLM em qualquer
   camada ou por imitação de um BERT maior, deixou a nota onde estava.
3. É o primeiro resultado do projeto que passa num critério de ganho escrito antes.

**Limites:** o ganho das respostas pode vir de dois lugares que esta rodada não separa: do que o professor sabe, ou
só de o alvo ser uma distribuição em vez de um rótulo duro (o professor desta rodada erra 21% dos pares do aluno, e
mesmo assim ajuda). O controle que separaria: suavizar os rótulos sem professor. 106 pares do aluno (2,7%) têm a
mesma premissa de algum par do professor. Os dois professores diferem também nos pares de treino. Um professor, uma
semente dele; sem temperatura; peso 1,0; um conjunto de teste.

## Subir o ganho das respostas, e de onde ele vem (16/11): não subiu; o ganho vem do que o professor diz de cada par

**Procedência:** Pedro (16/11): "se é o que deu certo, vamos ver se dá pra subir mais". Alavancas, controles e
critério escolhidos pelo Claude e escritos antes de rodar (plano, seção 11.4). Script `medir_respostas.py`, saída
`respostas-esnli-4000.csv` (40 alunos: 8 braços, 5 sementes). Auditoria antes de lançar: sem falha. 57 min.
**Isto é destilação de conhecimento padrão (Hinton et al., 2015); não usa LLM nem justificativa.**

**Conferido:** 40 linhas, 5 por braço; os quatro conjuntos de 4.000 pares (aluno, professor A, escolha, extra) não
têm par em comum entre si nem com o dev; "respostas, T=1" reproduz a rodada de 11.3 no dev (+1,58); critério aplicado
como escrito. **Não conferido:** a fórmula da temperatura no artigo (escrita de memória); um professor de cada
tipo, uma semente deles.

**Os professores (BERT base):** A, treinado em 4.000 pares: 79,2% no dev. B, treinado em 8.000 pares: 82,1% no dev.
Nenhum dos dois viu os pares do aluno (acertam 79,1% e 80,7% deles).

**Como ler a tabela:** cada linha é um jeito de treinar o BERT small nos mesmos 4.000 pares. As notas são acurácia
(3 classes, chute = 33%), média de 5 sementes, maior é melhor, em dois conjuntos: o **de escolha** (4.000 pares que
ninguém viu, o que decide qual variação é melhor) e o **dev do e-SNLI** (só confirma). "Diferença" é em pontos
percentuais contra o small sem destilação. A última coluna compara com o braço que já tinha passado (respostas do
professor A, T=1), no conjunto de escolha, e diz em quantas das 5 sementes a variação ficou acima dele.

| Jeito de treinar o small | Acurácia, conjunto de escolha | Diferença para sem destilação, escolha | Acurácia, dev | Diferença para sem destilação, dev | Contra "respostas do professor A, T=1", escolha |
|---|---|---|---|---|---|
| Sem destilação | 72,3% | — | 73,9% | — | — |
| Respostas do professor A, T=1 (o que passou em 11.3) | 73,9% | +1,6 | 75,5% | +1,6 | — |
| Respostas do professor A, T=2 | 73,8% | +1,5 | 75,7% | +1,8 | −0,1 (acima em 2 de 5) |
| Respostas do professor A, T=4 | 74,1% | +1,8 | 75,7% | +1,8 | +0,2 (acima em 4 de 5) |
| Respostas do professor B (8.000 pares), T=1 | 74,1% | +1,9 | 75,9% | +2,0 | +0,2 (acima em 3 de 5) |
| Respostas do professor B (8.000 pares), T=2 | 73,9% | +1,6 | 76,0% | +2,1 | 0,0 (acima em 3 de 5) |
| Controle: rótulo suavizado, sem professor | 72,2% | −0,1 | 73,9% | 0,0 | −1,7 (0 de 5) |
| Controle: respostas do professor A trocadas entre pares do mesmo rótulo | 70,6% | −1,7 | 72,1% | −1,8 | −3,3 (0 de 5) |

**Critério (escrito antes), parte 1, "subiu?":** uma variação precisava superar "respostas, T=1" em 0,5 ponto ou
mais nas 5 sementes, no conjunto de escolha. A melhor fica em +0,2 e não ganha nas 5. **Não subiu com estas
alavancas.** No dev, o professor B com T=2 fica +0,5 acima nas 5 sementes, mas o dev não era o conjunto que decide;
fica como indício, não como resultado.

**Parte 2, "de onde vem o ganho?":** os dois controles ficam mais de 0,5 ponto abaixo de "respostas, T=1" (−1,7 e
−3,3, nas 5 sementes, nos dois conjuntos). **Pelo critério: o ganho vem do que o professor diz sobre cada par.**

1. **Não é só o alvo ser mole.** O rótulo suavizado sem professor não ajuda nada (−0,1).
2. **Depende do par.** Com as mesmas respostas do professor entregues ao par errado (do mesmo rótulo), o aluno
   fica 1,7 ponto **pior** que sem destilação. O que ajuda é a resposta do professor para aquele par.
3. O ganho de 11.3 se repete num conjunto novo (+1,6 no de escolha, +1,6 no dev).

**Limites:** um professor de cada tipo, uma semente deles; cerca de 3% dos pares de escolha têm premissa repetida
num conjunto de treino, e o professor B viu o dobro delas; o rótulo suavizado, do jeito que foi montado (rótulo duro
mais alvo de 90%), equivale a 5% de suavização, não 10%; peso 1,0; alavancas não testadas: peso, professor maior
(BERT-large), mais pares para o aluno destilar.

## Juntar o interior do professor com as respostas (17/11): só a sequência do TinyBERT vira candidata; o dropout na atenção não pesava

**Procedência:** Pedro (16/11): "vamos rodar as 3"; em 17/11 ele tirou o jeito 3, mandou ler o MiniLM e o TinyBERT
(os dois lidos pelo Claude, nível 2, notas em `docs/artigos/`) e decidiu: os dois pacotes no jeito 2, média das
cabeças, soma simples sempre, fase 1 "como no TinyBERT", e "rodar dos dois jeitos" a perda de atenção (depois e
antes do dropout). Desenho e critério escritos antes de rodar (plano, seção 11.5). Script `medir_juntar.py`, saída
`juntar-esnli-4000.csv` (70 alunos: 14 braços, 5 sementes). Código auditado e brute-testado antes
(`docs/claude/brute-test-juntar.md`); auditoria de treino antes de lançar: sem falha. Rodada de 2h41.
**Não usa LLM nem justificativa: é destilação de um BERT base num BERT small.**

**Conferido:** 70 linhas, 5 por braço, sem duplicata e sem nota vazia; CSV com MD5 igual no PC e no notebook; o
professor A carregado do arquivo de 16/11 (78,0% no conjunto de escolha, 79,2% no dev); "sem destilação" e
"respostas" dão **exatamente** os números de 16/11, semente a semente; os conjuntos não têm par em comum (por
texto). **Não conferido:** um professor só, de uma semente; o candidato ainda não tem as 10 sementes novas que o
critério pede (rodando); os nulos de atenção de 16/11 não foram rodados de novo sem o dropout.

**Como ler a tabela:** cada linha é um jeito de treinar o BERT small nos mesmos 4.000 pares. A nota é acurácia (3
classes, chute = 33%), média de 5 sementes, em dois conjuntos: o **de escolha** (4.000 pares que ninguém viu; é o
que decide) e o **dev do e-SNLI** (confirma). "Diferença" é em pontos percentuais contra o braço "respostas", que é
a referência a bater (73,9% e 75,5%); "pior semente" é a menor das 5 diferenças; "sementes acima" conta em quantas
das 5 o braço ficou acima de "respostas".

| Jeito de treinar o small | Acurácia, escolha | Diferença para "respostas", escolha | Pior semente, escolha | Sementes acima, escolha | Acurácia, dev | Diferença para "respostas", dev | Sementes acima, dev |
|---|---|---|---|---|---|---|---|
| Sem destilação | 72,3% | −1,6 | — | 0 de 5 | 73,9% | −1,6 | 0 de 5 |
| Respostas do professor (referência) | 73,9% | — | — | — | 75,5% | — | — |
| **Sequência: 20 épocas imitando o interior, depois respostas** | **75,0%** | **+1,1** | +0,1 | 5 de 5 | **76,3%** | **+0,8** | 5 de 5 |
| Controle da sequência: fase 1 imitando um BERT base sem tarefa | 73,9% | +0,1 | −0,6 | 3 de 5 | 75,5% | +0,1 | 3 de 5 |
| Soma simples: respostas + atenção das 4 camadas, juntas | 73,8% | 0,0 | −0,6 | 2 de 5 | 75,7% | +0,3 | 4 de 5 |
| Pacote TinyBERT junto: respostas + atenção + estados internos | 73,3% | −0,6 | −1,5 | 2 de 5 | 75,1% | −0,4 | 0 de 5 |
| Pacote TinyBERT sem atenção | 73,5% | −0,4 | −0,9 | 1 de 5 | 75,3% | −0,2 | 1 de 5 |
| Pacote MiniLM junto: respostas + atenção + relação entre valores | 74,2% | +0,3 | −0,3 | 4 de 5 | 75,6% | +0,1 | 5 de 5 |
| Pacote MiniLM sem atenção | 74,1% | +0,2 | −0,2 | 3 de 5 | 75,6% | +0,1 | 4 de 5 |

**Critério (escrito antes):** candidato é o braço 0,5 ponto ou mais acima de "respostas" nas 5 sementes no conjunto
de escolha, com o dev 0,5 ponto ou mais acima na média; candidato só conta como ganho depois de 10 sementes novas.

1. **A sequência é candidata pela leitura usada em 11.4 (média de 0,5 ou mais e ganho nas 5 sementes):** +1,1 no
   conjunto de escolha, acima nas 5; +0,8 no dev, acima nas 5 (pior +0,6). **Pela leitura mais dura (0,5 em cada
   semente) ela não passa:** a pior semente no conjunto de escolha é +0,1. O critério foi escrito pelo Claude de um
   jeito que admite as duas leituras; as 10 sementes novas (sementes 6 a 15 de "respostas", "sequência" e do
   controle, lançadas em 17/11) decidem.
2. **O controle da sequência não ganha nada** (+0,1). Se a sequência se confirmar, o ganho vem de imitar um
   professor que aprendeu a tarefa, não de qualquer fase de imitação. O aluno imitou o professor sem tarefa até mais
   de perto (atenção 0,14 contra 0,21 no fim da fase 1) e isso não serviu.
3. **Juntar tudo num treino só não ajudou:** soma simples 0,0; pacote MiniLM +0,3 (não ganha nas 5); pacote TinyBERT
   −0,6 no conjunto de escolha e abaixo de "respostas" nas 5 sementes do dev. Pelo critério ("0,5 abaixo nas 5
   sementes no conjunto de escolha") o pacote TinyBERT junto **não** chega a "atrapalha": perde em 3 das 5.
4. **Tirar a atenção dos pacotes quase não muda nada** (TinyBERT −0,4 contra −0,6; MiniLM +0,2 contra +0,3).

**O acréscimo do dropout (critério escrito antes):** cada braço com perda de atenção rodou também com a atenção do
aluno lida antes do dropout. Diferença, em pontos, do braço "antes do dropout" para o seu par, no conjunto de escolha:

| Braço | Diferença média para o par | Pior semente | Melhor semente | Sementes acima do par |
|---|---|---|---|---|
| Soma simples | 0,0 | −0,2 | +0,2 | 2 de 5 |
| Pacote TinyBERT junto | +0,2 | 0,0 | +0,3 | 4 de 5 |
| Pacote MiniLM junto | +0,1 | 0,0 | +0,1 | 4 de 5 |
| Sequência | 0,0 | −0,4 | +0,3 | 3 de 5 |
| Controle da sequência | 0,0 | −0,8 | +0,7 | 3 de 5 |

Como ler: cada linha compara o mesmo braço com a perda de atenção calculada antes e depois do dropout; positivo quer
dizer que a versão sem o ruído foi melhor. **Nenhuma diferença chega a 0,5 ponto: neste desenho o ruído do dropout
não pesava.** A "sequência antes do dropout" faz 75,0% e 76,3%, igual à sequência, mas fica acima de "respostas" em
4 das 5 sementes no conjunto de escolha (pior −0,3), então não é candidata pelo critério.

**Limites:** um professor, uma semente dele; um aluno, uma tarefa, 4.000 pares; pesos fixos em 1,0; a sequência usa
3,5 vezes mais passos de treino que "respostas" (2.500 + 1.000 contra 1.000), e o controle com o professor sem
tarefa é o que separa isso de "mais passos"; a auditoria de treino mediu que no começo todo passo é cortado pelo
limite de gradiente (norma 22 contra 1,0), então nos braços "juntos" a classificação e as respostas recebem uma
fatia menor de cada passo, o que pode explicar a queda do pacote TinyBERT junto (não testado); a perda de atenção é
KL com média das cabeças (o TinyBERT usa erro quadrático antes do softmax, cabeça a cabeça); sem dados aumentados; a
fase 2 usa o rótulo certo mais as respostas (o TinyBERT, só as respostas); o apêndice C do TinyBERT relata que a
destilação na tarefa não ajuda um BERT pequeno pré-treinado direto em tarefas pequenas (MRPC, CoLA), e aqui o
indício é de ajuda: condições diferentes, não uma contradição medida.

### As 10 sementes novas do candidato (17/11): a sequência se confirma pelo critério, com ganho menor no dev

Rodada das sementes 6 a 15 de "respostas", "sequência" e do controle (`medir_juntar.py --sementes 6-15`, 1h45; o
CSV passa a ter 100 linhas, MD5 igual no PC e no notebook). Critério escrito antes: o candidato só conta como ganho
se o intervalo da diferença nas 15 sementes não cruzar o zero. O intervalo usado é o de 95% pela distribuição t
sobre as 15 diferenças semente a semente; **o tipo de intervalo não estava escrito antes, é escolha do Claude feita
depois de rodar.**

**Como ler a tabela:** cada linha é uma comparação entre dois jeitos de treinar, em pontos percentuais de acurácia,
nas mesmas 15 sementes. "Intervalo" é a faixa em que a diferença média deve estar; se ela não inclui o zero, a
diferença não é explicada pela variação entre sementes. "Sementes acima" conta em quantas das 15 o primeiro ficou
acima do segundo.

| Comparação | Conjunto | Diferença média | Intervalo de 95% | Pior semente | Sementes acima |
|---|---|---|---|---|---|
| Sequência menos "respostas" | escolha | +0,93 | +0,70 a +1,17 | +0,12 | 15 de 15 |
| Sequência menos "respostas" | dev | +0,45 | +0,25 a +0,65 | −0,17 | 13 de 15 |
| Controle (professor sem tarefa) menos "respostas" | escolha | +0,06 | −0,23 a +0,36 | −0,62 | 8 de 15 |
| Controle (professor sem tarefa) menos "respostas" | dev | −0,05 | −0,25 a +0,16 | −0,69 | 8 de 15 |
| Sequência menos o controle | escolha | +0,87 | +0,62 a +1,12 | −0,17 | 14 de 15 |
| Sequência menos o controle | dev | +0,49 | +0,28 a +0,71 | −0,40 | 14 de 15 |

Médias das 15 sementes: "respostas" 74,0% e 75,7% (escolha e dev); sequência 74,9% e 76,2%; controle 74,1% e 75,7%.

1. **Pelo critério, é ganho:** o intervalo da sequência contra "respostas" não cruza o zero em nenhum dos dois
   conjuntos, e ela fica acima nas 15 sementes no conjunto de escolha.
2. **O tamanho do ganho é cerca de 0,9 ponto no conjunto de escolha e 0,45 no dev.** As 5 primeiras sementes davam
   +0,8 no dev; as 10 novas dão +0,3. O número das 5 primeiras era otimista, e no dev o ganho fica abaixo do 0,5
   usado para escolher o candidato.
3. **O controle não ganha** (intervalo em torno de zero nos dois conjuntos), e a sequência fica acima dele por
   +0,9 e +0,5. O ganho não vem de treinar por mais passos nem de imitar qualquer BERT maior: vem de imitar o
   interior de um professor que aprendeu a tarefa, antes de imitar as respostas dele.
4. Somado ao +1,6 das respostas sozinhas, o small sai de 72,3% para 74,9% no conjunto de escolha (o professor faz
   78,0%).

**Limites:** os mesmos da seção acima (um professor, uma semente dele; uma tarefa; 4.000 pares; sem dados
aumentados; perda de atenção diferente da do TinyBERT), mais: a ambiguidade do critério de candidato (0,5 "nas 5
sementes") foi do Claude; a versão "antes do dropout" da sequência, que tinha a mesma média, não entrou nas 10
sementes porque não era candidata pelo critério; não se sabe qual parte da fase 1 (atenção, estados internos ou
embeddings) carrega o ganho, nem se menos épocas bastam.

## Quanto as palavras novas da justificativa dizem sobre o rótulo (17/11): 76%, o caso do meio da seção 11.6

**Procedência:** hipótese do Pedro (17/11) de levar as palavras novas da justificativa ao `[CLS]`; checagem
sugerida pelo Claude e autorizada por ele ("pode rodar"). Desenho e faixas escritos antes (plano, seção 11.6).
Script `medir_palavras_novas.py`, saída `palavras-novas-esnli-4000.csv`. Sem BERT e sem GPU: regressão logística
sobre presença de palavra, validação cruzada de 5 partes, nos 4.000 pares de treino do e-SNLI.

**Conferido:** os grupos de palavras vêm de `rte_gradientes.word_groups`, o mesmo código da medida de gradiente;
quatro pares lidos com as palavras novas ao lado; a acurácia é fora da amostra (validação cruzada). **Não
conferido:** só uma divisão das 5 partes (uma semente); a lista de palavras gramaticais não foi relida; isto não
diz se um treino com esse alvo dá ganho. **Fora do que estava escrito antes:** a linha "par + novas" e as duas
contas de depois (palavras de maior peso; tirar as mais frequentes) foram acrescentadas pelo Claude ao rodar.

**Como ler a tabela:** cada linha é uma regressão que tenta adivinhar o rótulo vendo só um conjunto de palavras.
"Acurácia" é a fração de pares em que acerta (3 classes; chutar a classe mais comum dá 33,5%). "Palavras por par" é
quantas palavras daquele conjunto um par tem em média; "pares sem nenhuma" é quantos dos 4.000 não têm nenhuma.

| O que a regressão vê | Acurácia | Palavras por par | Pares sem nenhuma |
|---|---|---|---|
| Nada (classe mais comum) | 33,5% | — | — |
| Palavras do próprio par (premissa e hipótese) | 46,6% | 20,5 | 0 |
| Palavras que a justificativa copia do par (C) | 53,8% | 3,7 | 104 |
| **Palavras novas da justificativa (N)** | **76,4%** | 6,1 | 31 |
| Palavras gramaticais da justificativa (F) | 82,1% | 8,3 | 0 |
| Expressões de rótulo da justificativa (S) | 91,2% | 3,9 | 663 |
| A justificativa inteira | 94,7% | 22,0 | 0 |
| Palavras do par + palavras novas | 74,7% | — | — |

**Pela faixa escrita antes (entre 40% e 90%): caso do meio.** As palavras novas carregam boa parte da decisão sem
serem o rótulo inteiro, e bem mais do que as palavras do próprio par (46,6%).

**O que mais apareceu:**

1. **Parte dessa informação é o molde de argumentar do LLM, não conhecimento novo sobre o par.** As palavras novas de
   maior peso por classe: entailment "defines", "definition", "logically", "synonymous", "located", "outdoors";
   neutro "simply", "specify", "specifically", "indicate", "like"; contradição "different", "prevents", "excludes",
   "claim", "locations", "vehicle". Mistura verbos de argumentação com conteúdo.
2. **Não é só meia dúzia de palavras.** Sem as 200 palavras novas mais frequentes a regressão ainda acerta 63,1%; só
   com essas 200, 70,2%. A informação está espalhada.
3. **A justificativa inteira entrega o rótulo (94,7%), e até as palavras gramaticais sozinhas dão 82,1%.** A
   justificativa foi escrita para defender o rótulo certo, então isso é esperado; como alvo de treino não é
   vazamento (na inferência não há justificativa), mas quer dizer que grande parte do que ela ensinaria é o rótulo.
4. Juntar as palavras do par às novas não melhora (74,7% contra 76,4%): mais colunas para os mesmos 4.000 pares.

**Limites:** presença de palavra ignora ordem; uma tarefa, um gerador (Qwen 35B, prompt F), 4.000 pares; o grupo N
depende da tabela de expressões de rótulo (corte de 30 ocorrências e 90% numa classe), e um corte mais frouxo
passaria mais palavras de molde para o grupo S; nada aqui separa em número "molde" de "conteúdo".

## Palavras novas agrupadas com HDBSCAN (17/11): um grupo de argumentar e 28 de assunto; o assunto também carrega o rótulo

**Procedência:** ideia do Pedro (17/11: "e HDBSCAN pra medir essas palavras novas?"; "pode instalar o UMAP e
rodar"). Vetores, parâmetros e leitura combinada escolhidos pelo Claude e escritos antes (plano, seção 11.7).
Script `medir_grupos_palavras.py`; saídas `grupos-palavras-novas.csv` (um grupo por linha) e
`grupos-palavras-novas-palavras.csv` (uma palavra por linha). `umap-learn` usado só na execução (`uv run --with`),
fora das dependências do projeto.

**Conferido:** 2.323 palavras, todas com vetor; 29 grupos e 1.069 palavras sem grupo (46%), abaixo do limite de
metade escrito antes; a regressão com todas as palavras repete os 76,4% da seção anterior. **Não conferido:** uma
semente de UMAP, um tamanho mínimo de grupo, um tipo de vetor; nenhum parâmetro foi variado. **Chamar o grupo 22 de
"argumentar" e os outros de "assunto" é leitura do Claude sobre as listas de palavras.** A conta "com e sem o grupo
22" foi acrescentada depois de ver os grupos.

**O que saiu do agrupamento:**

- **Um grupo grande de palavras de argumentar** (279 palavras, presente em 2.470 dos 4.000 pares): "involves",
  "means", "specific", "typically", "necessarily", "definition", "inherently", "indicates", "logically",
  "synonymous", "specify", "prove", "inference".
- **28 grupos de assunto**, cada um com 16 a 119 palavras: posturas (standing, sitting, riding), roupa, esporte,
  comida, animais, clima, trabalho, música, água, relações entre pessoas, eventos, emoções, tamanho, fotografia.
- **1.069 palavras sem grupo**, as mais frequentes delas genéricas ("like", "physical", "people", "person",
  "indoors", "movement").

**Como ler a tabela:** cada linha é a mesma regressão da seção anterior (adivinhar o rótulo pela presença de
palavras, 3 classes, acaso 33,5%), vendo só uma parte das palavras novas. "Pares com alguma" é quantos dos 4.000
pares têm ao menos uma palavra daquela parte; um conjunto que cobre poucos pares não tem como acertar muito.

| Palavras novas que a regressão vê | Nº de palavras | Pares com alguma | Acurácia |
|---|---|---|---|
| Todas | 2.323 | 3.967 | 76,4% |
| Só o grupo de argumentar | 279 | 2.470 | 57,8% |
| Todas menos o grupo de argumentar | 2.044 | 3.888 | 70,4% |
| Só os 28 grupos de assunto | 975 | 3.560 | 62,0% |
| Só as sem grupo | 1.069 | 3.437 | 63,2% |

1. **O sinal não é só o molde.** Tirando o grupo de argumentar, as palavras novas ainda acertam 70,4% (de 76,4%).
   A suspeita da seção anterior, de que boa parte dos 76% fosse o jeito de argumentar do LLM, fica enfraquecida:
   o grupo de argumentar sozinho dá 57,8%.
2. **O assunto que a justificativa traz acompanha o rótulo.** Entre os pares que têm palavras do grupo, a fração
   de neutros é 82% em "relações entre pessoas" (strangers, relatives, couple), 73% em "lazer e emoções", 70% em
   "eventos", 63% em "fotografia"; a de contradição é 62% em "ativo, passivo, rápido", 57% em "different, distinct,
   separate", 50% em "location, setting, time"; a de entailment é 47% em "presence, located, near".
3. **Uma leitura possível, do Claude, não testada:** no neutro a justificativa nomeia o que a hipótese acrescentou
   e a premissa não garante (quem são as pessoas, por que estão ali, o que sentem); na contradição nomeia o eixo em
   que as duas frases divergem (lugar, estado, quantidade). Seria informação sobre **por que** o rótulo é aquele,
   por par.

**Limites:** agrupamento por vizinhança de vetor, não por função na frase; palavras de argumentar podem ter ficado
entre as sem grupo ("simply", "require", "form") e palavras de assunto dentro do grupo 22 ("places", "wears");
vetor médio mistura sentidos; um gerador, uma tarefa, 4.000 pares; **nada disto diz se um treino com as palavras
novas como alvo melhora o classificador.**

## Etapa 1 da seção 11.8 (17/11): os grupos dependem do par, mas quase sempre pelo assunto do par

**Procedência:** plano do Claude para a hipótese do Pedro (levar as palavras novas ao `[CLS]`), aprovado por ele
("sim pra todos"; "rodar a etapa 1 aqui mesmo"). Desenho e regra de parada escritos antes (plano, seção 11.8).
Script `medir_grupos_dependem_do_par.py`, saída `grupos-dependem-do-par.csv`. CPU, sem BERT.

**Conferido:** 29 grupos, 4.000 pares, validação cruzada de 5 partes; regra de parada aplicada como escrita.
**Não conferido:** uma divisão das partes; os grupos são de uma única rodada de UMAP e HDBSCAN. **Fora do que estava
escrito antes:** a coluna "só o par" e a conta "o que o rótulo acrescenta ao par" foram acrescentadas ao rodar.

**Como ler a tabela:** para cada grupo de palavras novas, uma regressão tenta prever se o grupo aparece na
justificativa do par. A nota é a área sob a curva ROC (0,5 = acaso; 1,0 = perfeito), média dos 29 grupos. Cada
linha muda o que a regressão vê.

| O que a regressão vê | Nota média dos 29 grupos |
|---|---|
| Só o rótulo certo | 0,595 |
| Só as palavras do par | 0,729 |
| O rótulo certo e as palavras do par | 0,753 |

**Regra de parada (escrita antes):** a etapa 2 só não roda se a nota subir menos de 0,02 de "só o rótulo" para
"rótulo e par". Subiu 0,158, e em 26 dos 29 grupos sobe 0,02 ou mais. **Pela regra, o alvo não é o rótulo
disfarçado e a etapa 2 pode rodar.**

**A ressalva que a regra já trazia, e que os números confirmam:**

1. **O que prevê os grupos é, quase sempre, o assunto do par.** "Só o par" (0,729) fica quase igual a "rótulo e par"
   (0,753). Os maiores ganhos são de grupos de assunto puro: bicicleta e skate 0,86, água 0,87, comida 0,87,
   conversa 0,83, com o rótulo sem acrescentar nada. Um par sobre cães tem justificativa com palavras de animais.
2. **Em poucos grupos o rótulo acrescenta algo ao par:** relações entre pessoas (0,813 só o par, 0,877 com o
   rótulo), lazer e emoções (0,697 e 0,772), "different, distinct" (0,588 e 0,656), eventos (0,700 e 0,752),
   fotografia (0,761 e 0,806), gênero e idade (0,643 e 0,681). São os grupos em que a justificativa parece nomear o
   que decide.
3. **O grupo de argumentar não é previsível por nada disso** (0,54): ele aparece em 2.470 pares de qualquer assunto
   e de qualquer rótulo.

**O que isso muda na expectativa, leitura do Claude:** um alvo que é sobretudo "o assunto do par" é algo que um
BERT pré-treinado já sabe calcular; a cabeça de grupos pode aprender esse alvo sem ensinar nada novo ao
classificador. A etapa 2 está liberada pela regra, mas o Claude espera nulo, a menos que o alvo seja restrito aos
grupos do item 2. Restringir assim é escolher grupos depois de ver um resultado, e só valeria com a nota lida no
conjunto de escolha. **Decisão do Pedro.**

**Limites:** presença de palavra do par é uma descrição pobre do par (um BERT vê muito mais); a soma de rótulo e
palavras do par numa regressão não capta combinações de rótulo com assunto; uma tarefa, um gerador, 4.000 pares.

## Baseline no recorte dos sete grupos (17/11, noite): o recorte é mais difícil e as respostas do professor ajudam mais nele

**Procedência:** pedido do Pedro ("tirar um baseline nesses pares antes, e depois comparar o resultado com ele, e não
com o score geral do modelo"; "Seis mais gênero e idade"; "pode tirar esse baseline"). O que o baseline tinha de
entregar foi escrito antes (plano, seção 11.8, "Rediscussão com o Pedro"). Scripts `medir_grupos_cls.py` (treino,
no PC, 10 minutos) e `medir_recorte.py` (leitura); saídas `grupos-cls-acertos-esnli-4000.csv` e
`recorte-baseline.csv`.

**Conferido:** 10 alunos (2 braços x 5 sementes), 4.000 acertos por aluno no conjunto de escolha; a acurácia geral
de cada aluno é idêntica à da rodada de 17/11 em `juntar-esnli-4000.csv` (mesmas sementes, mesmo código). **Não
conferido:** outras sementes; o recorte com outra rodada de UMAP e HDBSCAN; o dev (não tem justificativa, não dá para
recortar). **Fora do que estava escrito antes:** a conta "ganho no recorte menos ganho fora".

**O recorte:** 1.249 dos 4.000 pares do conjunto de escolha têm, na justificativa do Qwen, palavra nova de algum dos
sete grupos (21, 2, 3, 14, 20, 16, 4). Um par vale 0,08 ponto no recorte.

**Como ler a tabela:** acurácia em pontos percentuais, média das 5 sementes; entre parênteses o desvio padrão entre
as sementes. "Recorte" são os 1.249 pares; "fora" são os outros 2.751; "geral" são os 4.000.

| Braço | Recorte | Fora | Geral |
|---|---|---|---|
| Sem nada | 69,08 (0,90) | 73,71 (0,22) | 72,27 (0,38) |
| Respostas do professor A | 71,29 (0,84) | 75,06 (0,48) | 73,89 (0,56) |
| Respostas menos sem nada, semente a semente | +2,21 (0,51) | +1,35 (0,41) | +1,62 (0,28) |

1. **O recorte é mais difícil:** o aluno sem nada acerta 4,6 pontos a menos nele do que fora.
2. **As respostas do professor ganham nas 5 sementes nos três conjuntos**, e no recorte o ganho vai de +1,52 a
   +2,88.
3. **O ganho é maior no recorte do que fora em 4 das 5 sementes** (diferença média +0,86; por semente +1,01, +1,38,
   −0,30, +0,58, +1,61). Com 5 sementes o intervalo de 95% dessa diferença vai de cerca de −0,1 a +1,8: encosta no
   zero, não dá para afirmar.
4. **Ruído que o critério dos braços com a cabeça vai enfrentar:** no recorte, a diferença entre dois braços, semente
   a semente, teve desvio de 0,51 ponto. Com 5 sementes, a média dessa diferença tem intervalo de 95% de cerca de
   ±0,64 ponto (distribuição t, 4 graus de liberdade). Um ganho de 0,5 ponto no recorte fica dentro desse ruído.

**Limites:** o recorte é definido pelo que o Qwen escreveu, não pelo par; o desvio de 0,51 vem de um único par de
braços (respostas contra sem nada) e pode ser outro para os braços com a cabeça; 5 sementes.

### O baseline com 15 sementes (17/11, noite): o ruído no recorte cai para ±0,36 ponto

**Procedência:** depois de ler as 5 sementes, o Pedro escolheu "Mais sementes antes". O número (sementes 6 a 15,
fechando 15) é escolha do Claude, registrada no plano antes de rodar. Mesmo script, 19 minutos no PC.

**Conferido:** 30 alunos (2 braços x 15 sementes) em `grupos-cls-acertos-esnli-4000.csv`; números refeitos por
script sobre `recorte-baseline.csv`. **Não conferido:** o mesmo dos 5 (outro recorte, o dev). **Previsão errada do
Claude:** a conta com o desvio das 5 sementes dava ±0,28; o desvio com 15 foi maior (0,66 contra 0,51) e o intervalo
ficou em ±0,36.

**Como ler a tabela:** como a de cima, com 15 sementes. Na última linha, depois do desvio, vem a metade do
intervalo de 95% da média (distribuição t, 14 graus de liberdade).

| Braço | Recorte (1.249 pares) | Fora (2.751 pares) | Geral (4.000 pares) |
|---|---|---|---|
| Sem nada | 69,03 (0,70) | 73,75 (0,38) | 72,28 (0,40) |
| Respostas do professor A | 71,36 (0,56) | 75,17 (0,44) | 73,98 (0,40) |
| Respostas menos sem nada, semente a semente | +2,34 (0,66; ±0,36) | +1,42 (0,38; ±0,21) | +1,71 (0,39; ±0,22) |

1. **O recorte continua mais difícil:** sem nada, 4,7 pontos abaixo do resto.
2. **As respostas ganham nas 15 sementes nos três conjuntos;** no recorte, de +1,36 a +3,76.
3. **O ganho das respostas é maior no recorte do que fora em 14 das 15 sementes:** diferença média +0,92 ponto,
   intervalo de 95% de +0,57 a +1,26. Com 15 sementes não cruza o zero. Essa conta não estava escrita antes, e o
   recorte é também onde o aluno mais erra (mais espaço para ganhar): ela não mostra que os grupos sejam a causa.
4. **Ruído para o critério dos braços com a cabeça:** no recorte, com 15 sementes, a média da diferença entre dois
   braços tem intervalo de 95% de cerca de ±0,36 ponto (cerca de 4 a 5 pares). Vale para este par de braços; para
   os braços com a cabeça o desvio pode ser outro.

## Etapa 2 da seção 11.8 (17 e 18/11): a cabeça de grupos no `[CLS]` é nula pelo critério; nenhum braço vira candidato

**Procedência:** hipótese do Pedro (levar as palavras novas da justificativa ao `[CLS]`); desenho, recorte e critério
escritos antes (plano, seção 11.8, "Critério dos braços com a cabeça de grupos"; ele escolheu "5 e depois 10", "Pode
escrever" e pediu o brute-test antes). Auditoria de treino e brute-test rodados antes de lançar
(`docs/claude/brute-test-grupos-cls.md`). Script `medir_grupos_cls.py`, 8 braços x 5 sementes, 43 minutos no PC;
leitura por `medir_recorte.py --sementes 1-5`; saídas `grupos-cls-acertos-esnli-4000.csv`,
`grupos-cls-cossenos-esnli-4000.csv` e `recorte-acuracias.csv`.

**Conferido:** 40 alunos novos, 4.000 acertos cada; as referências ("sem nada", "respostas") são as do baseline; a
cabeça aprendeu o alvo (abaixo). **Não conferido:** mais de 5 sementes nos braços com a cabeça (o critério só pedia
para candidato); outro peso da perda (só 1,0); outra rodada de UMAP e HDBSCAN; o BERT base (etapa 3, que não roda).

**Como ler a tabela:** diferença de acurácia em pontos percentuais no recorte (1.249 pares do conjunto de escolha),
média das 5 sementes, semente a semente; entre parênteses, a metade do intervalo de 95%. A referência é "sem nada"
nos braços sem professor e "respostas" nos braços com as respostas do professor A. O critério pedia mais de 0,64
ponto nas duas colunas.

| Braço com a cabeça | Sobre a referência | Sobre o seu controle trocado | Candidato? |
|---|---|---|---|
| Todos os 29 grupos, sem professor | −0,03 (±0,35) | −0,08 (±0,34) | não |
| Sete grupos, sem professor | +0,14 (±0,56) | +0,29 (±0,54) | não |
| Todos os 29 grupos, com respostas | +0,02 (±0,11) | 0,00 (±0,16) | não |
| Sete grupos, com respostas | +0,11 (±0,41) | +0,06 (±0,41) | não |

1. **Nenhum braço passa de 0,64 em nenhuma das duas colunas;** o maior número é +0,29 e todos os intervalos cruzam
   o zero. Pelo critério: nulo, as sementes 6 a 15 não rodam, a etapa 3 não roda e as justificativas do dev não são
   geradas.
2. **Fora do recorte e no geral também não muda:** a maior diferença é +0,10 ponto no geral (sete grupos, sem
   professor). No dev, os dez braços ficam em dois patamares, 73,9% sem professor e 75,5% com, e a cabeça não move
   nenhum deles mais que 0,06.
3. **A cabeça aprendeu o alvo, então o nulo não é de uma cabeça que não treinou.** Um aluno a mais (todos os grupos,
   sem professor, semente 1, treinado no notebook), medido nos 4.000 pares do conjunto de escolha, que ele nunca
   viu: a área sob a curva ROC média dos 29 grupos é 0,619 só com o viés por rótulo e 0,699 com a cabeça lendo o
   `[CLS]`. A regressão sobre as palavras do par, na etapa 1, chegava a 0,753. É um aluno só, sem repetição.
4. **O cosseno do gradiente (descritivo, não decide):** entre o gradiente de cada grupo e o da classificação, no
   encoder, a média fica em zero antes e depois do treino em todos os braços (de −0,02 a +0,01); o grupo mais
   afastado é o de eventos, −0,10 no alvo restrito. Os gradientes dos grupos nem ajudam nem atrapalham a
   classificação de forma medível: são quase perpendiculares a ela.

**Leitura do Claude, não medida:** o que a etapa 1 mostrou (o alvo é sobretudo o assunto do par) é compatível com
este resultado. O encoder aprende a dizer o assunto, o que ele já sabia calcular, e isso não muda a decisão.

**Limites:** o controle trocado do alvo restrito deixa 51% dos pares com a mesma linha de alvos (69% dos pares não têm
nenhum dos sete grupos); o recorte é definido pelo que o Qwen escreveu; um gerador, um tamanho de aluno, 4.000
pares, peso 1,0; o viés por rótulo nasce na taxa de cada rótulo (mudança feita depois da auditoria, antes de rodar).

### Dois testes sobre o nulo (18/11): a cabeça treinou, mas o `[CLS]` já tinha a informação dos grupos

**Procedência:** o Pedro achou o resultado esquisito e mandou testar as duas dúvidas que o Claude levantou ("pode
testar os dois"). O que cada resultado significaria foi escrito na conversa antes de ver os números. Script no
scratchpad da sessão (`cabeca_dois_testes.py`, fora do repositório), notebook (GTX 1650), semente 1.

**Conferido:** os números abaixo, de uma rodada. **Não conferido:** outras sementes; o alvo restrito (só o de 29
grupos foi medido); uma sonda não linear.

**Como ler as tabelas:** "perda" é a entropia cruzada da cabeça de grupos (menor é melhor); "ROC" é a área sob a
curva, média dos 29 grupos, nos 4.000 pares do conjunto de escolha, que nenhum aluno viu (0,5 = chute).

Teste A, a cabeça treinou? Um aluno com a cabeça de todos os grupos, medido antes e depois do treino:

| O que prevê os grupos | Perda no treino | Perda no conjunto de escolha | ROC no conjunto de escolha |
|---|---|---|---|
| Só o rótulo certo (o viés) | 0,2326 | 0,2285 | 0,619 |
| A cabeça do aluno, antes do treino | 0,2426 | 0,2382 | 0,608 |
| A cabeça do aluno, depois do treino | 0,2226 | 0,2209 | 0,699 |

Teste B, a perda de grupos ensinou algo ao encoder? Uma sonda treinada até convergir (regressão logística sobre o
`[CLS]` e o rótulo certo, ajustada nos 4.000 pares de treino):

| De qual encoder vem o `[CLS]` | ROC da sonda no conjunto de escolha |
|---|---|
| BERT small pré-treinado, sem treino nenhum | 0,765 |
| Aluno sem a perda de grupos | 0,758 |
| Aluno com a cabeça de grupos | 0,760 |
| (a cabeça com o seu próprio orçamento, 5e-5 e 1.000 passos, sobre o `[CLS]` congelado do aluno sem a perda) | 0,693 |

1. **A cabeça treinou:** a perda cai abaixo do que o rótulo sozinho dá e a ROC sobe de 0,608 para 0,699. A camada
   linear andou 0,355 sobre uma norma inicial de 3,11 (cerca de 11%): treinou, mas pouco.
2. **O `[CLS]` já tinha a informação dos grupos antes de qualquer treino:** a sonda dá 0,765 no BERT pré-treinado,
   0,758 no aluno sem a perda e 0,760 no aluno com a cabeça. A perda de grupos não acrescentou nada que uma sonda
   linear consiga ler.
3. **O 0,699 não é mérito da perda de grupos:** a mesma cabeça, com o mesmo orçamento, treinada sobre o `[CLS]`
   congelado de um aluno que nunca viu essa perda chega a 0,693.

**O que isso sustenta:** o nulo da etapa 2 não é de cabeça que não treinou. O alvo (quais grupos de palavras o Qwen
usa) é quase todo algo que o BERT small já codifica no `[CLS]` sem treino; cobrar esse alvo não obriga o encoder a
aprender nada novo. É o que a etapa 1 indicava ("quase tudo é o assunto do par"), agora medido no próprio `[CLS]`.
**O que não sustenta:** que nenhum alvo tirado das justificativas ajudaria; só este, com esta forma de agrupar.

### O braço dos sete grupos com 15 sementes (18/11): não conta pela regra; fica acima do controle trocado, não do aluno sem nada

**Procedência:** exceção ao critério decidida pelo Pedro depois de ver as 5 sementes ("sim, roda as 10 sementes").
A regra de leitura foi escrita no plano antes de rodar: só conta se o intervalo de 95% das **duas** diferenças não
cruzar o zero no recorte. Sementes 6 a 15 de `head_cut` e `head_cut_swapped`, 15 minutos no PC.

**Conferido:** 15 sementes nos três braços (sem nada, sete grupos, sete grupos trocados); números de
`medir_recorte.py`. **Não conferido:** o mesmo braço com as respostas do professor além de 5 sementes. **A declarar:**
o braço foi escolhido depois de olhar oito comparações.

**Como ler a tabela:** diferença de acurácia em pontos percentuais, média das 15 sementes, semente a semente; entre
parênteses, a metade do intervalo de 95%; depois, em quantas das 15 sementes a diferença é positiva.

| Sete grupos, sem professor, menos... | No recorte (1.249 pares) | Fora do recorte | Geral |
|---|---|---|---|
| ...o aluno sem nada | +0,17 (±0,21); 8 de 15 | +0,08 (±0,10); 10 de 15 | +0,11 (±0,10); 9 de 15 |
| ...o seu controle trocado | +0,28 (±0,22); 11 de 15 | +0,02 (±0,15); 7 de 15 | +0,10 (±0,13); 11 de 15 |

1. **Pela regra, não conta:** no recorte, a diferença sobre o aluno sem nada vai de −0,05 a +0,38 e cruza o zero.
2. **Sobre o controle trocado, o intervalo não cruza o zero** (+0,06 a +0,50; cerca de 3 a 4 pares em 1.249): com os
   grupos certos o aluno fica um pouco acima do que fica com os grupos de outro par. Como ele não fica acima do
   aluno sem nada, a leitura mais simples é que os grupos trocados atrapalham um pouco, e os certos não ajudam.
3. **No dev não há nada:** 74,04% com a cabeça, 73,99% com o controle, 73,98% sem nada.
4. **O +0,29 das 5 sementes se manteve em tamanho (+0,28), não cresceu:** se há efeito, é dessa ordem, abaixo de
   meio ponto e só visível contra o controle.

### Olhar exploratório: pares difíceis e rótulo (18/11, pergunta do Pedro: "a ideia era ajudar em labels difíceis")

**Procedência:** pergunta do Pedro depois do resultado; **nada aqui estava escrito antes**, e são 24 comparações
(com 5% de falso positivo cada, espera-se uma passando por acaso). Serve para dizer onde olhar, não para concluir.
Script no scratchpad (`dificeis.py`), sobre os mesmos acertos par a par, 15 sementes. Dificuldade de um par = em
quantos dos 15 alunos do braço "respostas" ele é acertado (um braço que não é nenhum dos dois comparados, para a
escolha dos pares difíceis não favorecer um lado); faixas fixadas antes de olhar as diferenças.

**Como ler:** sete grupos sem professor menos o aluno sem nada, e menos o controle trocado, em pontos percentuais;
entre parênteses a metade do intervalo de 95% e em quantas das 15 sementes é positivo.

| Subconjunto do conjunto de escolha | Pares | Acerto sem nada | Menos sem nada | Menos o controle trocado |
|---|---|---|---|---|
| Fáceis (13 a 15 de 15 acertam) | 2.707 | 95,7% | +0,07 (±0,11; 11) | +0,06 (±0,09; 11) |
| Médios (3 a 12) | 511 | 48,5% | +0,07 (±0,45; 8) | +0,12 (±0,64; 8) |
| Difíceis (0 a 2) | 782 | 6,8% | +0,26 (±0,21; 11) | +0,25 (±0,22; 11) |
| Rótulo entailment | 1.306 | 76,6% | +0,08 (±0,20; 9) | +0,01 (±0,16; 6) |
| Rótulo neutral | 1.381 | 67,3% | +0,05 (±0,28; 7) | +0,07 (±0,26; 9) |
| Rótulo contradiction | 1.313 | 73,1% | +0,20 (±0,24; 11) | +0,23 (±0,18; 11) |
| Contradiction dentro do recorte | 433 | 68,2% | +0,48 (±0,42; 12) | +0,51 (±0,34; 12) |

O ganho se concentra nos pares difíceis (+0,26, cerca de 2 pares em 782) e na contradição, mais ainda dentro do
recorte (+0,48, cerca de 2 pares em 433); nos fáceis, nos médios, no entailment e no neutral não há nada. É a direção
que a hipótese previa, mas o tamanho é de 2 pares, e a análise foi escolhida depois de ver o resultado.

### Os pares difíceis no dev (18/11): o padrão não se repete

**Procedência:** pedido do Pedro ("escreve o critério e lê os pares no dev"); critério escrito na seção 11.9 do
plano antes de ler o dev por subconjunto. Exceção, decidida por ele, à regra "dev só se algum braço passar". Nenhum
treino novo: `medir_dificeis.py` lê os acertos par a par já gravados, 15 sementes.

**Conferido:** o script, rodado no conjunto de escolha (`--split choice`), devolve a tabela exploratória acima
linha por linha (782 difíceis, +0,26 ±0,21, 11 de 15). **Não conferido:** quantos pares difíceis têm rótulo
discutível; o mesmo com outro aluno ou outro alvo.

**Como ler:** sete grupos sem professor menos o aluno sem nada, e menos o controle trocado, em pontos percentuais,
no dev do e-SNLI; entre parênteses a metade do intervalo de 95% e em quantas das 15 sementes é positivo. Dificuldade
= em quantos dos 15 alunos do braço "respostas" o par é acertado no dev.

| Subconjunto do dev | Pares | Acerto sem nada | Menos sem nada | Menos o controle trocado | Papel no critério |
|---|---|---|---|---|---|
| Difíceis (0 a 2) | 1.768 | 8,8% | −0,08 (±0,21; 6) | −0,03 (±0,20; 6) | principal |
| Rótulo contradiction | 3.278 | 74,3% | +0,12 (±0,16; 12) | +0,12 (±0,13; 10) | secundário |
| Fáceis (13 a 15) | 6.814 | 95,5% | +0,11 (±0,06; 12) | +0,09 (±0,06; 11) | só descrito |
| Médios (3 a 12) | 1.260 | 48,8% | −0,06 (±0,34; 7) | −0,07 (±0,26; 7) | só descrito |
| Rótulo entailment | 3.329 | 77,8% | 0,00 (±0,12; 7) | −0,07 (±0,14; 6) | só descrito |
| Rótulo neutral | 3.235 | 69,7% | +0,03 (±0,17; 6) | +0,09 (±0,18; 9) | só descrito |
| Geral | 9.842 | 74,0% | +0,05 (±0,07; 8) | +0,04 (±0,06; 9) | só descrito |

1. **O teste principal não passa:** nos pares difíceis do dev a diferença é −0,08 e −0,03, com intervalo cruzando o
   zero e positiva em 6 de 15 sementes. O +0,26 do conjunto de escolha não se repete, nem em sinal.
2. **O secundário não passa:** na contradição a média é +0,12 nas duas comparações, mas os dois intervalos encostam
   ou cruzam o zero (−0,04 a +0,28; −0,01 a +0,25).
3. **Pela regra escrita antes, o olhar exploratório fica como acaso de 24 comparações** e a pergunta fecha para este
   braço. Não se troca faixa, braço de dificuldade nem subconjunto para procurar de novo.
4. **Fora do critério, só descrito:** nos pares fáceis o intervalo fica acima de zero nas duas comparações (+0,11 e
   +0,09, cerca de 7 pares em 6.814). Não era previsto, é uma de sete linhas olhadas, e vai no sentido contrário ao
   da hipótese (ganho onde o aluno já acerta). No conjunto de escolha a mesma linha dava +0,07 (±0,11).

**O que isso sustenta:** este alvo (sete grupos de palavras novas no `[CLS]` do BERT small) não ajuda os pares
difíceis do e-SNLI. **O que não sustenta:** que nenhuma forma de usar a justificativa ajude pares difíceis; só esta
foi medida.

## Professor que lê a justificativa (18/11, noite): ele acerta 96,7% e não precisa do par; por dentro, as posições do par mudam com a justificativa

**Procedência:** linha escolhida pelo Pedro em 18/11 (professor que lê a justificativa, aluno que não lê); desenho,
controles e cortes do Claude, escritos antes de codar em `docs/2026-11-18-professor-que-le-a-justificativa.md`.
`medir_professor_justificativa.py`, no PC do amigo (RTX 5060 Ti), 15 minutos; 9 professores BERT base treinados nos
4.000 pares do professor de 16/11, 3 sementes por tipo de entrada. Dados em `professor-justificativa-esnli-4000.csv`
e `professor-justificativa-interior-4000.csv`. Nenhum aluno foi treinado.

**Conferido:** as 9 linhas e as 10 do interior, lidas do CSV copiado; a âncora (o professor "só o par" da semente 1
deu 78,8% nos pares do aluno e 77,7% no conjunto de escolha, contra 79,1% e 78,0% do professor de 16/11); o desvio
entre sementes do "só o par" (0,4 ponto nos pares do aluno), abaixo do 1 ponto que o critério pedia para ler as
diferenças; a checagem embutida do teste (b) (distância 0,00000 na saída dos embeddings); a auditoria de treino
(sem vazamento de pares entre o treino do professor e os dois conjuntos de prova; trocas e alinhamento conferidos
nos dados reais). **Não conferido:** nenhum exemplo foi lido (quais são os 3,3% que ele erra, o que a justificativa
diz neles); o dev do e-SNLI (não tem justificativa); o teste (b) em outra semente que não a 1.

### Teste (a): acurácia do professor

**Como ler:** acurácia em %, média de 3 sementes, em pares que nenhum professor treinou. Os pares do aluno decidem,
o conjunto de escolha confirma.

| Professor lê | Pares do aluno | Conjunto de escolha |
|---|---|---|
| Só o par | 78,4 | 77,0 |
| Par + justificativa | 96,7 | 96,5 |
| Só a justificativa | 96,9 | 96,5 |

**Como ler:** o professor "par + justificativa" com a justificativa trocada só na hora da prova, nos pares do aluno
(conjunto de escolha entre parênteses). "Segue a justificativa" é a parte dos pares em que a resposta é o rótulo de
onde a justificativa trocada veio; a troca é uma rotação fixa de rótulos, então o acaso fica perto de um terço.

| Justificativa na prova | Acurácia contra o rótulo do par | Segue a justificativa |
|---|---|---|
| A do próprio par | 96,7 (96,5) | — |
| De outro par do mesmo rótulo | 95,8 (95,4) | — |
| De um par de outro rótulo | 2,3 (2,4) | 94,6 (93,7) |

1. **A justificativa ajuda muito o professor:** +18,2 pontos sobre "só o par", nas 3 sementes (+17,9, +18,5, +18,3).
   A primeira linha da regra (a linha para) não se aplica.
2. **Ele não precisa do par:** "par + justificativa" menos "só a justificativa" dá −0,2 ponto (+0,0, −0,5, −0,2 por
   semente), abaixo do corte de 1 ponto. Pela regra escrita antes, ele lê o rótulo na justificativa.
3. **As trocas dizem o mesmo:** com a justificativa de outro par do mesmo rótulo ele perde 0,9 ponto; com a de outro
   rótulo ele responde o rótulo da justificativa em 94,6% dos pares e o do par em 2,3%.
4. **O corte de 97% não foi atingido, por 0,3 ponto** (96,7%). Pela letra da regra as respostas ficam como
   "candidatas a destilar", e não como "viraram o rótulo". O corte era escolha do Claude sem medida que o
   sustentasse; a diferença para ele é menor do que a escolha do próprio corte. As respostas coincidem com o rótulo
   do par em 96,7% dos pares e a confiança média é de 99,6%.

### Teste (b): o interior nas posições do par

**Como ler:** professor "par + justificativa" da semente 1, 4.000 pares do conjunto de escolha. Distância = 1 menos
o cosseno entre o vetor com a justificativa certa e o vetor com a justificativa trocada, média das posições do par
(sem o `[CLS]`) e dos pares; 0 é igual. Razão = distância com troca de mesmo rótulo dividida pela distância com
troca de outro rótulo. A última coluna é quanto da atenção das posições do par vai para a justificativa mais o
separador final.

| Camada | Distância, troca de mesmo rótulo | Distância, troca de outro rótulo | Razão | Atenção para a justificativa |
|---|---|---|---|---|
| Embeddings (checagem) | 0,000 | 0,000 | — | — |
| 3 | 0,014 | 0,015 | 0,94 | 20% |
| 6 | 0,030 | 0,033 | 0,92 | 23% |
| 9 | 0,052 | 0,082 | 0,64 | 30% |
| 12 | 0,109 | 0,346 | 0,32 | 46% |

No `[CLS]`: razão 0,90, 0,86, 0,41 e 0,15 nas camadas 3, 6, 9 e 12; distância com troca de outro rótulo de 1,25
na camada 12 (o vetor aponta para outro lado).

5. **As posições do par leem a justificativa:** a distância com troca de outro rótulo passa de 0,01 em todas as
   camadas e de 20% a 46% da atenção delas vai para a justificativa. A primeira linha da regra não se aplica.
6. **Não é só o rótulo, pela regra escrita antes:** nas posições do par a razão fica acima de um quarto nas quatro
   camadas. Nas camadas 3 e 6 trocar por uma justificativa do mesmo rótulo muda quase tanto quanto trocar por uma
   de outro (0,94 e 0,92); na camada 12 o rótulo responde pela maior parte (0,32), e no `[CLS]` da camada 12 passa
   do corte (0,15).
7. **O tamanho da mudança não tem régua:** 0,014 a 0,109 de distância nas posições do par não foi comparado com
   nada (por exemplo, com a distância entre dois professores de sementes diferentes no mesmo par).

**O que isso sustenta:** o professor que lê a justificativa decide pela justificativa e ignora o par quando os dois
discordam; as respostas dele são quase o rótulo; por dentro, as posições do par mudam com o texto da justificativa,
mais com o texto do que com o rótulo nas camadas do meio. **O que não sustenta:** que imitar esse interior ajude
um aluno que não lê a justificativa (nenhum aluno foi treinado); que a mudança nas posições do par seja "o motivo"
e não só o efeito de ter outras palavras ao lado (as duas trocas põem palavras diferentes; a medida não separa);
que as respostas dele sirvam ou não para destilar (o corte de 97% ficou a 0,3 ponto).

## Sequência com o professor que lê a justificativa (18/11, noite): imitar o interior dele atrapalha, 2,7 pontos abaixo da "sequência"

**Procedência:** desenho pedido pelo Pedro ("Desenhar a destilação"), braços, controle e cortes do Claude, escritos
antes de codar no fim de `docs/2026-11-18-professor-que-le-a-justificativa.md`; divisão entre as máquinas combinada
com ele. `medir_juntar.py`, braços `sequence_rationale` e `sequence_rationale_shuffled`: iguais à "sequência" de
17/11, mas na fase 1 o aluno imita, só nas posições do par, o professor que lê o par mais a justificativa (o da
semente 1 medido na seção anterior); na fase 2, classificação mais as respostas do professor que lê só o par, como
na "sequência". **Duas máquinas, cada semente com os três braços na mesma:** sementes 1 a 3 no PC do Pedro (a
"sequência" delas é a de 17/11), sementes 4 e 5 no PC do amigo (a "sequência" foi rodada de novo lá). Dados em
`juntar-esnli-4000.csv` (PC) e `juntar-esnli-4000-amigo.csv`.

**Conferido:** 10 alunos novos, 5 por braço, mais a "sequência" das sementes 4 e 5 no PC do amigo (74,7% e 75,3% no
conjunto de escolha, contra 74,9% e 75,1% das mesmas sementes no PC); a checagem embutida (a perda de imitação da
fase 1 cai nos 10 alunos: atenção de 3,1 para 0,17, estados internos de 2,9 para 0,75); as diferenças pareadas
refeitas a partir dos dois CSVs; a auditoria de treino antes de lançar (o braço antigo não muda com o código novo;
corte e renormalização conferidos com pares de tamanhos diferentes). **Não conferido:** por que cai (nenhuma
hipótese foi testada); o mesmo braço sem a perda de atenção ou com outra renormalização; outro professor que não o
da semente 1.

**Como ler:** acurácia em %, média das 5 sementes; a diferença é contra a "sequência", pareada por semente, com
intervalo de 95% e em quantas das 5 sementes o braço ficou acima. O conjunto de escolha decide, o dev confirma.

| Interior imitado na fase 1 | Acurácia, escolha | Diferença para a "sequência", escolha | Acurácia, dev | Diferença para a "sequência", dev |
|---|---|---|---|---|
| Professor que lê só o par ("sequência") | 75,0 | — | 76,3 | — |
| Professor que lê o par + a justificativa do par | 72,3 | −2,7 (−3,3 a −2,1), 0 de 5 | 74,2 | −2,1 (−2,3 a −1,9), 0 de 5 |
| Controle: o mesmo professor com a justificativa de outro par do mesmo rótulo | 72,4 | −2,5 (−3,4 a −1,6), 0 de 5 | 74,4 | −1,9 (−2,0 a −1,8), 0 de 5 |

1. **Pela regra escrita antes, imitar o interior do professor que lê a justificativa atrapalha:** 2,7 pontos abaixo
   da "sequência" no conjunto de escolha, abaixo nas 5 sementes (a menor queda é 1,8), e o dev confirma (−2,1).
2. **Não há candidato**, então as sementes 6 a 15 não rodam.
3. **A justificativa certa e a trocada dão o mesmo:** teste menos controle −0,2 ponto no conjunto de escolha (−0,6
   a +0,3, acima em 2 de 5) e −0,2 no dev (−0,3 a −0,1, 0 de 5). O que a justificativa diz sobre o par não fez
   diferença para o aluno; no dev a certa fica um pouco abaixo da trocada.
4. **Fora do critério, só descrito:** os 72,3% do braço novo são a nota do aluno sem destilação nenhuma (72,3%,
   17/11) e ficam 1,7 ponto abaixo de "respostas" sozinha (74,0%, 15 sementes). Essa comparação não é pareada na
   mesma máquina para as sementes 4 e 5.

**O que isso sustenta:** neste desenho (posições do par, embeddings mais atenção renormalizada mais estados
internos, 20 épocas), trocar o professor da fase 1 pelo que lê a justificativa piora o aluno, com ou sem a
justificativa certa. **O que não sustenta:** que nenhum jeito de usar um professor que lê a justificativa ajude (um
desenho, um professor, uma semente de professor); nem a causa da queda: a renormalização da atenção, o rótulo
carregado no interior ou a distância entre o que o professor vê e o que o aluno vê não foram separados.
