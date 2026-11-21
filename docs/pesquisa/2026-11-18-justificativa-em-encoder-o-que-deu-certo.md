# Justificativa no treino de um encoder: algo publicado deu certo?

Data: 18/11/2026. Pesquisa externa, só relatório. O Pedro decide.

## Procedência (leia primeiro)

**Tudo aqui é nível 3.** Um agente leu, para triagem. Nada serve para citação sem o Pedro abrir o original.

Como cada item foi lido (marcado em cada ficha):

- **HTML**: página HTML do arXiv ou ar5iv. O texto passou por um modelo pequeno que respondeu às minhas perguntas. Os números abaixo vêm dessas respostas e precisam ser conferidos no PDF.
- **Resumo**: só a página de resumo (arXiv ou Anthology).
- **Trecho de busca**: só o que o buscador mostrou. É o nível mais fraco.
- Nenhum PDF foi lido: a ferramenta não decodifica PDF.

Já conhecido e não repetido como novo: Agrawal 2025, LRKD, Distilling Step-by-Step, DHRD, KNIFE, Wadhwa 2024, Stacey 2022 (entra só como régua), marcas de atenção, cabeça de grupos no `[CLS]`, imitar o interior do professor. O que a pesquisa de 10/11 já tinha (Hase e Bansal, ER-Test, Pruthi, Ross 2022 etc.) não foi refeito, só aprofundado onde faltava número.

Respeitado o `## Rejected`: nada de Claude como gerador, nada de contraste tipo SCOTT, nada de "mais dados para o decoder", nada de variação das marcas, nada de cabeça no `[CLS]` para grupos.

## Resposta curta

Não achei método publicado, com encoder lendo só a entrada na inferência, que mostre ganho dentro da distribuição sobre linha de base bem ajustada, com controle e variância. Os melhores casos têm ganho de 0,1 a 1,3 ponto e falham em algum item (poucas sementes, sem variância, sem controle de justificativa embaralhada, ou justificativa que não é texto livre).

## Parte 1. Candidatos que cabem na pergunta (encoder, justificativa só no treino)

### 1.1 Wang e Wu 2026, EIDRR (o mais próximo e o mais recente)

- **Título:** Improving Implicit Discourse Relation Recognition with Natural Language Explanations from LLMs. Heng Wang, Changxing Wu. arXiv:2602.21763, AAAI 2026 (campo Comments diz "AAAI26 oral"). https://arxiv.org/abs/2602.21763
- **Lido:** resumo e HTML.
- **Treino:** entrada mais rótulo mais justificativa de LLM (Qwen-long, uma só). Modelo conjunto: encoder estilo RoBERTa (classificador com prompt) ligado a um decoder estilo T5 por **uma camada Transformer nova** que faz a ponte. O decoder gera a justificativa condicionada ao rótulo previsto.
- **Inferência:** o rótulo sai do caminho do classificador. O artigo **não diz** se a justificativa é necessária para prever. Marcado: não consegui ver.
- **Encoder-only:** o classificador sim; o conjunto tem decoder auxiliar (mesma família do Agrawal).
- **Dados:** PDTB (12.775 treino, 1.183 validação, 1.046 teste, 4 relações), ATSC (Restaurant15, 963/361/576) e **NLI** (1.499 treino, 400 validação, 600 teste, amostra do corpus de Chen et al. 2017; o artigo não nomeia o corpus).
- **Números dentro da distribuição:**
  - PDTB: 71,80 sem justificativa, 73,14 com. Ganho +1,34 de acurácia e +1,14 de F1.
  - NLI: 74,83 para 75,83 (+1,00); F1 74,79 para 75,73.
  - ATSC: 85,59 para 87,44 (+1,85).
- **Sementes e variância:** média de 3 sementes. Sem desvio, sem intervalo, sem teste. O texto diz "significativamente" sem teste.
- **Linha de base:** no PDTB há linhas de base da literatura (GOLF 72,52; SCIDER 72,11; Discoprompt 71,70). O ganho sobre a melhor é +0,62 de acurácia. No NLI e no ATSC não há linha de base externa, só o braço sem justificativa. Não sei se as linhas de base foram refeitas ou copiadas.
- **Controles:** só o braço sem justificativa. **Sem justificativa embaralhada ou aleatória no treino.**
- **Falhas que o artigo admite:** ganho de cerca de 1 ponto sobre as melhores; faithfulness avaliada só em parte; uma só fonte de justificativa; NLI e ATSC pequenos e sem linhas de base.
- **Código:** https://github.com/nlper-hub/EIDRR (licença: não consegui ver).
- **Para tentar com os dados do Pedro:** o desenho é o do braço `bert_decoder` que ele já tem, trocando a ponte por uma camada Transformer nova. Com os 16.000 pares do e-SNLI, o braço com decoder já deu nulo; a camada de ponte seria a única diferença.

### 1.2 Bhat, Sordoni e Mukherjee 2021 (BERT, e-SNLI, poucos dados)

- **Título:** Self-training with Few-shot Rationalization: Teacher Explanations Aid Student in Few-shot NLU. arXiv:2109.08259, EMNLP 2021. https://arxiv.org/abs/2109.08259
- **Lido:** resumo e ar5iv HTML.
- **Treino/inferência:** BERT-base compartilhado com duas cabeças (tarefa e justificativa). Na inferência prevê o rótulo com a entrada inteira (o artigo diz que usa a entrada completa).
- **Encoder-only:** sim. Mas a cabeça de justificativa é **por token (extrativa)**, não texto livre. Não consegui ver se vêm dos destaques humanos do e-SNLI.
- **Dados:** e-SNLI, Movies, FEVER, BoolQ, Evidence Inference.
- **Números (Tabela 2, F1 médio, 100 exemplos por classe, ou seja poucos dados):** BERT sem justificativa 61, BERT com justificativa 62, método completo 66. e-SNLI: 59, 61 e 67. A parte multitarefa sozinha dá +2 no e-SNLI; o resto do ganho vem de **autotreino com pseudo-rótulos**, que usa dados sem rótulo.
- **Com 25% dos dados:** 72, 72 e 74 (média).
- **Supervisão completa:** o texto diz "+2,6%" de BERT com justificativa sobre BERT puro. A tabela mostra 79 contra 77 (média de 5 conjuntos). O 2,6% é relativo (2/77), não pontos.
- **Sementes e variância:** não reportadas.
- **Linha de base fraca?** Poucos dados, então a base é baixa por desenho. Não serve para julgar o regime de 16.000 pares.
- **Controles:** nenhum com justificativa embaralhada.
- **Código:** https://aka.ms/RationaleST (licença: não consegui ver).
- **Para tentar:** exige justificativa por token e pseudo-rótulos em dados sem rótulo. O Pedro tem justificativa em texto livre, não por token (a não ser os destaques humanos do e-SNLI). Custo de horas só na versão de 300 exemplos.

### 1.3 Pruthi et al. 2022 (BERT, destaques, sem NLI)

- **Título:** Evaluating Explanations: How much do explanations from the teacher aid students? Pruthi e outros sete. arXiv:2012.00893, TACL (a busca de hoje diz 2021, o arquivo de 10/11 diz 10:359-375, 2022). https://arxiv.org/abs/2012.00893
- **Lido:** ar5iv HTML.
- **Treino/inferência:** explicação só no treino. Alunos BERT-base (sentimento IMDb e QA Natural Questions). **Não há NLI.** As explicações são destaques (humanos ou atribuição), não texto livre.
- **Números, BERT-base, F1 de QA com explicação do professor (250 / 1 mil / 4 mil / 16 mil exemplos):** sem explicação 25,0 / 37,7 / 52,6 / 61,6; regularização de atenção 27,6 / 42,8 / 54,4 / 62,3. O ganho **encolhe com mais dados** (+2,6, +5,1, +1,8, +0,7).
- **Multitarefa (perda auxiliar):** com explicação humana em sentimento, 75,2 / 80,0 / 82,5 contra 75,5 / 79,0 / 81,1 sem explicação. Praticamente nada. O que ajuda é regularizar a atenção, que é a família das marcas de atenção já testadas.
- **Sementes:** não reportadas. **Controles:** explicações aleatórias e triviais não superam o braço sem explicação (isso é um controle, e bom).
- **Código:** github.com/danishpruthi/evaluating-explanations (indicado na página; licença: não consegui ver).

## Parte 2. Evidência negativa ou nula direta

### 2.1 Hase e Bansal 2021/2022

- **Título:** When Can Models Learn From Explanations? A Formal Framework for Understanding the Roles of Explanation Data. arXiv:2102.02201, First Workshop on Learning with Natural Language Supervision (ACL 2022), pp. 29-39. https://arxiv.org/abs/2102.02201
- **Lido:** HTML (texto todo).
- **O que testa:** explicação **recuperada e lida como entrada**, RoBERTa-base, e-SNLI. Isso **não é** o caso do Pedro (a justificativa entra na inferência). Entra porque mede o e-SNLI com intervalos.
- **Números (Tabela 3, acurácia, intervalo de 95%):** 5 mil: 84,83 contra 85,04; 10 mil: 85,52 contra 86,03; 50 mil: 87,90 contra 87,55; completo: 91,06 contra 91,41. Efeito completo +0,35, intervalo ±0,79: **cruza o zero em todos os tamanhos**.
- **Sementes:** 3 sementes nos três outros conjuntos; **1 semente** no e-SNLI com 50 mil ou mais.
- **Útil para o Pedro:** dá régua de linha de base do RoBERTa no e-SNLI (84,83 com 5 mil; 91,06 completo) para saber se a base dele é fraca.
- **Alvo, não entrada:** o texto traz a frase "None of these works find improvements in task performance from incorporating explanations", citando Camburu e outros (aplicada a explicações como alvo). Li só a frase, não a revisão que a sustenta.

### 2.2 Popovič e Färber 2025, JEDI

- **Título:** Extractive Fact Decomposition for Interpretable Natural Language Inference in one Forward Pass. EMNLP 2025 main, pp. 31692-31705. arXiv:2509.18901. https://aclanthology.org/2025.emnlp-main.1615/
- **Lido:** resumo e HTML.
- **O que é:** encoder-only (DeBERTa) treinado com justificativas sintéticas de LLM (corpus SYRP) como spans, em ANLI. O objetivo é interpretabilidade, não nota. A inferência **emite spans**.
- **Números, DeBERTa-large, ANLI (Tabela 1):** base 68,1, JEDI 65,6 (−2,5). DeBERTa-base: 58,5 contra 57,0. HANS: 79,1 base, 76,9 JEDI. 10 sementes, sem desvio nem teste. As linhas de base vêm de Stacey et al. 2024 e foram reproduzidas "com diferenças pequenas".
- **Leitura:** supervisão por justificativa de LLM em encoder **perdeu** para a base em ANLI. É um achado negativo, mas o método tem outro objetivo.
- **Código:** jedi.nicpopovic.com (licença: não consegui ver).

### 2.3 Joshi et al. 2022, ER-Test

- Findings of EMNLP 2022, pp. 3315-3336, arXiv:2205.12542. **Resumo:** duas tarefas, seis conjuntos, regularização por explicação tem pouco efeito dentro da distribuição e ganhos fora. Já no arquivo de 10/11.

### 2.4 Soft labels de LLM em NLI com BERT e RoBERTa

- **Título:** "Seeing the Big through the Small": Can LLMs Approximate Human Judgment Distributions on NLI from a Few Explanations? arXiv:2406.17600 (campo de venue: não consegui ver). Lido em HTML (os últimos ~21 mil caracteres não foram lidos).
- **O que testa:** BERT-base e RoBERTa-base ajustados em distribuições de julgamento geradas por LLM (Llama 3, Mixtral), com explicações **só no prompt do LLM**, não no encoder. ChaosNLI.
- **Números (F1 ponderado e KL, dev/teste):** base com rótulos humanos do ChaosNLI, BERT 0,626/0,646, KL 0,074/0,077; melhor Llama 3, BERT 0,585/0,568, KL 0,086/0,087. O LLM **não alcança** o rótulo humano. Os autores falam em resultados "parcialmente inconsistentes".
- **Leitura:** é o caso "relabel/soft-label com LLM" e ele perde para o humano. Não é o mesmo que treinar com a justificativa.

### 2.5 Sentido contrário em modelos que não são encoder

- **Shah et al. 2025**, "Regularization Through Reasoning: Systematic Improvements in Language Model Classification via Explanation-Enhanced Fine-Tuning", arXiv:2511.02044 (v2 de 1/3/2026, sem venue na página, CC BY 4.0). **Resumo.** Modelo de 7B (decoder). Justificativa mais rótulo supera rótulo sozinho em 18 configurações, mas **pseudoexplicações embaralhadas ou em saco de palavras também superam o rótulo sozinho**; os autores atribuem a efeito de regularização e de mais tokens. Não é encoder, e não vi números. Serve de aviso: um ganho com justificativa real pode ser ganho de regularização.

## Parte 3. Não servem à pergunta (e por quê)

Cada um verificado até onde indica a coluna "lido". A razão de exclusão está dita.

| Obra | Lido | Por que não serve |
|---|---|---|
| ExpBERT, Murty, Koh, Liang. ACL 2020, arXiv:2005.01932 | resumo | Extração de relação (não NLI). O BERT, ajustado no MNLI, interpreta as explicações em relação a cada entrada para gerar atributos; o resumo sugere que as explicações são usadas ao montar a representação (não confirmado se na inferência). Ganho de 3 a 10 F1 com os mesmos dados, em três tarefas que o resumo não nomeia. Também cai em "encoder já ajustado para NLI" (previously rejected, 14/10). |
| NILE, Kumar e Talukdar. ACL 2020, arXiv:2005.12116 | trecho de busca | Gera explicações por rótulo na inferência. Não é treino só. Números não vistos. |
| LIREx, Zhao e Vydiswaran. AAAI 2021, arXiv:2012.09157 | trecho de busca | Gerador de explicação mais seletor, as explicações aumentam a entrada do modelo de NLI. SNLI 91,87, +0,32 sobre a base (da página do AAAI); sem variância vista. Explicação entra na inferência. Código: github.com/zhaoxy92/LIREx. |
| e-SNLI, Camburu et al. NeurIPS 2018, arXiv:1812.01193 | trecho de busca | BiLSTM/InferSent, não BERT. Resumo diz que as explicações melhoram representações de sentenças e transferem para outros NLI. Resumo de terceiros: SICK-E 53,54 contra 53,27 e MNLI 57,16 contra 57,00, ganhos marginais (não conferidos no artigo). |
| FLamE, Zhou, Zhang, Tan. ACL 2023, arXiv:2306.08042 | resumo | Poucos dados. Ganho de 17,6% sobre GPT-3 Babbage e 5,7% sobre Davinci (comparação com LLM, não com RoBERTa). A busca trouxe que treinar com explicação e testar sem cai para 60,5 no e-SNLI (PET); não conferi no artigo. Resumo diz que a maioria das explicações geradas não justifica a decisão. Não consegui ver se a explicação entra na inferência. |
| Li et al. 2022, "Explanations from LLMs Make Small Reasoners Better", arXiv:2210.06726 | HTML | **T5**, perguntas e respostas, sem controle embaralhado, sem código. T5-base: CommonsenseQA 63,05 para 64,50; OpenBookQA 58,08 para 60,68. Média de 5 rodadas só em parte dos casos. |
| Ludan et al. 2023, "Explanation-based Finetuning Makes Models More Robust to Spurious Cues", ACL 2023, arXiv:2305.04990 | trecho de busca | GPT-3, robustez a atalhos (+15,4 no e-SNLI), e **pequena perda de acurácia absoluta sem atalhos, mais em modelos pequenos**. Não é encoder. |
| RationaleCL, Xiong et al. EMNLP 2023, arXiv:2310.06547 | trecho de busca | T5, aprendizado contínuo de relações. |
| ExaRanker, Ferraretto et al. SIGIR 2023, arXiv:2301.10521 e ExaRanker-Open arXiv:2402.06334 | trecho de busca | Reranqueador seq2seq (monoT5). Ganho de 2,6 nDCG@10 com 5 mil exemplos, **encolhe com mais dados** segundo os autores. Cerca de 1 ponto médio no Open. Não é encoder. |
| DET, Du et al. Findings EMNLP 2025, pp. 12800-12816 | resumo | Um LLM gera explicações por rótulo e elas viram atributos para treinar um modelo pequeno. Não consegui ver se o LLM roda na inferência (provável). Sem número, sem código na página. |
| Hybrid Attribution Priors, Zhang et al. arXiv:2512.14719 | trecho de busca | Usa atribuição de modelo, não justificativa. Fora de escopo. |
| DISCO (arXiv:2212.10534) e contrafactuais por LLM (arXiv:2503.04463, 2405.00722, ACL 2025 long.260) | trecho de busca | Ganhos em robustez e fora de domínio. Nenhum trecho trazia ganho dentro da distribuição. |
| Hartmann e Sonntag 2022, survey, arXiv:2204.08892, LNLS 2022 pp. 40-47 | HTML | O levantamento diz que não há comparações entre os métodos e **não traz efeito de perda auxiliar com texto livre**. Sem número útil. |

## Parte 4. Pistas da lista que não verifiquei

- **MaRio** (arXiv:2311.02805, "Tailoring Self-Rationalizers with Multi-Reward Distillation"): só trecho de busca; é gerador de racional em perguntas e respostas, LM pequeno, sem encoder. Autoria e ano não confirmados.
- **SCOTT** (arXiv:2305.01879, ACL 2023): já rejeitado em CLAUDE.md. Só trecho de busca; backbone não visto.
- **UNIREX** (arXiv:2112.08802) e **LIREx**: UNIREX só no arquivo de 10/11.
- **Contrastivo com a justificativa como visão positiva, "label-description training":** não achei obra com NLI e BERT. O que a busca trouxe: "The Benefits of Label-Description Training for Zero-Shot Text Classification" (EMNLP 2023, RoBERTa, zero-shot em tópico e sentimento, não NLI com treino supervisionado), só trecho. QCRD (EMNLP 2025, arXiv:2405.13014) é destilação contrastiva de racional, geradora, não encoder. Não usados.
- **Reason2Decide** (arXiv:2512.20074): LLM, não encoder, trecho truncado.
- **2512.16236** (reranqueador com racional): só trecho, sem detalhe.

## Tabela de comparação (ONE-TABLE)

Legenda: "Força da evidência" vai de fraca a média pela minha leitura, só nível 3. "Custo para tentar" é estimativa minha sobre o código que o Pedro já tem, não medida. O Pedro escolhe.

| Opção | Força da evidência | Tamanho do ganho dentro da distribuição | Custo para tentar em horas, uma GPU de 16 GB | Encaixe com os dados do Pedro | Maturidade / licença e código |
|---|---|---|---|---|---|
| A. EIDRR (Wang e Wu 2026): RoBERTa mais decoder T5, camada de ponte nova, justificativa só no treino | Fraca: 3 sementes, sem variância, sem embaralhado, uma fonte de justificativa | +1,34 acurácia no PDTB; +1,00 no NLI pequeno (1.499 pares) | Baixo: é o braço com decoder que ele já tem, com outra ponte; cada semente de e-SNLI com 16 mil pares é longa, mas cabe em horas | Alto no formato (um racional por par). O nulo medido com decoder nos 16 mil pares é o mesmo desenho | Recente (AAAI 2026), código em github.com/nlper-hub/EIDRR, licença não vista |
| B. Bhat et al. 2021: BERT-base com cabeça de racional por token, mais autotreino | Fraca a média: sem sementes; ganho multitarefa de +2, o resto vem do autotreino | +2 só da cabeça de racional; +8 com autotreino, mas em 300 exemplos | Médio a alto: exige racional por token e pseudo-rótulos em dados sem rótulo | Baixo: a justificativa do Pedro é texto livre, não por token; regime de poucos dados | EMNLP 2021, código em aka.ms/RationaleST, licença não vista |
| C. Stacey et al. 2022: atenção supervisionada por destaques humanos do e-SNLI (**já conhecido**, entra só como régua) | Média: 25 sementes, intervalos, controle de OOD (pelo resumo de terceiros) | +0,40 em BERT, +0,10 em DeBERTa (92,59 para 92,69) | Baixo: já tem a infraestrutura de marcas de atenção | Já testado de outro jeito (marcas de atenção, nulo no e-SNLI) | AAAI 2022; código: não consegui ver |

## Resposta honesta, em um parágrafo

**O que foi conferido:** abri a fonte (resumo ou HTML) de nove obras que importam e vi só trechos de busca em outras tantas; nenhum PDF. **O que a evidência diz:** não, nada sólido. O único estudo com 25 sementes (Stacey) dá +0,40 em BERT e +0,10 em DeBERTa, com destaque humano em vez de texto livre. O melhor caso com texto livre de LLM e encoder (EIDRR) dá +1,0 a +1,3 com 3 sementes, sem variância e sem justificativa embaralhada, na mesma família do Agrawal que o Pedro não conseguiu repetir. Os que mostram ganho grande são poucos dados ou usam a explicação na inferência (Bhat, FLamE, ExpBERT, LIREx). Em todos os pares com NLI e mais dados, o ganho some ou fica dentro do intervalo (Hase e Bansal, JEDI, Pruthi nos 16 mil, ExaRanker). E há dois sinais de que o ganho publicado pode ser regularização e não conteúdo: Shah (decoder 7B, embaralhado também ajuda) e o que o próprio Pedro mediu (calendário sozinho ajuda). Isto vale para o que achei e li; não prova que não exista obra melhor.

## O que não consegui verificar

- Qualquer número exato de PDF: nenhum foi lido; os números de HTML passaram por um resumidor.
- Stacey 2022: a tabela com RoBERTa e os intervalos; o "estatisticamente significativo" vem de resumo de terceiros.
- Se a justificativa é necessária na inferência no EIDRR, FLamE, ExpBERT e DET.
- Se o rótulo da cabeça por token em Bhat 2021 vem dos destaques humanos do e-SNLI.
- Licença de todos os códigos citados.
- Números de NILE, LIREx (só o do resumo), Camburu (tabela), Ludan, RationaleCL, ExaRanker, DISCO.
- Venue de arXiv:2406.17600 e os últimos ~21 mil caracteres da página.
- MaRio e SCOTT: autoria, ano e backbone.
- Se existe obra de 2024 a 2026 com encoder e justificativa de LLM que as buscas não pegaram. As buscas usadas (cinco com termos diferentes) não acharam, mas o buscador não substitui um levantamento sistemático.
- Pruthi: ano de publicação (2021 na busca de hoje, 2022 no arquivo de 10/11).

## Fontes principais

- https://arxiv.org/abs/2602.21763 (EIDRR)
- https://arxiv.org/abs/2109.08259 e https://ar5iv.labs.arxiv.org/html/2109.08259 (Bhat 2021)
- https://ar5iv.labs.arxiv.org/html/2012.00893 (Pruthi)
- https://arxiv.org/html/2102.02201 (Hase e Bansal)
- https://aclanthology.org/2025.emnlp-main.1615/ e https://arxiv.org/html/2509.18901v1 (JEDI)
- https://arxiv.org/html/2406.17600v1 (soft labels)
- https://arxiv.org/abs/2511.02044 (Shah)
- https://arxiv.org/abs/2104.08142 (Stacey)
- https://arxiv.org/abs/2005.01932, https://arxiv.org/abs/2306.08042, https://arxiv.org/abs/2210.06726, https://arxiv.org/abs/2012.09157, https://arxiv.org/abs/1812.01193, https://arxiv.org/abs/2305.04990, https://arxiv.org/abs/2310.06547, https://arxiv.org/abs/2301.10521, https://aclanthology.org/2025.findings-emnlp.685/
