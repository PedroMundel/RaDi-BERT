# Professor que lê a justificativa: os dois testes baratos (desenho e critério escritos em 18/11, antes de codar e de rodar)

**Procedência.** A ideia de um professor que lê a entrada mais a justificativa e de um aluno que lê só a entrada vem
do KNIFE (Chan et al., 2022), que aqui é **nível 3**: só o resumo foi lido
(`docs/pesquisa/2026-11-10-combinar-sinais-racionalizacao-encoder.md`). Nada deste arquivo descreve o método deles;
não citar em texto assinado antes de ler. O Pedro confirmou em 18/11 a escolha desta linha e os dois testes, para
rodar no PC do Marcelo. O desenho, os controles e os números de corte abaixo são do Claude (o Pedro pediu para não
ver critério, salvo decisão que o Claude não queira tomar).

**Estado (18/11, 19:40): codado e rodado no PC do Marcelo depois deste texto; o desenho e as regras abaixo não
foram mudados. Leitura no fim de `resultados/rte-pequenos/leitura-grade.md`. Uma diferença do que está na seção
"Código": a coluna da justificativa continua nos dados (o passo de treino conta os tokens dela mesmo sem decoder),
como em todos os professores anteriores.**

## Por que dois testes antes de destilar

A destilação que deu positivo até aqui usa um BERT base que lê só o par. Trocar por um professor que também lê a
justificativa só faz sentido se duas coisas forem verdade, e as duas se medem sem treinar aluno nenhum:

1. **As respostas do professor ainda dizem algo além do rótulo.** Se, lendo a justificativa, ele acerta quase tudo,
   imitar as respostas dele é o mesmo que treinar no rótulo, o que o aluno já faz.
2. **O interior do professor, nas posições do par, muda com o que a justificativa diz.** O aluno só tem as posições
   do par. Se ali dentro nada muda quando a justificativa muda, não há o que imitar.

## O que foi conferido antes de escrever (18/11, notebook, só leitura)

- Os três conjuntos de 4.000 pares que entram (o do aluno, o do professor e o de escolha) têm justificativa do Qwen
  em todos os pares. **O dev do e-SNLI não tem**, então o professor que lê a justificativa não pode ser medido no
  dev: mede-se no conjunto de escolha e nos pares do aluno, que ele nunca treina.
- A justificativa entra no fim: `[CLS] premissa [SEP] hipótese [SEP] justificativa [SEP]`. Nos 4.000 pares do
  professor, os tokens do par ficam **nas mesmas posições** com e sem a justificativa (4.000 de 4.000), e o texto
  `[SEP]` dentro da segunda frase vira o token separador (3 separadores em todas). A entrada passa de 26 para 52
  tokens em média, máximo 124.
- Referência já medida (16/11, no PC): o professor que lê só o par acerta 79,2% no dev, 78,0% no conjunto de escolha
  e 79,1% nos pares do aluno, com confiança média de 97,6%. Ou seja, **confiança alta não serve de sinal** de que a
  resposta virou o rótulo: esse professor já é confiante e mesmo assim as respostas dele deram +1,6 ponto.
- Só com as palavras novas da justificativa, uma regressão acerta 76,4% do rótulo (17/11). A justificativa entrega
  boa parte do rótulo; o teste (a) mede quanto, para um BERT.
- PC do Marcelo às 19:15: GPU livre (888 MiB, 7%), o CSV das justificativas está lá, o arquivo do professor de
  16/11 **não** está (não faz falta: o professor de referência é treinado de novo lá, ver abaixo).

**Não conferido:** o tempo de treino de um BERT base nos 4.000 pares (nunca foi gravado separado); se o código do PC
do Marcelo segue igual ao do notebook desde as 17:45.

## Teste (a): o professor que lê a justificativa acerta quanto?

Três professores BERT base, cada um com 3 sementes, treinados nos 4.000 pares do professor (os mesmos de 16/11,
nenhum deles do aluno), com o treino de sempre (1.000 passos):

| Professor | O que ele lê |
|---|---|
| Par | premissa e hipótese (o professor de hoje, treinado de novo na mesma máquina) |
| Par + justificativa | premissa, hipótese e a justificativa do Qwen daquele par |
| Só justificativa | a justificativa sozinha, sem o par |

Como ler: o terceiro existe para saber quanto do acerto vem de ler o rótulo na justificativa sem precisar do par.

Medidas: acurácia nos pares do aluno (decide) e no conjunto de escolha (confirma), média das 3 sementes.

No professor "par + justificativa", sem treinar nada a mais, a justificativa é trocada na hora da prova:

| Troca na prova | O que mostra |
|---|---|
| Justificativa de outro par do **mesmo** rótulo | se a acurácia não cai, ele usa a justificativa só como rótulo |
| Justificativa de outro par de **outro** rótulo | em quantos pares a resposta segue a justificativa e não o par |

**Regra de leitura (acurácia nos pares do aluno):**

| Resultado | Leitura |
|---|---|
| "Par + justificativa" não passa de "par" em 2 pontos, ou não fica acima nas 3 sementes | a justificativa não ajuda nem o professor; a linha para aqui |
| "Par + justificativa" em 97% ou mais | as respostas dele são o rótulo em quase todo par; destilar respostas não serve, só sobra o interior (teste b) |
| Entre os dois | as respostas são candidatas a destilar |
| "Par + justificativa" menos "só justificativa" abaixo de 1 ponto | ele não precisa do par; lê o rótulo na justificativa |

Os cortes (2 pontos, 97%, 1 ponto) são escolha do Claude, sem base em medida anterior de ruído entre sementes do
BERT base nesta tarefa (o professor de 16/11 teve uma semente só). As três sementes do professor "par" dão essa
medida pela primeira vez; se o desvio entre elas passar de 1 ponto, a primeira e a última linha ficam sem leitura.

## Teste (b): o interior nas posições do par muda com a justificativa?

Sem treino novo. Usa o professor "par + justificativa" da semente 1 e os 4.000 pares do conjunto de escolha. Cada
par passa três vezes: com a justificativa dele, com a de outro par do mesmo rótulo, com a de outro par de outro
rótulo. Nas camadas 3, 6, 9 e 12 (as que o aluno imita na "sequência"), **só nas posições do par**, mede-se a
distância (1 menos o cosseno) entre o vetor com a justificativa certa e o vetor com a trocada. O `[CLS]` é medido à
parte. Junto, por camada, quanto da atenção das posições do par vai para as posições da justificativa.

Checagem embutida: na saída dos embeddings a distância tem de ser zero (mesmos tokens, mesmas posições); se não
for, a medida está errada.

**Regra de leitura (posições do par, as quatro camadas):**

| Resultado | Leitura |
|---|---|
| Com justificativa de outro rótulo a distância fica abaixo de 0,01 em todas as camadas | o interior nas posições do par quase não lê a justificativa; não há o que imitar |
| A distância com troca de mesmo rótulo fica abaixo de um quarto da distância com troca de outro rótulo, em todas as camadas | o que muda é só o rótulo; imitar o interior ensina o rótulo, não o motivo |
| Nenhuma das duas | o interior muda com o que a justificativa diz sobre o par |

Os cortes (0,01 e um quarto) são escolha do Claude, sem medida anterior que os sustente.

## O que estes testes não respondem

- **Se o aluno ganha nota.** Passar nos dois só diz que há algo para imitar. O ganho só se mede destilando, com o
  braço "sequência" de hoje como o que tem de ser batido (74,9% no conjunto de escolha, 15 sementes). Esse desenho
  não está escrito aqui.
- O teste (b) mede **mudança**, não utilidade: o interior pode mudar com a justificativa de um jeito que um aluno
  sem ela não consegue reproduzir.
- Um conjunto só (e-SNLI, 4.000 pares), justificativas de um modelo só (Qwen 35B, prompt F).
- A troca na prova tira o professor do que ele viu no treino (justificativa sempre certa); queda de acurácia com
  troca de outro rótulo é esperada e não é defeito.

## Código (a escrever, depois do sim do Pedro)

- `src/radibert/esnli_dados.py`: uma função que monta a entrada com a justificativa (no fim da segunda frase, ou
  sozinha) e uma que troca a justificativa por a de outro par de outro rótulo. A troca de mesmo rótulo já existe
  (`rte_dados.shuffle_within_label`).
- `resultados/rte-pequenos/medir_professor_justificativa.py`: treina os 9 professores (uma linha por professor num
  CSV, rodada retomável, `--fumaca` na CPU), faz as trocas na prova e a medida do teste (b). Reaproveita
  `treino.train`, `treino.predict`, `grade` e `run_encoder`; nada muda em `rte_treino.py` nem em `rte_destilacao.py`.
- Testes novos só das duas funções de dados (posições do par iguais; ninguém fica com justificativa do próprio
  rótulo na troca de outro rótulo).

## Rodada no PC do Marcelo

1. Fumaça na CPU do notebook, suíte verde.
2. Copiar por `scp` os arquivos mudados para `C:\RaDi-BERT`, conferir MD5.
3. Conferir a GPU dele na hora (é dele; às 19:15 estava livre).
4. `training-auditor` e lançamento pelo `train-watch`: são 9 treinos de BERT base. **Estimativa não medida:** 2 a 4
   minutos cada (os 16.000 pares sem decoder levaram 384 s no PC, com entrada de metade do tamanho), então 20 a 40
   minutos no total, mais as provas.
5. Copiar o CSV de volta, ler contra as regras acima, registrar no fim de
   `resultados/rte-pequenos/leitura-grade.md`.

---

# Destilação com o professor que lê a justificativa (desenho e critério escritos em 18/11, 19:50, antes de codar e de rodar)

**Procedência.** O Pedro pediu este desenho em 18/11, depois de ver os dois testes ("Desenhar a destilação"). Os
braços, o controle, os cortes e a máquina são escolha do Claude. **Nada codado, nada rodado.**

**Estado (18/11, 20:35): codado e rodado depois deste texto, sem mudar braços nem regra. Duas diferenças do que
está abaixo: a rodada foi dividida por semente entre as duas máquinas (combinado com o Pedro; 1 a 3 no PC dele, 4
e 5 no PC do Marcelo, com a "sequência" rodada de novo lá), e a atenção do professor é renormalizada em cada cabeça
antes da média das cabeças. Resultado: atrapalha (−2,7 pontos). Leitura no fim de
`resultados/rte-pequenos/leitura-grade.md`.**

## De onde parte

- O único positivo do projeto é a "sequência" (17/11): o BERT small passa 20 épocas imitando o interior de um BERT
  base que lê **só o par** (embeddings, atenção e estados internos das 4 camadas), e depois treina classificação
  mais as respostas desse professor. No conjunto de escolha: 74,9% com 15 sementes, contra 74,0% de "respostas" e
  74,1% do controle (fase 1 com um BERT base sem tarefa). Conferido hoje no `juntar-esnli-4000.csv`.
- Os dois testes de hoje dizem: as respostas do professor que lê a justificativa são quase o rótulo (96,7%), então
  não há por que destilá-las; o interior dele nas posições do par muda com o texto da justificativa.

**Pergunta:** trocar, **só na fase 1**, o professor que lê o par pelo professor que lê o par mais a justificativa
faz o aluno (que nunca lê a justificativa) passar da "sequência"?

## Braços

Tudo igual à "sequência" de 17/11 (mesmo aluno, mesmos 4.000 pares, mesmas perdas, 20 épocas de fase 1, mesma fase
2 com as respostas do professor que lê só o par). **Só muda de quem é o interior imitado na fase 1.**

| Braço | Interior imitado na fase 1 | Para que serve |
|---|---|---|
| Sequência (já rodada, 15 sementes) | professor que lê só o par | o braço a bater |
| Sequência com justificativa | professor que lê o par + a justificativa **daquele par**, só nas posições do par | o teste |
| Controle: justificativa trocada | o mesmo professor lendo o par + a justificativa de **outro par do mesmo rótulo** | se o teste passar: vem do que a justificativa diz sobre o par, ou de o interior carregar o rótulo? |

Como ler: o controle existe porque o professor que lê a justificativa sabe o rótulo em 96,7% dos pares, e esse
rótulo está no interior dele (na camada 12 a troca de rótulo muda três vezes mais que a troca de texto). Imitar o
interior pode ensinar o rótulo dos pares de treino por outro caminho, sem ensinar motivo nenhum. A justificativa de
outro par do mesmo rótulo leva o mesmo rótulo e nenhum conteúdo do par.

**Como o aluno imita só as posições do par:** os tokens do par ficam nas mesmas posições com e sem a justificativa
(conferido, 4.000 de 4.000). Dos estados internos e dos embeddings do professor usa-se só esse trecho. Da atenção
usa-se só o quadrado par-para-par, com cada linha dividida pela sua soma para voltar a somar 1 (de 20% a 46% da
atenção do professor vai para a justificativa, que o aluno não tem). **Essa renormalização é escolha do Claude:** a
alternativa seria tirar a perda de atenção, mas aí o braço mudaria duas coisas de uma vez em relação à "sequência".

**Professor:** o da semente 1 medido hoje (`professor-justificativa-4000.pt`, no PC do Marcelo). O professor que lê
só o par, na fase 2 de todos os braços, é o de 16/11 (o mesmo da "sequência").

## Onde roda

**No PC do Pedro** (escolha do Claude): a "sequência" e os controles de 17/11, com 15 sementes, rodaram lá, e o
arquivo do professor de 16/11 está lá (conferido às 19:45; GPU livre). Assim os braços novos, com as mesmas
sementes, ficam pareados com os antigos na mesma máquina. Custo: copiar os 436 MB do professor novo do PC do
Marcelo para o PC do Pedro. Diferença declarada: os dois professores foram treinados em máquinas diferentes (o de
16/11 no PC, o de hoje no PC do Marcelo); são arquivos fixos, iguais para todas as sementes.

## Regra de leitura (o conjunto de escolha decide, o dev confirma; a mesma da seção 11.5 do plano)

Desta vez o dev do e-SNLI serve: o aluno lê só o par.

| Resultado, com 5 sementes | Leitura |
|---|---|
| "Com justificativa" fica 0,5 ponto ou mais acima da "sequência" na média do conjunto de escolha, acima nas 5 sementes, e 0,5 ponto ou mais acima na média do dev | **Candidato.** Rodam as sementes 6 a 15 dele e do controle (a "sequência" já tem as 15); só conta como ganho se o intervalo de 95% da diferença nas 15 sementes não cruzar o zero |
| Candidato confirmado e o controle fica a menos de 0,5 ponto dele | Houve ganho, mas não vem do que a justificativa diz sobre o par |
| Candidato confirmado e o controle fica 0,5 ponto ou mais abaixo dele, com intervalo fora do zero | O conteúdo da justificativa chegou ao aluno pelo interior do professor |
| Menos de 0,5 ponto, ou sinal que troca entre sementes, ou o dev não confirma | **Não ajudou neste desenho** |
| 0,5 ponto ou mais **abaixo** da "sequência" nas 5 sementes | Imitar o interior do professor que lê a justificativa atrapalha |

Checagem embutida: a perda de imitação da fase 1 tem de cair nos dois braços novos (medida no mesmo lote fixo de
32 pares, antes e depois); se não cair, o braço não treinou e a nota não se lê.

## O que este desenho não responde

- Um professor só, de uma semente; um aluno (BERT small); um conjunto (e-SNLI, 4.000 pares).
- Se o teste não passar, vale para este jeito de imitar (as posições do par, estas perdas, 20 épocas), não para
  "professor que lê a justificativa" em geral.
- A renormalização da atenção muda o que o professor mostra; se o resultado for nulo, não se sabe se foi ela.

## Código (a escrever, depois do sim do Pedro)

- `src/radibert/rte_destilacao.py`: a `Distillation` ganha a opção de o professor receber outra entrada para o mesmo
  par (procurada pelo `idx`), cortar o resultado nas posições do par e renormalizar a atenção. Sem a opção, nada
  muda para os braços antigos.
- `resultados/rte-pequenos/medir_juntar.py`: dois braços novos (`sequence_rationale` e
  `sequence_rationale_shuffled`), que carregam o professor novo do arquivo.
- Testes: com a opção ligada e a justificativa vazia de efeito (professor recebendo a mesma entrada do aluno), as
  perdas têm de ser idênticas às de hoje; a atenção renormalizada soma 1 em cada linha real.
- Antes de lançar: fumaça na CPU, suíte verde, cópia para o PC com MD5, `training-auditor`, `train-watch`.

**Custo previsto (conta, não medida):** um aluno da "sequência" levou 277 s no PC; os braços novos passam o
professor em entradas com o dobro de tokens na fase 1. Estimativa de 5 a 6 minutos por aluno, 10 alunos, perto de
1 hora. Se houver candidato, mais 20 alunos.
