# Leitura 7 — Privacidade e anonimização de dados (dossiê C6)

**Referência:** **"Differential Privacy in Machine Learning: A Survey — from Symbolic AI to LLMs"**. arXiv:2506.11687 (2025; também publicado na ACM TIST). https://arxiv.org/abs/2506.11687
**Verificado em:** 18/08/2026 (dossiê `../areas/C6-privacidade-de-dados.md`).
**Complementares (também no dossiê):** "Differentially Private Federated Learning: A Systematic Review", arXiv:2405.08299 · "When Federated Learning Meets Privacy-Preserving Computation", ACM Computing Surveys 2024 · "Defending against attacks in deep learning with differential privacy: a survey", Artificial Intelligence Review (Springer) 2025.

⚠ **Decisão em aberto:** o anchor é DP-cêntrico; a leitura cobre privacidade de dados mais amplamente (ameaças, proteção, normas). Se na leitura o survey se mostrar estreito demais para O03/M11, buscar complemento de anonimização/MIA — reavaliar após a seção de ataques.

## Por que esta leitura

É a leitura 7 do plano da Fase 4 (ver `../clusters.md`): cobre o satélite C6 inteiro — **I16 privacy-preserving data mining, M10 métodos de proteção, M11 normas e políticas (LGPD), O03 ameaças de privacidade em big data**. Base do Pedro aqui é a mais fraca de toda a config ("nunca toquei" em M10/M11/O03; I16 só teoria) — é uma das três leituras marcadas para **ritmo lento** no mapa de lacunas. Objetivo: construir o vocabulário do zero e entender o "por quê" do satélite (dado jurídico sensível no Ultimatum).

## Como o survey organiza o campo (do dossiê C6)

As quatro frentes que se misturam no dia a dia da área:

1. **Differential privacy (DP)** — ruído calibrado com orçamento de privacidade (ε) contabilizado (DP-SGD/Opacus).
2. **Aprendizado federado** — treinar sem centralizar dado bruto.
3. **Dados sintéticos** — versão artificial do dataset que preserva utilidade sem expor registros (ponte direta com C1).
4. **Ataques e auditoria** — membership inference, reidentificação, extração de dados de LLMs; testar se a defesa funciona.

## Perguntas-guia (responder durante a leitura)

1. O que exatamente DP garante — e o que NÃO garante? (vocabulário mínimo: ε, mecanismo, composição; sem entrar na matemática pesada)
2. Quais são as **ameaças** catalogadas (O03): membership inference, reidentificação, extração de treino em LLMs — como cada uma funciona em uma frase?
3. Dado sintético protege privacidade de verdade? O que o survey diz sobre MIA continuar funcionando sobre dado sintético (problema aberto nº 2 do dossiê)? — cruza com o corpus sintético do Ultimatum.
4. Que métricas técnicas existem para ancorar exigências de conformidade (LGPD/GDPR, M11)? Onde o survey admite que a resposta não é técnica?
5. Qual é o trade-off privacidade×utilidade na prática — como se mede, e quanto se perde? (é o eixo do tema candidato nº 1 do dossiê C6)

## Protocolo

- Ler DEVAGAR (lacuna máxima): abstract → intro → taxonomia → seção de ataques/ameaças com calma → DP conceitual (pular provas) → dado sintético. Federated learning em leitura rápida (não é foco da config).
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo.
- Tempo-alvo: 2 sessões de leitura lenta + 1 de fichamento.

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final)_
