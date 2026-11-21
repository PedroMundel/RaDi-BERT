# Como combinar sinais de racionalização de LLM com a perda de classificação em encoder-only

Data: 10/11/2026. Pesquisa externa, relatório apenas. O Pedro decide.

## Procedência (leia primeiro)

Este arquivo é **nível 3**: um agente abriu a página de cada obra (arXiv ou ACL Anthology) e leu o resumo e os metadados. **Nenhuma obra foi lida em texto completo**, exceto que, para quatro números de tabela (Phang 2018 e Zhang 2020), a versão HTML do arXiv foi consultada; os PDFs de Phang, Zhang e Joshi 2022 não foram legíveis pela ferramenta. Interpretação de método e resultado pode conter erro de sumarização. Nada aqui é citável sem o Pedro ler o original. Onde não consegui abrir a fonte, está marcado "não verificado" e não entra na análise.

Itens da seção `## Rejected` do CLAUDE.md respeitados: nada de Claude como gerador, nada de contraste tipo SCOTT, nada de circularidade como filtro. "Encoder já ajustado para NLI como ponto de partida" (14/10) está rejeitado: aparece abaixo só como referência de quanto vale a base honesta, não como opção (ver "previously rejected").

## Resposta curta

1. Sobre linhas de base fortes e dentro da distribuição, a literatura que abri **não mostra ganho consistente** de sinais de racionalização em classificadores. Os ganhos aparecem em poucos dados, fora da distribuição (OOD) e em robustez a atalhos.
2. Os métodos de perda auxiliar para gradientes ortogonais **não resolvem** o caso do Pedro: PCGrad e similares tratam conflito, não ortogonalidade (detalhe na família 7).
3. A alavanca mais barata e mais bem documentada para um BERT-base no RTE não usa racionalização: endurecer a base (reiniciar camadas de cima, Adam corrigido, treino mais longo).
4. O único desenho com racionalização que casa com o que o Pedro já tem (um racional por par, nenhum decoder, 8 GB) e tem evidência direta, ainda que fraca, é o de **professor com informação privilegiada** (KNIFE, Chan 2022): o professor lê entrada mais racional, o aluno lê só a entrada, e os estados ocultos são alinhados.

## Família 1. Aprender com explicações: quando ajuda e quando não

- **Hase e Bansal 2021**, "When Can Models Learn From Explanations? A Formal Framework for Understanding the Roles of Explanation Data", arXiv:2102.02201 (https://arxiv.org/abs/2102.02201). Sem venue no arXiv. Resumo lido. Alegam que explicação como **entrada** é o papel mais promissor, e que em e-SNLI, TACRED e SemEval a recuperação baseada em explicações **não deu melhora**; sugerem que ao menos uma de seis pré-condições falha nesses dados. Evidência negativa direta sobre e-SNLI. Nota: o método testado é recuperação, não perda auxiliar.
- **Hartmann e Sonntag 2022**, "A survey on improving NLP models with human explanations", arXiv:2204.08892 (https://arxiv.org/abs/2204.08892), workshop Learning with Natural Language Supervision. Resumo lido. Diz que explicações podem melhorar eficiência de dados e desempenho dentro e fora do domínio, mas que os métodos quase nunca são comparados entre si. Não dá números.
- **Wiegreffe e Marasović 2021**, "Teach Me to Explain: A Review of Datasets for Explainable Natural Language Processing", arXiv:2102.12060 (https://arxiv.org/abs/2102.12060), NeurIPS 2021 Datasets and Benchmarks (campo Comments). Resumo lido. Catálogo de 65 conjuntos; serve de mapa, não de evidência de ganho.
- **Ross, Peters e Marasović 2022**, "Does Self-Rationalization Improve Robustness to Spurious Correlations?", EMNLP 2022, pp. 7403-7416 (https://aclanthology.org/2022.emnlp-main.501/). Resumo lido. Treinar modelos (encoder-decoder e decoder-only, seis tamanhos) para gerar racional **melhorou robustez com poucos dados e tendeu a piorar com mais dados**. Conclusão dos autores: explicabilidade pode custar robustez. É o resultado negativo mais próximo do que o Pedro mediu. Não é encoder-only.
- **Wadhwa, Amir e Wallace 2024**, arXiv:2406.14511, EMNLP 2024 (https://arxiv.org/abs/2406.14511). Já no projeto. Resumo relido: racional depois do rótulo é melhor, embaralhar tokens do racional ainda dá ganho, poucos tokens-chave bastam. Leitura: o que ajuda pode não ser o conteúdo semântico do racional. Alunos são geradores, não encoders.

## Família 2. Regularização por explicação, atenção ou atribuição com destaques

- **Ross, Hughes e Doshi-Velez 2017**, "Right for the Right Reasons", arXiv:1703.03717 (https://arxiv.org/abs/1703.03717). Sem venue no arXiv. Penaliza gradientes de entrada fora da região anotada. Base conceitual; não é NLP com BERT.
- **Stacey, Belinkov e Rei 2022**, "Supervising Model Attention with Human Explanations for Robust Natural Language Inference", AAAI 2022 (arXiv:2104.08142, https://arxiv.org/abs/2104.08142). Resumo lido. Supervisionar a atenção com destaques de explicações humanas (e-SNLI) melhora desempenho **dentro da distribuição e OOD**. A página não traz números; magnitude **não verificada**. Reaproveita os destaques do e-SNLI que o Pedro já tem. Não serve ao RTE (sem destaques humanos).
- **Joshi et al. 2022**, "ER-Test: Evaluating Explanation Regularization Methods for Language Models", Findings of EMNLP 2022 (arXiv:2205.12542, https://arxiv.org/abs/2205.12542). Resumo lido (PDF ilegível). Em duas tarefas e seis conjuntos: regularização por explicação teve **pouco efeito dentro da distribuição e ganhos OOD muitas vezes grandes**, inclusive com supervisão de racional limitada. Controle de racional embaralhado: **não verificado** no texto.
- **Herrewijnen, Nguyen, Bex e Gatt 2026**, "BERT, are you paying attention? Attention regularization with human-annotated rationales", EACL 2026 long, pp. 720-751 (https://aclanthology.org/2026.eacl-long.31/). Resumo lido. Tokens aleatórios dão melhoras parecidas com racionais humanos; racionais humanos ganham só em reduzir sensibilidade a correlações espúrias fortes. Implicação: boa parte do ganho de regularizar atenção não vem da informação do racional. Tarefas e variante de BERT não constam na página.
- **Chan et al. 2022**, "UNIREX", ICML 2022 (arXiv:2112.08802, https://arxiv.org/abs/2112.08802). Resumo lido. Treina extrator de racional junto com o modelo; mede fidelidade e plausibilidade e "não prejudicar" o desempenho. O objetivo é explicar bem, não melhorar a acurácia. Não é fonte de ganho de acurácia.
- **Pruthi et al. 2022**, "Evaluating Explanations: How Much Do Explanations from the Teacher Aid Students?", TACL 10:359-375 (arXiv:2012.00893; Anthology 2022.tacl-1.21). Resultados do buscador, página do arXiv não aberta diretamente: tratar como parcialmente verificado. Enquadra o valor da explicação como ganho do aluno que a vê só no treino. Ponte conceitual para a família 5.

## Família 3. Racional livre como alvo auxiliar com gargalo (decoder fraco lendo só o vetor agrupado)

- **Condenser** (Gao e Callan 2021, EMNLP 2021, arXiv:2104.08253), **SEED-Encoder** (Lu et al. 2021, arXiv:2102.09206, sem venue no arXiv; decoder fraco impede atalhos de linguagem), **TSDAE** (Wang, Reimers e Gurevych 2021, Findings EMNLP 2021, arXiv:2104.06979) e **RetroMAE** (Xiao et al. 2022, EMNLP 2022, arXiv:2205.12035). Todos abertos no resumo. São **pré-treino** para recuperação densa ou embeddings de sentença, com **reconstrução do próprio texto**, não racional de rótulo, e nenhum reporta acurácia de classificação NLI. O princípio (decoder fraco força o encoder a pôr informação no vetor) é o que o Pedro mediu faltar: no Agrawal, o decoder lê todos os estados e copia da entrada.
- Não encontrei, nas buscas feitas, trabalho que use gargalo em [CLS] com racional de rótulo como ajuste fino para classificação. **Lacuna na literatura que abri**, não prova de que não existe. Qualquer desenho assim seria sem confirmação independente.

## Família 4. Destilação em nível de embedding

- **LRKD**, Qiu et al. 2026, "Thinking Broad, Acting Fast: Latent Reasoning Distillation from Multi-Perspective Chain-of-Thought for E-Commerce Relevance", arXiv:2601.21611, WWW 2026 industry track (campo Comments). Resumo lido: o resumo não traz linha de base nem números ("ganhos significativos offline"), e o aluno tem um **extrator de raciocínio latente que roda na inferência**, ou seja, não é "descartado". Dado proprietário. Evidência pública fraca.
- Variantes contrastivas: não encontrei, nas buscas feitas, obra verificável com número sobre NLI. Não verificado.

## Família 5. Racional como informação privilegiada (LUPI e destilação generalizada)

- **Lopez-Paz, Bottou, Schölkopf e Vapnik 2016**, "Unifying distillation and privileged information", ICLR 2016 (arXiv:1511.03643, https://arxiv.org/abs/1511.03643). Resumo lido. Teoria e simulações; destilação como caso de informação privilegiada. Base teórica para "professor lê entrada mais racional".
- **Chan et al. 2022**, "KNIFE: Distilling Reasoning Knowledge From Free-Text Rationales", arXiv:2212.09721 (https://arxiv.org/abs/2212.09721), workshop TrustML-(un)Limited do ICLR 2023 (campo Comments). Resumo lido. Professor treinado com entrada mais racional; aluno com só a entrada tem os **estados ocultos alinhados** aos do professor. Alunos menores que 1B (T5-Base entre eles), dois conjuntos de QA (OpenBookQA e StrategyQA segundo resultado de busca, não confirmado na página), regimes supervisionado completo e poucos recursos. Os autores dizem que ajuste fino com racional livre "não melhora muito" os métodos existentes e que o KNIFE melhora; **números não vistos**. Uma só fonte, workshop, não é NLI. Reaproveita os racionais do Pedro como estão, sem decoder.
- DHRD (Xu 2025) e Distilling Step-by-Step (Hsieh 2023) já estão no projeto.
- Resultado de busca sem abrir a fonte: arXiv:2606.15920 (OmniOPSD, afetivo multimodal). **Não verificado**, não usado.

Risco específico para o Pedro: se o racional diz o rótulo, o professor acerta quase tudo e seus logits viram o rótulo duro. O que sobra de útil é o alinhamento de estados ocultos, que é exatamente o que o KNIFE faz. Medir a acurácia do professor-com-racional é o primeiro teste barato.

## Família 6. Aumento de dados guiado por racional ou por LLM

- **Kaushik, Hovy e Lipton 2020**, "Learning the Difference that Makes a Difference with Counterfactually-Augmented Data", ICLR 2020 (arXiv:1909.12434). Resumo lido. Revisões **humanas** contrafactuais em NLI e sentimento; modelo treinado só no original vai mal no revisado; o treino conjunto fica quase tão bom quanto os especializados e depende menos de sinais espúrios. É robustez, não ganho dentro da distribuição.
- **Liu, Swayamdipta, Smith e Choi 2022**, "WANLI", Findings of EMNLP 2022 (arXiv:2201.05955). Resumo lido. GPT-3 gera exemplos com padrões difíceis (cartografia de dados do MultiNLI), filtrados e revisados por **trabalhadores humanos**; modelo treinado no WANLI (108 mil) ganha 11% no HANS e 9% no ANLI contra o MultiNLI, em oito conjuntos fora do domínio. Ganho é OOD; o custo humano da curadoria é parte do método. Não parte de racionais, e um gerador local de 35B sem curadoria humana não tem evidência equivalente.
- Aumento guiado especificamente por racional para NLI com BERT: não achei obra verificada com baseline forte.

## Família 7. Otimização multitarefa com perda auxiliar (o que trata ortogonalidade)

| Método | Fonte | O que trata |
|---|---|---|
| Similaridade de gradiente como peso | Du et al. 2018 (arXiv:1812.02224, sem venue no arXiv) | Usa o cosseno entre gradientes como peso adaptativo da auxiliar. Pelo resumo, indica quando a auxiliar ajuda. Com cosseno ≈ 0, o peso tende a ~0 (leitura minha, texto completo não lido): ou seja, desliga a auxiliar, não a torna útil. Testado em ImageNet reduzido e RL, não em NLP. |
| PCGrad | Yu et al. 2020 (arXiv:2001.06782, NeurIPS 2020) | Projeta fora só o componente **conflitante** (resumo). Com gradientes ortogonais não faz nada. Trata conflito, não ortogonalidade. |
| GradNorm | Chen et al. 2018 (arXiv:1711.02257, ICML 2018) | Equilibra **magnitudes** de gradiente entre tarefas. Trata escala, não direção. A razão medida de 0,05 a 0,38 sugere um problema de escala, mas aumentar o peso de uma perda ortogonal só soma atualização ortogonal, que pode ser ruído ou regularização (leitura minha). |

Conclusão: nenhum dos três cria alinhamento onde ele não existe. Meta-peso de auxiliar e máscara de perda por tipo de token: não encontrei fonte verificada para NLP.

## Família 8. Alternativas simples sem racional (base honesta a vencer)

- **Zhang et al. 2021**, "Revisiting Few-sample BERT Fine-tuning", arXiv:2006.05987 (sem venue no arXiv; leitura via ar5iv). BERT-large no RTE, 20 sementes, teste: base 69,5 ± 2,5; reiniciar as camadas de cima 72,6 ± 1,6; treinar mais 72,3 ± 1,9; ambos 73,1 ± 1,3; Mixout 71,3 ± 1,4; decaimento de taxa por camada 69,7 ± 3,2. Com Adam corrigido, os ganhos de Mixout e similares **encolhem**; Adam original dava 48% de execuções abaixo de 55% no RTE. É BERT-large, não base. Lição para o Pedro: **verificar o otimizador da linha de base antes de atribuir ganho a qualquer sinal auxiliar.**
- **Mosbach, Andriushchenko e Klakow 2021**, "On the Stability of Fine-tuning BERT", ICLR 2021 (arXiv:2006.04884). Resumo lido. Instabilidade vem de gradientes que somem e de variação de generalização; propõem uma linha de base estável simples (GLUE).
- **Lee, Cho e Kang 2020**, "Mixout", ICLR 2020 (arXiv:1909.11299). Resumo lido. Estabilidade e acurácia média em GLUE.
- **Liang et al. 2021**, "R-Drop", NeurIPS 2021 (arXiv:2106.14448). Resumo lido. KL bidirecional entre duas passagens com dropout; "ganhos maiores" ao ajustar modelos grandes pré-treinados. Sem número de RTE visto.
- **Bahri, Mobahi e Tay 2022**, "Sharpness-Aware Minimization Improves Language Model Generalization", ACL 2022 (arXiv:2110.08529; Anthology 2022.acl-long.508), via resultado de busca. T5 e mT5, ganhos maiores com poucos dados. Não é BERT-base.
- **Phang, Févry e Bowman 2018/2019**, "Sentence Encoders on STILTs", arXiv:1811.01088 (sem venue no arXiv; leitura via ar5iv). BERT-large, RTE teste: 70,1 sem, 80,1 com treino intermediário no MNLI (o texto fala em 8 pontos, a tabela mostra 10; discrepância da fonte). Dev com BERT-base: 68,6 contra 79,1. **Previously rejected**: "Encoder já ajustado para NLI como ponto de partida" (14/10, teto e contaminação com o SNLI). Citado só para dimensionar: nenhum método de racionalização nesta pesquisa tem ganho dessa ordem no RTE.
- Destilação de rótulos suaves de um professor LLM: busca não achou fonte NLI-específica com baseline forte. Não verificado.

## Tabela de comparação (ONE-TABLE)

| Opção | Ganho esperado, com evidência | Custo/tempo (RTX 5060 8 GB, ~3 semanas) | O que dos dados e código é reaproveitado | Maturidade / confirmações independentes | Risco principal |
|---|---|---|---|---|---|
| A. Base endurecida (reiniciar camadas de cima, Adam corrigido, treino mais longo; opcional Mixout ou R-Drop) | RTE: +3 a +4 pontos sobre a base padrão em BERT-large (Zhang 2021); em BERT-base não verificado. Sem racional. | Muito baixo: mesmas rodadas, horas de GPU | Código de treino do BERT e pareamento por semente | Alta: Zhang 2021, Mosbach 2021, Lee 2020 se corroboram em parte | Não responde à pergunta de racionalização; serve de braço de controle e eleva a régua |
| B. Professor com informação privilegiada, racional lido só pelo professor, alinhamento de estados ocultos (KNIFE) | Não verificado em número. Autores afirmam melhora em QA com alunos <1B; nada em NLI nem em BERT-base. | Médio: dois treinos de BERT-base por semente (professor depois aluno), cabe em 8 GB; sem decoder | Racionais como estão (RTE 2.490, e-SNLI 16 mil), sondas de gradiente | Baixa: uma fonte, workshop, sem réplica | Professor decora o rótulo e o alinhamento não transmite nada além do rótulo; exige controle com racional embaralhado ou de outro par |
| C. Regularização de atenção com destaques humanos do e-SNLI (Stacey 2022, Joshi 2022, Herrewijnen 2026) | Dentro da distribuição: perto de zero ou pequeno; OOD: maior (Joshi 2022, Stacey 2022). Tokens aleatórios igualam em geral (Herrewijnen 2026). | Baixo a médio: perda extra sobre atenção do BERT-base | Destaques humanos do e-SNLI (não os racionais do Qwen); nada para o RTE | Média: três grupos, resumos concordam | Ganho só fora da distribuição; precisa de HANS ou similar; não usa os racionais gerados |
| D. Aumento com exemplos difíceis gerados por LLM local (WANLI-like) | OOD: +11% HANS, +9% ANLI contra MNLI (Liu 2022), mas com curadoria humana e GPT-3 | Alto: gerar, filtrar e retreinar; 3 semanas é apertado | Qwen 35B local, prompts, e-SNLI | Média para a ideia, baixa para versão sem curadoria humana | Sem filtro humano o ruído de rótulo come o ganho; mede-se em OOD, não em acurácia de teste do RTE |

**Recomendação: B**, com A obrigatório como braço de controle. Justificativa: é o único desenho que usa os racionais já gerados sem decoder, sem gargalo novo, cabe em 8 GB e ataca diretamente o que foi medido (o aluno Agrawal não aprende conteúdo copiado). A evidência é fraca (uma fonte), então a expectativa honesta é nulo ou ganho pequeno, e um nulo com controle positivo (A) e controle de racional embaralhado (Wadhwa 2024, Herrewijnen 2026) conta como ciclo completo pelo critério do programa. **A decisão final é do Pedro.**

## O que a literatura diz que não funciona

- Explicação como entrada por recuperação não melhorou e-SNLI (Hase e Bansal 2021).
- Aprender a gerar racional melhora robustez com poucos dados e **piora com mais dados** (Ross, Peters e Marasović 2022). O RTE com 2.490 pares é pouco; o e-SNLI com 16 mil é bastante.
- Regularização por explicação tem pouco efeito dentro da distribuição (Joshi 2022); com tokens aleatórios o ganho é parecido (Herrewijnen 2026); racional embaralhado também ajuda (Wadhwa 2024). O conteúdo do racional pode não ser a causa do ganho publicado.
- PCGrad e GradNorm não tratam ortogonalidade (família 7). Similaridade de gradiente desliga a auxiliar quando o cosseno é ~0.
- Em Zhang 2021, vários métodos de regularização somem quando o otimizador da base é corrigido: um ganho sobre base mal configurada não vale.
- Os ganhos grandes no RTE vêm de transferência de um conjunto de NLI maior (STILTs, +10 pontos em BERT-large), não de sinais de racionalização; esse caminho está previously rejected pelo Pedro (14/10).
- No próprio Agrawal et al. 2025, os ganhos sobre bases fortes são pequenos (dado do projeto, não verificado de novo).

## Não consegui verificar

- Números de KNIFE (Chan 2022) e se os conjuntos são OpenBookQA e StrategyQA (só por resultado de busca).
- Magnitude dos ganhos de Stacey 2022 e Joshi 2022; controle de racional embaralhado em ER-Test.
- Pruthi 2022: página do arXiv não aberta diretamente, só resultados de busca com Anthology e DOI.
- Du 2018: se o peso é truncado em zero para cosseno negativo (leitura do texto completo pendente).
- Bahri 2022: só resultados de busca; BERT-base não testado.
- LRKD: números e linhas de base ausentes do resumo.
- Variantes contrastivas de destilação em embedding e aumento guiado por racional em NLI: nenhuma fonte encontrada.
- Meta-peso de auxiliar e máscara de perda por tipo de token em NLP: nenhuma fonte encontrada.
- Soft labels de professor LLM para BERT-base em NLI com baseline forte: nenhuma fonte encontrada.
- OmniOPSD (arXiv:2606.15920) e Kunz et al. (BlackboxNLP 2022): vistos só em resultados de busca; não usados.
- Os PDFs de Phang 2018, Zhang 2020 e Joshi 2022 não eram legíveis; números de Phang e Zhang vêm do HTML do ar5iv.

## Acréscimo de 18/11: KNIFE (Chan et al., 2022) pelo texto completo, ainda nível 3

**Procedência:** resumo feito por um modelo pequeno sobre a página inteira do artigo (ar5iv, arXiv:2212.09721), a
partir de sete perguntas do Claude. O Claude não leu o texto; o Pedro não leu. Serve para comparar com o teste de
18/11, **não para citar**; todo número abaixo precisa ser conferido no PDF.

- **Arquitetura:** T5 (encoder e decoder), pares Base para Base, Large para Large e Large para Base. O professor lê
  a entrada mais a justificativa; o **decoder do professor só enxerga os estados da entrada**, os da justificativa
  ficam fora da atenção cruzada (seção 4.1.2, o gargalo). O aluno lê só a entrada.
- **O que o aluno imita:** só a **última camada**, erro quadrático, nas posições da entrada no encoder e nos estados
  do decoder para cada rótulo candidato. Sem perda de atenção. A perda da tarefa fica de fora por padrão (seção 5.5).
- **Dados:** OpenBookQA e StrategyQA nos resultados principais; ECQA e QuaRTz na análise de falha. Não é NLI.
- **Ganhos relatados (Tabela 1, 3 sementes, média e desvio):** T5-Base +3,6 (OpenBookQA) e +1,4 (StrategyQA);
  T5-Large +3,1 e +6,2. Sem intervalo de confiança nem teste.
- **Onde não funciona, segundo o próprio artigo (Tabela 3):** no ECQA todas as variantes ficam de 5 a 7 pontos
  **abaixo** do baseline sem justificativa; no QuaRTz empata. Os autores atribuem a justificativas que só repetem
  a pergunta e a resposta, e chamam a qualidade da justificativa de crítica (seção 5.6).
- **Controles (Tabela 7):** justificativa embaralhada entre exemplos ou com tokens trocados fica abaixo da certa, e
  no StrategyQA abaixo do baseline sem justificativa. Um professor sem justificativa (Tabela 6) dá 60,12 no
  StrategyQA, contra 60,45 do KNIFE na Tabela 1.
- **Diferenças para o teste de 18/11 (`docs/2026-11-18-professor-que-le-a-justificativa.md`):** aqui o professor é
  um BERT cujo `[CLS]` lê a justificativa direto (sem gargalo); o aluno imita quatro camadas, embeddings e atenção
  renormalizada; a tarefa é NLI com justificativa que entrega o rótulo em 96,9% dos pares. O teste de 18/11 não é
  uma reprodução do KNIFE.
