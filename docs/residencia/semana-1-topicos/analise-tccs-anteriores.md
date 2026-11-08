# Análise dos TCCs das turmas anteriores (verificado em 19/08/2026)

Fonte: coleção do repositório institucional da UFG (80 itens, turmas 2024-02 a 2025-12), extraída via API DSpace.
Motivação: checar a impressão do Pedro ("dos 80, apenas 1 aborda dados") e o estranhamento de colegas com a config C2×C1×C6.

## Contagem por tema (título como proxy)

| Tema | Qtde | Exemplos |
|---|---|---|
| LLMs / agentes / RAG / alinhamento | ~20 | multiagentes p/ finanças (×2), RAG (×2), alinhamento via RL (×2), agentOps |
| Visão computacional | ~8 | segmentação, diagnóstico dermatológico, reconhecimento facial, edge |
| RL aplicações | ~7 | trading, estoque, jogos, saúde, sim-to-real |
| MLOps / infra | ~6 | pipelines cloud, LLMOps, CUDA |
| **Trabalho de dados como núcleo** | **~8** | ver lista abaixo |
| NLP clássico | 4 | sendo 2 em domínio jurídico (análise de textos, NER) |
| Áudio / fala | 4 | ASR, codecs neurais, tradução simultânea |
| Teoria (grafos, cálculo) | 3 | |
| Outros (federado, séries, BCI, neuro, social...) | ~10 | |

## Os TCCs com dados no núcleo (não é 1 — são ~8)

1. **Geração automática de datasets** a partir de ligações de call center para fine-tuning de LLMs (2024-02) — construção de dataset via pipeline, C2×C1 puro.
2. **Geração de dataset sintético: benchmark multirrótulo para detecção de preconceitos em textos em português** (2024-12) — dataset pt-BR do zero; vizinho direto do tema estacionado do Pedro.
3. Adaptação de domínio na **geração de dados sintéticos** de imagens (DCGAN) (2024-12).
4. RL em NLP com **dados sintéticos** para monitoria de call center (2024-12).
5. **Detecção de concept drift** temporal em textos (2025-07) — é o Q09 da config.
6. **Detecção de concept drift** em MLOps (2025-12) — Q09 de novo.
7. Procedural content generation: **desenvolvimento de datasets** + fine-tuning para jogos (2025-12).
8. **Privacidade de dados** em serviços web: requisitos legais e mecanismos de proteção (2025-12) — é o C6 da config.

## Leituras

- A percepção "1/80" provavelmente contou só o item 2 (único com "dataset" no título principal). Olhando o conteúdo, **~10% das turmas já trabalha dados como núcleo** e a frequência CRESCE (1 em 2024-02 → 4 em 2025-12, contando drift e privacidade).
- O pool saturado é LLM/agentes (~25%) e RL (~9%) — é lá que diferenciação é zero.
- Nenhum TCC toca **estruturação/integração/warehouse/documentação de dados** — a ênfase declarada do Pedro é território virgem no programa.
- Precedentes diretos de cada peça da config existem: C2×C1 (itens 1–4, 7), Q09 (5, 6), C6 (8), domínio jurídico (2 TCCs de NLP jurídico em 2024-02).

**Conclusão:** o repositório NÃO sustenta o "não tem a ver"; sustenta o oposto — a config tem precedente, tendência de crescimento e espaço em aberto exatamente na parte (estruturação) onde o Pedro quer ênfase.
