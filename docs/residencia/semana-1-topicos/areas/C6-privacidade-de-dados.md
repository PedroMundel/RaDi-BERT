# C6 — Privacidade de dados em ML

## 1. O que a área é no dia a dia

Na prática, é o trabalho de fazer um pipeline de ML funcionar sem vazar informação sobre indivíduos específicos do conjunto de treino. Isso cobre quatro frentes que se misturam: (1) **differential privacy (DP)** — adicionar ruído calibrado a gradientes (DP-SGD), consultas ou saídas de modelo, com um orçamento de privacidade (ε) que se gasta e se contabiliza; (2) **aprendizado federado** — treinar sem centralizar dados brutos, combinando com DP local/global e agregação segura; (3) **dados sintéticos** — gerar uma versão artificial do dataset (GANs tabulares, modelos probabilísticos, ou LLMs) que preserve utilidade estatística sem expor registros reais; (4) **ataques e auditoria** — testar se um modelo memoriza e vaza treino (membership inference, reidentificação, extração de dados de LLMs) para validar se as defesas realmente funcionam. No dia a dia isso é código: instrumentar treino com Opacus, rodar SDV, medir trade-off privacidade×utilidade, e navegar exigências de conformidade (LGPD/GDPR) que raramente têm resposta puramente técnica.

## 2. Problemas abertos quentes (2024-2026)

- Memorização e extração de dados de treino em LLMs — quantificar e mitigar sem destruir capacidade do modelo.
- Dados sintéticos gerados por LLM nem sempre protegem privacidade: ataques de membership inference continuam funcionando mesmo sobre texto sintético.
- DP em federated learning ainda tem gap grande entre garantia teórica (ε pequeno) e utilidade prática em dados heterogêneos (non-IID).
- Falta de protocolo confiável de avaliação de MIA — resultados atuais são inflados por overlap de n-gramas ou shift temporal ("crise de avaliação").
- Auditoria de privacidade de geradores de dados sintéticos tabulares (ex.: ataques tipo "canary") como contraponto às alegações de fornecedores.
- Conformidade regulatória (LGPD/ANPD, agenda 2025-2026 sobre anonimização e IA) ainda carece de métricas técnicas padronizadas ligadas à lei.

## 3. Surveys de referência (verificados)

- **"Differential Privacy in Machine Learning: A Survey from Symbolic AI to LLMs"** (2025/2026) — arXiv:2506.11687, também publicado na ACM TIST. https://arxiv.org/abs/2506.11687
- **"Differentially Private Federated Learning: A Systematic Review"** (2024) — arXiv:2405.08299. https://arxiv.org/pdf/2405.08299
- **"When Federated Learning Meets Privacy-Preserving Computation"** (ACM Computing Surveys, 2024) — https://dl.acm.org/doi/10.1145/3679013
- **"Defending against attacks in deep learning with differential privacy: a survey"** (Artificial Intelligence Review, Springer, 2025) — https://link.springer.com/article/10.1007/s10462-025-11350-3 (bônus: mesma casa editorial do ICDATA, Springer Nature).

## 4. Onde se publica

- Topo da área: **PETS/PoPETs** (Privacy Enhancing Technologies Symposium / Proceedings on Privacy Enhancing Technologies), **USENIX Security**, **ACM CCS**, **IEEE S&P** — todos com barra de entrada muito alta, comunidade fortemente teórica/criptográfica.
- Venues de dados/aplicado, mais acessíveis: workshops de privacidade em KDD/ICDM, IEEE BigData, e o próprio **ICDATA/CSCE**, que lista explicitamente "Privacy-preserving data mining", "Privacy Threats of Big Data", "Data Protection Methods" como tópicos do CfP — ou seja, um paper aplicado (ex.: benchmark de trade-off privacidade×utilidade em dados sintéticos) se encaixa diretamente sem precisar competir com o rigor matemático de PETS/CCS.

## 5. Stack necessária (verificada)

- **Opacus** (Meta, PyTorch) — DP-SGD pronto para uso, `pip install opacus`, paper original arXiv:2109.12298, repo ativo (github.com/meta-pytorch/opacus).
- **SDV — Synthetic Data Vault** (`pip install sdv`, sdv.dev) — geração de dados tabulares sintéticos (GaussianCopula, CTGAN) e métricas de qualidade/privacidade built-in; projeto do MIT Data-to-AI Lab, mantido pela DataCebo.
- Bibliotecas de ataque para auditoria (ex.: implementações de membership inference / MIA benchmarks) normalmente vêm junto de papers no arXiv — não há um pacote único dominante consolidado; a escolha dependeria do tema exato.
- TensorFlow Privacy existe como alternativa ao Opacus para quem usa TF em vez de PyTorch (não aprofundado aqui pois o perfil do Pedro é mais GenAI/PyTorch).

## 6. Sinal de mercado

Regulação: LGPD segue em fiscalização crescente pela ANPD, com agenda regulatória 2025-2026 incluindo explicitamente IA, anonimização e pseudonimização como prioridades. No Brasil, o mercado de dados sintéticos é estimado em crescer de ~R$340 milhões (2025) para ~R$4,2 bilhões (2028), puxado por setores regulados (saúde, fintech) que precisam treinar modelos sem expor dados pessoais reais. Isso cria demanda concreta por profissionais que saibam medir e comunicar trade-off privacidade×utilidade — não só implementar DP, mas justificar decisões para compliance.

## 7. Como seria um tema de residência

1. **Avaliação de trade-off privacidade×utilidade em dados tabulares sintéticos gerados por LLM** — comparar (a) SDV clássico (CTGAN/GaussianCopula) vs. (b) geração via LLM (few-shot ou fine-tuned) em datasets públicos, medindo utilidade (fidelidade estatística, desempenho downstream) e privacidade (membership inference, distância a registros reais). Encaixa direto no CfP do ICDATA e no interesse máximo do Pedro em "generative AI for generating data".
2. **Benchmark de ataques de membership inference contra geradores sintéticos** — replicar/adaptar técnicas tipo "Canary" em geradores tabulares acessíveis (SDV) para auditar se datasets "anonimizados" divulgados por empresas brasileiras realmente resistem a reidentificação.
3. **DP-SGD aplicado a fine-tuning de LLM pequeno em dado sensível (ex.: texto clínico sintético em português)** — medir custo de utilidade (queda de qualidade de geração) por nível de ε, usando Opacus; mais pesado matematicamente, mas mais próximo do "gold standard" da área.

A proposta 1 é a mais exequível para um TCC/residência de graduação: stack pronta (SDV + qualquer LLM via API), métrica clara, sem exigir prova formal de DP.

## 8. Riscos

DP tem matemática pesada (cálculo de composição de privacidade, mecanismos de ruído) que pode exigir apoio de um orientador com base em teoria da informação/estatística — mitigável escolhendo temas aplicados (dados sintéticos + MIA) em vez de DP teórico puro. A comunidade "de ponta" (PETS/CCS/USENIX) é extremamente exigente e não é realista como alvo de publicação nesta fase; o caminho real é ICDATA/workshops aplicados, o que é adequado ao objetivo declarado mas limita o prestígio do venue. Por fim, a área de MIA/auditoria sofre de problemas metodológicos reconhecidos (avaliação inflada) — um trabalho aplicado precisa citar essas ressalvas para não ser descartado por revisores mais rigorosos.
