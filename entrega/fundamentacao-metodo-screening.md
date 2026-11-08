# Fundamentação do método de screening

As decisões que o método de screening fecha são os componentes-padrão de um protocolo de revisão
bibliográfica: os mesmos de uma revisão sistemática, de um scoping study ou de um mapping study. O
que o método faz de próprio é adaptar esses componentes ao screening pedido na Etapa 1: retira a
exaustividade e troca a regra de parada por saturação. Este documento mostra de onde vem cada
decisão, o que foi adaptado e por quê, e no que usei IA como ferramenta de apoio.

---

## 1. De onde vêm as decisões - mapeamento para a literatura de método

Os frameworks abaixo são os de referência para método de revisão em computação e áreas afins. Estão
em nível 3 de procedência (conhecimento prévio, adquirido ou recomendado por uma ferramenta de IA).

**Níveis de conhecimento:** 1. Li por completo. 2. Li parcialmente. 3. Li somente a introdução e/ou
abstract/resumo e/ou alguma seção. 4. Leitura completa ou parcial feita por agentes com geração de
resumo (normalmente em casos de extensividade, como livros).

**Artigos citados** (nível de conhecimento entre colchetes):

- [2] Arksey, H.; O'Malley, L. (2005). Scoping studies: towards a methodological framework.
  International Journal of Social Research Methodology, 8(1), 19-32. DOI 10.1080/1364557032000119616.
- [4] Glaser, B. G.; Strauss, A. L. (1967). The Discovery of Grounded Theory: Strategies for
  Qualitative Research. Aldine.
- [4] Kitchenham, B.; Charters, S. (2007). Guidelines for performing Systematic Literature Reviews in
  Software Engineering. EBSE Technical Report EBSE-2007-01, Keele University e Durham University.
- [1] Petersen, K.; Feldt, R.; Mujtaba, S.; Mattsson, M. (2008). Systematic Mapping Studies in
  Software Engineering. 12th International Conference on Evaluation and Assessment in Software
  Engineering (EASE 2008). DOI 10.14236/ewic/ease2008.8.
- [3] Tricco, A. C. et al. (2018). PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and
  Explanation. Annals of Internal Medicine, 169(7), 467-473. DOI 10.7326/M18-0850.
- [4] Wohlin, C. (2014). Guidelines for snowballing in systematic literature studies and a
  replication in software engineering. 18th International Conference on Evaluation and Assessment in
  Software Engineering (EASE 2014). DOI 10.1145/2601248.2601268.

| # | Decisão do método | Componente-padrão | Onde está na literatura |
|---|---|---|---|
| 1 | Screening de quê? (unidade de busca) | **Questão de pesquisa / escopo** | Kitchenham & Charters 2007, research questions; Arksey & O'Malley 2005, estágio 1, identifying the research question |
| 2 | Divisões antes ou depois da busca? | **Esquema de classificação**, a priori ou emergente | Petersen et al. 2008, classification scheme construído por keywording dos resumos (bottom-up); é a origem direta da decisão "bottom-up no conteúdo" |
| 3 | Tipos de fonte aceitos | **Critérios de inclusão por tipo de publicação** | Kitchenham & Charters 2007, study selection criteria; Arksey & O'Malley 2005, estágio 3, study selection |
| 4 | Como se identifica o seminal | **Snowballing e conjunto inicial** | Wohlin 2014, backward snowballing a partir de um start set; a interseção de referências entre surveys é snowballing com voto |
| 5 | Regra de parada | **Saturação teórica** (em vez de exaustividade) | Glaser & Strauss 1967, theoretical saturation; é a diferença formal entre screening e revisão sistemática |
| 6 | Profundidade de leitura por tipo | **Triagem em estágios** (título/resumo -> texto integral) | Kitchenham & Charters 2007, seleção em dois passos; PRISMA-ScR (Tricco et al. 2018), fluxo de triagem |
| 7 | Procedência (3 -> 2 -> 1) | **Confiabilidade da extração**: quem extraiu, quem validou | Kitchenham & Charters 2007, extração por mais de um revisor e verificação |
| 8 | Registro | **Formulário de extração de dados** | Kitchenham & Charters 2007, data extraction form; Petersen et al. 2008, data extraction |
| 9 | Saída do screening | **Síntese / mapa** | Petersen et al. 2008, o produto é um systematic map; Arksey & O'Malley 2005, estágios 4 e 5, charting e summarizing |
| 10 | Orçamento de tempo | **Protocolo: recursos e cronograma** | Kitchenham & Charters 2007, o protocolo inclui project timetable |

**Leitura da tabela:** nenhuma decisão é inventada. O método é um protocolo de revisão com os nomes
trocados para o vocabulário do processo de especialização (screening, Etapa 1, divisões,
fundamentos).

## 2. O que o método muda em relação ao padrão, e por quê

| Padrão (revisão sistemática / mapping) | Este método | Motivo |
|---|---|---|
| Cobertura exaustiva das bases | **Saturação** por divisão e por mapa (cap. 5) | Screening não é revisão sistemática; o objetivo é suportar o início da Etapa 1, não esgotar a literatura |
| String de busca fixa, registrada no protocolo | **Pool de termos versionado** (cap. 2.1); strings são composições | O vocabulário da área é o que eu ainda não tenho; uma string v0 congelaria a ignorância de partida |
| Esquema de classificação fechado antes da extração | **União com consolidação** (cap. 9): divisões vêm dos surveys, singulares ficam marcadas | Petersen já faz o esquema emergir; aqui isso é levado ao mapa inteiro, porque eu não conheço a área |
| Qualidade avaliada por checklist | **Filtro de qualidade de survey em três pernas** (cap. 3.2) | Surveys de arXiv sem revisão são comuns e às vezes bons; a citação cruzada resgata os recentes |
| Extração por dois revisores humanos | **Procedência 3 -> 2 -> 1** (cap. 7): agente extrai, Claude lê, eu leio | Um revisor só; o agente substitui o segundo revisor **só na extração**, nunca na interpretação |
| Produto: mapa + contagens | **Lista por divisão + mapa + confronto do pool** (caps. 9, 2.1) | O confronto antes/depois é o que torna o processo visível: critério do programa |

## 3. Decisões e uso de IA

O que eu decidi, e no que usei IA como ferramenta de apoio à decisão.

- **Eu:** todas as decisões, os critérios de revisão, as respostas à revisão, a reorientação do cap.
  2, o pool, os critérios de aceite.
- **Eu + IA:** a revisão de 21 achados, a profundidade por tipo de fonte (decisão 6), os defaults
  numéricos (caps. 3.2 e 4), a lista de fundamentos do cap. 1.1, as sementes de origem "claude" no
  pool, e a redação em prosa de algumas seções.
