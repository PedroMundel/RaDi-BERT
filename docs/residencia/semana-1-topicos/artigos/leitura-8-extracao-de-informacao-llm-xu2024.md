# Leitura 8 (opcional) — LLM + dado não estruturado / texto

**Referência:** Xu, D.; Chen, W.; Peng, W. et al. **"Large Language Models for Generative Information Extraction: A Survey"**. arXiv:2312.17617, v3 (31/10/2024; Frontiers of Computer Science 2024). https://arxiv.org/abs/2312.17617
**Verificado em:** 28/08/2026 (arXiv ao vivo).
**Alternativa (verificada):** Liu, P.; Gao, W. et al. "A Survey on Open Information Extraction from Rule-based Model to Large Language Model". arXiv:2208.08690, v7 (23/10/2024). https://arxiv.org/abs/2208.08690 — arco histórico 2007–2024 (regras → neural → LLM), útil para contexto pré-LLM.

## Por que esta leitura

É a leitura 8 do plano da Fase 4 (ver `../clusters.md`), marcada como **opcional**: cobre **A02 NLP (estruturar texto)** e, secundariamente, **J12 streaming**. É a etapa "estruturar dado não-estruturado" — exatamente o que o Ultimatum faz (NER jurídico), então a base é forte e a leitura funciona como fechamento: liga a ponta de entrada do pipeline (texto bruto) à âncora (dado estruturado de qualidade). Fazer por último, ou pular se as leituras 2/4/7 consumirem o tempo — o custo de pular é baixo porque a leitura 6 já cobre a interface LLM→estrutura em parte.

## Como o survey organiza o campo (do abstract)

Extração de informação **generativa**: em vez de classificar tokens, o LLM gera a estrutura. Organiza por:

1. **Subtarefas** — NER, extração de relações, extração de eventos: texto → entidades → ligações → acontecimentos.
2. **Técnicas** — prompting, fine-tuning, formatos de saída estruturada.
3. **Cenários** — domínios específicos, poucos rótulos, etc.

## Perguntas-guia (responder durante a leitura)

1. Como o campo formula NER generativo vs. o NER clássico de token-classification que o Ultimatum usou? O que se ganha e se perde?
2. O que o survey diz sobre **domínios especializados** (jurídico, médico) e poucos dados — o cenário exato do Ultimatum?
3. Como se garante e se avalia **saída estruturada válida** (schema, JSON)? — cruza com F05 (esquema de anotação) da leitura 4.
4. Extração é a ponte texto→pipeline: o que o survey diz sobre qualidade do dado extraído (erro se propaga para o dataset)? — cruza com a leitura 1.
5. Algo sobre extração em fluxo contínuo (J12) ou é tudo batch? Se nada, registrar que J12 fica sem survey dedicado — decisão consciente.

## Protocolo

- Ler: abstract → figuras/taxonomia → seção de NER e de domínios específicos com calma; eventos/relações em leitura rápida.
- Alternativa: só se quiser o contexto histórico pré-LLM (não obrigatória).
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo.
- Tempo-alvo: 1 sessão única (leitura + fichamento) — é a leitura de fechamento, base forte.

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final)_
