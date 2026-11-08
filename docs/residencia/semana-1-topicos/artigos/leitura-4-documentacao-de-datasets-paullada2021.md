# Leitura 4 — Documentação e proveniência de datasets

**Referência:** Paullada, A.; Raji, I. D.; Bender, E. M.; Denton, E.; Hanna, A. **"Data and its (dis)contents: A survey of dataset development and use in machine learning research"**. arXiv:2012.05345, v1 (09/12/2020; Patterns 2021). https://arxiv.org/abs/2012.05345
**Verificado em:** 28/08/2026 (arXiv ao vivo).
**Alternativa (verificada):** Gebru, T.; Morgenstern, J. et al. "Datasheets for Datasets". arXiv:1803.09010, v8 (2021; Communications of the ACM 2021). https://arxiv.org/abs/1803.09010 — não é survey, é a PROPOSTA-marco de prática de documentação; ler junto como artefato primário que o anchor discute.

## Por que esta leitura

É a leitura 4 do plano da Fase 4 (ver `../clusters.md`): cobre a etapa de **documentação e governança** da âncora — **M09 preservação/proveniência, F05 metadados/ontologias**. Ambos são "nunca toquei" e ambos foram *promovidos* na poda por serem essenciais ao C2 (documentação de dataset; esquema de anotação) — uma das três leituras marcadas para **ritmo lento**. É também a etapa que transforma "dataset que funciona" em "dataset que outros podem confiar e reusar" — o elo com o elevador ("documento dados de ponta a ponta").

## Como o survey organiza o campo (do abstract)

Revisa o ciclo de vida do dataset em ML e onde ele falha:

1. **Desenvolvimento de datasets** — como são criados, e os problemas de origem (coleta, consentimento, representatividade).
2. **Uso e reuso** — benchmarks herdados sem exame, dataset usado fora do propósito original.
3. **Documentação e transparência** — as práticas propostas (datasheets, data statements, nutrition labels) e por que a adoção falha.

A alternativa (Datasheets) é o instrumento concreto: a lista de perguntas que todo dataset deveria responder.

## Perguntas-guia (responder durante a leitura)

1. Que instrumentos de documentação existem (datasheets, data statements, model cards para dados) e o que cada um registra? — candidato direto a prática no próprio trabalho da residência.
2. O que "proveniência" (M09) significa operacionalmente: o que rastrear (origem, transformações, versões) e com que granularidade?
3. Onde entram **metadados e ontologias** (F05): como um esquema de anotação vira artefato documentado e versionável?
4. Que falhas catalogadas o Ultimatum cometeu ou evitou (corpus sintético: qual é a "origem" documentável de um dado gerado por LLM)?
5. Existe proveniência PARA dado sintético — alguém documenta prompt, modelo gerador e versão como linhagem? (cruza com C1 e com o gap sintético→real)

## Protocolo

- Ler DEVAGAR (lacuna de documentação): anchor inteiro com calma — é curto para um survey.
- Ler a alternativa (Datasheets) na sequência: as 7 seções de perguntas do datasheet valem como checklist a adotar.
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo.
- Tempo-alvo: 2 sessões de leitura lenta + 1 de fichamento (anchor + datasheet).

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final)_
