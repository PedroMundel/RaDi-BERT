# Objeções à config C2×C1×C6 — e as respostas (registrado em 19/08/2026)

Objeções levantadas por colegas e pelo próprio Pedro durante a Semana 1. Registradas porque VÃO reaparecer: na banca, em entrevista, no corredor. Cada uma tem a resposta curta (para falar) e a evidência (para sustentar).

## O1 — "Você faz Bacharelado em IA, não Ciência de Dados"

**Resposta curta:** Não vou fazer BI nem dashboards. Vou fazer a parte da IA que decide se o modelo aprende algo ou aprende lixo — construção e avaliação dos dados que treinam modelos, usando LLMs no meio do pipeline. O campo chama isso de *data-centric AI*, e é área da IA: o survey de referência (Zha et al.) é da comunidade de ML, o NeurIPS tem trilha de Datasets & Benchmarks, o DataPerf é da MLCommons.

**Distinção de uma linha:** Ciência de Dados extrai insight de dados para decisão de negócio; a minha âncora engenheira o dado que faz a IA aprender.

**Cuidado prático:** o rótulo "qualidade de dados" convida a leitura errada. Usar o elevador aprovado, nunca o rótulo cru.

## O2 — "Todo profissional de ML deve saber dados; nem todo profissional de dados sabe modelos"

**Onde a objeção acerta:** se a especialização virasse "profissional de dados que não sabe treinar modelo", seria escolher o subconjunto commodity. Risco real, tratado pela regra R1 abaixo.

**Onde falha (1): confunde "deve saber" com "sabe".** A comunidade de modelos é sistematicamente fraca em dados — é por isso que data-centric AI existe como área. Evidência: Sambasivan et al. (Google, 2021), "Everyone wants to do the model work, not the data work: Data Cascades in High-Stakes AI" — ~92% dos praticantes relatam cascatas causadas por dado malfeito; os 80 TCCs das turmas anteriores (79 correm para o modelo). Habilidade universalmente exigida + universalmente subdesenvolvida = especializar não é commodity, é virar fornecedor do gargalo. `dropna()` é universal; desenhar esquema de anotação, medir qualidade de dataset independente do F1 e provar que dado sintético funciona é raro até entre doutores.

**Onde falha (2): a config não larga o lado do modelo.** E01 (DL/LLMs) tem nota 3; C1 inteiro é aplicar LLM; G06/G08 é avaliar e interpretar modelo; os fundamentos de ML ficaram em nota 2 ("quero estudar de verdade"). O perfil é *engenheiro de IA cujo diferencial é o dado*, não "pessoa de dados sem modelo". A assimetria, aplicada a esse perfil, joga a favor: fico no lado de que todos precisam sem sair da conversa de IA.

## O3 — "Ninguém no programa faz isso" (o falso 1/80)

**Resposta curta:** contagem real do repositório: ~8/80 TCCs com dados no núcleo, frequência crescendo (1 em 2024-02 → 4 em 2025-12), pool saturado é LLM/agentes (~25%), e estruturação de dados é território virgem. Análise item a item em `analise-tccs-anteriores.md`.

## O4 — "Se nem os profissionais de ML valorizam dados, empregador também não vai valorizar"

**Falha lógica:** empregador não paga pelo que é glamouroso para o praticante; paga pelo que faz projeto quebrar. Precedentes: testes, DevOps/SRE e segurança — desprezados por devs, viraram especialidades caras. Dados têm a mesma assinatura (baixo prestígio interno + custo de falha alto, documentado em Sambasivan et al. 2021).

**Evidência verificada (19/08/2026):**
- Meta pagou US$ 14,3 bi por 49% da Scale AI (valuation ~US$ 29 bi) — empresa cujo produto É rotulagem/qualidade de dados — para resolver o gargalo de datasets de treino. OpenAI e Google eram clientes. (Forbes 06/2025; IEEE Spectrum)
- Engenharia de dados entre os papéis mais demandados de 2026: +23% em 2025, ~260 mil vagas projetadas nos EUA, salários US$ 127–180 mil (Robert Half 2026). Diagnóstico do mercado: "todo projeto de IA depende de um pipeline de dados que a empresa subestima até estar no meio do projeto".

**Refinamento que a objeção rende (gradiente de valor):** rotular manualmente = commodity terceirizada; *desenhar* o processo, automatizar com LLM, medir qualidade, provar confiabilidade e proteger privacidade = a ponta premium (o que Scale/labs monetizam). A config está inteira na ponta premium; R1 mantém lá.

## O5 — "ML paga mais que dados"

**Onde acerta:** na tabela de cargos, MLE mediano (~US$ 159–166 mil; TC ~US$ 212 mil) > Data Engineer (US$ 127–180 mil, Robert Half 2026). Verificado 19/08/2026.

**Por que não muda a decisão:** salário é definido pelo cargo em que te contratam, não pela âncora da especialização. O perfil de saída da config (treina/avalia modelo por R1 + domina pipeline) é contratado como **MLE** — a âncora em dados diferencia *dentro* da régua MLE, não te rebaixa à régua DE. O cenário que pagaria menos (DE puro) exigiria abandonar E01, C1 e R1 — exatamente o que a config proíbe. Risco real é de rótulo: vender-se como "qualidade de dados" cai na régua errada (~20% de diferença); usar sempre o posicionamento da O1.

## O6 — "Meu maior gap é engenharia de ML, então a âncora deveria ser ML"

**Distinção central: âncora ≠ plano de estudos.** Gap é agenda de aprendizado; âncora é onde se quer ser *reconhecido*. "Ser bom engenheiro de ML" é barra de competência que TODA config exige — e a R1 já força a prática em todo projeto. Barra de competência não é diferencial: os 79 colegas fecham o mesmo gap. Ancorar no déficit = ancorar contra o interesse medido (funil, estruturação, Ultimatum 60%) para competir no território mais saturado.

**Cenários delimitados em que a resposta vira SIM** (probabilidade baixa, monitorar):
1. O "gap" for na verdade **desejo** — preferir construir modelos a construir datasets no dia a dia. Só o Pedro responde; o teste é a reação às duas listas de temas (`temas-candidatos.md`).
2. Base de ML fraca demais para pesquisa de dados com credibilidade — mitigável antecipando prática de ML (R1 agressiva) sem mover a âncora.

## Medos anteriores, já tratados (trilha)

- **Viés por desconhecimento** — refutado pelo comportamento real no Ultimatum (~60% do código é trabalho de dados, por escolha).
- **Obsolescência pós-dataset** — refutado: drift, churn de modelos, LGPD/governança; empresa comum terceiriza o modelo, não o dado.
- **"Uma IA disse que ia dar certo"** — a decisão decompõe em: escolhas do Pedro (notas, ranking, vetos) + fatos verificáveis sem IA (Ultimatum, TCCs, CfPs) + opiniões interpretativas da IA (nomeadas e tratadas como hipótese). As duas primeiras camadas sustentam a config sozinhas.

## R1 — Regra anti-atrofia (adotada em 19/08/2026)

> **Todo projeto de dados meu termina treinando ou avaliando um modelo de verdade.**

Motivo: neutralizar o único risco real da O2 — o lado de modelo atrofiar com os anos. O Ultimatum já cumpre (NER treinado + F1 medido). Vale para TCC, PoCs e estudos da Fase 4: nenhum trabalho de pipeline entrega só o dataset; entrega o dataset + o modelo que prova que ele presta.
