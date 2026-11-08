# C2 — Processo e Qualidade de Dados para ML (Data-Centric AI)

## 1. O que a área é no dia a dia

É o trabalho que ocupa a maior parte do tempo real de quem faz ML aplicado: entender por que uma coluna tem 30% de nulos, decidir se um outlier é erro de sensor ou evento raro legítimo, escolher entre imputação simples (média/mediana) e um modelo preditivo para preencher valores faltantes, balancear classes raras sem inflar artificialmente o desempenho, e validar que o pipeline de features de produção não "quebrou" silenciosamente quando a distribuição dos dados muda (data drift). Inclui também comparar modelos de forma honesta (cross-validation correta, métricas que não mentem em dados desbalanceados) e explicar decisões de modelos a stakeholders não técnicos (XAI). É a "cozinha" do ML: pouco glamourosa, mas é onde a maioria dos projetos reais falha ou funciona. Ferramentas típicas: pandas, scikit-learn, bibliotecas de validação de schema, testes estatísticos de drift.

## 2. Problemas abertos quentes (2024–2026)

- **Data-centric AI como paradigma formal** (Andrew Ng, 2021+): mover o esforço de "melhorar o modelo" para "melhorar sistematicamente o dado", com poucas metodologias rigorosas de *como* priorizar qual dado limpar/coletar primeiro.
- **Benchmarks de qualidade de dado ainda imaturos**: DataPerf (NeurIPS 2023) tentou padronizar avaliação de técnicas data-centric, mas cobertura por domínio/modalidade ainda é escassa comparada a benchmarks de modelo.
- **Detecção de rótulos ruidosos em escala** (confident learning, cleanlab): funciona bem em benchmarks acadêmicos, mas validação em dados tabulares de produção com múltiplos anotadores humanos é pouco explorada.
- **Data validation em MLOps/produção**: ferramentas como Great Expectations cobrem checagem de schema, mas detecção de drift semântico (não só estatístico) e integração com pipelines de feature store ainda tem lacunas de pesquisa aplicada.
- **Data-centric AI na era de LLMs**: como curar, deduplicar e avaliar qualidade de dados de treino em escala massiva (pré-treino de LLM) é uma frente nova que reaproveita técnicas clássicas de limpeza de dados sob restrições completamente diferentes de escala.
- **Active learning + seleção de dados**: quais exemplos rotular/coletar a seguir para máximo ganho de desempenho por custo — ainda carece de métodos que generalizem bem entre domínios tabulares.

## 3. Surveys de referência (verificados)

- Zha, D. et al. **"Data-centric Artificial Intelligence: A Survey"** (2023). arXiv:2303.10158. https://arxiv.org/abs/2303.10158 — survey mais citado da área, organiza o campo em desenvolvimento de dados de treino, dados de inferência e manutenção de dados.
- Xu, X. et al. **"Data-Centric AI in the Age of Large Language Models"** (jun. 2024). arXiv:2406.14473. https://arxiv.org/abs/2406.14473 — posiciona data-centric AI no contexto de LLMs, útil para conectar a área a tendências atuais.
- Wan, Z. et al. (ou similar) **"Data Cleaning and Machine Learning: A Systematic Literature Review"** (2023, atualizado maio 2024). arXiv:2310.01765. https://arxiv.org/abs/2310.01765 — foco específico em limpeza de dados aplicada a ML, direto ao escopo do ICDATA.

## 4. Onde se publica

- **ICDATA** (CSCE) — o próprio venue-alvo de Pedro; tópicos de data cleaning/quality/feature selection/model assessment estão explicitamente na CfP.
- **VLDB, SIGMOD, ICDE** — venues de banco de dados com forte tradição em data cleaning/data quality (nível mais competitivo, não é o alvo imediato).
- **NeurIPS Datasets and Benchmarks Track** — específico para contribuições data-centric e benchmarks (ex.: DataPerf saiu daqui).
- Journals aplicados: *Journal of Data and Information Quality* (JDIQ, ACM), *Information Systems* (Elsevier).

## 5. Stack necessária (ferramentas reais, verificadas)

- **cleanlab** (PyPI: `cleanlab`, GitHub `cleanlab/cleanlab`) — detecção de rótulos ruidosos via confident learning; base teórica no paper "Confident Learning" (JAIR 2021).
- **great-expectations** (PyPI: `great-expectations` / `great_expectations`, versão atual ~1.20) — validação e documentação de dados, integra com pandas/SQL/Spark.
- **pandas / scikit-learn** — manipulação e pipelines de imputação, seleção de features, avaliação de modelo (já domínio de Pedro).
- **SHAP / LIME** (não verificados nesta rodada, mas nomes amplamente conhecidos — checar existência exata antes de citar em texto formal) — interpretabilidade de modelos, relevante para o item "Model interpretation" da CfP.

## 6. Sinal de mercado

Demanda por papéis de dados/ML segue forte: previsão de ~11,5 milhões de novas vagas de dados até o fim de 2026 e crescimento de 163% em postagens de vagas de IA/ML entre 2024 e 2025 nos EUA. O WEF projeta que a demanda por talentos em dados/IA supere a oferta em 30–40% até 2027, com habilidades de "AI e big data" no topo do ranking de skills em crescimento. Isso não é específico de "data quality", mas confirma que a competência central da área (preparação, validação e avaliação de dados) continua sendo empregável e crescente — é a base de qualquer vaga de data scientist/ML engineer, diferente de nichos mais estreitos.

## 7. Como seria um tema de residência (propostas concretas)

1. **Benchmark comparativo de métodos de imputação em dados tabulares desbalanceados**: comparar imputação simples vs. baseada em modelo (KNN, MICE, autoencoders leves) medindo impacto no desempenho final de classificadores sob diferentes taxas de missingness e desbalanceamento — exequível com datasets públicos (UCI, Kaggle), replicável, com contribuição clara ("qual método usar quando").
2. **Detecção de rótulos ruidosos aplicada a um domínio tabular específico** (ex.: dados de saúde ou financeiros públicos): aplicar cleanlab, medir concordância com anotação manual/heurística e propor um critério de priorização de revisão humana — conecta-se diretamente ao tópico "Algorithms for Enhancing Data Quality" da CfP.
3. **Pipeline de validação de dados para monitoramento de drift em produção**: estudo de caso comparando Great Expectations vs. testes estatísticos simples (KS-test, PSI) para detectar mudança de distribuição em um cenário simulado de produção — tema aplicado, fácil de defender como "process/quality" na CfP e alinhado ao perfil profissional de Pedro.

## 8. Riscos

- **Percepção de "encanamento"**: limpeza/preparação de dados é vista por parte da comunidade acadêmica como trabalho de engenharia, não de pesquisa — a contribuição precisa ser enquadrada como comparação sistemática ou novo critério, não apenas "apliquei ferramenta X".
- **Dificuldade de novidade**: técnicas de imputação, seleção de features e validação já são maduras; para aceitação em venue com ~40-50% (ICDATA), isso é gerenciável, mas para venues mais competitivos (VLDB/SIGMOD) a barra de originalidade é bem mais alta.
- **Risco de virar benchmark puro sem storytelling**: comparações empíricas sem uma pergunta de pesquisa clara ("quando X supera Y e por quê") tendem a ser vistas como relatório técnico, não paper.

---

Sources:
- [Data-centric Artificial Intelligence: A Survey (arXiv:2303.10158)](https://arxiv.org/abs/2303.10158)
- [Data-Centric AI in the Age of Large Language Models (arXiv:2406.14473)](https://arxiv.org/abs/2406.14473)
- [Data Cleaning and Machine Learning: A Systematic Literature Review (arXiv:2310.01765)](https://arxiv.org/abs/2310.01765)
- [DataPerf: Benchmarks for Data-Centric AI Development (arXiv:2207.10062)](https://arxiv.org/abs/2207.10062)
- [DataPerf — About](https://www.dataperf.org/about)
- [cleanlab on PyPI](https://pypi.org/project/cleanlab/)
- [cleanlab GitHub](https://github.com/cleanlab/cleanlab)
- [great-expectations on PyPI](https://pypi.org/project/great-expectations/)
- [Data Engineer Demand Report 2026](https://www.jobspikr.com/blog/global-data-engineer-demand-2026/)
- [AI and Data Scientist Job Market in 2026](https://medium.com/data-science-collective/ai-and-data-scientist-job-market-in-2026-analysis-trends-opportunities-early-year-report-1641d1f8a30d)
