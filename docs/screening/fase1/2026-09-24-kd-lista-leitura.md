# Lista de leitura de destilação de conhecimento — funil sobre a árvore externa (24/09)

**Procedência: nível 3.** Títulos, anos, venues, resumos e contagens do Semantic Scholar. Ninguém leu os
artigos por causa desta lista, **exceto o Distilling Step-by-Step (nível 1, Pedro)**. A lista serve para
escolher o que ler; nada aqui é citável até ser lido.

## 1. O que é e por quê

**Pedido do Pedro (24/09):** usar a árvore da F1 para começar a ler agora, sem esperar o mapa, começando por
destilação. Motivos discutidos: destilação é certamente uma divisão da área (o survey central dela está na
árvore, ligado), é o centro da trilha do tema v3 e atravessa as três famílias de arquitetura que o ciclo
quer ensinar. **As outras divisões esperam o mapa v1** (alvo 05/10); a lista delas sai do mesmo funil depois.

**Onde isto fica no método:** é a volta de primários como seminais (§3.4: "fica no bruto e volta como
seminal"), antecipada para uma divisão. Não cria divisão nem altera a tabela-mestra.

## 2. Como foi feito

A árvore da F1 liga só surveys entre si. Os artigos que fundaram destilação (Hinton 2015, DistilBERT…) não
são surveys e nunca entraram na floresta. Eles aparecem nas **listas de referências** — a árvore externa.

| Passo | Regra | Resultado |
|---|---|---|
| 1. Votantes | obras da camada C com `distill` no título | 211 |
| 2. Escopo (decisão do Pedro) | fora: visão/CNN, *dataset distillation*, federada | 31 + 14 + 14 fora -> **152** |
| 3. Com referências no S2 | lista de referências recuperada (lote ou obra a obra) | 88 (54 de 2024-26) |
| 4. Candidatos | citado por >= 3 votantes (ou >= 3 votantes de 2024-26) | 240 |
| 5. Poda de genéricos | **especificidade** = votos de destilação ÷ citações na camada C inteira (14.901) >= 0,06 | ver §4 |
| 6. Escopo nos candidatos | mesma regra do passo 2, sobre título, resumo e venue | ver §5 |
| 7. Cotas por época | 5 por época; era LLM votada só pelos votantes de 2024-26; 2025-26 é fronteira, fora da base | §3 |

**Por que especificidade:** obra genérica é citada por todo mundo. BERT tem 23 votos de destilação, mas é citado
por 1.182 obras da camada C (0,019). Hinton 2015 tem 51 votos em 380 (0,134). O corte 0,06 está no vão dos
dados: os genéricos ficam em até 0,05 (BERT, Attention, GPT-2/3, T5, RoBERTa, InstructGPT, Llama, GLUE, Adam,
BLEU, DeepSeekMath), e a linhagem de destilação começa em 0,07 (DistilBERT, 0,072).

**Por que 2018+ exige sinal de linguagem:** o escopo acordado é destilar modelo de linguagem para implantação.
Antes de 2018 a regra não se aplica, porque a origem do método é anterior à separação entre linguagem e visão.

## 3. A lista (17 obras)

**Surveys de entrada** (entre os votantes: o mais citado em geral e o mais citado sobre LLM)

| Ano | Citações | Título | Id |
|---|---|---|---|
| 2020 | 4.643 | Knowledge Distillation: A Survey (Gou et al.) | arXiv 2006.05525 |
| 2024 | 379 | A Survey on Knowledge Distillation of Large Language Models (Xu et al.) | arXiv 2402.13116 |

O survey de Gou 2020 **também cai na regra de visão** pelo resumo (§5). Ficou aqui porque é o hub da área
(citado por 24 dos 88 votantes). **Decisão do Pedro:** manter ou tirar.

**História (até 2017)**

| Votos | Espec. | Ano | Título | Id | Família |
|---|---|---|---|---|---|
| 51 | 0,134 | 2015 | Distilling the Knowledge in a Neural Network (Hinton et al.) | arXiv 1503.02531 | geral |
| 13 | 0,210 | 2006 | Model compression (Buciluă et al.) | KDD 2006 | geral |
| 10 | 0,345 | 2016 | Sequence-Level Knowledge Distillation (Kim & Rush) | arXiv 1606.07947 | tradução (enc-dec, a confirmar) |
| 7 | 0,179 | 2013 | Do Deep Nets Really Need to be Deep? (Ba & Caruana) | arXiv 1312.6184 | geral |
| 6 | 0,316 | 2017 | Learning from Multiple Teacher Networks | KDD 2017 | a confirmar |

Quase entraram: Mean teachers (2017, 5) · Efficient KD from an Ensemble of Teachers (2017, 4) · Unifying
distillation and privileged information (2015, 4).

**Era BERT (2018-2021)**

| Votos | Espec. | Ano | Título | Id | Família |
|---|---|---|---|---|---|
| 17 | 0,072 | 2019 | DistilBERT | arXiv 1910.01108 | encoder |
| 11 | 0,423 | 2018 | Born Again Neural Networks | arXiv 1805.04770 | a confirmar (resumo cita modelo de linguagem) |
| 11 | 0,262 | 2019 | Patient Knowledge Distillation for BERT Model Compression | arXiv 1908.09355 | encoder |
| 11 | 0,112 | 2019 | TinyBERT | arXiv 1909.10351 | encoder |
| 7 | 0,269 | 2019 | Distilling Task-Specific Knowledge from BERT into Simple Neural Networks | arXiv 1903.12136 | encoder -> BiLSTM |

Quase entraram: When Does Label Smoothing Help? (6) · **MobileBERT** (6; eficiência em dispositivo) ·
Probabilistic Knowledge Transfer (5).

**Era LLM (2022-2024)**

| Votos 24-26 | Espec. | Ano | Título | Id | Família |
|---|---|---|---|---|---|
| 9 | 0,391 | 2023 | On-Policy Distillation of Language Models (GKD) | arXiv 2306.13649 | a confirmar |
| 9 | 0,188 | 2023 | Distilling Step-by-Step! — **Pedro já leu** | arXiv 2305.02301 | enc-dec (T5) |
| 6 | 0,086 | 2022 | Self-Instruct | arXiv 2212.10560 | geração de dado, não destilação em sentido estrito |
| 5 | 0,185 | 2023 | Specializing Smaller Language Models towards Multi-Step Reasoning | arXiv 2301.12726 | enc-dec (T5, pelo resumo) |
| 4 | 0,800 | 2023 | f-Divergence Minimization for Sequence-Level Knowledge Distillation | arXiv 2307.15190 | a confirmar |

Quase entraram: Universal Logit Distillation Loss (2024, 4) · **Teaching Small Language Models to Reason**
(2022, 4) · **Large Language Models Are Reasoning Teachers** (2022, 4). Os dois últimos são da mesma linha
do DSbS (destilar raciocínio).

**Correção a uma fala minha no chat (24/09):** eu disse que o On-Policy Distillation era da família decoder.
O resumo não diz a arquitetura (cita sumarização e tradução); fica "a confirmar na leitura".

## 4. Teste com gabarito embutido

- **Distilling Step-by-Step** (lido pelo Pedro) entrou, com 9 votos. O funil acha o que já sabemos ser central.
- **DHRD não entrou:** tem menos de 3 votantes. É de 2025 e é trabalho de workshop; ainda não foi citado o
  bastante. Isso mostra o limite do funil com obra recente, não que o DHRD seja irrelevante.

## 5. Fora por escopo, mas muito votadas (exceção possível — decisão do Pedro)

| Votos | Espec. | Ano | Título | Por que caiu |
|---|---|---|---|---|
| 24 | 0,159 | 2020 | Knowledge Distillation: A Survey | resumo cita visão (mantido como survey de entrada, §3) |
| 16 | 0,258 | 2014 | FitNets | resumo cita visão |
| 15 | 0,385 | 2019 | Improved KD via Teacher Assistant | resumo cita visão |
| 14 | 0,378 | 2016 | Attention Transfer | título: CNN |
| 13 | 0,302 | 2019 | Relational Knowledge Distillation | venue CVPR |
| 12 | 0,545 | 2019 | A Comprehensive Overhaul of Feature Distillation | resumo cita visão |

São métodos **gerais** de destilação testados em CNN, não aplicações de visão. FitNets, em particular, é a
origem da destilação de camadas intermediárias, que o TinyBERT e o PKD usam. A regra "visão/CNN fora" os tira;
**se a intenção era tirar só aplicações de visão**, FitNets deveria voltar para a história.

Também caíram pela regra de venue, depois de escaparem da de resumo: *A Gift from Knowledge Distillation* e
*Deep Mutual Learning* (ambos CVPR).

## 6. Fronteira 2025-26 (fora da base, só para saber que existe)

Os votos de 2024-26 concentram-se num cluster de 2026 sobre **autodestilação on-policy para raciocínio**
(RL + destilação): A Survey of On-Policy Distillation for LLMs (2026) · Reinforcement Learning via
Self-Distillation (2026) · Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?
(2026) · Rethinking On-Policy Distillation of LLMs (2026). DAPO (2025) é RL, não destilação. Obra com um
ano ainda não é fundamento; é o que a área discute agora.

## 7. Ordem de leitura sugerida (proposta; decisão do Pedro)

1. **Hinton 2015** — o artigo que dá nome ao método (logits suavizados por temperatura).
2. **Buciluă 2006** e **Ba & Caruana 2013** — a pré-história: comprimir um conjunto de modelos em um só.
3. **Gou 2020** (survey) — só a taxonomia (tipos de conhecimento, esquemas, algoritmos), para ter o mapa da divisão.
4. **Kim & Rush 2016** — destilação em nível de sequência (a ponte para geração de texto).
5. **DistilBERT -> PKD -> TinyBERT** — as três formas de destilar um encoder (só saída, camadas intermediárias, tudo).
6. **Xu 2024** (survey de LLM) — só a taxonomia.
7. **On-Policy Distillation (GKD)** e **Specializing Smaller LMs** — destilação na era LLM; o DSbS (já lido) entra aqui como ponto de comparação.

## 8. Limites

- 88 dos 152 votantes têm referências no S2; as de editora (IEEE/Elsevier/ACM) ficaram ocultas, e as
  referências do OpenAlex não foram casadas nesta rodada. Obras citadas sobretudo por artigos de editora ficam
  subcontadas.
- A regra de escopo é por expressão regular sobre título, resumo e venue. Pega o óbvio e erra na borda (os
  casos da §5 mostram os dois lados).
- `distill` no título perde surveys de compressão com seção de destilação. É recorte da divisão, não mapa.
- Contar votos favorece o antigo. As cotas por época corrigem isso só em parte.
- A família (encoder/decoder/enc-dec) só está marcada quando o título ou o resumo diz. O resto se confirma na leitura.

## 9. Decisões do Pedro

1. **FitNets e os outros métodos gerais testados em CNN (§5):** voltam ou ficam fora?
2. **Gou 2020:** fica como survey de entrada, mesmo tendo caído pela regra de visão?
3. **Self-Instruct:** fica? É geração de dado a partir de LLM (o survey de Xu 2024 trata isso como "extração de
   conhecimento"), não destilação de logits.
4. **Ordem de leitura (§7):** serve?

## 10. Arquivos

`scripts/screening/kd/`: `kd_funil.py` (votantes, candidatos, metadados) -> `kd_funil_candidatos.csv` (240
candidatos, todas as colunas; **ordena, não apaga**), `kd_funil_surveys.csv` (surveys votantes),
`kd_funil_meta.json` (cache do S2), `kd_funil_resumo.json`; `kd_lista.py` -> `kd_lista_saida.md`. Medição
anterior: `2026-09-24-kd-medicao.md`.
