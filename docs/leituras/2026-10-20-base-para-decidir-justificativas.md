# Base para decidir como devem ser as justificativas (20/10/2026)

**Pedido do Pedro (20/10):** "me falta uma base pra ter clareza nas decisões". Esta é uma lista curta, ligada às
decisões abertas da geração (rodada 0 e prompt). As seções foram mapeadas pelo Claude via ar5iv/arXiv (nível 3).
**Página e conteúdo, só lendo.** A ordem de leitura usa o método das 5 paradas (`docs/metodo-de-leitura.md`).

## Núcleo (~2h no total)

| # | Obra | Já estava no projeto? | Onde ler | Decisão que ajuda a tomar |
|---|---|---|---|---|
| 1 | **Wiegreffe & Marasović (2021)**, *Teach Me to Explain: A Review of Datasets for Explainable NLP*, NeurIPS 2021 Datasets and Benchmarks. arXiv:2102.12060 (~10 p. + apêndice) | Sim. Planejada no gate 6 (`docs/residencia/trilha-gate-6.md`) e nunca lida. Guia pronto: `docs/leituras/explicacao-racionalizacao.md` | §2 (vocabulário e tipos: destaque, texto livre, estruturada) · **§5** (o e-SNLI e os moldes: 56 filtrados, ~11% refeitos, 28 moldes por rótulo que ficaram, e por que isso seria "consequência natural da tarefa") · §6.1 e §7.2 (qualidade; mais de uma explicação válida por instância) | O que é qualidade em explicação; se o formato "moldado" das humanas é defeito ou é próprio do NLI; uma ou várias justificativas por par. Também fecha a definição cobrada no gate 5 |
| 2 | **Camburu et al. (2018)**, *e-SNLI*, NeurIPS 2018. arXiv:1812.01193 | Sim. Está na Lista de Obras (pedido seu, 07/10) | Só a **§3, "Collecting explanations"** (~1,5 p.) e o Apêndice A (moldes) | A especificação do que os anotadores tinham de escrever: base direta para a instrução do prompt e para julgar as humanas pelo critério com que foram feitas |
| 3 | **Wiegreffe et al. (2022)**, *Reframing Human-AI Collaboration for Generating Free-Text Explanations*, NAACL 2022. arXiv:2112.08674 | **Não.** Apareceu na pesquisa de 19/10 | §2 (GPT-3 × humano no e-SNLI; Tab. 3–5; a Tab. 4 foi conferida pelo Claude) · §3 (atributos avaliados: informação nova, sustenta o rótulo, factualidade etc.) | **Humano × LLM** com dados, no próprio e-SNLI. Os atributos da §3 servem de rubrica pronta para a sua avaliação manual. Ressalva: o professor é o GPT-3 (2022) |

## Opcional

| Obra | Onde | Para quê |
|---|---|---|
| Hase et al. (2020), *Leakage-Adjusted Simulatability*, Findings of EMNLP 2020. arXiv:2010.04119 | só a seção que define vazamento (a frase dos ~97% está na p. 5) | Decidir se vazamento do rótulo é defeito (decisões 1 e 6 da rodada 0) |
| Gurrapu et al. (2023), *Rationalization for Explainable NLP: A Survey*, Frontiers in AI. arXiv:2301.08912 | — | Já estava planejada. Panorama de métodos; pesa menos nas decisões desta semana |
| Chen, Zhang & Yang (2021; v2 2024), *Multi-Task Learning in NLP: An Overview*, ACM Computing Surveys. arXiv:2109.09138 | **Não conferi** se explica por que tarefas auxiliares ajudam | Seria a base do mecanismo: o que o decoder auxiliar ensina ao encoder. Só vale se tiver essa seção |

**Já lido por você e central aqui:** Wadhwa et al. (2024). A forma e a gramática pesam pouco; o que pesa são os
tokens que trazem sinal novo.

## Perguntas para levar à leitura

1. As humanas do e-SNLI são ruins, ou são o formato que o NLI pede? (Teach Me to Explain §5; Camburu §3)
2. Quais atributos definem uma boa justificativa, e qual deles importa para o aluno, não só para o leitor? (Wiegreffe 2022 §3; Wadhwa)
3. Vazar o rótulo é defeito ou é inevitável na tarefa? (Hase 2020; Teach Me to Explain §5)
4. Vale gerar mais de uma justificativa por par? (Teach Me to Explain §7.2)
