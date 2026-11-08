# Leitura sobre seleção de dados de treino: quantos pares e quais pares

**Procedência (nível 3):** um agente conferiu a página da fonte (arXiv, ACL Anthology) e o resumo. Serve para triagem, **nunca para citação**. O Pedro ainda não leu nenhuma destas obras. Detalhes de método e resultado abaixo vêm de busca e de leitura parcial do HTML por modelo e podem ter erro de sumarização.

**Conferência do Claude (26/10):** abriu de novo a página e o HTML de #1, #2 e #3. Batem os títulos, os autores, o
venue (#1 CoLLAs 2024 pelo campo *Comments*; #3 COLING 2025, p. 1294–1308; #2 sem *Comments*, então é preprint), o
SNLI e o RoBERTa-large no #1 (§4.1), a comparação com subconjunto aleatório e com o Dataset Cartography no #1, e o T5
com ANLI1 no #2. A fração de pares com racionalização varia de 0% a 100% no §5.4 do #2. O "um terço dá mais de 90% do
ganho" está só na conclusão do #2, não na tabela de resultados. Continua nível 3 para o conteúdo.

**Data da pesquisa:** 26/10/2026. Nada aqui decide o desenho do experimento; o Pedro escolhe.

## Tabela de candidatas

Todas de 2023 ou depois. Nenhuma das rejeitadas (MobileBERT, Gou 2020) entrou.

| # | Obra (título, autores, ano, venue, link) | Pergunta | Por que serve a este experimento | NLI/SNLI ou encoder? | Tamanho | Ressalvas |
|---|---|---|---|---|---|---|
| 1 | **Automatic Pruning of Fine-tuning Datasets for Transformer-based Language Models**. Tayaranian, Mozafari, Meyer, Clark, Gross. 2024. CoLLAs 2024 (campo *Comments* do arXiv). [arXiv:2407.08887](https://arxiv.org/abs/2407.08887). **RECOMENDADA** | Quais (e quantos, pois gera subconjuntos de vários tamanhos) | Poda o conjunto de ajuste fino pelo número de vezes que cada exemplo é classificado certo (escore H). Compara com subconjunto aleatório do mesmo tamanho e com a seleção "ambígua" do Dataset Cartography. Os subconjuntos vão de ~4% a ~33% do treino, o que funciona como curva de aprendizado | **Sim: SNLI e MNLI** (também SST-2, SQuAD v2, RACE). Modelos: RoBERTa-large e OPT-350M (conferido no HTML) | 28 p. + 17 figuras (campo *Comments*) | Exige treinar o modelo várias vezes para contar acertos; custo na 5060 a avaliar. Só classificação, sem racionalização. A seleção usa só o rótulo, então vale igual aos 4 braços |
| 2 | **Leveraging Zero-Shot Prompting for Efficient Language Model Distillation**. Vöge, Gurgul, Lessmann. 2024. [arXiv:2403.15886](https://arxiv.org/abs/2403.15886) | Quantos (fração de pares com racionalização) | Mesmo mecanismo do Distilling Step-by-Step: LLM professor gera rótulo + racionalização, aluno treina multitarefa. Varia de 0% a 100% a fração de exemplos com racionalização. Relatam que ~85% empata com 100% e que ~1/3 dos exemplos dá >90% do ganho | **NLI sim (ANLI)**, mas aluno é **T5** (encoder-decoder, 77M a 3B), professor gpt-3.5-turbo. Não é encoder-only | Não verificado (artigo curto) | **Preprint: sem venue verificável** (sem *Comments* no arXiv; a busca não achou publicação). Os 2 conjuntos são pequenos (ANLI R1 ~17 mil pares, CQA ~8,8 mil). O limiar de 1/3 vem de um aluno T5-base, pode não valer para o encoder |
| 3 | **FTFT: Efficient and Robust Fine-Tuning by Transferring Training Dynamics**. Du, Gatt, Nguyen. 2023 (v1) / 2025 (versão final). COLING 2025, pp. 1294-1308, ID 2025.coling-main.86 ([ACL Anthology](https://aclanthology.org/2025.coling-main.86)); [arXiv:2310.06588](https://arxiv.org/abs/2310.06588) | Quais, a custo menor | Sucessor direto do Dataset Cartography: um modelo de referência barato (ex.: ELECTRA-small) calcula a dinâmica de treino e o modelo principal treina só nos 33% mais ambíguos. Corta até ~50% do custo e compara com subconjunto aleatório de 33% | **MNLI** (teste fora de domínio em ANLI) e discurso de ódio. Modelos encoder: DeBERTaV3 base/large, ELECTRA, BERT-large, RoBERTa-large, TinyBERT. **Não usa SNLI** | 15 p. nos anais + apêndice | O alvo principal é **robustez fora de domínio**, não eficiência pura. A seleção por ambiguidade é de um único tamanho (33%), não uma curva. Sem racionalização |
| 4 | **A Survey on Data Selection for Language Models**. Albalak et al. (14 autores). 2024. TMLR 2024 (índice [mlanthology](https://mlanthology.org/tmlr/2024/albalak2024tmlr-survey); OpenReview `XfHWcNTSHp` não abriu); [arXiv:2402.16827](https://arxiv.org/abs/2402.16827) (v3, ago/2024) | Quais (visão geral) | Taxonomia dos métodos de seleção (filtragem, deduplicação, mistura) e lacunas; serve como mapa de vocabulário para saber o que existe | Não. Foco em **pré-treino** de LLM; cobre também ajuste por instruções e multitarefa. Nada específico de NLI nem de encoder | Longo (página não informada no arXiv; contagem não verificada). Ler só as seções de ajuste fino/multitarefa | Pouca ligação direta com o experimento. É a "no máximo um survey" pedida. O arXiv não tem campo *Comments* de venue, por isso o venue vem do índice |

## Recomendação (ler primeiro)

**Tayaranian et al. 2024 (#1).** É a única que reúne SNLI, aluno encoder, comparação com Dataset Cartography e subconjuntos de vários tamanhos num mesmo texto, com venue conferido. Responde "quais" e dá uma régua de "quantos" para classificação. Se depois quiser a pergunta da racionalização, o Vöge (#2) é a segunda leitura (curto, mesmo mecanismo, mas T5 e preprint). O Pedro decide.

## O que cada uma NÃO responde

- **#1 Tayaranian:** não diz nada sobre racionalização nem sobre se ela ajuda mais com pouco dado. Seleciona pelo rótulo e pelo comportamento do modelo; não diz quantos pares precisam de racionalização.
- **#2 Vöge:** não testa SNLI nem aluno encoder-only; o resultado da fração é de T5 em ANLI/CQA (conjuntos de ~9-17 mil pares). Não diz **quais** pares devem receber racionalização (só reduz a fração, em amostra). Sem venue.
- **#3 FTFT:** mede robustez fora de domínio, não ganho em dados escassos. Usa MNLI, não SNLI. Um tamanho fixo de subconjunto, sem curva.
- **#4 Albalak:** nada específico de NLI, de encoders ou de racionalização; é pré-treino.
- **Nenhuma** testa se a racionalização ajuda mais com poucos dados em e-SNLI com encoder. Essa é a lacuna que o experimento do Pedro mexe (a curva 10k a 100k com os quatro braços).

## Pontos de atenção para o desenho (observação do agente, sem decidir)

- Qualquer seleção (#1, #3) usa o rótulo; aplicada **antes** de gerar racionalizações vale para os 4 braços iguais. Selecionar pela dificuldade de um modelo treinado no próprio e-SNLI custa um treino prévio.
- Vöge sugere que racionalizar só uma fração dos pares basta; no experimento do Pedro isso seria um braço adicional (fração da racionalização), não só o tamanho total.

## Fontes conferidas

- [arXiv 2407.08887 (abs)](https://arxiv.org/abs/2407.08887) e [HTML](https://arxiv.org/html/2407.08887): título, autores, *Comments* (CoLLAs 2024), conjuntos e modelos.
- [arXiv 2403.15886 (abs)](https://arxiv.org/abs/2403.15886) e [HTML](https://arxiv.org/html/2403.15886v1): autores, conjuntos, modelos, seção 5.4 (fração de racionalização).
- [arXiv 2310.06588](https://arxiv.org/abs/2310.06588) (*Comments*: COLING 2025 Camera-Ready) e [ACL Anthology 2025.coling-main.86](https://aclanthology.org/2025.coling-main.86); [HTML v3](https://arxiv.org/html/2310.06588v3): conjuntos e modelos.
- [arXiv 2402.16827](https://arxiv.org/abs/2402.16827) e [mlanthology](https://mlanthology.org/tmlr/2024/albalak2024tmlr-survey).

## Estado de verificação

| Obra | Título/autores/ano | Venue | Conjuntos/modelos |
|---|---|---|---|
| #1 Tayaranian | conferido (arXiv) | conferido (*Comments* do arXiv) | conferido (HTML) |
| #2 Vöge | conferido (arXiv) | **sem venue verificável** | conferido (HTML) |
| #3 FTFT | conferido (arXiv + Anthology) | conferido (Anthology) | conferido (HTML) |
| #4 Albalak | conferido (arXiv) | TMLR via índice secundário; OpenReview não abriu | n/a (survey) |

## Becos sem saída e descartes

- **Dataset Cartography (Swayamdipta et al., EMNLP 2020, [arXiv:2009.10795](https://arxiv.org/abs/2009.10795))**: avaliado em SNLI, mas é de 2020 (6 anos), a regra do Pedro é recusar. Não listado; o #1 e o #3 já o usam como baseline e o descrevem, então ele não é indispensável para ler.
- **Du et al., "Disentangling the Roles of Representation and Selection in Data Pruning"** (ACL 2025, [2025.acl-long.821](https://aclanthology.org/2025.acl-long.821)): existe e é recente, mas não usa NLI (CAD, WinoGrande, DialogSum). Fora.
- **Chimoto et al., ACL Findings 2024** (dinâmica de treino): é de tradução automática. Fora.
- **Jazbec et al., "On Efficient Distillation from LLMs to SLMs"** (workshop NeurIPS 2024): decoder 7B, matemática. Fora.
- **MoRSD (arXiv:2509.23574, 2025)**: seleção de racionalizações em CoT de raciocínio, não NLI nem encoder; encontrado só no resumo da busca, não verificado na fonte. Fora.
- **"Are Training Resources Insufficient? Predict First Then Explain!"** (arXiv:2110.02056, 2021): trata de poucos dados de explicação, mas é de 2021 e não foi verificado. Fora.
- Não achei estudo de curva de aprendizado de encoder em NLI (2023+) que seja de fato sobre tamanho de amostra; a evidência de "quantos" vem de #1 (tamanhos de subconjunto) e #2.

## Decisão do Pedro (26/10)

- **#1 (Tayaranian 2024): interessante, guardado para a fase de treino.** "A gente não tá pronto pra treinar ainda,
  pode servir quando for." A poda dele exige vários treinos, então só cabe quando houver pipeline de treino.
- **#2 (Vöge 2024) sozinho não ajuda muito.** Fica sem leitura por ora.
