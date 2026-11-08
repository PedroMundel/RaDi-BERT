# Frameworks para a fase de geração de racionalizações (e-SNLI, Claude em lote)

Data: 20/10/2026 · Agente: researcher · Pedido do Pedro: frameworks para *seguir* durante a geração, não só leitura de fundo.
Definição de framework usada (do Pedro, 30/09): estrutura flexível de diretrizes, práticas e ferramentas que serve de esqueleto a um projeto; vale nos dois sentidos (a: metodológico, b: software). Taxonomia só conta se disser quando usar cada ramo.

## Aviso de procedência (leia primeiro)

**Nada abaixo é citável pelo Pedro sem que ele leia a fonte.** Tudo é nível 3: o agente leu página, resumo ou trechos renderizados, nunca o artigo inteiro. Cada fonte leva a etiqueta de quanto foi lido. Onde a fala é do agente, vem marcada como **inferência do agente**. Venues foram conferidos no campo *Comments* do arXiv, na ACL Anthology ou no PyPI/GitHub, nunca em rodapé de PDF. Citações têm menos de 15 palavras.

**Checagem de Rejected (projeto):** nenhum candidato abaixo está em `## Rejected`. Não se recomenda trocar o professor por modelo de pesos abertos. Todos os frameworks de software foram avaliados só quanto ao suporte ao Claude.

---

## Parte A. Frameworks metodológicos

### A.0 Tabela (ONE-TABLE, adaptada: benchmark não se aplica a framework metodológico)

| # | Framework (verificado) | O que prescreve | Idade / venue | Esforço de leitura | Citável em métodos? | Marca |
|---|---|---|---|---|---|---|
| 1 | Long et al., *On LLMs-Driven Synthetic Data Generation, Curation, and Evaluation: A Survey* | Fluxo genérico **geração -> curadoria -> avaliação** com sub-decisões em cada etapa | Jun/2024; **Findings of ACL 2024**, pp. 11065-11082 (Anthology 2024.findings-acl.658) | ~18 págs. (pelas páginas da Anthology); só §3 (~5-6 págs.) é o esqueleto | Sim, como referência do fluxo e do vocabulário; é survey, não protocolo validado | **RECOMENDADO (esqueleto)** |
| 2 | Tan et al., *Large Language Models for Data Annotation and Synthesis: A Survey* | Taxonomia: gerar anotação (inclui **rationale**, §3.3) -> avaliar/filtrar (§4) -> usar (§5, inclui destilar modelo menor) | Fev/2024 (v3 dez/2024); **EMNLP 2024 Main** (2024.emnlp-main.54), pp. 930-957 | ~28 págs.; ler §3.3, §4, §5.1 (~8 págs.) | Sim, para situar a abordagem na literatura; sem checklist | Complementar |
| 3 | Liu et al., *Best Practices and Lessons Learned on Synthetic Data* | Panorama: usos (§2, inclui raciocínio), limites (§4: factualidade, fidelidade, viés), futuro (§5). Cita filtragem de racionalizações por resposta correta (STaR) | Abr/2024 (v2 ago/2024); **COLM 2024** (campo *Comments*) | Curto (HTML sem contagem de páginas; **não confirmado**); ~1 h | Sim, para riscos e limites; não prescreve passos | Complementar (lista de riscos) |
| 4 | Wiegreffe & Marasović, *Teach Me to Explain: A Review of Datasets for Explainable NLP* | Recomendações de coleta de explicações livres (§4-§7): documentar restrições em datasheet; piloto antes; coletar-e-editar; ensinar e testar a tarefa; pool grande de anotadores; várias explicações por instância | Fev/2021 (v4 dez/2021); **NeurIPS 2021 Datasets & Benchmarks** (v3: "NeurIPS 2021 accepted") | 10 págs. + 6 de apêndice (*Comments*); só §4-§7 (~3 págs.) | Sim, para justificar escolhas e riscos do e-SNLI. **Ressalva:** as recomendações são para coleta *humana*; a aplicação à geração por LLM é inferência do agente | Complementar (específico de explicações) |
| 5 | Anthropic, docs: *Define success criteria and build evaluations* (+ visão geral de prompt engineering) | Critérios **específicos, mensuráveis, atingíveis, relevantes**, várias dimensões; evals que espelham a distribuição real; automatizar; "volume sobre qualidade" | Doc viva, sem data fixa (consultado em 20/10/2026) | ~1 página; o mais barato | Sim como documentação técnica do fornecedor (citar URL e data de acesso); não é literatura revisada por pares | Complementar (operacional) |
| 6 | Gebru et al., *Datasheets for Datasets* | 7 seções de perguntas ao longo do ciclo do dataset: Motivation, Composition, Collection Process, Preprocessing/cleaning/labeling, Uses, Distribution, Maintenance | arXiv 2018 (v8 dez/2021); **Communications of the ACM, dez/2021** (campo *Comments*) | O corpo das perguntas ~6-8 págs.; preencher leva horas | Sim, é a referência padrão de documentação de dataset | Complementar (documentação) |
| 7 | **Achado extra.** Wiegreffe et al., *Reframing Human-AI Collaboration for Generating Free-Text Explanations* | Pipeline "gerar com LLM + filtro supervisionado treinado em julgamentos humanos de aceitável/inaceitável"; qualidade dos exemplos no prompt importa | Dez/2021; **NAACL 2022**, pp. 632-658 (2022.naacl-main.47) | 13 págs. + 14 de apêndice (*Comments*) | Sim. É o precedente mais próximo (explicações livres geradas por LLM em NLI/classificação). O uso de e-SNLI **não foi confirmado** na página lida | Complementar (precedente) |
| 8 | **Achado extra (métrica, não fluxo).** Hase et al., *Leakage-Adjusted Simulatability* | Métrica que desconta explicações que só revelam o rótulo; avaliada em e-SNLI e CoS-E | Out/2020; **Findings of EMNLP 2020** (*Comments*) | 17 págs. | Sim, só para a checagem de vazamento da rodada 0 | Complementar (opcional) |

**Recomendação (exatamente uma): Long et al. 2024 (#1) como esqueleto.** Motivo: é o único que cobre o ciclo completo gerar -> curar -> avaliar com decisões nomeadas, e é citável em métodos. Os demais entram como peças baratas (documentar, medir, justificar).

### A.1 O que cada fonte DIZ (fonte) e o que é inferência do agente

**#1 Long et al. 2024 (nível 3 — texto lido pelo agente em HTML arXiv v1, §3 e §4.4).**
- Fonte diz: geração (§3.1) = engenharia de prompt (especificação da tarefa, *conditional prompting* com pares condição-valor para forçar diversidade, exemplos in-context escolhidos por qualidade e diversidade) + geração em várias etapas; curadoria (§3.2) = filtragem por métricas heurísticas ou reponderação, e melhoria de rótulo (humana ou por modelo auxiliar); avaliação (§3.3) = direta (fidelidade/correção, diversidade por n-gramas e similaridade de cosseno) e indireta (treinar com os dados e medir em benchmark). Não traz checklist; o mais prático é §4.4 (colaboração humano-modelo).
- Inferência do agente: o fluxo é linear; o protocolo do Pedro intercala avaliação *antes* de gerar em escala (rodadas 0-2). Não é contradição, é refinamento: o framework não diz como reduzir risco de custo.
- Esforço de aplicar: baixo. É vocabulário e lista de decisões, não ferramenta.

**#2 Tan et al. 2024 (nível 3 — texto lido pelo agente em HTML arXiv v3, estrutura de seções; §3.3 e §5.1 só pelo sumário/trecho).**
- Fonte diz: §3.3 trata de "Rationale" como tipo de anotação; §4.1 avalia anotações (comparação humana, métricas por tarefa, LLM como juiz); §4.2 filtra (regras, fontes externas, LLM); §5.1 diz que muitos estudos ajustam modelos menores com racionalizações sintéticas. Distilling Step-by-Step **não** é descrito pelo nome nas partes lidas.
- Inferência: serve como mapa da literatura de "anotação por LLM" onde o trabalho do Pedro se encaixa; não prescreve ordem de passos.

**#3 Liu et al. 2024 (nível 3 — texto lido pelo agente, HTML arXiv, estrutura e exemplos).**
- Fonte diz: a seção de desafios discute factualidade, fidelidade à distribuição real e viés; os exemplos incluem filtrar racionalizações que levam à resposta correta. As recomendações próprias são gerais (testes rigorosos, benchmarks internos protegidos).
- Inferência: boa para a seção de "ameaças à validade" do Pedro; fraca como guia de passos.

**#4 Wiegreffe & Marasović 2021 (nível 3 — texto lido pelo agente em versão ar5iv, que pode diferir da v4; §4-§7).**
- Fonte diz (paráfrase curta): relatar com precisão como as explicações foram coletadas; documentar restrições em datasheet; fazer estudo-piloto antes da coleta; "Collect-and-Edit"; ensinar e testar a tarefa dos anotadores; usar pool grande de anotadores, pois pools pequenos geram artefatos (cita o e-SNLI, ~860 explicações por trabalhador); várias explicações por instância quando a tarefa é subjetiva.
- Inferência do agente: o problema do "pool pequeno" do e-SNLI humano vira, na geração por LLM, o problema de **modo único** (um só professor e um só prompt geram estilo uniforme). Isso sustenta medir diversidade na rodada 0/2 e declarar o limite. Não está escrito assim na fonte.

**#5 Anthropic docs (nível 3 — texto de doc lido pelo agente; a página *Define success criteria and build evaluations* foi lida só até o exemplo de privacidade, o restante truncado).**
- Fonte diz: critérios devem ser específicos, mensuráveis, atingíveis e relevantes; avaliar várias dimensões; evals devem espelhar a distribuição real, incluindo casos de borda; automatizar; "volume sobre qualidade" (mais itens com nota automática que poucos corrigidos à mão). Para avaliação por LLM, recomenda modelo diferente do que gerou.
- Inferência: bate com a rodada 0 (critérios + script). A recomendação "volume sobre qualidade" **complementa** (não contradiz) a avaliação cega de ~20 itens do Pedro: o automático dá cobertura, o manual calibra o automático.
- A URL de prompt engineering que foi pedida (`/docs/en/prompt-engineering/overview`) deu 404; a versão que a busca retorna é `/docs/en/build-with-claude/prompt-engineering/overview` (não aberta pelo agente, só vista no resultado de busca).

**#6 Datasheets (nível 3 — texto lido pelo agente em ar5iv).**
- Fonte diz: sete seções; o guia pede ler as perguntas de Composição, Coleta e Preprocessamento **antes** de começar e responder ao fim; Distribuição e Manutenção antes de distribuir; "não se pretende automatizar" o processo. O exemplo do paper ocupa 4 páginas.
- Inferência: rodada 0 já é o momento de abrir o datasheet com as seções 1-3 respondidas pelo que ele já decidiu (professor, licença, sem publicar dataset).

**#7 Wiegreffe et al. 2022 (nível 3 — só abstract/página).** Fonte diz que o pipeline combina GPT-3 com filtro supervisionado treinado em julgamentos binários de aceitabilidade e que o filtro "screens out" explicações que humanos rejeitam. Inferência: análogo ao seu "lote canário + checagem automática", mas com juiz humano treinado; custo de anotação humana que ele não tem. Útil como precedente a citar, não como procedimento.

**#8 Hase et al. 2020 (nível 3 — só abstract/página).** Já citada no seu doc de 19/10 "de memória"; agora o venue e o título estão **verificados** (Findings of EMNLP 2020; arXiv 2010.04119).

### A.2 Mapa para as 4 rodadas (resumo; passo a passo na Parte C)

| Rodada | Adiciona (framework) | Contradiz? |
|---|---|---|
| 0 Régua | Critérios SMART e multidimensionais (#5); avaliação direta de fidelidade e diversidade (#1 §3.3.1); vazamento (#8); abrir datasheet (#6) | Não |
| 1 Variantes | Prompt = tarefa + condições + exemplos (#1 §3.1.1); qualidade do exemplo importa (#7) | Não |
| 2 Confirmação | Eval com itens não vistos, espelhando a distribuição (#5); LLM-juiz com outro modelo (#2 §4.1, #5) | Não |
| 3 Rodada grande | Curadoria por filtro heurístico e reenvio das falhas (#1 §3.2); datasheet seções 4-7 (#6) | Não |

Lacuna comum a todos (inferência): nenhum cobre custo, lotes de API nem termos de uso. Isso fica com o doc de 19/10.

---

## Parte B. Frameworks de software

### B.0 Tabela única

Versões consultadas no PyPI/GitHub em 20/10/2026.

| Candidato (nome exato · versão) | O que faz | API Messages (Claude) | **Message Batches API (-50%) nativo** | Cache / retomada / idempotência | Saída estruturada | Windows · Py 3.11 | Licença | Maturidade | Custo de aprendizado |
|---|---|---|---|---|---|---|---|---|---|
| **Status quo: `gerar.py`** (anthropic 1.13.0; PyPI mostra 1.15.0 como última) | Script próprio, `custom_id = pairID`, reenvio só das falhas | Sim | **Sim** (SDK oficial; lote até 100.000 requisições ou 256 MB, resultados por 29 dias) | Idempotente por `pairID`; `cache_control` livre para o bloco de exemplos | O que o SDK oferece | Já roda | n/a | Já em uso, 1 pessoa | Zero |
| **`bespokelabs-curator` 0.1.30** (Bespoke Labs) | Biblioteca de geração sintética; classe `LLM` com `prompt`/`parse`; backends OpenAI, Anthropic, Gemini, Mistral, LiteLLM, vLLM | Sim (backend `anthropic` escolhido quando o nome do modelo contém `claude`) | **Sim, verificado no código:** `anthropic_batch_request_processor.py` chama `messages.batches` create/retrieve/results/cancel; liga com `batch=True`; `batch_size` padrão 10.000 | Cache em diretório de trabalho; retoma lotes interrompidos (há fixtures de teste `basic_batch_resume`); **`custom_id` = índice da linha**, não o `pairID` (mapear por coluna). Sem `cache_control` no código lido | Sim, via `instructor` (modo `ANTHROPIC_JSON`) | Py `>=3.10,<4.0` ok. **Windows não documentado**; issues #570 "Request: Windows compatibility" e #290 "No module named 'resource'" (só os títulos lidos; estado desconhecido). **Conflito de dependências:** `anthropic>=0.84.0,<0.85.0`, `litellm==1.83.7`, `pandas==2.2.2` fixos, contra o `anthropic` 1.13.0 do Pedro, então exige venv separado | Apache-2.0 | 1,7 mil estrelas; 0.1.30 em 13/10/2026; releases a cada ~1-3 meses; push em 13/10/2026; 79 issues abertas; versão 0.x | Médio (modelo mental de `LLM` e de cache; docs curtas) |
| **`distilabel` 1.5.3** (Argilla) | Framework de pipelines de dados com feedback de IA; passos, tarefas, `AnthropicLLM` | Sim (`AnthropicLLM`, via `messages.create`) | **Não, no código lido:** `anthropic.py` (branch `develop`) só tem `agenerate`; método de lote offline não implementado nesse arquivo. "Batch" no pacote = lotes internos do pipeline, não a API | Cache de pipeline próprio (não verificado a fundo); sem `cache_control` no arquivo | Sim, via `instructor` | Py `>=3.9`; Windows não verificado | Apache-2.0 | 3,4 mil estrelas; **última release no PyPI: 1.5.3 em 28/01/2025** (9 meses atrás); branch `develop` com push em 19/10/2026; README informa que os autores originais saíram e mantenedores comunitários preparam a próxima versão; 114 issues abertas | Alto (pipeline, steps, dependências pesadas) |
| **`datadreamer.dev` 0.46.0** (Patel, Raffel, Callison-Burch) | Biblioteca de fluxos de LLM reprodutíveis: geração, treino, alinhamento; cache e retomada "agressivos" | Sim (existe `src/llms/anthropic.py`, que herda de `LiteLLM`) | **Não:** a classe só delega a `_run_batch` do LiteLLM, lotes do lado do cliente; sem `messages.batches` | **Ponto forte:** cache e retomada nativos (README); sem `cache_control` verificado | Não verificado | Py `>=3.10,<3.14`; Windows não documentado | MIT | 1,1 mil estrelas; **última release 0.46.0 em 02/02/2025, último push 02/02/2025**; artigo **ACL 2024 (long, theme track)**, 2024.acl-long.208 (não é *demo*); 6 issues abertas | Médio |
| **EasyDistill** (Alibaba, repo `modelscope/easydistill`) | Kit de destilação de LLM (síntese de dados, SFT, DPO, RL) por arquivos de configuração | **Só via camada OpenAI-compatível:** backends documentados são `openai` (qualquer endpoint compatível), `pai_token`, `pai_eas`. Claude/Anthropic **não citados** | **Não** (nenhuma menção a lote) | Não verificado | Não verificado | Instala do código-fonte (`pip install -e .`); Windows não mencionado. **Cuidado:** `easydistill` no PyPI (0.0.1, 2020, TF 1.12) é **outro projeto** da PAI, não este | Apache-2.0 | 482 estrelas; sem release no GitHub (existe tag v1.0.0); push em 25/09/2026; artigo **EMNLP 2025 System Demonstrations** (2025.emnlp-demos.60; arXiv 2505.20888) | Médio-alto; foco em treino do aluno, o que o Pedro não precisa aqui |

**Recomendação (exatamente uma): manter o script próprio (status quo).** Curator é o único candidato que cumpre o critério decisivo (Batches API nativa), mas hoje não ganha do script: IDs por índice de linha, ausência de `cache_control` (o bloco de exemplos cacheável é parte da economia do plano), conflito de versão do SDK e Windows não documentado. Se o Pedro quiser aprender um framework (Etapa 2), Curator é o único tecnicamente compatível, num venv separado.

### B.1 O que cada fonte DIZ e o que é inferência

**Curator (nível 3 — doc/código lido pelo agente: README, docs de batch, `anthropic_batch_request_processor.py`, `base_request_processor.py`, metadados PyPI 0.1.30).**
- Fonte diz: "Currently batch APIs from OpenAI and Anthropic are supported." No código: limites 100.000 requisições / 256 MB por lote, até 100 operações concorrentes. A doc pede instalar `instructor==1.15.1` ao lado para o backend Anthropic. `max_tokens` vem de `litellm.get_max_tokens(modelo)`, não de parâmetro do usuário (no arquivo lido).
- Inferência do agente: (1) como `max_tokens` depende da tabela do LiteLLM fixado em 1.83.7, é **possível** que modelos recentes (Haiku/Sonnet 5.5) não estejam na tabela; testar antes de confiar. (2) O desconto de 50% é do lado da Anthropic; o código lido não aplica desconto, só calcula custo. (3) Sem `cache_control`, perde-se o desconto de leitura de cache do bloco de exemplos (ver seu doc §1.4). Nenhum dos três foi executado.
- Não verificado: comportamento real no Windows; se o pin `anthropic<0.85` conflita de fato na resolução com `anthropic==1.13.0` (o conflito é lido do metadado, não testado com `pip`).

**distilabel (nível 3 — doc/código lido: PyPI JSON, README GitHub, `anthropic.py`, `base.py`).**
- Fonte diz: `AnthropicLLM` aceita `structured_output` via `instructor`; `base.py` define `offline_batch_generate` como opcional, com `DistilabelNotImplementedError` por padrão e `use_offline_batch_generation=False`.
- Inferência: sem lote Anthropic, o ganho de 50% some. O sinal de manutenção é misto (release velha, branch ativo).

**DataDreamer (nível 3 — doc/código lido: PyPI JSON, README, `src/llms/anthropic.py`, resultados de busca da Anthology).**
- Fonte diz: "Aggressive caching and resumability built-in" (README); a classe Anthropic herda de LiteLLM.
- Inferência: bom para reprodutibilidade, mas parado desde fev/2025 e sem Batches API.
- Não verificado: `docs.datadreamer.dev` não resolveu (DNS); logo a doc oficial de provedores não foi lida.

**EasyDistill (nível 3 — doc lida: README, `docs/backends.md`, busca da Anthology).**
- Fonte diz: backends só OpenAI-compatíveis e PAI. Anthropic mantém uma camada de compatibilidade OpenAI que a própria Anthropic descreve como voltada a "test and compare", não produção; nela, `response_format` é ignorado e o cache de prompt não é suportado.
- Inferência: usar o Claude por essa camada perderia cache e Batches; improvável de ser útil aqui.

---

## Parte C. Como usar durante a geração

### C.1 Passo a passo por rodada (inferência do agente, a partir das fontes acima; decisões são do Pedro)

**Rodada 0 (régua, US$ 0).**
1. (#5) Escrever os critérios de aceite como específicos e mensuráveis, em várias dimensões: vazamento do rótulo, tamanho, cópia do par, falha de geração, contradição com o rótulo, hesitação. É a tabela da sua §1.3, reescrita como lista de critérios com limiar.
2. (#1 §3.3.1) Acrescentar uma checagem de **diversidade** (n-gramas repetidos, similaridade de cosseno entre justificativas) ao script de checagem; a §1.3 não tem nenhuma.
3. (#8, opcional) O teste "adivinhar o rótulo só pela justificativa" é a ideia de simulatability; já tem venue verificado.
4. (#6) Abrir o datasheet e responder Motivação e Composição agora.

**Rodada 1 (variantes A-D, ~300 pares).**
5. (#1 §3.1.1) Ler as variantes como as três peças do prompt: especificação da tarefa (A/B), exemplos (C), restrição de formato (D). *Conditional prompting* (pares condição-valor) seria um eixo novo a considerar; **não** está nas variantes A-D.
6. (#5) A amostra estratificada com neutros e rótulo disputado já cumpre "espelhar a distribuição, incluindo bordas".
7. (#5) Se usar o Haiku como juiz automático, recomenda-se modelo diferente do gerador.

**Rodada 2 (1.000 pares novos).**
8. (#5, #1) É o conjunto de teste do prompt: mesmos critérios, itens nunca vistos. Registrar o hash do prompt.
9. (#4) Anotar quantos estilos distintos aparecem; o "modo único" é a versão-LLM do artefato de pool pequeno que o paper aponta no e-SNLI.

**Rodada 3 (canário de 5 mil e o resto).**
10. (#1 §3.2) Curadoria = filtro heurístico com os critérios da rodada 0; reenviar só as falhas já é o que `gerar.py` faz. Descartar e reenviar, não consertar à mão.
11. (#6) Responder Coleta, Preprocessamento/rotulagem, Usos, Distribuição e Manutenção do datasheet. Distribuição depende da decisão já tomada de não publicar pesos nem dataset.
12. Avaliação **indireta** (#1 §3.3.2: treinar o aluno e medir) acontece depois da geração; é o experimento principal do projeto, não parte desta fase.
13. Lembrar do lote máximo de 100.000 requisições / 256 MB: 280 mil pares exigem pelo menos 3 lotes (doc oficial de batch).

### C.2 Vale adotar framework de software nesta escala?

Inferência do agente: **provavelmente não**. A tarefa é uma execução única de 100-280 mil requisições curtas, uma pessoa, com o script já idempotente por `pairID` e cache de prefixo planejado. Os recursos que um framework daria (lotes, retomada, estatísticas) já existem no script ou na API. O único que cumpre Batches nativa (Curator) troca o `custom_id` por índice, não usa `cache_control` e exige venv separado por causa do pin do SDK. O framework metodológico (#1 como esqueleto, #5 e #6 como peças) acrescenta mais do que o de software, e custa leitura, não código.

Ângulo da Residência (neutro): a Etapa 2 do programa é justamente aprender frameworks de apoio, então aprender um tem valor de processo. Se ele quiser, o experimento mais barato é rodar o Curator só na rodada 1 (~300 pares, centavos) num venv separado, como estudo, sem tocar o `gerar.py` da rodada grande. Isso é uma opção dele, não uma recomendação para a geração. Observação do histórico do projeto: a regra 11 da skill `termogate` (descrever o achado, não o rigor do método) vale para o termo; a seção de métodos pode citar os frameworks.

---

## Becos sem saída e não verificados

- `docs.datadreamer.dev` não resolveu; doc oficial de provedores do DataDreamer não lida.
- Busca de código na API do GitHub exigiu autenticação (401); usei árvores de arquivos e leitura direta de `raw.githubusercontent.com`.
- Os PDFs do arXiv vieram como bytes ilegíveis; usei as versões HTML/ar5iv. A versão ar5iv do Wiegreffe & Marasović pode ser anterior à v4.
- Páginas de Liu et al. e Long et al.: contagem de páginas de Liu **não confirmada**; Long inferida pelas páginas da Anthology (11065-11082).
- Wiegreffe et al. 2022 usar e-SNLI: **confirmado pelo Claude no PDF** (Tab. 4, p. 4, com uma linha "e-SNLI"; ver `docs/2026-10-19-pesquisa-prompt-racionalizacao.md`).
- Curator no Windows e a resolução real do pin `anthropic<0.85` com `anthropic==1.13.0`: **não testados** (nada foi instalado).
- Cache/idempotência do distilabel e saída estruturada do DataDreamer: **não verificados**.
- Estados das issues #570 e #290 do Curator: só os títulos foram vistos.
- A página de limites de lote da Anthropic foi lida via ferramenta de busca de página inteira (arquivo salvo localmente); a tabela de preços na página mostra valores do Haiku 5.5 que não foram usados aqui.

## Fontes

Todas nível 3 (lidas pelo agente; extensão indicada acima).

- Long et al. 2024: https://arxiv.org/abs/2406.15126 · HTML https://arxiv.org/html/2406.15126v1 · Anthology https://preview.aclanthology.org/add_acl24_videos/2024.findings-acl.658
- Tan et al. 2024: https://arxiv.org/abs/2402.13446 · HTML https://arxiv.org/html/2402.13446v3 · https://preview.aclanthology.org/setup/2024.emnlp-main.54
- Liu et al. 2024: https://arxiv.org/abs/2404.07503 · HTML https://arxiv.org/html/2404.07503
- Wiegreffe & Marasović 2021: https://arxiv.org/abs/2102.12060 · https://ar5iv.labs.arxiv.org/html/2102.12060 · https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/698d51a19d8a121ce581499d7b701668-Abstract-round1.html
- Wiegreffe et al. 2022: https://arxiv.org/abs/2112.08674 · https://aclanthology.org/2022.naacl-main.47
- Hase et al. 2020: https://arxiv.org/abs/2010.04119
- Gebru et al.: https://arxiv.org/abs/1803.09010 · https://ar5iv.labs.arxiv.org/html/1803.09010
- Anthropic, success criteria e evals: https://platform.claude.com/docs/en/test-and-evaluate/define-success
- Anthropic, prompt engineering (resultado de busca, não aberto): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- Anthropic, Message Batches: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- Anthropic, compatibilidade OpenAI: https://platform.claude.com/docs/en/api/openai-sdk
- anthropic no PyPI: https://pypi.org/pypi/anthropic/json
- Curator: https://pypi.org/pypi/bespokelabs-curator/json · https://github.com/bespokelabsai/curator · https://docs.bespokelabs.ai/bespoke-curator/how-to-guides/batch-processing · https://raw.githubusercontent.com/bespokelabsai/curator/main/src/bespokelabs/curator/request_processor/batch/anthropic_batch_request_processor.py
- distilabel: https://pypi.org/pypi/distilabel/json · https://github.com/argilla-io/distilabel · https://raw.githubusercontent.com/argilla-io/distilabel/develop/src/distilabel/models/llms/anthropic.py
- DataDreamer: https://pypi.org/pypi/datadreamer.dev/json · https://github.com/datadreamer-dev/DataDreamer · https://raw.githubusercontent.com/datadreamer-dev/DataDreamer/main/src/llms/anthropic.py · https://aclanthology.org/2024.acl-long.208
- EasyDistill: https://github.com/modelscope/easydistill · https://raw.githubusercontent.com/modelscope/easydistill/main/docs/backends.md · https://arxiv.org/abs/2505.20888 · https://pypi.org/pypi/easydistill/json (projeto diferente, homônimo)
