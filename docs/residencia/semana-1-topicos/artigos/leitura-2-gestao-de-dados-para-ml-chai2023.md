# Leitura 2 — Integração e estruturação de dados

**Referência:** Chai, C.; Wang, J.; Luo, Y.; Niu, Z.; Li, G. **"Data Management for Machine Learning: A Survey"**. IEEE TKDE, vol. 35, n. 5, pp. 4646–4667 (2023). DOI: 10.1109/TKDE.2022.3148237 (sem versão arXiv; PDF do autor em dbgroup.cs.tsinghua.edu.cn).
**Verificado em:** 28/08/2026 (DOI + repositório institucional + Semantic Scholar, três fontes concordantes).
**Alternativa (verificada):** Roh, Y.; Heo, G.; Whang, S. E. "A Survey on Data Collection for Machine Learning: a Big Data–AI Integration Perspective". arXiv:1811.03402, v2 (2019; IEEE TKDE 2021). https://arxiv.org/abs/1811.03402 — mais estreita (aquisição/rotulagem), backup.

## Por que esta leitura

É a leitura 2 do plano da Fase 4 (ver `../clusters.md`): cobre a etapa de **estruturação e modelagem** da âncora — **I14 integração de dados, F03 warehousing/OLAP, M08 modelos de dados, I27 engenharia de dados**. É uma das três leituras marcadas para **ritmo lento**: F03 e M08 são "nunca toquei", I14 é só teoria (bronze/silver/gold em 1 atividade); o contrapeso é I27 (pipeline completo do Ultimatum). F03 e M08 foram *promovidos* na poda 2 justamente pela ênfase declarada em estruturação — esta leitura é o centro da lacuna.

## Como o survey organiza o campo (do abstract)

Revisa gestão de dados para ML em **três eixos ao longo do pipeline**:

1. **Dados para ML** — aquisição, integração, preparação dos dados que alimentam o modelo.
2. **Armazenamento e consulta** — como guardar e servir dados/features (a parte de warehousing).
3. **Gestão de modelos** — armazenar, consultar, implantar e depurar modelos.

O eixo 1 conversa com o que a leitura 1 (Zha et al.) chama de training data development — comparar as duas taxonomias.

## Perguntas-guia (responder durante a leitura)

1. Que técnicas o campo cataloga para **integrar fontes heterogêneas** (I14) — schema matching, entity resolution? Qual o vocabulário para "montar corpus de fontes heterogêneas" (o porquê pessoal registrado na consolidação)?
2. O que warehouse/OLAP (F03) significa num pipeline de ML em 2023+ — feature store é o herdeiro disso? O que existe entre "tabela solta" e "warehouse corporativo"?
3. Que **modelos de dados além da tabela** (M08) aparecem — grafos, documentos, tensores? Quando cada um compensa?
4. Onde o padrão bronze/silver/gold (que o Pedro já versionou em disciplina) se encaixa na taxonomia formal?
5. O que o survey considera "engenharia de dados" (I27) que o Ultimatum ainda NÃO faz — o delta entre o pipeline artesanal e o estado da arte?

## Protocolo

- Ler DEVAGAR (lacuna de estruturação): abstract → intro → figuras/taxonomia → eixo 1 (dados para ML) e eixo 2 (armazenamento/consulta) com calma; eixo 3 (gestão de modelos) em leitura rápida.
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo.
- Tempo-alvo: 2 sessões de leitura lenta + 1 de fichamento.

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final)_
