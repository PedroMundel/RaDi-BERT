# Por que o decoder não ajudou: hipóteses tiradas dos dados já medidos (10/11/2026)

**Procedência:** análise do Claude sobre `resultados/{rte-treino,esnli-treino,rte-t5enc}/pc/*.csv`, o código de
`src/radibert/rte_treino.py` e as notas de nível 2 do Agrawal 2025. Nenhum treino novo. São **hipóteses**: cada uma
traz o dado que a sustenta e o teste que a derruba. O Pedro não leu este arquivo.

## H1. Os dois braços não receberam o mesmo treino de classificação (confundidor nosso)

No braço com decoder, a L_cls fica **desligada nos passos 1–187** (fase B) e a taxa do BERT tem o pico no passo 187
(decisão E1). No BERT cru, a L_cls vale do passo 1 e o pico segue a Tabela 4.

Área sob a curva da taxa com a L_cls ligada, em "passos de taxa cheia" (conta sobre `linear_schedule`):

| | BERT cru | BERT + decoder | Fração |
|---|---|---|---|
| Encoder, `prop` | 312 | 219 | 70% |
| Cabeça, `prop` | 312 | 170 | 54% |
| Encoder, `500` | 312, com pico só no passo 500 | 219, com pico no passo 187 | 70%, mas com curva melhor |
| Cabeça, `500` | 312 | 277 | 89% |

- No `prop` o braço com decoder perde 30–46% do treino de classificação, e deu **−0,028**.
- No `500` ele perde pouco e ainda ganha uma curva melhor para o BERT, e deu **+0,007**.
- Só trocar a curva no BERT cru (`500` × `prop`) já vale **0,025**, o mesmo tamanho do "efeito do decoder".
- Na sonda, a L_cls fica em 0,695–0,70 durante toda a fase B (RTE) e em 1,12 (e-SNLI): 30% dos passos sem aprender
  a tarefa.
- A semente 5 do `prop`, a pior (−0,087), termina com L_cls de 0,25 nos pares de **treino**: nem convergiu. (No `500`
  a semente 5 também termina em 0,17 e foi a melhor, então isso sozinho não fecha.)

**Leitura:** os sinais dos dois deltas saem do calendário, sem precisar do decoder. O que medimos pode ser "BERT com
menos treino", não "o decoder atrapalha".

**Teste que derruba (sem decoder, ~2 min por treino):** BERT cru com o calendário do braço com decoder (L_cls
desligada até o passo 187, pico do BERT em 187). Se der ~0,707 no `prop`, o delta é do calendário.

**Resultado (10/11): a H1 caiu.** Braço `bert_calendar`, `prop`, 5 sementes (`resultados/rte-calendario/pc/`):
0,746 ± 0,021 de ROC-AUC, contra 0,736 do BERT cru (+0,010, IC −0,020 a +0,041, vence 3/5) e 0,707 do braço com
decoder. Perder os 187 passos de classificação não custa nada ao BERT. O braço com decoder fica 0,039 abaixo do
controle (IC −0,097 a +0,020, perde 5/5 no ROC-AUC e 2/5 na acurácia): a queda vem do que o decoder faz com o BERT
(a L_aux na fase B e na C), não do calendário. A minha hipótese principal estava errada.

## H2. A fase A não cumpriu a função dela nesta escala

O §4.4 do paper põe a fase A para o decoder aprender a ler o BERT antes de o gradiente dele entrar no BERT.

- "50% dos dados" no RTE são **39 passos**. Num conjunto de 100 mil pares seriam ~1.560.
- No primeiro passo da fase B a L_aux ainda está em **7,0 nats por token** (lendo o próprio encoder do T5 ela começa
  em 4,2). O decoder entra na fase B sem saber ler o BERT.
- A fase B então empurra o BERT com ‖g_a‖ ≈ 9,5 (contra ‖g_c‖ ≈ 0,8), que é o cenário que o próprio paper diz evitar.
- A L_aux estaciona em ~3,0 perto do passo 300 e daí só cai 0,1. As palavras copiadas do par ficam em **4,5 nats**
  (2,5 lendo o encoder do T5) e as novas em 4,2; só o molde (rótulo e gramaticais, ~2,0 e ~1,8) é aprendido.
- 60–65% do empurrão no BERT vem das palavras copiadas: o sinal é "deixe os tokens legíveis para o T5", não "ache o
  fato que decide".

**Leitura:** todos os tamanhos da receita (500 passos, 50%, 30%) são de conjunto com 10–100 mil pares. Com 2,5–4 mil
o decoder não passa do molde, e a parte da justificativa que carrega o motivo nunca vira sinal.

**Teste que derruba:** fase A longa (BERT congelado, até a L_aux das copiadas parar de cair), feita **uma vez** e
salva; os treinos partem desse decoder. Se a L_aux das copiadas não descer de ~4,5, a ponte BERT → T5 é o limite.

## H3. Em números, a L_aux quase não fala da classe

- Uma justificativa do RTE tem ~30 tokens (sonda de `palavras.csv`) a ~3,0 nats: ~90 nats. O rótulo vale no máximo
  ln 2 = 0,69 nat, **menos de 1%**.
- Na fase C, pela média das normas, 0,1·‖g_a‖ / ‖g_c‖ é 0,38 no passo 200 e 0,05–0,09 do passo 400 em diante (em
  semente que já decorou o treino a ‖g_c‖ some e a razão passa de 1). O cosseno médio fica entre −0,11 e +0,05.
- A L_cls da sonda vai a 0,003–0,06: a classe o BERT já aprende sozinho. O que falta é generalizar, e isso só viria
  da parte "qual fato decide", que é a parte que o decoder não aprende (H2).

## H4. O ganho grande do paper só aparece onde o baseline está quebrado

Tabela 2 do Agrawal 2025: RTE 0,4754 → 0,5873 (baseline abaixo do acaso); com baseline forte, QQP +0,005, QNLI
+0,006, SST-2 −0,001. Os nossos intervalos (RTE `500`: −0,031 a +0,045; e-SNLI: −0,015 a +0,002) **contêm** esses
ganhos pequenos. O nosso BERT cru (0,736) fica 0,15 acima do **método** deles no RTE.

**Leitura:** contra baseline são, o paper promete meio ponto, e 5 sementes não enxergam meio ponto (no e-SNLI seriam
~15; no RTE, centenas). O que não repetimos é só a linha do baseline quebrado.

**Previsão para o braço MS-MARCO:** se o baseline sair perto de 0,47–0,55, o braço com decoder sobe, porque a fase B
tira o BERT da especialização em ranqueamento antes de a classificação começar. **Justificativa embaralhada daria o
mesmo ganho.** Se o baseline MS-MARCO sair perto de 0,70, o 0,4754 não vem da descrição do paper.

**Resultado (10/11, `resultados/rte-msmarco/leitura-grade.md`):** o baseline MS-MARCO (nboost) saiu em 0,767, não
em 0,47, e o decoder deu −0,049 (IC −0,078 a −0,021, perde 5/5). O paper não se repetiu com este checkpoint, e a
condição da previsão acima não aconteceu. O braço com decoder cai para 0,718, o mesmo valor do BERT cru com
decoder: apoia a H2 (a fase B desfaz o que o encoder trazia). A H1 não explica este caso.

## Como pode dar certo, por custo

1. **Controle de calendário (H1):** BERT cru com o calendário do decoder, 5 sementes, ~10 min. Diz se há efeito do
   decoder para explicar.
2. **Braço MS-MARCO (H4):** ~1 h. É o "repetir" que o professor pediu e o único lugar onde o paper mostra efeito
   grande.
3. **Fase A longa salva uma vez + L_cls ligada desde o passo 1 (H1 + H2):** foge da leitura literal do paper; é a
   variante em que a justificativa teria chance de virar sinal.
4. **e-SNLI com os 16 mil pares já gerados (H2):** primeira condição em que a Tabela 4 cabe (4.000 passos, fase A de
   250). O ganho esperado é de meio ponto, então pede mais sementes.

## Pode ser erro no nosso código? (pergunta do Pedro, 10/11)

Duas checagens feitas, as duas sem achar erro:

- **Equivalência (I17, `tests/test_rte_treino.py`):** com o peso da L_aux em 0, sem fase B e com um calendário só, o
  braço com decoder termina com os mesmos pesos do BERT cru (encoder e cabeça, diferença abaixo de 1e-7; modelo
  minúsculo, CPU, sem dropout). Com o peso 0,1 os pesos saem diferentes, então o teste compara de fato. Carregar o
  decoder não tem efeito colateral sobre o classificador.
- **Corte de gradiente (`resultados/rte-treino/run/medir_corte.py`, `corte.csv`; um treino por braço, `prop`,
  semente 1):** o corte em 1,0 é feito sobre o modelo inteiro, mas o gradiente do decoder quase não pesa na norma.
  A escala aplicada ao classificador é a mesma que seria sem o decoder: razão mediana 0,9998 na fase C (mínimo
  0,993) e 0,977 na fase B (mínimo 0,953). Não é a causa.
- **Observação do mesmo registro, uma semente só:** nos últimos 50 passos a norma do gradiente do encoder + cabeça
  é 0,06 no BERT cru e 1,4 no braço com decoder. O BERT cru termina com o treino decorado; o braço com decoder
  termina ainda longe disso. Eu li isso como compatível com a H1, mas o controle de calendário derrubou a H1
  (acima); a norma alta no fim deve vir da própria L_aux e do estado em que ela deixa o BERT, e isso não foi medido.

Continua sem resposta possível: se a nossa leitura dos pontos vagos do paper é igual à implementação deles.

## Fora desta análise

O braço T5 com decoder (L_cls parada em ln 2 por 600 passos) tem causa própria (taxa de BERT num T5, média dos
tokens) e não entra na explicação do BERT.
