# Leitura 6 — LLMs para dados (dossiê C1)

**Referência:** Zhou, X.; He, Z.; Zhou, X. et al. **"A Survey of LLM × DATA"**. arXiv:2505.18458, v3 (01/06/2025). https://arxiv.org/abs/2505.18458
**Verificado em:** 18/08/2026 (dossiê `../areas/C1-genai-para-dados.md`).
**Complementares (também verificados no dossiê):** Tan et al., "Large Language Models for Data Annotation and Synthesis: A Survey", arXiv:2402.13446 (EMNLP 2024) · Wang et al., "A Survey on Data Synthesis and Augmentation for Large Language Models", arXiv:2410.12896.

## Por que esta leitura

É a leitura 6 do plano da Fase 4 (ver `../clusters.md`): cobre o satélite C1 inteiro — **C01 GenAI gerando dados, C02 GenAI para data handling, C03 GenAI para analytics/relatórios, E01 LLMs**. Base do Pedro aqui é forte (Ultimatum é C1 executado: corpus sintético via LLM + anotação assistida), então o objetivo — como na leitura 1 — é **organizar a prática com o vocabulário do campo** e mapear o que a comunidade já mediu sobre os problemas que o Ultimatum viveu na pele.

## Como o survey organiza o campo (do dossiê C1)

Cobre as **duas direções** da relação LLM×dados:

1. **DATA4LLM** — dado para treinar/alimentar LLM (curadoria, deduplicação, qualidade em escala de pré-treino).
2. **LLM4DATA** — LLM como ferramenta de gestão de dados (limpeza, integração, descoberta, análise).

A direção 2 é a que interessa à config (C1 = ferramenta dentro do pipeline C2); a direção 1 interessa como espelho — as técnicas clássicas de C2 reaparecem sob restrições de escala completamente diferentes.

## Perguntas-guia (responder durante a leitura)

1. Que nome o campo dá ao que o Ultimatum fez (geração de corpus sintético guiada por prompt, anotação assistida, gates de qualidade sobre saída de LLM)? — vocabulário para escrever depois.
2. O que o survey diz sobre **alucinação em limpeza/imputação** (LLM inventa valor plausível mas errado)? Existe sinal de confiança calibrado proposto?
3. Onde entra o **custo por linha/célula**: quando o survey diz que vale LLM vs. regra/ML clássico? (problema aberto nº 2 do dossiê)
4. Como se avalia dado sintético gerado por LLM — alguma métrica além de desempenho downstream? Algo que fale diretamente com o **gap sintético→real** (F1 0,918 → 0,655)?
5. Que interfaces LLM→dado estruturado o survey cobre (text-to-SQL, extração)? — ponte com a leitura 8.

## Protocolo

- Ler: abstract → taxonomia/figuras → seções de **LLM4DATA** com calma (limpeza, integração, anotação); DATA4LLM em leitura rápida, só para o espelho de escala.
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo. Candidato já verificado no dossiê: RetClean (PVLDB 17, 2024 — limpeza retrieval-based com LLM).
- Tempo-alvo: 1 sessão de leitura + 1 de fichamento (base forte, ritmo normal).

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final)_
