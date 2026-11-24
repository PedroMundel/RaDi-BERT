# Gaps da argumentação do nulo do decoder: o que já dá para responder (18/11/2026)

**Procedência:** escrito pelo Claude em 18/11 a pedido do Pedro ("vamos mexer nos gaps primeiro"). Nenhum treino
novo. Fontes: a Tabela 2 do Agrawal, Ahemad & Sembium (2025), conferida hoje no texto extraído do PDF
(`docs/artigos/2025.coling-industry.12-agrawal.pdf`, página 6; o Pedro leu o artigo, nível 1); as leituras
`resultados/rte-treino/leitura-grade.md`, `resultados/rte-msmarco/leitura-grade.md`,
`resultados/esnli-treino/leitura-grade.md` e `docs/2026-11-10-hipoteses-do-nulo.md`. O Pedro não leu este arquivo.

**Conferido hoje:** os sete pares de números da Tabela 2 e os seus intervalos; o trecho da seção 5 que define o
baseline; a contagem do dev do RTE (146 entailment, 131 not_entailment). **Não conferido:** em qual conjunto o
artigo avaliou o GLUE, quantas sementes usou e como ajustou o baseline (o texto não diz, até onde procurei); os
intervalos nossos foram copiados das leituras, não recalculados dos CSVs.

## Gap 1. O nosso teste enxergaria o ganho que o artigo relata?

**Como ler a primeira tabela:** ROC-AUC do artigo, com o intervalo de 95% que ele mesmo dá entre parênteses; "ganho"
é a diferença das duas médias; "separa?" diz se os dois intervalos do próprio artigo deixam de se sobrepor.

| Tarefa (Tabela 2 do artigo) | BERT (MS-MARCO) | + Reasoning | Ganho | Os intervalos do artigo se separam? |
|---|---|---|---|---|
| RTE | 0,4754 (±0,011) | 0,5873 (±0,007) | +0,112 | sim |
| MRPC | 0,7955 (±0,008) | 0,8811 (±0,003) | +0,086 | sim |
| CoLA | 0,5912 (±0,009) | 0,6130 (±0,007) | +0,022 | sim, por 0,006 |
| QNLI | 0,9467 (±0,005) | 0,9531 (±0,012) | +0,006 | não |
| QQP | 0,9571 (±0,006) | 0,9625 (±0,009) | +0,005 | não |
| SST-2 | 0,9488 (±0,004) | 0,9480 (±0,006) | −0,001 | não |
| QADSM | 0,7174 (±0,010) | 0,9123 (±0,005) | +0,195 | sim |

**Como ler a segunda tabela:** diferença de ROC-AUC do braço com decoder menos o braço sem, pareada por semente, 5
sementes, com o intervalo de 95%; as duas últimas colunas dizem se o ganho do artigo no RTE (+0,112) e o ganho dele
com baseline forte (+0,005) cabem dentro desse intervalo.

| Grade nossa | Decoder menos sem decoder | +0,112 cabe? | +0,005 cabe? |
|---|---|---|---|
| RTE, BERT cru, aquecimento `prop` | −0,028 (−0,071 a +0,015) | não | sim |
| RTE, BERT cru, aquecimento `500` | +0,007 (−0,031 a +0,045) | não | sim |
| RTE, BERT MS-MARCO (nboost), `500` | −0,049 (−0,078 a −0,021) | não | não |
| e-SNLI, 4.000 pares, 3 classes | −0,007 (−0,015 a +0,002) | não | não, por 0,003 |

O que as duas tabelas sustentam, juntas:

1. **O ganho grande do artigo no RTE teria sido visto.** O maior limite superior nosso é +0,045; o artigo relata
   +0,112. Nas quatro grades ele fica fora do intervalo.
2. **Onde o baseline do artigo é forte, o próprio artigo não separa o ganho do ruído** (QNLI, QQP, SST-2: os
   intervalos dele se sobrepõem). O ganho que aparece é o das tarefas em que o baseline dele é baixo.
3. **O ganho pequeno (+0,005) o nosso RTE não enxerga**: cabe nos dois intervalos do BERT cru. O e-SNLI e o
   MS-MARCO o excluem, mas com 5 sementes; no BERT small o mesmo treino na GPU variou até 0,026 entre rodadas, e um
   +0,017 de 5 sementes já sumiu com 15. Não se afirma "meio ponto não existe" com isso.

**Frase que os números permitem:** "nas quatro condições medidas, o ganho de 11 pontos relatado no RTE não aparece
e ficaria visível; um ganho de meio ponto, como o que o artigo mostra com baseline forte, não é distinguível no RTE
com 5 sementes". **Frase que não permitem:** "o método não funciona".

## Gap 2. De onde pode vir o 0,4754?

O artigo define o baseline assim (seção 5): BERT base "further trained on MS-MARCO query-passage-relevance
dataset", treinado com entropia cruzada. Não achei no texto como ele foi ajustado no GLUE.

**Como ler:** ROC-AUC no dev do RTE (277 pares) do checkpoint `nboost/pt-bert-base-uncased-msmarco` em cada
condição; a última coluna diz de onde vem o número.

| Condição | ROC-AUC | Origem |
|---|---|---|
| Artigo, Tabela 2 | 0,4754 (±0,011) | PDF, conferido hoje |
| Ajustado no RTE, 5 sementes | 0,767 (±0,013) | rodado em 10/11 |
| Sem treino no RTE, hipótese como consulta | 0,620 | rodado em 10/11 (`zero_shot.py`) |
| Sem treino no RTE, premissa como consulta | 0,575 | rodado em 10/11 |
| As três acima com a classe positiva trocada | 0,233 · 0,380 · 0,425 | conta (1 menos o valor), sem rodar |
| Notas sem relação com o rótulo, nestes 277 pares | 0,500, desvio de 0,035 | conta de hoje (146 e 131 pares) |

1. **Nenhuma condição medida dá 0,4754.** A mais próxima é a de um modelo cujas notas não dizem nada sobre o
   rótulo: o 0,4754 fica a 0,7 desvio do 0,5 nesse conjunto.
2. **O que isso não prova:** que o baseline deles "não aprendeu". O intervalo de ±0,011 do artigo diz que as
   rodadas deles concordam entre si abaixo de 0,5, e eu não sei em qual conjunto nem com quantas sementes. É
   compatível com um baseline sem informação de rótulo no RTE; é hipótese, sem teste.
3. **O método deles (0,5873) fica abaixo do mesmo checkpoint sem nenhum treino no RTE (0,620)** e 0,18 abaixo dele
   ajustado. O ganho relatado no RTE é sobre um ponto de partida que um ajuste comum já supera.

Condições não tentadas, por custo (nenhuma decidida):

| Condição | O que diria | Custo estimado, não medido |
|---|---|---|
| Outro checkpoint (`Capreolus/bert-base-msmarco`) | se o 0,767 é do checkpoint escolhido | cerca de 1 hora no PC |
| Encoder congelado, só a cabeça treina | se "baseline" podia ser só uma cabeça nova | minutos |
| Poucos passos de ajuste | se sai um 0,47 de treino curto | minutos |
| Baseline no MRPC e no CoLA | se os outros baselines baixos da Tabela 2 também não se repetem | não estimado |
| Perguntar aos autores | a resposta direta | fora do prazo |

**Limite que fica:** o gap 2 não fecha sem a resposta dos autores. O que dá para dizer é quantas condições
razoáveis foram tentadas e que nenhuma dá o número.

## Gap 2b. Duas condições rápidas do baseline (critério escrito em 18/11, antes de rodar)

**Procedência:** pedido do Pedro ("duas condições rapidas no note"). A pergunta é descritiva: alguma forma barata
de "ajustar o BERT MS-MARCO no RTE" dá um ROC-AUC perto do 0,4754 do artigo? Checkpoint
`nboost/pt-bert-base-uncased-msmarco`, braço sem decoder, 5 sementes, dev do RTE (277 pares), no notebook.

| Condição | O que muda em relação ao baseline de 10/11 (0,767) |
|---|---|
| Encoder congelado | os pesos do BERT não treinam; só a cabeça nova de classificação. Mesmas 8 épocas, aquecimento `500` |
| Uma época, aquecimento `500` | 78 passos em vez de 624; como o aquecimento é de 500 passos, a taxa nunca passa de 16% de 5e-5 |
| Uma época, aquecimento `prop` | 78 passos, aquecimento de 7 passos |

**Regra de leitura:** uma condição "dá o número do artigo" se a média das 5 sementes ficar entre 0,44 e 0,51 (o
0,4754 mais ou menos um desvio de 0,035, que é o de notas sem relação com o rótulo nesses 277 pares). Fora dessa
faixa, a condição é registrada como "não dá". Nenhuma condição é acrescentada depois de ver o resultado sem voltar
a esta seção.

**O que cada resultado sustenta:** se alguma der, fica "um baseline assim produz o número; não sei se foi o que os
autores fizeram". Se nenhuma der, a tabela do gap 2 ganha três linhas e a frase continua "nenhuma condição tentada
dá 0,4754".

## Gap 3. O outro checkpoint MS-MARCO (critério escrito em 18/11, antes de rodar)

**Procedência:** pedido do Pedro ("depois capreolus"). `Capreolus/bert-base-msmarco` conferido no Hub em 18/11:
existe, `BertForSequenceClassification`, `vocab.txt` com o mesmo MD5 do BERT base. Mesma grade de 10/11 no PC: dois
braços (sem e com decoder), aquecimento `500`, 5 sementes, micro-lote 8, dev do RTE.

**Regra de leitura, três perguntas separadas:**

1. **O baseline dá o número do artigo?** Mesma faixa do gap 2b: média do braço sem decoder entre 0,44 e 0,51.
2. **O 0,767 era do checkpoint nboost?** Se o baseline do Capreolus ficar a menos de 0,03 do 0,767 (0,03 é o
   tamanho que 5 sementes no RTE não distinguem), os dois checkpoints contam a mesma história.
3. **O decoder ajuda aqui?** Só conta como ganho se o intervalo de 95% da diferença pareada ficar inteiro acima de
   zero; como perda se ficar inteiro abaixo; senão, nulo.

**O que cada resultado sustenta:** baseline alto e decoder sem ganho nos dois checkpoints fecha "não é do
checkpoint escolhido" para os dois que existem com esse nome no Hub, não para o checkpoint dos autores, que o
artigo não nomeia. Baseline perto de 0,47 reabre a replicação: aí o braço com decoder deste checkpoint passa a ser
a condição do artigo.

## Gap 4. O decoder com os 16 mil pares do e-SNLI (desenho de 18/11; ESPERA AS DECISÕES DO PEDRO, nada rodou)

**Procedência:** pedido do Pedro ("depois 16mil pares"). É o teste que derruba ou sustenta a H2 de
`docs/2026-11-10-hipoteses-do-nulo.md`: com 2,5 a 4 mil pares a fase A tem 39 a 63 passos e o decoder não passa
do molde; com 16 mil a receita do artigo cabe.

**O que muda em relação à grade do e-SNLI de 10/11 (4.000 pares, nulo de −0,007):** só o número de pares. Treino =
as 16.000 linhas do lote 35B (variante F), avaliação no dev do e-SNLI (9.842 pares, disjunto do lote). BERT base,
lote 32, 8 épocas, peso da L_aux 0,1.

| Item | Com 4.000 pares (10/11) | Com 16.000 pares |
|---|---|---|
| Passos totais | 1.000 | 4.000 |
| Fase A (decoder aprende a ler o BERT congelado) | 63 passos | 250 passos |
| Fase B (só a L_aux) | 300 passos | 1.200 passos |
| Aquecimento | `prop`, 100 passos | `500` da Tabela 4, que agora é 12,5% do treino |

**Tempo, estimado dos tempos medidos em 10/11 no PC (8 min por 1.000 passos com decoder; 1,6 sem), não medido
nesta escala:** cerca de 34 min por treino com decoder e 6 a 7 sem; 5 sementes dos dois braços, cerca de 3h30; 10
sementes, cerca de 7 h. O primeiro treino mede o tempo real antes de a grade seguir.

**Regra de leitura proposta (a confirmar):**

1. **Ganho:** só conta se o intervalo de 95% da diferença pareada de ROC-AUC (decoder menos sem decoder) ficar
   inteiro acima de zero. Inteiro abaixo, conta como perda. Senão, nulo.
2. **Poder:** junto com o resultado se diz se o +0,005 do artigo com baseline forte cabe no intervalo. Se couber,
   a frase é "não distinguível", não "não existe".
3. **A H2, separada do ganho:** a L_aux por grupo de palavra no fim do treino, contra os valores de 4.000 pares
   (copiadas do par 3,6; novas 3,9; rótulo 1,4; gramaticais 1,7). A H2 prevê que copiadas e novas caem com mais
   passos. Se caírem e não houver ganho, a H2 deixa de explicar o nulo; se não caírem, o limite é a ponte BERT ->
   T5 e não a escala.

**Lançado em 18/11, cerca de 5h, antes das decisões abaixo:** 5 sementes dos dois braços, que fazem parte de
qualquer resposta (mais sementes e o controle de calendário se somam depois sem refazer). Dois ajustes vindos da
auditoria de treino, antes de lançar: (1) a tabela de expressões de rótulo (grupo S) é montada nos mesmos 4.000
pares de 10/11 e não nos 16.000, porque o corte dela é uma contagem absoluta e com 16.000 pares o grupo S passaria
de 17,6% para 24,7% das palavras, o que tiraria a comparação do item 3; conferido: as 202 expressões e as contagens
são as do arquivo de 10/11. (2) Micro-lote 16, como em 10/11, e não 8. A auditoria também mediu o confundidor de
calendário nesta escala: no braço com decoder o BERT tem 70% e a cabeça 56% da área de taxa com a L_cls ligada.
**A regra de leitura continua sem a confirmação do Pedro; o resultado não é lido contra ela antes disso.**

**Decisões do Pedro que faltam:** (a) 5 ou 10 sementes; (b) se entra o controle de calendário (BERT sem decoder
com o calendário do braço com decoder; no RTE ele derrubou a H1; aqui pede uma mudança pequena no código, porque
hoje só existe para o RTE, e cerca de 6 min a mais por semente); (c) se a regra de leitura acima vale.

### Gap 4b. Controle de calendário nos 16 mil pares (critério escrito em 18/11, antes de rodar)

**Procedência:** decisão do Pedro em 18/11 ("faz so o controle de calendário"): das três pendências do gap 4, só
esta roda; ficam 5 sementes. Ele não respondeu sobre a regra de leitura do gap 4, que segue como proposta.

**O que é:** o braço `bert_calendar`, BERT sem decoder com o calendário do braço com decoder: nenhum passo de
classificação nos passos 1 a 1.200 (a fase B) e a taxa do BERT com pico no passo 1.200. Mesmos 16.000 pares, mesmas
5 sementes, mesmo dev. Separa duas coisas que a diferença "decoder menos sem decoder" mistura: o que o calendário
custa e o que o decoder faz.

**Regra de leitura (mesma forma das outras de hoje: diferença pareada por semente, intervalo de 95%, ROC-AUC e
acurácia lidos lado a lado):**

| Comparação | O que responde | Como se lê |
|---|---|---|
| Calendário menos BERT sem decoder | perder 1.200 passos de classificação custa? | intervalo inteiro abaixo de zero = custa; cruzando = não distinguível |
| Decoder menos calendário | o efeito do decoder, com o mesmo calendário dos dois lados | intervalo inteiro acima de zero = o decoder ajuda; inteiro abaixo = atrapalha; cruzando = nulo |

**Leitura combinada antes:** (a) se o calendário custa e o decoder fica acima do calendário, o nulo do gap 4 era
um ganho do decoder escondido pelo calendário, e a frase "o decoder não ajuda" cai para esta escala; (b) se o
calendário não custa, a diferença do gap 4 já era o efeito do decoder e a leitura dele fica; (c) se o calendário
custa e o decoder não fica acima dele, o decoder não compensa nem o próprio calendário. Com 5 sementes, diferenças
menores que cerca de 0,005 de ROC-AUC ficam dentro do intervalo (o do gap 4 teve metade de 0,007).

### Gap 4c. Controle de calendário nos 4.000 pares do e-SNLI (critério escrito em 18/11, antes de rodar)

**Procedência:** pedido do Pedro ("roda o calendario nos 4k do e-snli"). Mesmo braço `bert_calendar` do gap 4b, na
grade de 10/11: 4.000 pares, 1.000 passos, fase B de 300, aquecimento `prop`, 5 sementes, dev do e-SNLI. Pareia com
`resultados/esnli-treino/pc/resultados.csv` (BERT sem decoder 0,916; com decoder 0,909).

**Pergunta:** o calendário ajuda também com 4.000 pares, ou só com 16.000?

**Regra de leitura (a do gap 4b, agora com o caso que faltava):** diferença pareada por semente, intervalo de 95%,
ROC-AUC e acurácia lado a lado. Calendário menos BERT sem decoder: intervalo inteiro acima de zero = ajuda; inteiro
abaixo = custa; cruzando = não distinguível. Decoder menos calendário: mesma leitura para o efeito do decoder.

**Antes de ver:** se ajudar aqui também, "o calendário ajuda" vale nas duas escalas do e-SNLI; se não, fica como
efeito visto só com 16.000 pares. Em nenhum caso explica o motivo. As grades de 10/11 e de hoje têm o mesmo rótulo
de código (`59278b8-dirty`) com `src/` diferente; o caminho do braço sem decoder não mudou entre elas, pela leitura
do diff que a auditoria fez hoje, mas isso não foi testado rodando de novo o braço `bert`.

## Gap 5. Justificativa embaralhada nos 16.000 pares (critério escrito em 18/11, antes de codar e de rodar)

**Procedência:** decisão do Pedro em 18/11 ("Sim, 16 mil"), depois da estimativa pedida por ele. É o controle que o
Agrawal, Ahemad & Sembium (2025) não fizeram e que o tema nomeava; o desenho é o de 10/11 (`AUTONOMIA.md`, 01:05),
nunca implementado: os 3 testes vermelhos de `tests/test_rte_treino.py` são dele.

**O que é:** braço `bert_decoder_shuffled`. Igual ao braço com decoder em tudo (fases, calendário, peso 0,1,
sementes, os mesmos 16.000 pares de entrada e os mesmos rótulos), menos uma coisa: o decoder tem de gerar a
justificativa de **outro par do mesmo rótulo**. A troca é uma só, fixa (semente 0), e nenhum par fica com a
própria. O que se mantém: tudo o que a justificativa diz sobre o rótulo (as expressões de rótulo, o molde). O que
sai: o conteúdo específico do par.

**Comparações (diferença pareada por semente, 5 sementes, intervalo de 95%, ROC-AUC e acurácia lado a lado):**

| Comparação | O que responde |
|---|---|
| Decoder real menos embaralhado | o conteúdo específico do par muda o que o decoder faz com o classificador? |
| Embaralhado menos calendário | um decoder com justificativa de outro par também tira acurácia, como o real tirou (−0,9 ponto)? |

**Checagem de que a troca funcionou (antes de ler a nota):** a perda do decoder nas palavras copiadas do par tem de
ficar bem acima da do braço real (2,01 no fim), porque o par não ajuda mais a prever a justificativa. Se ficar
igual, a troca não aconteceu e a rodada não vale. Os grupos de palavra na sonda do embaralhado são calculados
contra o par errado, então "copiada" e "nova" mudam de tamanho; isso se relata.

**Leitura combinada antes:**

- **Real menos embaralhado cruza o zero nas duas métricas:** o efeito do decoder no classificador não depende de a
  justificativa ser a do par, dentro do que 5 sementes enxergam (cerca de 0,6 ponto de acurácia). Sustenta "o
  classificador não usa o porquê".
- **Real acima do embaralhado, intervalo fora do zero:** o conteúdo do par vale alguma coisa em relação a conteúdo
  errado, mesmo sem ficar acima do calendário.
- **Real abaixo do embaralhado, intervalo fora do zero:** o conteúdo específico atrapalha mais do que o molde.

Em nenhum caso o resultado vira ganho de nota: o braço real já ficou abaixo do calendário.

**Correção da checagem, antes de lançar (18/11, vinda da auditoria de treino):** na sonda do embaralhado o grupo
"copiada do par" quase some (0,4% dos tokens, cerca de 7 de 1.826; no real são 15,2%), porque a justificativa é de
outro par e quase nada dela está no par; as palavras vão para "nova" (39,9% contra 21,8%). A perda por grupo desse
braço não se compara por nome com a do real. **A checagem passa a ser a perda do decoder em todas as palavras:**
no braço real ela termina em 1,79; no embaralhado tem de terminar claramente acima. Se ficar igual, a troca não
aconteceu e a rodada não vale.

## Gap 6. O decoder faz a classificação arrancar mais rápido? (critério escrito em 18/11, antes de codar e de rodar)

**Procedência:** pergunta do Pedro em 18/11 ("teria como calcular pra ver se ajuda ele a treinar mais rapido?") e
o sim dele para rodar; ele pediu para não ver o critério, salvo decisão que o Claude não queira tomar. **As
escolhas desta seção são do Claude.** O que já existia: a perda de classificação por passo só nos braços com
decoder; nos sem decoder, só a nota final.

**O que roda:** os braços `bert_calendar` e `bert_decoder` de novo, nos mesmos 16.000 pares, sementes 1 a 5, com
duas medidas gravadas em 11 passos depois do início da classificação (1.225, 1.250, 1.300, 1.400, 1.500, 1.750,
2.000, 2.500, 3.000, 3.500, 4.000): a acurácia e o ROC-AUC no dev inteiro, e a perda de classificação nos 63 pares
de treino da sonda. Os dois braços têm o mesmo calendário, a mesma ordem de lotes e a mesma cabeça inicial; a
diferença é o que o decoder fez com o encoder nos passos 1 a 1.200 e o peso 0,1 dele depois. Saída em pasta
própria (`resultados/esnli-treino-16k-curva/`), sem tocar nas grades de hoje.

**Regra de leitura:**

| Medida | Como se lê |
|---|---|
| Principal: acurácia média no dev nos cinco primeiros passos medidos (1.225 a 1.500), decoder menos calendário, pareada por semente | intervalo de 95% inteiro acima de zero = o decoder faz a classificação arrancar mais rápido; inteiro abaixo = mais devagar; cruzando = não distinguível |
| Secundária: o primeiro passo medido em que cada braço chega a 80% de acurácia no dev | descrita por semente, sem intervalo |
| Só descrita | a curva inteira das duas medidas; a diferença no passo 4.000, que tem de repetir a de hoje cedo (−0,9 ponto) dentro do ruído |

**Conferência do instrumento:** no braço com decoder, a perda de classificação da sonda medida pelo script novo
tem de bater com a coluna `l_cls` do `gradientes.csv` da mesma rodada, nos passos em comum.

**O que cada resultado sustenta:** arranque mais rápido com nota final igual ou pior é "o decoder adianta o
aprendizado, sem melhorar o ponto de chegada", que é a leitura do Pedro; arranque igual ou mais lento a derruba
para esta escala. Em nenhum caso é ganho de nota final. Limite já sabido: são 11 passos escolhidos antes; entre
1.201 e 1.225 nada é medido.

### Gap 6b. A curva de arranque do braço embaralhado (critério escrito em 18/11, antes de rodar)

**Procedência:** o Pedro pediu os gráficos que faltam para o artigo ("pode criar todos"); este é o único que
depende de treino novo. As escolhas são do Claude. Braço `bert_decoder_shuffled` (justificativa de outro par do
mesmo rótulo), mesmos 16.000 pares, mesmas 11 medidas no dev depois do passo 1.200. **Cada semente na máquina em
que os outros dois braços dela rodaram:** sementes 1 a 3 no PC, 4 e 5 no PC do amigo.

**Pergunta:** a vantagem de arranque do decoder (+15,4 pontos no passo 1.225) vem do conteúdo da justificativa, ou
de qualquer decoder que treine o encoder antes da classificação?

**Regra de leitura (mesma medida principal do gap 6: acurácia média no dev nos passos 1.225 a 1.500, diferença
pareada por semente, intervalo de 95%):**

| Comparação | Como se lê |
|---|---|
| Decoder real menos embaralhado | intervalo inteiro acima de zero = o arranque depende de a justificativa ser a do par |
| Embaralhado menos calendário | intervalo inteiro acima de zero = mesmo com a justificativa trocada o decoder adianta o começo |

**Leitura combinada antes:** se o embaralhado também arranca na frente do calendário e empata com o real, a
vantagem inicial vem de pré-treinar o encoder com uma tarefa de geração sobre os mesmos textos, não do conteúdo; se
o real fica acima do embaralhado, o conteúdo do par conta para o arranque; se o embaralhado fica abaixo do
calendário, a justificativa trocada atrasa a classificação desde o começo. O passo 4.000 tem de repetir a nota final
do braço embaralhado (80,7%) dentro do ruído.

**Mudança antes de as sementes 4 e 5 rodarem (Pedro, 18/11: "Rodar no meu PC"):** a GPU do amigo estava em uso por
ele, então as cinco sementes do braço embaralhado rodam no PC. Consequência para a leitura, fixada antes de ver os
números: **embaralhado menos calendário** usa o calendário do PC nas cinco sementes (ele rodou lá de 1 a 5), então
continua tudo na mesma máquina; **real menos embaralhado** fica na mesma máquina só nas sementes 1 a 3, e nas
sementes 4 e 5 compara o decoder real do PC do amigo com o embaralhado do PC. Essa segunda comparação é relatada
com as cinco sementes e também só com as três da mesma máquina; se as duas leituras discordarem, vale a de três.

## Gap 7. O decoder fora de domínio (versão 2 do critério, 18/11, 23h30, antes de qualquer número de braço com decoder)

**Procedência:** decisão do Pedro em 18/11 ("acho que tem que rodar tbm"), depois da avaliação
(`docs/2026-11-18-avaliacao-da-pesquisa.md`, opção B). É a pendência 10 do `tema-v3` (10/09): "avaliação fora de
domínio é obrigatória". **Desenho, medidas e cortes são escolha do Claude.**

**Por que há versão 2.** A versão 1 (22h55) foi escrita em dez minutos e lançada às 23:07. O Pedro perguntou se o
teste estava bem feito; a resposta listou atalhos, e ele mandou corrigir ("salva os pesos, e pensa mais no desenho").
A rodada da versão 1 foi parada por volta das 23:25 com 4 sementes do braço de calendário prontas e nenhuma de braço com
decoder. **O que já foi visto antes de escrever esta versão:** só o braço de calendário no RTE (ROC-AUC 0,708, 0,689
e 0,697 nas sementes 1 a 3; a 4 não foi lida), ou seja, o piso do instrumento, nenhuma comparação entre braços.
Essas linhas ficam em `resultados/esnli-treino-16k-calendario-fora/` no PC e não entram na leitura.

**O que mudou da versão 1:**

| Ponto | Versão 1 | Versão 2 | Motivo |
|---|---|---|---|
| Pesos | não salvos | o classificador de cada treino fica em `pesos/` (cerca de 0,4 GB cada, 20 arquivos) | outro conjunto de fora deixa de custar 6h40 de treino |
| Conjunto principal | RTE, porque estava no disco | **MNLI** (validação matched + mismatched, 19.647 pares), **se o Pedro autorizar o download**; sem ele, o principal continua o RTE | mesmas 3 classes do e-SNLI (não mistura mudança de domínio com mudança de rótulo), sete vezes mais pares, é a transferência usual de quem treina no SNLI |
| RTE | principal | secundário, medido dentro da própria rodada | já implementado e auditado |
| HANS | não havia | terceiro, só descrito, se o Pedro autorizar o download | mede atalho por sobreposição de palavras, que é o mecanismo 1 da tabela do `tema-v3` ("aponta onde olhar"); risco de piso (modelos pequenos costumam responder entailment em tudo) |
| Passar com 5 sementes | já contava | vira **candidato**; só conta como ganho com as sementes 6 a 15 dos braços calendário e decoder | regra usada em 17/11 na "sequência", depois do +0,017 de 5 sementes que sumiu |
| Braços com decoder | lançados sem fumaça com `--fora` | fumaça dos quatro braços com `--fora --salvar-pesos` antes de lançar | atalho apontado na resposta ao Pedro |

**O que roda:** os quatro braços da grade dos 16.000 pares (`bert`, `bert_calendar`, `bert_decoder`,
`bert_decoder_shuffled`), mesma receita, sementes 1 a 5, com `--fora --salvar-pesos`. No fim de cada treino o
classificador é avaliado no RTE (2.747 pares: 2.470 do treino com justificativa mais 277 do dev; nenhum entra no
treino aqui) e os pesos são gravados antes da linha de resultado. No RTE o modelo de 3 classes é lido assim: a nota
do par é a probabilidade de entailment, e a decisão é "entailment" quando essa é a classe mais provável. Saída em
`resultados/esnli-treino-16k*-fora-pesos/`. Tudo no PC do Pedro (a GPU do Marcelo estava em uso às 23h00), nesta
ordem: calendário, sem decoder e com decoder, embaralhado. MNLI e HANS são avaliados depois, a partir dos pesos, por
um script à parte que ainda não existe.

**Conferências do instrumento (antes de ler qualquer conjunto de fora):**

1. A acurácia no dev do e-SNLI de cada braço repete a da grade de hoje dentro de 0,6 ponto na média das 5 sementes
   (83,4 sem decoder; 83,7 calendário; 82,8 decoder; 80,7 embaralhado). Se algum braço sair disso, a rodada não se lê.
2. Para MNLI e HANS: cada classificador carregado do arquivo de pesos tem de repetir, no dev do e-SNLI, a acurácia
   que a própria rodada gravou para ele (diferença de no máximo 0,1 ponto). Sem isso, os pesos não se usam.

**Regra de leitura (diferença pareada por semente, intervalo de 95% pela distribuição t, 5 sementes):**

| Comparação | O que responde | Como se lê |
|---|---|---|
| **Decoder menos calendário (a principal)** | fora de domínio, o decoder ajuda? | intervalo inteiro acima de zero = candidato a ajudar; inteiro abaixo = atrapalha; cruzando = nulo |
| Decoder real menos embaralhado | fora, o conteúdo da justificativa conta? | idem |
| Calendário menos sem decoder | o ganho do calendário se mantém fora? | idem, só descrito |

**Medida por conjunto:** no MNLI, acurácia de 3 classes nos 19.647 pares (ROC-AUC ao lado; matched e mismatched
também separados, só descritos). No RTE, ROC-AUC (acurácia ao lado). No HANS, acurácia nos pares de não-entailment,
só descrita.

**Um conjunto decide.** "O decoder ajuda fora" só se diz se a comparação principal passar no conjunto principal. Se
o principal der nulo e um secundário passar, fica escrito como "indício num conjunto", sem contar como ganho. Se o
principal passar com 5 sementes, as sementes 6 a 15 de calendário e decoder rodam antes de qualquer frase de ganho
(cerca de 6h30 de GPU, conta sobre os tempos de hoje).

**Poder:** junto com cada resultado vai a metade do intervalo; a frase de um nulo é "não distinguível até esse
tamanho", não "não existe". Pelas 3 sementes do calendário no RTE (desvio de cerca de 0,009 de ROC-AUC), a estimativa
é que 5 sementes enxergam por volta de 0,015 de ROC-AUC no RTE; no MNLI não há estimativa ainda.

**Regra de parada:** o resultado fica como sair. Nenhum outro conjunto de fora, outra forma de juntar as classes,
outro subconjunto ou outra medida entra depois de ver os números sem decisão do Pedro e sem voltar a esta seção.

**O que cada resultado sustenta:** ganho fora (confirmado nas 15 sementes) com nota igual dentro seria o primeiro
resultado em que a justificativa melhora o classificador final, com um só LLM e uma só receita; nulo ou perda fecha
a pendência 10 para esta receita: "o decoder não ajuda dentro nem fora, nos conjuntos medidos".

**Acréscimo de 18/11, 23h45, ainda sem nenhum número de braço com decoder:** o Pedro autorizou os dois downloads
("Baixa os dois"), então **o MNLI é o conjunto principal**. Os arquivos estão em `dados/mnli/` e `dados/hans/` (hashes
em `dados/README.md`); nenhum par passa de 512 tokens. O script é `resultados/esnli-treino-16k/avaliar_fora.py`.
A conferência 2 vale na mesma máquina e na mesma placa do treino: num ensaio com os pesos da fumaça, a acurácia
recarregada foi idêntica à gravada quando as duas contas rodaram na CPU, e diferiu em 2 e 13 pares de 9.842 quando a
avaliação foi para a GPU do notebook.

**Mudança de máquina do braço embaralhado (19/11, 02h10, antes de ele rodar e antes de ler qualquer comparação):**
o Pedro avisou que a GPU do Marcelo liberou ("o pc do marcelo ta livre"; conferido: 1,0 GB e 2% às 02:05). O braço
embaralhado inteiro (sementes 1 a 5) passa a rodar lá, em paralelo com a parte A no PC do Pedro; é escolha do
Claude entre os dois jeitos apresentados (o outro pedia parar e relançar a grade do PC). Consequências, fixadas agora:

- **A comparação principal (decoder menos calendário) não muda:** os dois braços rodam no PC do Pedro.
- **"Decoder real menos embaralhado" passa a comparar duas placas.** Para medir quanto disso é da placa, o braço de
  calendário também roda no PC do Marcelo, nas mesmas 5 sementes, depois do embaralhado: a diferença "calendário do
  Marcelo menos calendário do Pedro", pareada por semente, é a **âncora de máquina** em cada medida.
- **Regra:** "real menos embaralhado" só se lê numa medida se o intervalo dela ficar fora do zero **e** a diferença
  média for maior, em valor absoluto, do que o dobro da âncora de máquina naquela medida. Senão fica escrito "não se
  separa da diferença entre placas".
- Os pesos do embaralhado e do calendário de lá são avaliados lá (MNLI, HANS e painel), na mesma placa em que
  treinaram, para a conferência 2 valer.
- A auditoria de treino não foi refeita para a máquina do Marcelo: mesmo código, conferido por MD5.

**O que este desenho não cobre:** mede só o fim do treino (a vantagem do decoder dentro da distribuição era só no
começo); uma receita, um LLM, um prompt; MNLI e RTE são fora de domínio "brandos" (mesma tarefa, outro texto); os
decoders treinados não são salvos, só os classificadores.

## Gap 8. Painel fora da acurácia, nos pesos salvos (critério escrito em 19/11, 01h15, antes de ler qualquer número de braço com decoder desta rodada)

**Procedência:** pergunta do Pedro em 19/11 ("será que a gente n ta olhando pra métrica errada tbm? ... se a acurácia
não sobe, mas o treino tem sinal, será que ele só não está aparecendo em outro lugar?") e a resposta dele à lista de
medidas ("acho que vale as 4 que vc recomendou"; fora: o atalho da hipótese e a resistência à compressão). **Quais
são as quatro é leitura do Claude, a confirmar com ele:** as que saem dos pesos salvos sem treino novo. Medidas,
cortes e controles são escolha do Claude. Nenhum script do painel existe ainda.

**Correção do Pedro (19/11, cerca de 01h16), antes de qualquer script ou número:** as medidas que ele quis dizer eram
**calibração, robustez fora de domínio e predição seletiva**; a quarta ainda está em escolha. **Saem do painel, sem
terem sido calculadas, a saída antecipada (3) e as palavras marcadas por pessoas (4)** da tabela abaixo. A robustez
fora de domínio entra pelo critério do Gap 7, sem mudar nada nele. A tabela fica como registro da leitura errada do
Claude; a versão final do painel vem numa seção própria quando a quarta medida for decidida.

**Por que um painel fechado:** medir uma coisa de cada vez até uma passar produz positivo falso. As quatro medidas
ficam escritas agora, de uma vez, e as quatro são relatadas, tenham dado ou não. Com quatro medidas a 95%, a chance
de pelo menos uma passar por acaso é de cerca de 19%.

**Modelos:** os 20 classificadores da rodada do Gap 7 (quatro braços, sementes 1 a 5), lidos dos pesos, no PC.
**Comparações, em todas as medidas:** decoder menos calendário (a principal) e decoder real menos embaralhado,
diferença pareada por semente, intervalo de 95% pela distribuição t.

| # | Medida | Como se calcula | O que diria |
|---|---|---|---|
| 1 | **Calibração** | erro de calibração esperado (ECE) da classe mais provável, 15 faixas de largura igual, no dev do e-SNLI (9.842 pares); no MNLI ao lado. Menor é melhor | a probabilidade que o modelo dá pode ser usada como está |
| 2 | **Predição seletiva** | ROC-AUC da confiança (probabilidade da classe escolhida) para separar acertos de erros, no dev; MNLI ao lado; descritas: a acurácia nos 50% e nos 80% mais confiantes. Maior é melhor | o modelo sabe quando está errado, que é o que uma cascata com modelo maior precisa |
| 3 | **Saída antecipada** | para cada uma das 12 camadas, uma regressão logística sobre o vetor do `[CLS]` daquela camada, ajustada em 4.000 pares do treino (amostra fixa, semente 0) e testada no dev. Medida: a média da acurácia das camadas 1 a 11. Maior é melhor; a curva por camada vai descrita | o rótulo fica legível mais cedo, então um modelo cortado no meio perde menos |
| 4 | **Decidir pelas palavras que as pessoas marcam** | no dev, com os destaques humanos do e-SNLI (anotação 1; todos os 9.842 pares têm marca): queda da probabilidade da classe prevista quando as palavras marcadas viram `[MASK]`, menos a mesma queda com o mesmo número de palavras não marcadas sorteadas (semente fixa). Maior é melhor; descrita: o mesmo deixando só as palavras marcadas | a decisão depende mais da evidência que uma pessoa aponta do que de palavras quaisquer (é a medida que o Pedro decidiu em 16/11, com destaque humano no lugar das palavras da justificativa, porque todo par com justificativa do Qwen entrou no treino) |

**Só descritas, sem critério:** o desvio entre sementes de cada braço (com 5 sementes não há teste que preste); a
robustez fora de domínio é o Gap 7 e não se conta de novo aqui.

**Regra de leitura:** em cada medida, intervalo inteiro do lado bom = **candidato**; inteiro do lado ruim = piora;
cruzando = nulo, com a metade do intervalo ao lado. Candidato só vira resultado com as sementes 6 a 15 de calendário
e decoder, como no Gap 7. Uma medida que passe sozinha entre as quatro é relatada com a frase "uma de quatro".

**Limites sabidos antes:** as medidas 1 e 2 andam junto com a acurácia, e o decoder perdeu 0,9 ponto dentro da
distribuição, então parte de qualquer diferença pode ser só isso; a medida 3 é uma sonda, não uma saída antecipada
treinada; na medida 4 as palavras marcadas por pessoas são, em boa parte, palavras que aparecem nas duas frases (limite
já visto em 16/11), e nos pares neutros só a hipótese tem marca; um LLM, uma receita, 5 sementes.

**Regra de parada:** nenhuma quinta medida, nem troca de faixas, camadas, cobertura ou anotação, depois de ver os
números, sem decisão do Pedro e sem voltar a esta seção.

### Gap 8, versão final do painel (19/11, cerca de 01h18; decidida pelo Pedro, escrita antes de qualquer script e de ler qualquer coluna)

**Procedência:** Pedro, 19/11: as três medidas ("calibração, robustez fora de domínio, predição seletiva") e a
quarta ("A, B se a predição tiver resultado, C só por medir se nada der certo, pra ter mais uma medida"). Fórmulas,
cortes e conjuntos são escolha do Claude.

**Comparações, em todas:** decoder menos calendário (a principal) e decoder real menos embaralhado; diferença pareada
por semente, 5 sementes, intervalo de 95% pela distribuição t.

| # | Medida | Como se calcula | Lado bom | De onde sai |
|---|---|---|---|---|
| 1 | Robustez fora de domínio | o Gap 7, sem mudança: acurácia no MNLI | maior | pesos desta rodada |
| 2 | Calibração | ECE da classe mais provável, 15 faixas de largura igual, no dev do e-SNLI; MNLI ao lado | menor | pesos desta rodada |
| 3 | Predição seletiva | ROC-AUC da confiança (probabilidade da classe escolhida) para separar acertos de erros, no dev; MNLI ao lado | maior | pesos desta rodada |
| 4 | Pior classe (A) | o menor dos três F1 por classe de cada modelo, no dev; descritos: o F1 e o recall de cada classe; MNLI ao lado | maior | **F1 por classe: já gravado nas grades de 18/11** (`resultados.csv`, colunas `f1_*`, nunca lidas); recall: pesos desta rodada |

**Condicionais, só descritas (decisão do Pedro):**

- **B, cobertura com erro garantido:** a maior fração dos pares mais confiantes em que a acurácia fica em 95% ou
  mais, no dev. Só é relatada se a medida 3 der candidato.
- **C, troca de resposta entre retreinos:** a fração dos pares do dev em que duas sementes do mesmo braço dão classes
  diferentes, média dos 10 pares de sementes. Só é medida se nenhuma das quatro der candidato, e sem teste (os 10
  pares de sementes não são independentes).

**A medida 4 tem duas leituras, fixadas agora:** a que conta é a das grades de 18/11 (as cinco sementes de cada
braço, PC). A rodada desta noite repete as mesmas sementes e serve de conferência: o sinal da diferença tem de se
repetir; se não se repetir, a medida fica como "não se sustenta".

**Regra de leitura, igual à do Gap 7:** intervalo inteiro do lado bom = candidato; inteiro do lado ruim = piora;
cruzando = nulo, com a metade do intervalo ao lado. Candidato só vira resultado com as sementes 6 a 15 de calendário
e decoder. As quatro são relatadas, tenham dado ou não; com quatro medidas a 95%, a chance de pelo menos uma passar
por acaso é de cerca de 19%, e uma que passe sozinha leva a frase "uma de quatro".

**Limites sabidos antes:** as medidas 2, 3 e 4 andam junto com a acurácia, e o decoder perdeu 0,9 ponto dentro da
distribuição; com três classes quase do mesmo tamanho, a pior classe pode só repetir a acurácia; um LLM, uma receita,
5 sementes.

**Regra de parada:** nenhuma outra medida, nem troca de faixas, de conjunto ou de corte, depois de ver os números,
sem decisão do Pedro e sem voltar a esta seção.

## Gap 9. O peso da perda do decoder (critério escrito em 19/11, 04h05, antes de rodar)

**Procedência:** dúvida do Pedro em 19/11 ("eu nunca vou deixar de achar que a gente só fez algo errado") e a
lista do Claude do que nunca foi variado; o Pedro escolheu os valores ("eu faria 0, 0,05 e 0,5 talvez") e deu o
prazo ("O gate fecha 12h"). Desenho, sementes e cortes são do Claude. **É uma varredura exploratória: 3 sementes por
valor, porque o prazo não comporta 5.**

**O que roda:** o braço `bert_decoder` nos 16.000 pares, mesma receita, com o peso da perda do decoder na fase C
(passos 1.201 a 4.000) em 0, 0,05 e 0,5, no lugar do 0,1 do artigo; sementes 1 a 3; `--fora --salvar-pesos`. As
fases A e B não usam o peso, então são iguais em todos os valores. **Peso 0** quer dizer: o decoder treina o encoder
só até o passo 1.200 e depois não pesa mais; separa o efeito dessa fase do efeito do peso durante a classificação.
Cada valor roda inteiro numa máquina e se compara com o calendário **da mesma máquina** (sementes 1 a 3) e com o
decoder de peso 0,1 quando ele existir nela.

**Medidas:** acurácia no dev do e-SNLI (a que decide) e acurácia no MNLI ao lado; diferença pareada por semente
contra o calendário, com o intervalo de 95% (com 3 sementes ele é largo: o fator é 4,3 em vez de 2,8).

**Regra de leitura:** um valor com o intervalo inteiro acima de zero no dev é **candidato**, e só isso: não vira
resultado sem as sementes 4 e 5 e depois 6 a 15, que não cabem antes do gate. Intervalo inteiro abaixo = piora;
cruzando = nulo. São três valores, então três chances de passar por acaso. O que se relata em qualquer caso é a
curva dos quatro pesos (0, 0,05, 0,1 e 0,5), descrita.

**Regra de parada:** nenhum outro valor de peso e nenhuma outra medida depois de ver os números, sem decisão do
Pedro. Corte de horário: nenhum treino novo começa depois das 08h30.

## Gaps que este arquivo não toca

- **Escala da receita (H2):** a fase A teve 39 passos no RTE e 63 no e-SNLI; o decoder com os 16 mil pares do
  e-SNLI, onde a Tabela 4 cabe, nunca rodou. É o único teste que derruba ou sustenta a explicação do nulo.
- **Qualidade das justificativas:** a avaliação humana de 29/10 não tem resultado registrado.
- **Dropout na atenção:** os nulos de 16/11 não foram rodados de novo sem ele.
