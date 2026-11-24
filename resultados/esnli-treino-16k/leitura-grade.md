# Leitura da grade do e-SNLI com 16.000 pares (10 treinos), 18/11/2026

**Procedência:** pedido do Pedro ("depois 16mil pares"); desenho em `docs/2026-11-18-gaps-da-argumentacao.md`,
"Gap 4". Treino nas 16.000 linhas do lote 35B (variante F), dev do e-SNLI (9.842 pares, 3 classes). BERT base, lote
32, 8 épocas = 4.000 passos, fase A 250, fase B 1.200, aquecimento `500` (Tabela 4), peso da L_aux 0,1, micro-lote
16, 5 sementes, PC, código `59278b8-dirty`, 3h23. CSVs copiados para `pc/`.

**A regra de leitura abaixo é a proposta do Claude na seção "Gap 4", escrita antes de rodar; o Pedro ainda não a
confirmou.** Os números não dependem dela; as frases "nulo" e "a H2 deixa de explicar" dependem.

**Conferido:** as 10 linhas de `pc/resultados.csv`, médias e diferenças pareadas calculadas sobre o arquivo; as
médias por grupo de `pc/gradientes.csv` nas 5 sementes; a mesma conta refeita sobre a grade de 4.000 pares de
10/11. **Não conferido:** `pc/palavras.csv` (medida por palavra, semente 1) não foi lido; o controle de calendário
não rodou (no braço com decoder o BERT tem 70% e a cabeça 56% da área de taxa com a L_cls ligada, conta da
auditoria de treino); a sonda da medida de gradiente são 63 pares sorteados do treino de cada grade, não os mesmos
pares nas duas.

## Classificação

**Como ler:** média de 5 sementes no dev, com o desvio padrão entre sementes; na linha da diferença, decoder menos
sem decoder, pareada por semente, com o intervalo de 95% e em quantas das 5 sementes o decoder vence.

| | ROC-AUC, 16.000 pares | Acurácia, 16.000 pares | ROC-AUC, 4.000 pares (10/11) | Acurácia, 4.000 pares (10/11) |
|---|---|---|---|---|
| BERT sem decoder | 0,929 ± 0,005 | 0,834 ± 0,003 | 0,916 ± 0,005 | 0,797 ± 0,009 |
| BERT com decoder | 0,932 ± 0,001 | 0,828 ± 0,003 | 0,909 ± 0,003 | 0,787 ± 0,003 |
| Decoder menos sem decoder | +0,003 (−0,004 a +0,010), vence 3 | −0,006 (−0,011 a +0,000), vence 1 | −0,007 (−0,015 a +0,002), vence 1 | −0,009 (−0,023 a +0,005), vence 1 |

1. **Nulo no ROC-AUC, pela regra proposta:** +0,003, intervalo cruzando o zero, vence em 3 de 5.
2. **Na acurácia a diferença é negativa e o intervalo encosta no zero** (−0,0112 a +0,0003); o decoder perde em 4
   das 5 sementes. As duas métricas apontam para lados opostos, as duas dentro ou na borda do ruído.
3. **Poder:** o +0,005 que o artigo mostra com baseline forte cabe no intervalo do ROC-AUC. A frase é "não
   distinguível com 5 sementes", não "não existe". Um ganho de 0,011 ou mais ficaria fora.
4. **Quatro vezes mais pares valem mais do que o decoder:** o BERT sem decoder sobe de 0,797 para 0,834 de
   acurácia.

## A H2 (a escala explicava o nulo?)

A H2 de `docs/2026-11-10-hipoteses-do-nulo.md` dizia: com poucos pares a fase A é curta, o decoder só aprende o
molde, e a parte da justificativa que carrega o motivo nunca vira sinal.

**Como ler:** perda do decoder em nats por token, média das 5 sementes, na sonda de 63 pares do treino, separada
pelo grupo da palavra-alvo; menor é melhor.

| Grupo da palavra-alvo | 4.000 pares, passo 1 | 4.000 pares, fim | 16.000 pares, passo 1 | 16.000 pares, fim |
|---|---|---|---|---|
| Copiada do par (C) | 7,44 | 3,63 | 5,66 | 2,01 |
| Nova, fora do par (N) | 7,40 | 3,94 | 5,45 | 3,14 |
| Expressão de rótulo (S) | 5,22 | 1,43 | 2,33 | 0,90 |
| Gramatical (F) | 3,17 | 1,71 | 2,14 | 1,40 |
| Todas | 5,15 | 2,50 | 3,43 | 1,79 |

5. **O decoder aprendeu bem mais do que com 4.000 pares, em todos os grupos.** As copiadas caem de 3,63 para 2,01
   e as novas de 3,94 para 3,14; as 5 sementes concordam (copiadas entre 1,95 e 2,11). A fase A mais longa também
   aparece: o decoder entra na fase B em 3,43, não em 5,15.
6. **E a classificação não ganhou.** Pela regra proposta ("se caírem e não houver ganho, a H2 deixa de explicar o
   nulo"), a escala curta não é a explicação: com a receita cabendo e o decoder lendo melhor o BERT, o resultado
   continua nulo.
7. **O empurrão da L_aux segue quase ortogonal ao da classificação:** cosseno médio na fase C entre +0,006 e
   +0,051 por semente (com 4.000 pares, +0,011 a +0,031).

**O que isso sustenta:** no e-SNLI, com BERT base, justificativas do Qwen e a receita do artigo cabendo inteira,
o decoder auxiliar aprende a gerar a justificativa melhor e o classificador não fica melhor por isso. **O que não
sustenta:** que o método não funcione em outra tarefa ou com outro professor; que meio ponto de ROC-AUC não exista
(5 sementes não o enxergam); nem que o calendário não pese aqui (o controle não rodou).

## Controle de calendário (18/11): o calendário ajuda, e descontado ele o decoder não ajuda

**Procedência:** decisão do Pedro ("faz so o controle de calendário"); critério escrito antes em
`docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 4b". Braço `bert_calendar`: BERT sem decoder com o calendário do
braço com decoder (nenhum passo de classificação nos passos 1 a 1.200; taxa do BERT com pico no passo 1.200). Mesmos
16.000 pares, mesmas 5 sementes, PC, 24 minutos; `../esnli-treino-16k-calendario/pc/resultados.csv`.

**Conferido:** as 15 linhas dos dois CSVs e as três diferenças pareadas calculadas sobre eles; a auditoria de
treino confirmou, por simulação, que o braço de calendário tem a mesma taxa do braço com decoder em todos os passos
de 1.201 a 4.000, os mesmos lotes na mesma ordem e a mesma cabeça inicial. **Não conferido:** por que o calendário
ajuda (nenhum teste); o mesmo controle com 4.000 pares.

**Como ler:** média de 5 sementes no dev do e-SNLI; nas linhas de diferença, pareada por semente, com o intervalo
de 95% e em quantas das 5 sementes a diferença é positiva.

| | ROC-AUC | Acurácia |
|---|---|---|
| BERT sem decoder | 0,929 ± 0,005 | 0,834 ± 0,003 |
| BERT sem decoder, com o calendário do decoder | 0,936 ± 0,005 | 0,837 ± 0,004 |
| BERT com decoder | 0,932 ± 0,001 | 0,828 ± 0,003 |
| Calendário menos BERT sem decoder | **+0,007 (+0,006 a +0,008), 5 de 5** | **+0,004 (+0,003 a +0,005), 5 de 5** |
| Decoder menos calendário | −0,004 (−0,011 a +0,003), 2 de 5 | **−0,009 (−0,016 a −0,003), 0 de 5** |
| Decoder menos BERT sem decoder (a comparação do gap 4) | +0,003 (−0,004 a +0,010), 3 de 5 | −0,006 (−0,011 a +0,000), 1 de 5 |

8. **O calendário não custa: ajuda.** Esperar 1.200 passos para começar a classificar, com o pico da taxa do BERT
   no passo 1.200, dá +0,007 de ROC-AUC e +0,4 ponto de acurácia, nas 5 sementes. **O critério não previa este
   caso** (as três leituras escritas antes supunham custo ou nenhum efeito); fica registrado como resultado fora do
   previsto. No RTE o mesmo controle tinha dado +0,010 com intervalo cruzando o zero.
9. **Com o mesmo calendário dos dois lados, o decoder não ajuda:** no ROC-AUC é nulo (intervalo cruzando o zero);
   na acurácia o intervalo fica inteiro abaixo de zero e o decoder perde nas 5 sementes (−0,9 ponto).
10. **O +0,003 de ROC-AUC do decoder no gap 4 era do calendário.** A diferença bruta somava duas coisas: +0,007 do
    calendário e −0,004 do decoder.
11. **Limites da comparação (da auditoria):** os dois braços diferem ainda no sorteio do dropout, no corte de
    gradiente (feito junto com o decoder) e no estado do otimizador do BERT ao fim da fase B. O intervalo estreito
    da primeira diferença vem também de os dois braços verem os mesmos lotes na mesma ordem a partir do passo 1.201.

**O que isso sustenta:** no e-SNLI com 16.000 pares, a parte do braço com decoder que melhora o ROC-AUC é o
calendário de treino, que funciona sem decoder e sem justificativa; o decoder em si não acrescenta e, na acurácia,
tira. **O que não sustenta:** por que o calendário ajuda (hipótese sem teste: menos passos de classificação decoram
menos o treino); que o mesmo valha no RTE ou com 4.000 pares; que valha para o artigo, cujo baseline não sabemos
como foi treinado.

## Justificativa embaralhada (18/11): o conteúdo importa, e o errado atrapalha bem mais que o certo

**Procedência:** decisão do Pedro ("Sim, 16 mil"); critério escrito antes de codar em
`docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 5", com a checagem corrigida antes de lançar. Braço
`bert_decoder_shuffled`: igual ao braço com decoder, mas o decoder gera a justificativa de outro par do mesmo
rótulo (troca fixa, semente 0). Mesmos 16.000 pares, mesmas 5 sementes, PC, 2h50;
`../esnli-treino-16k-embaralhado/pc/`.

**Conferido:** as 20 linhas dos três CSVs de resultado e as diferenças pareadas calculadas sobre eles; a perda do
decoder nas 5 sementes dos dois braços; a troca nos 16.000 pares (nenhum par com a própria justificativa); a
auditoria de treino confirmou que o braço é idêntico ao `bert_decoder` fora os alvos (modelo, taxas, ordem dos
lotes, metade da fase A). **Não conferido:** `pc/palavras.csv` não foi lido; a troca em qualquer rótulo (e não só
dentro do rótulo) não rodou; um braço com alvo sem relação nenhuma (texto aleatório) não rodou.

**A checagem de que a troca funcionou passa:** a perda do decoder em todas as palavras termina em 2,29 no
embaralhado (2,28 a 2,32 nas 5 sementes) contra 1,79 no real (1,77 a 1,82). Sem o par para ajudar, o decoder
prevê pior, como tinha de ser.

**Como ler:** média de 5 sementes no dev do e-SNLI; diferenças pareadas por semente, com intervalo de 95% e em
quantas das 5 sementes a diferença é positiva.

| | ROC-AUC | Acurácia |
|---|---|---|
| BERT sem decoder, com o calendário | 0,936 ± 0,005 | 0,837 ± 0,004 |
| BERT com decoder, justificativa do par | 0,932 ± 0,001 | 0,828 ± 0,003 |
| BERT com decoder, justificativa de outro par do mesmo rótulo | 0,916 ± 0,002 | 0,807 ± 0,006 |
| Real menos embaralhado | **+0,016 (+0,014 a +0,019), 5 de 5** | **+0,021 (+0,014 a +0,029), 5 de 5** |
| Embaralhado menos calendário | **−0,020 (−0,027 a −0,013), 0 de 5** | **−0,030 (−0,042 a −0,019), 0 de 5** |
| (gap 4b) Real menos calendário | −0,004 (−0,011 a +0,003), 2 de 5 | −0,009 (−0,016 a −0,003), 0 de 5 |

12. **O conteúdo específico do par muda o que o decoder faz com o classificador.** Com a justificativa de outro
    par, o classificador perde 2,1 pontos de acurácia em relação à justificativa certa, nas 5 sementes, com o
    intervalo longe do zero. Pelo critério, é o caso "real acima do embaralhado": a leitura "o classificador não
    usa o porquê" **não** se sustenta.
13. **Com a justificativa errada o decoder custa 3,0 pontos de acurácia em relação ao calendário; com a certa,
    0,9.** A troca é dentro do rótulo, então tudo o que a justificativa diz sobre o rótulo foi mantido: o que
    protege o classificador não é o rótulo escrito, é o texto casar com o par.
14. **O gradiente do decoder chega ao encoder com força para mover a nota.** Isso responde a uma objeção ao nulo
    ("o sinal do decoder é fraco demais para fazer diferença"): o mesmo caminho, com outro alvo, move a acurácia
    em pontos inteiros.
15. **Observação da sonda, uma leitura só:** no fim do treino a perda de classificação nos pares da sonda é 0,067
    no embaralhado e 0,001 no real, e a norma do gradiente de classificação é 4,1 contra 0,18. O braço embaralhado
    termina sem ter decorado o treino.

**O que isso sustenta:** o encoder é sensível ao que o decoder tem de gerar; uma justificativa que casa com o par
custa muito menos do que uma que não casa. **O que não sustenta:** que a justificativa certa ajude o classificador
(ela continua abaixo do calendário, na acurácia com intervalo fora do zero); nem que a diferença venha de a
justificativa certa "ensinar o motivo": ela também sai de a tarefa errada ser impossível de aprender a partir do
par e atrapalhar o encoder como ruído. Separar as duas coisas pede outro controle (por exemplo um alvo que se
aprende a partir do par mas não fala do rótulo), que não rodou.

## Curva de arranque (18/11): o decoder adianta o começo em passos, some em 100 passos e termina 0,9 ponto atrás

**Procedência:** pergunta do Pedro ("teria como calcular pra ver se ajuda ele a treinar mais rapido?"); critério
escrito antes de codar em `docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 6", com as escolhas do Claude.
`medir_curva.py`: os braços `bert_calendar` e `bert_decoder` de novo nos 16.000 pares, sementes 1 a 5, com a
acurácia no dev inteiro e a perda de classificação na sonda gravadas em 11 passos depois do início da classificação
(passo 1.201). **Duas máquinas:** sementes 1 a 3 no PC do Pedro (RTX 5060), sementes 4 e 5 no PC de um amigo dele
(RTX 5060 Ti, `ssh amigo`); cada semente tem os dois braços na mesma máquina. Dados em
`../esnli-treino-16k-curva/pc/curva.csv` e `../esnli-treino-16k-curva/amigo/curva.csv`.

**Conferido:** as 110 linhas usadas (55 por braço) e as diferenças pareadas calculadas sobre elas; a conferência do
instrumento (a perda da sonda medida pelo script novo e a da medida de gradiente antiga, na mesma rodada, diferem
no máximo 0,001 em 55 pontos); a auditoria de treino confirmou que a medida é feita numa cópia e não altera o
treino na GPU. **Não conferido:** o que acontece entre os passos 1.201 e 1.225 (nada é gravado ali); a mesma curva
no braço embaralhado; a auditoria de treino não foi refeita para a segunda máquina (mesmo script, MD5 igual).

**Como ler:** acurácia no dev do e-SNLI, em %, média das 5 sementes; a diferença é decoder menos calendário,
pareada por semente, com o intervalo de 95% e em quantas das 5 sementes é positiva.

| Passo | Sem decoder (calendário) | Com decoder | Diferença |
|---|---|---|---|
| 1.225 | 56,4 | 71,8 | +15,4 (+9,9 a +20,9), 5 de 5 |
| 1.250 | 69,7 | 75,3 | +5,6 (+3,8 a +7,4), 5 de 5 |
| 1.300 | 76,5 | 76,7 | +0,2 (−0,6 a +1,0), 4 de 5 |
| 1.400 | 78,5 | 78,6 | +0,1 (−1,8 a +1,9), 3 de 5 |
| 1.500 | 80,5 | 80,0 | −0,5 (−1,1 a +0,2), 1 de 5 |
| 2.000 | 83,2 | 82,4 | −0,8 (−1,9 a +0,3), 1 de 5 |
| 2.500 | 83,3 | 82,4 | −1,0 (−1,6 a −0,4), 0 de 5 |
| 3.000 | 83,6 | 82,6 | −1,0 (−1,4 a −0,5), 0 de 5 |
| 4.000 | 83,7 | 82,9 | −0,9 (−1,6 a −0,1), 0 de 5 |
| **Principal: média dos passos 1.225 a 1.500** | 72,3 | 76,5 | **+4,1 (+3,3 a +5,0), 5 de 5** |

16. **Pela regra escrita antes, o decoder faz a classificação arrancar mais rápido:** a média dos cinco primeiros
    passos medidos fica 4,1 pontos acima, com o intervalo inteiro acima de zero, nas 5 sementes. A vantagem está
    toda nos primeiros 50 passos (+15,4 no passo 1.225, +5,6 no 1.250).
17. **No passo 1.300 os dois braços empatam, e do 2.500 em diante o braço sem decoder fica cerca de 1 ponto à
    frente,** com intervalo fora do zero. O passo 4.000 repete a diferença medida de manhã (−0,9).
18. **A medida secundária aponta para o outro lado:** o braço sem decoder chega a 80% de acurácia no mesmo passo
    medido ou antes, nas 5 sementes (1.400 ou 1.500, contra 1.500 a 2.000 do braço com decoder).
19. **Em tempo de relógio a vantagem não existe.** Os 1.200 passos da fase B, que o braço sem decoder pula, custam
    de 7,5 a 10,5 minutos; o braço sem decoder termina o treino inteiro (83,7%) em 4,5 a 5,5 minutos, antes de o
    braço com decoder dar o primeiro passo de classificação. "Mais rápido" vale em passos de classificação.
20. **Variação entre as duas placas, no mesmo braço e semente** (calendário, sementes 4 e 5): até 4,4 pontos no
    passo 1.225 e no máximo 0,6 do passo 1.400 em diante. O começo da curva é o trecho mais ruidoso.

**O que isso sustenta:** o encoder sai da fase em que só o decoder o treinou mais pronto para classificar (15
pontos de vantagem nos primeiros 25 passos), e o classificador sem decoder recupera essa diferença em cerca de 100
passos e termina na frente. É a leitura do Pedro, "o encoder aprenderia isso de qualquer forma", para esta escala.
**O que não sustenta:** que a vantagem inicial venha do conteúdo da justificativa (o braço embaralhado não tem
curva); que valha com poucos pares, onde 100 passos de classificação pesam mais (com 4.000 pares a diferença final
também foi negativa, mas a curva não foi medida); nem ganho de nota final.

## Curva de arranque do braço embaralhado (18/11, 3 sementes): a vantagem do começo vem do conteúdo da justificativa

**Procedência:** pedido do Pedro ("pode criar todos", as figuras que faltavam para o artigo); critério escrito antes
em `docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 6b", com as escolhas do Claude. Braço `bert_decoder_shuffled`
com as mesmas 11 medidas no dev. **Só as sementes 1 a 3, todas no PC**, onde os outros dois braços dessas sementes
também rodaram; 1h38. As sementes 4 e 5 não rodaram (decisão do Pedro em aberto).

**Conferido:** as 33 linhas novas de `../esnli-treino-16k-curva/pc/curva.csv` e as diferenças pareadas calculadas
sobre os três braços nas sementes 1 a 3; o instrumento (perda da sonda contra a medida de gradiente da mesma
rodada: diferença máxima 0,001); o passo 4.000 do embaralhado (81,0 a 81,5) repete a nota final da grade (80,7 ±
0,6) dentro do ruído. **Não conferido:** com 3 sementes os intervalos são largos e um efeito de 2 pontos não se
distingue; as sementes 4 e 5.

**Como ler:** acurácia no dev, em %, média das sementes 1 a 3; diferenças pareadas por semente com intervalo de 95%.

| Passo | Sem decoder (calendário) | Com decoder, justificativa do par | Com decoder, justificativa de outro par |
|---|---|---|---|
| 1.225 | 56,8 | 70,5 | 60,7 |
| 1.250 | 69,6 | 75,3 | 64,8 |
| 1.300 | 76,7 | 76,7 | 72,2 |
| 1.500 | 80,6 | 80,4 | 77,5 |
| 2.000 | 83,1 | 82,5 | 80,6 |
| 4.000 | 83,7 | 83,2 | 81,3 |

| Medida principal: acurácia média nos passos 1.225 a 1.500 | Diferença |
|---|---|
| Decoder real menos embaralhado | **+6,2 (+4,0 a +8,3), 3 de 3** |
| Embaralhado menos calendário | −2,3 (−5,5 a +1,0), 0 de 3 |

21. **Pela regra escrita antes, o arranque depende de a justificativa ser a do par:** o decoder com a justificativa
    certa fica 6,2 pontos acima do embaralhado nos primeiros passos, com o intervalo inteiro acima de zero.
22. **Com a justificativa trocada o decoder não adianta nada.** O embaralhado fica abaixo do calendário nas 3
    sementes na medida principal, com o intervalo cruzando o zero (3 sementes); do passo 1.300 em diante a
    diferença é de −4,5 pontos com intervalo fora do zero, e no fim de −2,4.
23. **Então a vantagem inicial do decoder não vem de "qualquer tarefa de geração antes da classificação".** Vem de
    gerar a justificativa daquele par. É o primeiro resultado em que o conteúdo certo ajuda em relação ao braço sem
    decoder, e dura cerca de 100 passos.

**O que isso sustenta:** a justificativa do par carrega algo que o encoder aproveita para classificar, e ele chega
ao mesmo lugar sozinho em cerca de 100 passos de classificação. **O que não sustenta:** ganho de nota final; nem
que valha com poucos pares (a curva só foi medida com 16.000).

## Pior classe (19/11, medida 4 do painel do Gap 8): com decoder a pior classe fica pior, como a acurácia

**Procedência:** quarta medida do painel escolhida pelo Pedro em 19/11 ("A"); critério escrito antes de ler as colunas,
em `docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 8, versão final do painel". Nenhum treino novo: são as colunas
`f1_*` dos `resultados.csv` das grades de 18/11 (`pc/`, `../esnli-treino-16k-calendario/pc/`,
`../esnli-treino-16k-embaralhado/pc/`), que nunca tinham sido lidas.

**Conferido:** as 20 linhas (4 braços, sementes 1 a 5) e as diferenças pareadas calculadas sobre elas. **Não
conferido:** o recall por classe (não está gravado; sai dos pesos da rodada de 19/11); a conferência com a rodada de
19/11, que o critério pede; o MNLI.

**Como ler:** F1 de cada classe no dev do e-SNLI, média das 5 sementes; "pior classe" é o menor dos três F1 de cada
modelo (em todos os 20 modelos é a classe neutra); nas linhas de diferença, pareada por semente, com intervalo de
95% e em quantas das 5 sementes é positiva.

| | F1 entailment | F1 neutral (a pior classe) | F1 contradiction |
|---|---|---|---|
| Sem decoder, treino comum | 0,858 | 0,795 | 0,848 |
| Sem decoder, mesmo calendário | 0,860 | 0,799 | 0,854 |
| Com decoder, justificativa do par | 0,857 | 0,790 | 0,838 |
| Com decoder, justificativa de outro par | 0,843 | 0,763 | 0,817 |
| Decoder menos calendário | −0,003 (−0,006 a +0,000), 1 de 5 | **−0,009 (−0,017 a −0,001), 1 de 5** | **−0,015 (−0,025 a −0,005), 0 de 5** |
| Decoder real menos embaralhado | +0,014 (+0,008 a +0,020), 5 de 5 | **+0,027 (+0,018 a +0,036), 5 de 5** | +0,022 (+0,013 a +0,030), 5 de 5 |

24. **Pela regra escrita antes, na medida 4 o decoder piora:** a pior classe (neutra) perde 0,9 ponto de F1 contra
    o calendário, com o intervalo inteiro abaixo de zero. Não é candidato; é o lado ruim.
25. **A medida repete a acurácia,** como o critério avisava que podia acontecer (−0,9 ponto de acurácia na mesma
    comparação). Não mostra um lugar novo onde o sinal aparece.
26. **Só descrito:** a classe que mais perde com o decoder é a contradição (−1,5 ponto, nas 5 sementes), não a pior;
    a de entailment quase não muda. Na comparação com o embaralhado as três classes ganham.

## Fora de domínio (19/11, Gap 7): no MNLI o decoder atrapalha, 1,5 ponto abaixo do calendário; no RTE não se distingue

**Procedência:** decisão do Pedro em 18/11 ("acho que tem que rodar tbm"); critério em
`docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 7" (versão 2, com o MNLI como conjunto principal, escrito antes de
existir número de braço com decoder). Os braços `bert`, `bert_calendar` e `bert_decoder` treinados de novo nos 16.000
pares, sementes 1 a 5, no PC do Pedro, com `--fora --salvar-pesos`; MNLI e HANS medidos depois, a partir dos pesos
(`avaliar_fora.py`). Arquivos copiados para `../esnli-treino-16k-fora-pesos/pc/` e
`../esnli-treino-16k-calendario-fora-pesos/pc/`; contas de `ler_fora.py pc`.

**Conferido:** as 15 linhas de resultado e as 15 de `mnli-hans.csv`; conferência 1 (a acurácia no dev repete a de
18/11: −0,04, +0,04 e +0,11 ponto, limite 0,6); conferência 2 (cada classificador recarregado repete a acurácia
gravada no treino: diferença máxima 0,00000). **Não conferido:** o braço embaralhado (roda no PC do Marcelo, não
terminou); nenhum par do MNLI ou do RTE foi lido; a auditoria de treino não foi refeita para o relançamento em duas
partes (mesmo código de treino).

**Como ler:** média das 5 sementes; no MNLI, acurácia de 3 classes nos 19.647 pares das duas validações (acaso
33%); no RTE, ROC-AUC e acurácia nos 2.747 pares, com o modelo de 3 classes lido em 2 rótulos; no HANS, acurácia
nos 15.000 pares de não-entailment. Diferenças pareadas por semente, com intervalo de 95% e em quantas das 5
sementes são positivas.

| | Dev do e-SNLI, acurácia | **MNLI, acurácia (o conjunto que decide)** | RTE, ROC-AUC | RTE, acurácia | HANS, não-entailment |
|---|---|---|---|---|---|
| Sem decoder, treino comum | 83,4% | 64,9% | 0,697 | 65,3% | 2,2% |
| Sem decoder, mesmo calendário | 83,7% | 65,0% | 0,699 | 65,4% | 0,4% |
| Com decoder, justificativa do par | 82,9% | 63,5% | 0,690 | 65,0% | 0,9% |
| **Decoder menos calendário** | −0,8 (−1,4 a −0,2), 0 de 5 | **−1,5 (−2,3 a −0,7), 0 de 5** | −0,010 (−0,022 a +0,002), 1 de 5 | −0,5 (−1,4 a +0,5), 1 de 5 | +0,4 (−0,6 a +1,5), 3 de 5 |
| Calendário menos sem decoder | +0,4 (+0,3 a +0,5), 5 de 5 | +0,1 (−1,6 a +1,8), 2 de 5 | +0,003 (−0,003 a +0,009), 4 de 5 | +0,1 (−1,3 a +1,5), 3 de 5 | −1,7 (−4,1 a +0,6), 0 de 5 |

27. **Pela regra escrita antes, fora de domínio o decoder atrapalha:** no MNLI, o conjunto que decide, ele fica 1,5
    ponto abaixo do calendário, com o intervalo inteiro abaixo de zero, nas 5 sementes. As duas validações dão o
    mesmo (matched −1,5; mismatched −1,5) e o ROC-AUC no MNLI também (−0,013, intervalo fora do zero).
28. **A perda fora é maior que a de dentro:** −1,5 ponto no MNLI contra −0,8 no dev do e-SNLI, nos mesmos modelos.
    A diferença entre as duas quedas não tem critério nem intervalo; fica descrita.
29. **No RTE não se distingue:** −0,010 de ROC-AUC, com o intervalo cruzando o zero por pouco; a metade do intervalo
    é 0,012, então um efeito menor que isso não se vê ali. O sinal é o mesmo do MNLI.
30. **O HANS ficou no piso, como o critério previa:** os três braços respondem "entailment" em 98% a 99,6% dos pares
    de não-entailment. Não diz nada sobre atalho.
31. **O ganho do calendário não aparece fora:** +0,1 ponto no MNLI, com intervalo de ±1,7. Dentro ele se repetiu
    (+0,4 ponto, 5 de 5).
32. **Não há candidato**, então as sementes 6 a 15 não rodam.

**O que isso sustenta:** com esta receita, um LLM e um prompt, o decoder auxiliar não ajuda o classificador fora do
domínio de treino; no conjunto maior e de mesmo rótulo ele piora, e mais do que piora dentro. A pendência 10 do
`tema-v3` fica respondida para esta receita: "não ajuda dentro nem fora, nos conjuntos medidos". **O que não
sustenta:** que seja assim com poucos rótulos, com outro LLM ou com outro jeito de usar a justificativa; que o HANS
ou um conjunto mais distante dariam o mesmo; nem o porquê de a queda ser maior fora (sem teste).

## Painel fora da acurácia (19/11, Gap 8): três medidas do lado ruim e uma nula; nenhum candidato

**Procedência:** pergunta do Pedro ("será que a gente n ta olhando pra métrica errada tbm?") e o painel que ele
fechou: robustez fora de domínio, calibração, predição seletiva e pior classe; critério em
`docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 8, versão final do painel", escrito antes de qualquer script. Os 15
classificadores do PC do Pedro (sem decoder, calendário e decoder, sementes 1 a 5), lidos dos pesos por
`painel_pesos.py`; `../esnli-treino-16k-fora-pesos/pc/painel.csv`; contas de `ler_fora.py pc`.

**Conferido:** as 15 linhas do painel; cada classificador recarregado repete a acurácia gravada no treino
(diferença máxima 0,00000); a conferência da medida 4 com a rodada de 19/11 (o sinal se repete). **Não conferido:**
o braço embaralhado (PC do Marcelo, não terminou); a ECE com outro número de faixas (o critério fixa 15).

**Como ler:** média das 5 sementes no dev do e-SNLI; ECE é o erro de calibração (0 = a confiança bate com o acerto;
menor é melhor); a predição seletiva é o ROC-AUC da confiança para separar acertos de erros (0,5 = acaso; maior é
melhor); pior classe é o menor F1 das três classes. Diferença = decoder menos calendário, pareada por semente, com
intervalo de 95% e em quantas das 5 sementes é positiva.

| # | Medida (lado bom) | Calendário | Decoder | Decoder menos calendário | Pelo critério |
|---|---|---|---|---|---|
| 1 | Robustez: acurácia no MNLI (maior) | 65,0% | 63,5% | −1,5 ponto (−2,3 a −0,7), 0 de 5 | **piora** |
| 2 | Calibração: ECE no dev (menor) | 0,142 | 0,152 | +0,010 (+0,003 a +0,017), 5 de 5 | **piora** |
| 3 | Predição seletiva: ROC-AUC da confiança no dev (maior) | 0,742 | 0,737 | −0,005 (−0,029 a +0,019), 2 de 5 | nulo; não distinguível até 0,024 |
| 4 | Pior classe: menor F1 no dev (maior) | 0,799 | 0,790 | −0,009 (−0,013 a −0,005), 0 de 5 | **piora**, e repete a de 18/11 (−0,009) |

33. **Nenhuma das quatro medidas é candidata.** Três ficam do lado ruim com o intervalo fora do zero, e a predição
    seletiva é nula. O sinal do treino com decoder não apareceu em nenhum dos quatro lugares escolhidos.
34. **No MNLI as três medidas "ao lado" apontam para o mesmo lado:** ECE +0,015 (+0,004 a +0,027), confiança −0,011
    (−0,019 a −0,003) e pior classe −2,6 pontos de F1 (−4,3 a −0,9).
35. **Recall por classe, só descrito:** entailment −0,5 ponto, neutral −0,5, contradiction −1,4; os três intervalos
    cruzam o zero.
36. **B não é relatada** (a medida 3 não deu candidato). **C foi medida porque nada deu certo, sem teste:** a fração
    dos pares do dev em que duas sementes do mesmo braço discordam é 9,3% sem decoder, 9,1% no calendário e 9,5% com
    decoder; no MNLI, 17,0%, 16,6% e 16,4%. Não há diferença que se veja.
37. **Fora do critério, visto depois e só descrito:** o calendário sozinho, contra o treino comum, melhora a
    calibração (ECE −0,012, de −0,014 a −0,010, 0 de 5 positivas) e a predição seletiva (+0,022, de +0,012 a
    +0,032, 5 de 5). Essa comparação não estava entre as do painel; fica como observação, sem valer como resultado.
38. **Os modelos são confiantes demais:** ECE de 0,14 a 0,15 no dev e de 0,29 a 0,31 no MNLI, nos três braços.

**O que isso sustenta:** nas quatro medidas que o Pedro escolheu, gerar a justificativa como tarefa auxiliar não
melhora o classificador, e em três delas piora um pouco. **O que não sustenta:** que não haja outra medida em que
ajude (a regra de parada fecha o painel nestas quatro); que as pioras em calibração e pior classe sejam algo além da
perda de acurácia (as três andam juntas); nem nada sobre o braço embaralhado, que falta.

## Braço embaralhado fora de domínio (19/11): a conferência do instrumento não passa por 0,03 ponto; os números ficam só descritos

**Procedência:** critério em `docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 7", com a "Mudança de máquina" escrita
antes de rodar. O braço embaralhado (5 sementes) e o calendário de âncora (5 sementes) rodaram no PC do Marcelo
(RTX 5060 Ti), das 02:08 às 05:40, e os pesos foram avaliados lá (MNLI, HANS, painel). Arquivos copiados para
`../esnli-treino-16k*-fora-pesos/amigo/`; contas de `ler_fora.py pc amigo`.

**Conferido:** as 10 linhas de resultado, as 10 de `mnli-hans.csv` e as 10 de `painel.csv` do PC do Marcelo; a
conferência 2 (peso recarregado repete a acurácia do treino: diferença máxima 0,00000). **Não conferido:** nenhuma
justificativa trocada desta rodada foi lida; a auditoria de treino não foi refeita para a máquina do Marcelo (mesmo
código, por MD5).

**A conferência 1 não passa para o braço embaralhado.** A regra pedia que a acurácia no dev de cada braço repetisse
a de 18/11 dentro de 0,6 ponto: o embaralhado deu 81,3% contra 80,7%, +0,63 ponto. O calendário do Marcelo passa
(+0,10). **Pela letra do critério, a rodada do embaralhado não se lê; os números abaixo ficam descritos, sem
conclusão.** O limite de 0,6 foi escolha do Claude; o desvio entre sementes desse braço em 18/11 já era de 0,6 ponto.

**Como ler:** média das 5 sementes; "âncora de máquina" é o calendário do PC do Marcelo menos o do PC do Pedro, nas
mesmas sementes; a regra pedia a diferença "real menos embaralhado" fora do zero e maior que o dobro da âncora.

| Medida | Decoder real (PC do Pedro) | Embaralhado (PC do Marcelo) | Real menos embaralhado | Âncora de máquina |
|---|---|---|---|---|
| Dev do e-SNLI, acurácia | 82,9% | 81,3% | +1,6 ponto (+1,3 a +1,8), 5 de 5 | +0,1 (−0,2 a +0,3) |
| MNLI, acurácia | 63,5% | 60,6% | +2,9 pontos (+1,4 a +4,4), 5 de 5 | −0,2 (−1,4 a +1,0) |
| RTE, ROC-AUC | 0,690 | 0,676 | +0,014 (+0,003 a +0,025), 5 de 5 | −0,003 (−0,010 a +0,005) |
| Calibração, ECE no dev (menor é melhor) | 0,152 | 0,165 | −0,014 (−0,018 a −0,009), 0 de 5 | −0,000 (−0,004 a +0,004) |
| Predição seletiva no dev | 0,737 | 0,707 | +0,031 (+0,001 a +0,060), 4 de 5 | +0,003 (−0,018 a +0,024) |
| Pior classe, F1 no dev | 0,790 | 0,771 | +0,019 (+0,014 a +0,024), 5 de 5 | +0,000 (−0,003 a +0,004) |

39. **Descrito:** em todas as medidas a justificativa do par fica melhor que a de outro par, e fora de domínio a
    distância é maior (2,9 pontos no MNLI contra 1,6 no dev). Em todas elas a diferença passa do dobro da âncora de
    máquina, que fica em torno de zero.
40. **Isso repete o que as grades de 18/11 mostraram dentro da distribuição** (real menos embaralhado +2,1 pontos),
    e não muda a comparação principal: o decoder com a justificativa certa continua abaixo do calendário.
41. **O que não se pode dizer:** que o conteúdo da justificativa "conta mais fora de domínio" como resultado; a
    conferência 1 não passou e a comparação é entre duas placas.

## Varredura do peso da perda do decoder (19/11, Gap 9): nenhum peso passa; com peso 0 a perda é a mesma

**Procedência:** dúvida do Pedro ("eu nunca vou deixar de achar que a gente só fez algo errado") e os valores que
ele escolheu ("0, 0,05 e 0,5"); critério em `docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 9", escrito antes de
rodar. Braço `bert_decoder` nos 16.000 pares com o peso da fase C trocado, **sementes 1 a 3 (exploratório)**. Pesos 0
e 0,05 no PC do Pedro (04:05 a 07:21), peso 0,5 no PC do Marcelo (05:42 a 07:21); cada um contra o calendário da
mesma máquina, nas mesmas 3 sementes. Arquivos em `../esnli-treino-16k-fora-pesos-aux-*/`; contas de `ler_peso.py`.

**Conferido:** as 9 linhas de resultado e as 9 de MNLI; a fumaça de cada lançamento imprimiu o peso em uso, e com
peso 0 a acurácia da fumaça difere da de peso 0,1 na mesma semente (o peso é aplicado). **Não conferido:** o painel
do peso 0,5 (ainda rodando às 07:23); auditoria de treino (não foi feita para a opção `--peso-aux`); sementes 4 e 5.

**Como ler:** acurácia no dev do e-SNLI, média das sementes 1 a 3; a diferença é o braço menos o calendário da mesma
máquina, pareada por semente, com intervalo de 95% (com 3 sementes ele é largo) e em quantas das 3 é positiva. A
linha do peso 0,1 são as sementes 1 a 3 da rodada de 19/11 no PC do Pedro (a média vem da diferença para o peso 0).

| Peso do decoder na fase C | Máquina | Acurácia no dev | Menos o calendário | MNLI menos o calendário |
|---|---|---|---|---|
| 0 (o decoder só treina o encoder até o passo 1.200) | PC do Pedro | 82,9% | −0,8 ponto (−1,9 a +0,3), 0 de 3 | −1,3 (−2,3 a −0,3), 0 de 3 |
| 0,05 | PC do Pedro | 82,8% | −0,9 (−2,0 a +0,1), 0 de 3 | −1,5 (−2,8 a −0,2), 0 de 3 |
| 0,1 (o do artigo) | PC do Pedro | 83,1% | 5 sementes: −0,8 (−1,4 a −0,2), 0 de 5 | 5 sementes: −1,5 (−2,3 a −0,7), 0 de 5 |
| 0,5 | PC do Marcelo | 83,2% | −0,7 (−1,4 a +0,1), 0 de 3 | −1,0 (−3,9 a +1,8), 0 de 3 |

42. **Nenhum peso é candidato.** Nos três valores novos o braço fica abaixo do calendário nas 3 sementes; no dev os
    intervalos cruzam o zero (3 sementes), então pela regra são nulos, todos com o mesmo sinal do peso 0,1.
43. **Com peso 0 a perda é praticamente a mesma do peso 0,1** (−0,2 ponto entre os dois, nas 3 sementes). Como o
    peso 0 desliga o decoder durante a classificação, o que custa a nota é a fase em que só o decoder treina o
    encoder (passos 1 a 1.200), não o peso dele depois. Isso é leitura de 3 sementes, sem teste desenhado para ela.
44. **Variar o peso entre 0 e 0,5 não muda o quadro:** a acurácia fica entre 82,8% e 83,2% nos quatro valores.

**O que isso sustenta:** a falta de ganho não vinha de o peso estar em 0,1; nesta receita, dentro da faixa de 0 a
0,5, o resultado é o mesmo. **O que não sustenta:** nada sobre pesos acima de 0,5, sobre mudar a duração da fase só
do decoder (que é onde o custo parece estar) ou sobre outra taxa de aprendizado; com 3 sementes, uma diferença de
até cerca de 1 ponto entre os pesos não se distingue.
