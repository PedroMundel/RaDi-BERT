# C1 — GenAI/LLMs aplicados a engenharia e análise de dados

Área candidata a especialização de residência. Cobre os tópicos do ICDATA'26: "Applications of
generative AI for generating data", "(Generative) AI for data handling", "(Generative) AI for
analytics, visualization, reporting".

## 1. O que a área é no dia a dia

Um pesquisador nessa área não treina LLMs do zero — usa LLMs (via API ou modelos locais
pequenos) como componente de um pipeline de dados e mede se isso melhora custo, qualidade ou
cobertura em relação a métodos clássicos (regras, ML supervisionado, estatística). Na prática:
(1) constrói pipelines de "data agents" que recebem uma tabela suja/incompleta e produzem
correções (imputação, deduplicação, padronização de formato, resolução de entidades); (2) gera
dados sintéticos tabulares ou textuais para aumentar classes raras, testar sistemas, ou
substituir dados sensíveis (privacidade); (3) constrói e avalia sistemas text-to-SQL / text-to-
insight que traduzem perguntas em linguagem natural para consultas/gráficos/relatórios sobre
bases reais; (4) desenha benchmarks e métricas de avaliação (porque a avaliação "solta" de LLM em
dados estruturados é o gargalo central da área — não existe métrica única aceita). O trabalho é
mais empírico/comparativo (testar prompts, modelos, arquiteturas de agente em datasets públicos)
do que teórico.

## 2. Problemas abertos quentes (2024-2026)

- **Alucinação em limpeza/imputação de dados**: LLM "inventa" valores plausíveis mas incorretos ao preencher lacunas, sem sinal de confiança calibrado.
- **Custo e latência em pipelines de produção**: chamar LLM por linha/célula é caro em escala; falta consenso sobre quando vale a pena vs. regra/ML clássico.
- **Falta de benchmark de qualidade de dado sintético**: medir se dado sintético tabular preserva utilidade estatística sem vazar privacidade ainda é ad-hoc por paper.
- **Avaliação de text-to-SQL em bases reais/multi-tabela**: benchmarks como Spider/BIRD não capturam bem esquemas empresariais complexos, ambiguidade de linguagem natural e schemas privados.
- **Privacidade e dado sintético como substituto de dado sensível**: risco de memorização/leakage do LLM gerador não é bem quantificado nos papers atuais.
- **Agentes multi-etapa (planejar → limpar → validar → reportar) ainda são frágeis**: falha em uma etapa se propaga sem correção humana no loop.

## 3. Surveys de referência (verificados)

1. **"A Survey of LLM × DATA"** — Zhou, He, Zhou et al., arXiv:2505.18458, submetido em 24/05/2025 (v3 em 01/06/2025). Cobre as duas direções: dado para treinar LLM e LLM para gestão de dados (limpeza, integração, descoberta). https://arxiv.org/abs/2505.18458
2. **"Large Language Models for Data Annotation and Synthesis: A Survey"** — Tan, Li, Wang et al., arXiv:2402.13446, fev/2024, aceito no EMNLP 2024 Main. https://arxiv.org/abs/2402.13446
3. **"Next-Generation Database Interfaces: A Survey of LLM-based Text-to-SQL"** — Hong et al., arXiv:2406.08426, jun/2024 (atualizado várias vezes). Cobre especificamente text-to-SQL com LLM. https://arxiv.org/abs/2406.08426

Survey adicional específico de síntese de dados (não essencial, mas relevante): "A Survey on Data
Synthesis and Augmentation for Large Language Models" — Wang et al., arXiv:2410.12896, out/2024.
https://arxiv.org/abs/2410.12896

## 4. Onde se publica

A área é **híbrida entre venues de banco de dados/dados e venues de NLP**:
- **Dados/sistemas**: VLDB (PVLDB) e SIGMOD publicam sistemas concretos — ex. RetClean (retrieval-based data cleaning com LLM) saiu na PVLDB vol. 17 (2024). ICDE também é relevante.
- **NLP**: ACL, EMNLP, Findings — a maioria dos surveys de synthetic data/annotation está lá (ex. survey #2 acima, aceito EMNLP 2024).
- **Aplicada/multidisciplinar**: ICDATA/CSCE (o alvo de Pedro) é um venue de menor exigência que aceita bem esse cruzamento aplicado — não compete com VLDB/ACL em rigor, o que é uma vantagem realista para um primeiro paper de graduação.

## 5. Stack necessária

- **APIs de LLM**: OpenAI API, Google Gemini API (ambos citados nos papers, ex. RetClean usa GPT e Gemini).
- **Modelos locais pequenos** (para cenários de privacidade/custo): família Llama (Meta) ou Mistral via Hugging Face `transformers`, fine-tuning leve (LoRA via biblioteca `peft`).
- **Bibliotecas de dados**: `pandas`, `duckdb` (comum em papers de text-to-SQL/analytics), SQL padrão.
- **Benchmarks públicos**: Spider, BIRD (text-to-SQL); datasets de limpeza como os usados por RetClean (data lakes públicos).
- **Frameworks de agente**: LangChain ou implementação própria de pipeline multi-etapa (a maioria dos papers usa orquestração simples, não frameworks pesados).
- **Avaliação**: métricas de execução (execution accuracy em text-to-SQL), métricas estatísticas de fidelidade para dado sintético (ex. distância de distribuição).

## 6. Sinal de mercado

Forte. Gartner estima que até 2026 ~60% do dado usado em IA/analytics será sintético, o que puxa
demanda por essa especialização. Startups dedicadas existem e contratam ativamente: Gretel,
MOSTLY AI, Tonic.ai, Hazy. Empresas de dados maiores (Databricks, Snowflake) também investem na
área. O mercado geral de data engineering segue em crescimento (~15% CAGR estimado para 2026),
mas com nota de cautela: postings de nível de entrada caíram bastante desde a popularização de
GenAI — a demanda forte é mais para perfis intermediários/seniores do que para primeiro emprego.

## 7. Como seria um tema de residência (exequível, GPU modesta)

1. **Benchmark comparativo de custo x qualidade para limpeza de dados tabulares com LLM**: comparar
   um modelo local pequeno (Llama/Mistral 7-8B via API gratuita ou GPU local) vs. API paga
   (GPT-4o-mini/Gemini Flash) vs. baseline clássico (regras + ML) em tarefas de imputação/dedup
   num dataset público (ex. os usados por RetClean), reportando acurácia, custo por linha e
   latência. Alinhado a "(Generative) AI for data handling".
2. **Geração de dados sintéticos tabulares para balanceamento de classes raras**: pegar um dataset
   desbalanceado público (ex. saúde ou fraude), gerar amostras sintéticas com LLM guiado por
   prompt estruturado, medir ganho de um classificador downstream e comparar com SMOTE/técnicas
   clássicas. Alinhado a "Applications of generative AI for generating data".
3. **Avaliação de text-to-SQL em esquema de domínio nicho (não coberto por Spider/BIRD)**: montar
   um mini-benchmark de perguntas em português sobre um schema de domínio brasileiro (ex. dados
   públicos do governo), testar 2-3 LLMs, medir execution accuracy e categorizar tipos de erro.
   Contribuição incremental mas publicável, alinhada a "AI for analytics, visualization,
   reporting" e ainda dá espaço para nota de contribuição em português/PT-BR (ângulo de
   originalidade regional).

Qualquer um dos três é exequível com GPU modesta (ou até sem GPU, usando APIs), dataset público, e
prazo de um paper ICDATA.

## 8. Riscos

- Área muda muito rápido (novos modelos/APIs a cada poucos meses); um benchmark pode ficar
  desatualizado entre submissão e publicação.
- Competição indireta com labs grandes e startups (Gretel, Databricks) que publicam sistemas mais
  maduros — mas isso é mitigado pelo nível de exigência do ICDATA, que valoriza contribuição
  aplicada/incremental, não SOTA absoluto.
- Avaliação de qualidade de dado sintético/limpeza ainda não tem métrica padrão aceita pela
  comunidade — risco de reviewers questionarem a validade da métrica escolhida.

## Fontes verificadas

- [A Survey of LLM × DATA (arXiv:2505.18458)](https://arxiv.org/abs/2505.18458)
- [Large Language Models for Data Annotation and Synthesis: A Survey (arXiv:2402.13446)](https://arxiv.org/abs/2402.13446)
- [Next-Generation Database Interfaces: A Survey of LLM-based Text-to-SQL (arXiv:2406.08426)](https://arxiv.org/abs/2406.08426)
- [A Survey on Data Synthesis and Augmentation for Large Language Models (arXiv:2410.12896)](https://arxiv.org/abs/2410.12896)
- [RetClean: Retrieval-Based Data Cleaning Using LLMs and Data Lakes, PVLDB 17(12) (2024)](https://www.vldb.org/pvldb/vol17/p4421-eltabakh.pdf)
