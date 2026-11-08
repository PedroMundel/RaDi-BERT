# Clusters — Semana 1, Residência em IA (consolidado em 18/08/2026)

Derivado do funil macro→meso→micro sobre os 289 tópicos das CfPs do CSCE'26, após ranking (C2 › C1 › C6) e duas podas. Fonte das notas e trilha de decisão: `topicos-csce2026.md`.

## Configuração final

| Papel | Cluster | Conceitos (IDs canônicos) |
|---|---|---|
| **Âncora** | **C2 — Engenharia e qualidade de dados: o pipeline inteiro** | G01, G02, G04, G05, G06, G08, D04, D05, Q09, I17, I14, I27, F03, M08, M09, F05, M14, J12, B40, F04, A02 (21) |
| **Satélite 1** | **C1 — GenAI para dados** | C01, C02, C03, E01 (4) |
| **Satélite 2** | **C6 — Privacidade de dados** | I16, M10, M11, O03 (4) |

**Por que fazem sentido juntos:** a âncora é um único processo — coletar → limpar/preparar → **estruturar/integrar** (ênfase declarada do Pedro) → anotar/adquirir → documentar/governar → avaliar/confiar. O satélite C1 é a ferramenta nova dentro desse processo (LLMs gerando, limpando, anotando e analisando dados). O satélite C6 é a condição de contorno quando o dado é sensível (ameaças, proteção, LGPD).

## O pipeline como mapa da âncora (C2)

| Etapa | Conceitos |
|---|---|
| Limpeza e preparação | G01, G02, G05, D04 |
| Amostragem | G04 |
| Estruturação e modelagem | F03 (warehouse/OLAP), M08 (modelos de dados), I14 (integração), I27 (engenharia), J12 (streaming), A02 (estruturar texto) |
| Anotação e aquisição | M14 (crowdsourcing), I17 (active learning), B40 (aquisição de conhecimento), F04 (conhecimento de domínio) |
| Documentação e governança | M09 (proveniência), F05 (metadados/ontologias) |
| Avaliação e confiança | G06 (avaliação), G08 (interpretação), D05 (exploração), Q09 (drift) |

## Teste do elevador (aprovado em 18/08/2026)

> Eu faço dados prestarem: estruturo, limpo, anoto e documento dados de ponta a ponta, usando LLMs como ferramenta do pipeline.
> E provo quando dá para confiar no resultado — inclusive quando o dado é sensível.

**Regra R1 — anti-atrofia (19/08/2026):** todo projeto de dados termina treinando ou avaliando um modelo de verdade. Objeções à config e respostas prontas: `objecoes-e-respostas.md`.

## Ainda não está resolvido

O **gap sintético→real**: dados gerados por LLM passam nos gates de qualidade, mas o desempenho despenca no dado real (Ultimatum: F1 0,918 → 0,655). Medir, explicar e fechar esse gap é pergunta de pesquisa viva na interseção C2×C1 — candidato natural a tema.

## Evidência de que a config já é praticada

Auditoria do projeto Ultimatum (`ultimatum_ner_pipeline`): ~60% do código é trabalho de dados, 13,7% treino, <0,5% arquitetura; as 12 decisões não-automatizáveis documentadas são todas de dados. O Ultimatum é C2×C1×C6 executado (corpus sintético via LLM + gates de qualidade + domínio jurídico sensível).

## Próxima etapa — Fase 4 (leitura por etapa, não por tópico)

Regra ajustada (18/08/2026): 1 survey por **etapa do pipeline** — 25 surveys "por tópico de CfP" seria contar a burocracia da CfP, não o escopo. ~8 leituras; para cada uma, depois 2–3 papers apontados pelo survey (título + abstract + figuras). Notas em `artigos/`, um .md por leitura. Surveys já verificados estão nos dossiês em `areas/`.

Esqueletos das 8 leituras criados em `artigos/` (28/08/2026), todos com referência verificada, perguntas-guia amarradas às lacunas e protocolo:

| # | Leitura (1 survey) | Cobre | Arquivo em `artigos/` |
|---|---|---|---|
| 1 | Data-centric AI — Zha et al. 2023, arXiv:2303.10158 (dossiê C2) | G01, G02, G05, D04, G06 | `leitura-1-data-centric-ai-zha2023.md` |
| 2 | Integração e estruturação — Chai et al., TKDE 2023 | I14, F03, M08, I27 | `leitura-2-gestao-de-dados-para-ml-chai2023.md` |
| 3 | Anotação: active learning + crowdsourcing — Ren et al. 2021, arXiv:2009.00236 | I17, M14, B40 | `leitura-3-anotacao-active-learning-ren2021.md` |
| 4 | Documentação e proveniência — Paullada et al. 2021, arXiv:2012.05345 (+ Datasheets) | M09, F05 | `leitura-4-documentacao-de-datasets-paullada2021.md` |
| 5 | Drift e manutenção — Lu et al., TKDE 2019, arXiv:2004.05785 | Q09, G06, G08 | `leitura-5-concept-drift-lu2019.md` |
| 6 | LLMs para dados — Zhou et al. 2025, arXiv:2505.18458 (dossiê C1) | C01, C02, C03, E01 | `leitura-6-llm-para-dados-zhou2025.md` |
| 7 | Privacidade e anonimização — arXiv:2506.11687 (dossiê C6) | I16, M10, M11, O03 | `leitura-7-privacidade-de-dados-2025.md` |
| 8 | (opcional) LLM + texto não estruturado — Xu et al. 2024, arXiv:2312.17617 | A02, J12 | `leitura-8-extracao-de-informacao-llm-xu2024.md` |

**Mapa de lacunas (autoavaliação de 18/08/2026):** base mais fraca ("nunca toquei") concentrada em estruturação (F03, M08), documentação (M09, F05), anotação eficiente (I17), interpretação (G08), streaming (J12) e todo o C6 exceto I16 — ou seja, as leituras **2, 4 e 7** merecem o ritmo mais lento; a 3 e a 5 têm base parcial ("só teoria"); a 1 e a 6 são as de base mais forte (prática em disciplinas + Ultimatum). Autoavaliação completa nas colunas da consolidação do `topicos-csce2026.md`.

## Temas candidatos estacionados (retomar quando Pedro pedir temas)

→ **19/08/2026: Pedro pediu temas — 20 propostas formais em `temas-candidatos.md`** (10 âncora C2 + 10 âncora ML). O tema estacionado abaixo se decompôs em A2∩A4∩A7 da lista.

⚠ **Ideias soltas, NÃO são critério para poda, clusters ou qualquer decisão.** O foco declarado do Pedro (18/08/2026) é **o pipeline de dados inteiro**, com interesse especial na parte de estruturação/engenharia.

- **Construção e avaliação de datasets anotados em pt-BR para domínios de baixo recurso (jurídico), com anotação assistida por LLM** — C2 + C1 + componente de C6. Ideia aleatória do Pedro em 18/08/2026. Conexão com o Ultimatum (corpus sintético jurídico, gap sintético→real F1 0,918→0,655).
