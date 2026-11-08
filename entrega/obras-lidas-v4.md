# Obras Lidas (v4)

Registro das obras que li, por semana. Cada versão acumula a anterior: a v1 cobre as semanas 1 e 2, a v2 a semana 3, a v3 a semana 4 e esta v4 a semana 5. Separo o que li na fonte do que li por resumo preparado com apoio de LLM; o que foi lido apenas por agentes, sem leitura minha, fica fora.

## v1 - Semanas 1 e 2: o tema

| Obra | Referência | O que tirei dela |
|---|---|---|
| Distilling Step-by-Step | Hsieh et al. (2023). Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes. Findings of ACL 2023. arXiv:2305.02301 | a racionalização gerada por um LLM pode treinar um modelo pequeno como tarefa separada, e ele não precisa do LLM nem da racionalização na hora de responder |
| DHRD | Xu et al. (2025). Dual-Head Reasoning Distillation: Improving Classifier Accuracy with Train-Time-Only Reasoning. arXiv:2509.21487 | uma segunda cabeça aprende o raciocínio só no treino e é desligada no teste, e mesmo assim melhora o classificador |
| Agrawal | Agrawal, Ahemad e Sembium (2025). Rationale-Guided Distillation for E-Commerce Relevance Classification: Bridging Large Language Models and Lightweight Cross-Encoders. COLING 2025 Industry Track | um classificador BERT ganha uma cabeça auxiliar que aprende a racionalização do LLM durante o treino e é descartada na entrega |

## v2 - Semana 3: o método

| Obra | Referência | O que tirei dela |
|---|---|---|
| Petersen | Petersen, Feldt, Mujtaba e Mattsson (2008). Systematic Mapping Studies in Software Engineering. EASE 2008 | um mapeamento sistemático organiza uma área em categorias, sem julgar a qualidade de cada estudo; mapeamento e revisão sistemática ficam num contínuo, e quanto mais fundo se lê, mais perto da revisão |

Lidos por resumo (li com atenção o resumo preparado com apoio de LLM, não a obra na fonte):

| Obra | Referência | O que tirei dela |
|---|---|---|
| Arksey e O'Malley | Arksey e O'Malley (2005). Scoping Studies: Towards a Methodological Framework. International Journal of Social Research Methodology | uma scoping study mapeia os conceitos e as fontes de uma área em cinco estágios (pergunta, busca, seleção, extração, síntese) e uma consulta opcional, sem avaliar a qualidade de cada estudo, que é o tipo de pesquisa que o professor pediu |
| Kitchenham e Charters | Kitchenham e Charters (2007). Guidelines for Performing Systematic Literature Reviews in Software Engineering. Relatório técnico EBSE-2007-01 | uma revisão começa por um protocolo: perguntas, estratégia de busca e critérios de seleção decididos antes, testados numa amostra e aplicados por dois revisores; foi a base para eu declarar cada decisão antes de rodar |

## v3 - Semana 4: a lista da área

| Obra | Referência | O que tirei dela |
|---|---|---|
| Hinton | Hinton, Vinyals e Dean (2015). Distilling the Knowledge in a Neural Network. arXiv:1503.02531 | a história da destilação e as referências anteriores a ela (o trabalho de Buciluă, Caruana e colaboradores, que já comprimia um conjunto de modelos num modelo só); entra na linha do tempo da área |
| Yuan | Yuan et al. (2024). LLM Inference Unveiled: Survey and Roofline Model Insights. arXiv:2402.16363 | como cada fase da inferência (prefill e decode) afeta o hardware; as ferramentas da área para lidar com cada tipo de gargalo (computação ou memória) nos quatro níveis (modelo, algoritmo, sistema e hardware); vocabulário da área. Vou aplicar o método no meu hardware, para descobrir as minhas limitações e o que vai funcionar e o que não vai |
| Kwon | Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention. SOSP 2023. arXiv:2309.06180 | como a forma de gerenciar a memória do KV cache melhora ou piora a eficiência de um sistema de serving |

## v4 - Semana 5: destilação de racionalização

| Obra | Referência | O que tirei dela |
|---|---|---|
| DistilBERT | Sanh, Debut, Chaumond e Wolf (2019). DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. EMC2 Workshop, NeurIPS 2019. arXiv:1910.01108 | destilar já no pré-treino reduz o modelo e mantém a compreensão de linguagem; a loss de destilação responde por grande parte do ganho e a de mascaramento por pouco. Como vou destilar racionalização e não conhecimento, preciso estudar outros tipos de loss |
| Wadhwa | Wadhwa, Amir e Wallace (2024). Investigating Mysteries of CoT-Augmented Distillation. EMNLP 2024. arXiv:2406.14511 | o aluno não precisa raciocinar na hora da inferência: a racionalização depois do rótulo funciona melhor, a gramática não importa, e manter só os tokens importantes mantém o ganho quando eles são escolhidos por atribuição de gradiente. Tokens específicos da racionalização parecem carregar informação extra sobre o rótulo |
| Chen | Chen, Zhou, Liang e Liu (2025). Distilling Reasoning Ability from Large Language Models with Adaptive Thinking. IEEE Transactions on Neural Networks and Learning Systems (early access). arXiv:2404.09170 | responder antes de racionalizar protege a resposta de erros na racionalização e faz a racionalização funcionar como amplificador de erro, concentrando o aprendizado nas amostras difíceis; para perguntas muito complexas, racionalizar antes ainda é melhor |
| KPOD | Feng et al. (2024). Keypoint-based Progressive Chain-of-Thought Distillation for LLMs. ICML 2024. arXiv:2405.16064 | os tokens de uma racionalização não têm a mesma importância; um módulo aprende pesos por máscara para o aluno imitar com precisão os tokens-chave |
| EasyDistill | Wang et al. (2025). EasyDistill: A Comprehensive Toolkit for Effective Knowledge Distillation of Large Language Models. arXiv:2505.20888 | framework de destilação de LLM, caixa-preta e caixa-branca, com síntese de dados, ajuste supervisionado, otimização de ranking e aprendizado por reforço |

## Totais

- v1: 3 obras;
- v2: 1 obra na fonte e 2 por resumo;
- v3: 3 obras;
- v4: 5 obras;
- Total acumulado: 12 obras na fonte e 2 por resumo.
