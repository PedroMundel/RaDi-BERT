# C4 — Busca, Recuperação de Informação e Recomendação

## 1. O que a área é no dia a dia

Information Retrieval (IR) moderno gira em torno de transformar texto/consulta em vetores (embeddings) e buscar por similaridade em índices vetoriais (FAISS, HNSW) em vez de (ou combinado com) busca lexical clássica (BM25/Elasticsearch). RAG usa esse retrieval como "memória externa" para LLMs: busca documentos relevantes e injeta no prompt antes de gerar a resposta, reduzindo alucinação e permitindo conhecimento atualizado sem re-treinar o modelo. Sistemas de recomendação (RecSys) preveem o que um usuário vai gostar combinando sinais colaborativos (histórico de outros usuários parecidos) com conteúdo (embeddings de itens) — hoje cada vez mais usando LLMs tanto para gerar as recomendações quanto para explicá-las. No dia a dia prático isso envolve: escolher/otimizar embeddings, desenhar pipelines de chunking de documentos, ranquear e re-ranquear resultados, e avaliar tudo isso com métricas de recall/precision/NDCG — problema que fica mais difícil quando o "consumidor final" é um LLM e não um humano lendo uma lista.

## 2. Problemas abertos quentes (2024-2026)

- **Avaliação de RAG**: não há consenso de métrica — RAGAS, ARES e afins tentam medir "fidelidade" e "relevância" sem golden labels humanos confiáveis.
- **Chunking**: como dividir documentos longos (tamanho, overlap, chunking semântico vs. fixo) impacta fortemente recall e ainda é decidido por heurística, não por teoria.
- **Reranking**: retrieval denso traz muito ruído no top-k; cross-encoders e LLM-as-reranker melhoram precisão mas custam latência — trade-off ainda mal explorado sistematicamente.
- **Hybrid/dense+sparse search**: combinar BM25 com embeddings (RRF, fusão ponderada) supera cada abordagem isolada, mas a forma ótima de fusão é dependente de domínio.
- **RecSys com LLM (LLM4Rec)**: usar LLMs como recomendador direto (zero/few-shot) versus como gerador de features/explicações para modelos colaborativos tradicionais — ainda não está claro quando compensa o custo computacional.
- **Graph-based retrieval (GraphRAG)**: estruturar conhecimento em grafos de entidades para melhorar respostas multi-hop é promissor mas caro de construir e manter atualizado.

## 3. Surveys de referência (verificados)

- Gao, Y. et al. **"Retrieval-Augmented Generation for Large Language Models: A Survey"**, arXiv:2312.10997 (dez/2023). https://arxiv.org/abs/2312.10997 — referência canônica de RAG (Naive/Advanced/Modular RAG).
- **"A Survey of Generative Search and Recommendation in the Era of Large Language Models"**, arXiv:2404.16924 (abr/2024). https://arxiv.org/pdf/2404.16924 — cobre a interseção search+recsys sob LLMs, relevante por casar com os dois tópicos da CfP.
- **"Large Language Model Enhanced Recommender Systems: A Survey"**, arXiv:2412.13432 (dez/2024). https://arxiv.org/pdf/2412.13432 — survey mais recente e focado especificamente em LLM4Rec.

(Descartados por não confirmação exata de título/venue: "Towards Next-Generation LLM-based Recommender Systems" e "Efficient LLMs for Recommendation" apareceram na busca mas não foram verificados a fundo — citar apenas se necessário, com cautela.)

## 4. Onde se publica

Venues-âncora da área: **SIGIR**, **ECIR**, **RecSys**, **CIKM**, **WSDM** (todos com IR/RecSys como foco central, alta seletividade). Para o objetivo de Pedro (ICDATA/CSCE, Springer, ~40-50% aceitação), o encaixe é direto: a CfP do ICDATA'26 lista explicitamente "Information Retrieval", "Web search and information extraction", "Recommendation Systems", "Collaborative filtering", "Search engine query processing" e "Graph Based Search" como tópicos aceitos — ou seja, não é preciso forçar enquadramento, a área já está no escopo declarado da conferência.

## 5. Stack necessária

- **FAISS** (Meta, biblioteca open-source de busca vetorial) — indexação e busca por similaridade, roda em CPU ou GPU.
- **Elasticsearch** / OpenSearch — busca lexical (BM25) e híbrida, padrão de mercado.
- **Sentence-Transformers** (Hugging Face) — geração de embeddings para retrieval denso.
- Frameworks de orquestração RAG: **LangChain** ou **LlamaIndex** — aceleram prototipagem de pipelines RAG.
- Datasets/benchmarks públicos: **MS MARCO**, **BEIR** (para IR), **MovieLens**, **Amazon Reviews** (para RecSys) — todos gratuitos e amplamente usados em papers.

Tudo roda com GPU modesta (embeddings + reranking em modelos pequenos/médios); não exige treinar LLM do zero.

## 6. Sinal de mercado

Demanda alta e crescente: "search/RAG engineer" e "recommendation systems engineer" são papéis ativos em empresas de e-commerce, streaming, fintech e em toda empresa que adota chatbots corporativos com RAG (caso de uso nº 1 de LLM em produção hoje). Vantagem para o currículo: é uma habilidade que soma diretamente com o interesse de Pedro em LLM/GenAI, mas com uma vertente mais "engenharia de dados aplicada" que abre portas em vagas de Data Science/ML Engineering, não só pesquisa.

## 7. Como seria um tema de residência

1. **Avaliação sistemática de estratégias de chunking em RAG**: comparar chunking fixo vs. semântico vs. recursivo em um corpus de domínio (ex. legislação, artigos científicos em pt-BR) medindo recall@k e qualidade da resposta final — exequível com um dataset público + embeddings open-source + GPU única.
2. **Hybrid search (BM25 + denso) com fusão adaptativa**: propor/testar uma regra de fusão que pondera BM25 e embeddings por tipo de query, medindo ganho de NDCG em BEIR ou subset dele — trabalho contido, replicável, publicável em formato "empirical study".
3. **RAG vs. fine-tuning leve para domínio específico em português**: comparar custo/benefício de RAG contra LoRA fine-tuning num LLM pequeno para um domínio de nicho (ex. suporte técnico, dados da UFG) — conecta IR com o interesse maior em LLM/GenAI e é um tema "de fronteira" ainda pouco coberto para PT-BR.

Todas as três são exequíveis por um aluno sozinho, com dados públicos ou fáceis de coletar, sem necessidade de treinar modelos grandes do zero.

## 8. Riscos

- Área extremamente ativa e populosa — concorrência alta em SIGIR/RecSys/CIKM (esses são difíceis); no ICDATA o risco é menor mas o "estado da arte" muda rápido, tornando comparações datadas em poucos meses.
- Avaliação de RAG ainda carece de padrão — há risco de o reviewer discordar da métrica escolhida por falta de consenso na comunidade.
- Boa parte do "hype" de RAG é aplicação de ferramentas prontas (LangChain/LlamaIndex); para virar contribuição científica publicável é preciso ir além do tutorial e isolar uma pergunta empírica clara.
