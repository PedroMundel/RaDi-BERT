# Leitura 5 — Drift e manutenção de datasets

**Referência:** Lu, J.; Liu, A.; Dong, F.; Gu, F.; Gama, J.; Zhang, G. **"Learning under Concept Drift: A Review"**. arXiv:2004.05785, v1 (13/04/2020; IEEE TKDE, vol. 31, n. 12, 2019). https://arxiv.org/abs/2004.05785
**Verificado em:** 28/08/2026 (arXiv ao vivo). Referência-padrão da área; revisa 130+ trabalhos.
**Alternativa (verificada):** Hinder, F.; Vaquet, V.; Hammer, B. "One or Two Things We Know about Concept Drift — A Survey on Monitoring Evolving Environments". arXiv:2310.15826, v1 (24/10/2023). https://arxiv.org/abs/2310.15826 — mais recente; cobre detecção não supervisionada em streaming e *explicação* do drift (toca G08).

## Por que esta leitura

É a leitura 5 do plano da Fase 4 (ver `../clusters.md`): cobre a etapa de **avaliação e confiança** pelo ângulo temporal — **Q09 concept drift, G06 avaliação de modelo, G08 interpretação**. Base parcial: Q09 é só teoria (porquê pessoal: reavaliação contínua de datasets), G06 tem prática forte (avaliação F1 sintético vs. real no Ultimatum), G08 é "nunca toquei". É a leitura que responde "o dado que era bom continua bom?" — a metade temporal do elevador ("provo quando dá para confiar no resultado").

## Como o survey organiza o campo (do abstract)

Framework em três frentes que virou o padrão da área:

1. **Detecção de drift** — perceber que a distribuição mudou (testes, janelas, monitoramento de erro).
2. **Entendimento do drift** — quando, onde e quanto mudou.
3. **Adaptação ao drift** — retreinar, ajustar, ensembles evolutivos.

A alternativa (Hinder et al. 2023) estende para o cenário sem rótulo (monitoramento não supervisionado) e para explicar o drift — a ponte com interpretação (G08).

## Perguntas-guia (responder durante a leitura)

1. Tipos de drift e vocabulário exato (real vs. virtual; súbito, gradual, incremental, recorrente) — mapa mínimo de Q09.
2. Como se DETECTA drift sem rótulo novo (o caso realista de produção)? Quais testes estatísticos são o baseline (KS, PSI — os mesmos do dossiê C2)?
3. O que "manutenção de dataset" herda daqui: com que frequência reavaliar um dataset estático (caso Ultimatum), não só um stream?
4. O gap sintético→real do Ultimatum (F1 0,918 → 0,655) pode ser lido como um drift entre distribuição sintética e real? O framework de "entendimento do drift" ajuda a localizar ONDE o corpus sintético diverge?
5. Onde interpretação (G08) entra: explicar o drift para um humano decidir o que fazer — o que o survey de 2019 não cobre e a alternativa de 2023 cobre?

## Protocolo

- Ler: abstract → intro → taxonomia de tipos de drift → detecção com calma → entendimento; adaptação (ensembles evolutivos) em leitura rápida — a config foca no DADO, não em algoritmo adaptativo.
- Folhear a alternativa: abstract + seções de monitoramento não supervisionado e explicação de drift.
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo.
- Tempo-alvo: 1 sessão de leitura + 1 de fichamento (base parcial, ritmo normal).

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final)_
