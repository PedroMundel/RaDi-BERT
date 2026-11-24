# O que o decoder gera (desenho e leitura escritos em 18/11, noite, antes de codar e de rodar)

**Procedência.** Pedro (18/11): "bota pra gerar so por gerar", depois de ler as notas do EIDRR (Wang e Wu, 2026;
`docs/artigos/notas-eidrr-wang-wu-2026.md`, nível 2), onde o encoder ligado direto ao decoder do T5 gera
justificativas com nota humana 1,71 de 5 e, com uma camada nova no meio, 4,20. O desenho e as categorias de leitura
são do Claude. É uma olhada: não há regra de parada nem hipótese de nota.

**Pergunta:** o braço com decoder deste projeto (receita do Agrawal, BERT base ligado direto ao decoder do T5 base),
treinado nos 16.000 pares do e-SNLI, gera para pares que nunca viu uma justificativa que faz sentido?

## Desenho

- **Um modelo:** braço `bert_decoder`, semente 1, exatamente a receita dos 16.000 pares (8 épocas, 4.000 passos,
  fase A 250, fase B 1.200, aquecimento `500`, peso 0,1), sem as medidas de gradiente (não mudam o treino). Os
  pesos ficam salvos (a primeira vez neste projeto para um braço com decoder).
- **Âncora:** a acurácia no dev inteiro tem de cair perto dos 83,4% da semente 1 na curva de arranque (PC). Na outra
  máquina, a diferença esperada é a de placa (até 0,6 ponto no fim da curva, medido em 18/11).
- **Geração:** 200 pares do dev do e-SNLI sorteados uma vez (semente 0), gulosa (sem amostragem), até 64 tokens. O
  decoder recebe os vetores do encoder lendo só o par, como no treino: **não recebe o rótulo previsto** (no EIDRR
  recebe). Para cada par ficam: premissa, hipótese, rótulo certo, rótulo e probabilidades do classificador, a
  justificativa gerada e a primeira explicação humana do e-SNLI (só para comparar na leitura).

## Leitura (o Claude lê os 50 primeiros dos 200; os outros ficam no arquivo)

Cada justificativa gerada cai em uma categoria:

| Categoria | Quando |
|---|---|
| Defende o rótulo previsto, fato certo | argumenta pelo rótulo que o classificador deu e não diz nada que o par contradiga |
| Defende o rótulo previsto, fato trocado | argumenta pelo rótulo do classificador, mas afirma algo que o par não diz ou contradiz |
| Defende outro rótulo | argumenta por um rótulo diferente do que o classificador deu |
| Não argumenta | frase quebrada, repetição, só reconta o par, ou não dá para dizer qual rótulo defende |

Como ler o resultado: é a leitura de uma pessoa (o Claude), sem segundo avaliador; não se compara em número com a
avaliação humana do EIDRR (outra escala, outra tarefa, avaliadores treinados). Serve para dizer se o texto é
"usável", "às vezes usável" ou "não usável", com exemplos.

## O que não responde

- Se uma camada de ponte melhoraria (não roda aqui).
- Se a justificativa gerada é fiel ao que o classificador usou para decidir.
- Uma semente só.

---

## Resultado (18/11, 21:50; rodado no PC do Marcelo, 19 minutos)

**Conferido:** a âncora (83,3% de acurácia no dev inteiro, dentro da faixa de 82,5% a 84,0%; ROC-AUC 0,933); as 200
justificativas copiadas para `resultados/esnli-treino-16k-gerado/geradas.csv` (nenhuma vazia, 20,9 palavras em
média); a leitura dos 50 primeiros, um por um, pelo Claude; a auditoria de treino antes de lançar (sem bloqueio).
**Não conferido:** segundo leitor; os 150 restantes à mão. Os pesos (cerca de 1,3 GB) ficaram só no PC do
Marcelo, em `C:\RaDi-BERT\resultados\esnli-treino-16k-gerado\`.

**Como ler:** os 50 primeiros dos 200 pares sorteados, cada justificativa numa categoria, pela leitura do Claude.
"Rótulo previsto" é o que o classificador deu (ele acerta 44 dos 50 e 177 dos 200).

| Categoria | Pares | Previsto entailment (23) | Previsto neutral (16) | Previsto contradiction (11) |
|---|---|---|---|---|
| Defende o rótulo previsto, fato certo | 22 | 14 | 5 | 3 |
| Defende o rótulo previsto, fato trocado | 10 | 6 | 0 | 4 |
| Defende outro rótulo | 2 | 1 | 1 | 0 |
| Não argumenta | 16 | 2 | 10 | 4 |

1. **Usável em menos da metade:** 22 de 50 defendem o rótulo do classificador sem errar o fato. Exemplos: #4 "A man
   is a person, and a sidewalk is an outdoor surface, so he is outside."; #5 "Baseball players can be any height,
   so the player could be any height, not just a tall, athletic player."; #28 "Swimming in a pool requires being in
   water, while sitting on a bench implies being stationary on a surface, making both impossible simultaneously."
2. **Fato trocado em 10:** a frase argumenta pelo rótulo certo, mas cita o que o par não diz (#2 "the man is
   carrying the animal", quando os cavalos puxam o homem; #13 chapéu e camisa vermelha que não existem).
3. **Não argumenta em 16, quase todos com rótulo previsto neutral (10 de 16 desse rótulo):** frase circular ou que
   se contradiz (#3 "selling a cart does not imply he is selling a cart"; #47 "A woman can be a young woman or a
   young woman, not necessarily a young woman"), ou o molde de contradição sem conclusão (#19, #23).
4. **O texto segue um molde por rótulo**: entailment "X is a person, and ... so ..."; neutral "... can be ..., not
   necessarily ..."; contradiction "... requires ..., while ..., making both impossible simultaneously". O molde
   vem do lote do Qwen: nas 16.000 justificativas de treino, "simultaneous" está em 44,8% das de contradiction (0,4%
   e 1,4% nas outras) e "not necessarily" em 17,7% das de neutral (0,5% nas outras). Na leitura, a forma acompanha o
   rótulo na maior parte dos pares; o conteúdo é o que mais falha.
5. **Fora da leitura, só descrito (conta por expressões, nos 200):** o molde da justificativa coincide com o rótulo
   previsto em 148 de 200 e com o rótulo certo em 140. A conta é grosseira (uma lista de expressões feita pelo
   Claude depois de ler), não substitui a leitura.

**O que isso sustenta:** o decoder ligado direto ao BERT, sem o rótulo na entrada, aprende a forma da justificativa
de cada rótulo e acerta o conteúdo em cerca de 4 de cada 10 pares. **O que não sustenta:** comparação em número
com o EIDRR (outra escala, outra tarefa, avaliadores humanos treinados); que uma camada de ponte ou o rótulo
previsto na entrada do decoder melhorariam (não rodou); fidelidade ao que o classificador usou.

---

# T5 sozinho contra o decoder ligado ao BERT (critério escrito em 18/11, 22:00, antes de codar e de rodar)

**Procedência.** Pedro (18/11): "teria que comparar com o t5 sem nada pra n precisar julgar as justificativas";
"pode rodar o mais pesado lá" (PC do Marcelo). Medidas, juiz e cortes são escolha do Claude.

**Pergunta:** pôr o BERT no lugar do encoder do T5 piora a justificativa gerada?

## Os dois geradores

| Gerador | O que é | Treino |
|---|---|---|
| T5 sozinho | `google-t5/t5-base` inteiro (encoder e decoder), lê o par e gera a justificativa do Qwen; sem classificação | os mesmos 16.000 pares, 4.000 passos, lote 32, taxa 5e-5 com aquecimento de 500 passos, decaimento 0,001, corte de gradiente 1,0, bf16; semente 1 |
| BERT + decoder | o modelo da seção anterior (pesos salvos no PC do Marcelo) | receita do Agrawal; o decoder só treina com peso 0,1 depois do passo 1.200 |

Diferenças declaradas: o T5 sozinho treina só para gerar, do primeiro ao último passo, com o próprio encoder (que
também treina, com o mesmo decaimento 0,001; o BERT do outro gerador tem 0); o decoder do outro gerador divide o
treino com a classificação. **Máquina:** o PC do Pedro (RTX 5060), porque a GPU do Marcelo estava em uso (Pedro: "roda no
meu entao"); o BERT + decoder foi treinado e gerou no PC do Marcelo. O `t5-base` foi pré-treinado vendo
MNLI com rótulo, então o T5 sozinho tem essa vantagem no encoder; no outro, o encoder é o BERT.

## Medidas (os mesmos 200 pares do dev da seção anterior)

1. **Principal, qual rótulo a justificativa defende, julgado por um modelo:** o juiz é o professor BERT base de hoje
   que lê o par + a justificativa (`professor-justificativa-4000.pt`), que segue a justificativa em 94,6% dos pares
   quando ela contradiz o par. Para cada justificativa gerada, a resposta do juiz é "o rótulo que ela defende". A
   medida é a parte dos 200 em que esse rótulo é o certo. Referência: o mesmo juiz com a primeira explicação humana
   do e-SNLI no lugar da gerada.
2. **Secundária, perda nas explicações humanas:** a perda média por token de cada decoder na primeira explicação
   humana de todos os 9.842 pares do dev (texto que nenhum dos dois viu; mesmo tokenizador do T5 dos dois lados).

**Regra de leitura:**

| Resultado | Leitura |
|---|---|
| Medida 1: T5 sozinho menos BERT + decoder com o intervalo de 95% (pareado por par, reamostragem) inteiro acima de zero | o BERT no lugar do encoder piora a justificativa, no rótulo que ela defende |
| Intervalo inteiro abaixo de zero | o BERT + decoder gera justificativas que defendem o rótulo certo mais vezes |
| Intervalo cruza o zero | sem diferença visível com 200 pares |
| Medida 2 no mesmo sentido da 1, com intervalo fora do zero | reforça; em sentido contrário, as duas ficam descritas e nenhuma decide |

## O que não responde

- Fato inventado: o juiz vê o rótulo que a frase defende, não se ela inventa detalhe.
- O juiz foi treinado com justificativas do Qwen de outros pares; justificativas geradas são texto fora do que ele viu.
- Uma semente de cada gerador; 200 pares na medida principal.

## Resultado da comparação (18/11, 22:30; PC do Pedro, 27 minutos)

**Conferido:** os três arquivos copiados do PC (`comparacao-t5-sozinho.csv`, `t5-sozinho-geradas.csv`,
`perdas-explicacao-humana.csv`); os 200 pares das duas fontes na mesma ordem (por `idx`); nenhuma justificativa
vazia ou de até 5 palavras nos dois geradores (21,0 e 20,9 palavras em média), o cuidado que a auditoria pediu; a
auditoria de treino antes de lançar (um bloqueio, o aquecimento de 400 em vez de 500 passos, corrigido antes).
**Não conferido:** nenhuma justificativa do T5 sozinho foi lida além das seis primeiras; uma semente de cada.

**Como ler:** medida 1 é a parte dos 200 pares em que o juiz (o professor que lê o par + a justificativa) dá o
rótulo certo quando lê a justificativa daquela fonte; medida 2 é a perda média por token de cada decoder na primeira
explicação humana dos 9.842 pares do dev (menor é melhor). Diferença = T5 sozinho menos BERT + decoder, pareada por
par, com intervalo de 95% por reamostragem.

| Fonte | Medida 1: juiz dá o rótulo certo | Medida 2: perda por token na explicação humana |
|---|---|---|
| T5 sozinho | 73,5% | 2,84 |
| BERT + decoder | 71,5% | 3,16 |
| Explicação humana (referência) | 87,5% | — |
| **Diferença** | **+2,0 pontos (−5,0 a +9,0)** | **−0,32 (−0,33 a −0,31)** |

1. **Pela regra escrita antes, sem diferença visível com 200 pares** na medida principal: o intervalo cruza o zero.
   Os dois acertam juntos em 121 pares, erram juntos em 31; o T5 sozinho acerta sozinho em 26 e o BERT + decoder em
   22.
2. **A medida 2 aponta para o mesmo lado e fica fora do zero:** o T5 sozinho acha a explicação humana mais provável
   (perda 10% menor). Pela regra ela só reforça se a medida 1 tiver decidido; como não decidiu, fica descrita.
3. **Fora do critério, só descrito:** o juiz lendo a justificativa do BERT + decoder concorda com o rótulo que o
   próprio classificador dele deu em 74,5% dos pares (o classificador acerta 88,5%). A justificativa gerada e a
   decisão do classificador divergem em um quarto dos pares.
4. **O juiz tem teto:** com a explicação humana ele dá o rótulo certo em 87,5%, não em 100%. Parte do que falta nas
   duas fontes é do juiz, não do texto.

**O que isso sustenta:** com esta medida e 200 pares, pôr o BERT no lugar do encoder do T5 não muda de forma visível
quantas justificativas defendem o rótulo certo; o T5 sozinho modela um pouco melhor o texto humano. **O que não
sustenta:** comparação com o EIDRR (lá a diferença de qualidade sem a ponte era grande; aqui a medida é outra e não
lê fato inventado); que uma ponte melhoraria; diferença menor que uns 7 pontos na medida 1 (o intervalo tem 14
pontos de largura).
