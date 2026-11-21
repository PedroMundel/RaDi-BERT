# Residência em IA — UFG 2026/2

Atividades do processo da Residência em Bacharelado em Inteligência Artificial.
Atividade atual (10/09): **TEMA v3 em formulação** — injeção de racionalização de LLM em modelos encoder-only, que não geram texto. Nasceu do Pedro lendo o Distilling Step-by-Step. Hipótese viva: **H2, cabeça decodificadora auxiliar descartada na inferência** (mecanismo validado pelo DHRD sobre decoder-only; lacuna arquitetural sobre encoder). H1 (regressão para embedding da racionalização) foi verificada e está **ocupada** (LRKD, WWW'26). Estado, hipóteses, ponte teórica e pendências em `docs/pesquisa/tema-v3-racionalizacao-encoder.md`. Prazo de execução: 3–4 meses. Hardware: RTX 5060 8GB. **Orçamento (13/10): US$ 100 de crédito de API da Anthropic + US$ 250 de sessões na nuvem do Claude Code** (gerar racionalização do treino inteiro do e-SNLI com Haiku 5.5 em lote ≈ US$ 10; ver `docs/2026-10-13-custo-racionalizacao-llm.md`). **Nuvem (Pedro, 20/10):** roda sessões com agentes (nuvem do Claude + app do GitHub). Uma tarefa de ~17M tokens custou ~US$ 65 (~US$ 3,8/M), sobram ~US$ 185. Serve para trabalho de agente, **não para gerar o dataset**: sai mais caro que o lote da API, não fixa modelo e prompt por item, e pode cair nos Consumer Terms (§3: proíbe treinar "any" modelo de IA; o plano dos créditos está a verificar).

**Tarefa e dataset DECIDIDOS (Pedro, 13/10): NLI de 3 classes no e-SNLI**, cross-encoder com cabeça de classificação; professor = Claude, sem publicar pesos nem dataset (14/10). Semana 6 entregue (14/10). **Semana 7 (19/10) = gerar o dataset:** protocolo de 4 rodadas contra prompt ruim (< US$ 5 arriscados antes da rodada grande) e precedentes de licença (Tülu 3 usou Claude 3.5 Sonnet; sanções conhecidas da Anthropic = corte de acesso, nenhum processo) em `docs/2026-10-19-geracao-dataset-prompt-e-licenca.md`. Decisões de variantes, nº de pares e professor: do Pedro. **⚠️ 20/10: a Usage Policy (incorporada pelo §D.2) proíbe treinar *qualquer* modelo de IA com as saídas sem autorização prévia, e não só concorrente.** O argumento do §D.4 não cobre isso. Ver a correção no §2.1 do doc de licença. **20/10 (Pedro): Claude como gerador ARQUIVADO por ora.** Duas frentes: (1) piloto de 45 pares com `Qwen/Qwen3.5-9B` local (GGUF Q4_K_M via `llama-server`), script em `src/radibert/piloto_qwen.py`, mesmos pares e prompt do piloto do Claude; **rodado em 20/10 com as variantes A/B/D** (relatório `resultados/piloto-qwen/relatorio.md`: tirar as definições não tira o molde; "uma frase, o fato que decide" (D) dá ~16 palavras sem frase vazia; ~1 s/par na 5060; espera a leitura do Pedro); **25/10: gate 7 sem feedback; E não é final para o Pedro → variante F (pergunta "por quê", sem rótulo nem "premise/hypothesis") rodou, seção F do relatório; 26/10: FR (pergunta reescrita pelo Qwen) rodou, inverteu 1 rótulo em 45 (#126); FRG (FR + guarda de molde por regex) corrige; FR × FRG mostrou que o llama-server NÃO reproduz entre rodadas (34/44 respostas mudam com prompt igual): só diferença maior que ~6 casos em 45 é sinal; F e FRG no Qwen3.6-35B-A3B (26/10): corrige #948 e #9, os erros fixos do 9B, a ~4–5× o tempo; 26/10: `--n-cpu-moe 27` leva o 35B a 2,0 s/par na F; em 90 pares (`amostra-90.csv`) a F do 35B errou ~3–4 × ~10 da F do 9B (leitura do Claude), a reescrita perde o detalhe que decide (guarda não vê) e a F do 9B reproduziu 45/45 num servidor novo (o ruído é da FR/FRG); 27/10: com pedidos simultâneos (`QWEN_WORKERS`), F no 9B a 0,28 s/par (8 pedidos, `-ub 128 -cms 0`) e no 35B a 1,66 s/par (4 pedidos, `--n-cpu-moe 30`: o 27 estoura a VRAM quando outros apps seguram GPU); configuração congelada reproduz, mudar lote muda o texto mas não a superfície; 27/10 (Pedro): 35B + F decididos; primeiro lote no TREINO do e-SNLI (baixado com OK dele em 27/10; antes só o dev estava no disco) terminado às 6h24: 16.000 pares, 1,20 s/par, sem queda, todos com `stop`; ninguém leu os textos ainda, ordem aleatória com semente 42; 28/10: eco marcado (`marcar_eco.py` -> `marcas.csv`, 1.252 pares, 7,8%; regra reproduz o dev), discordância não marcada (PC instável); 29/10: avaliação humana cega pela rubrica de Wiegreffe et al. 2022 (30 Qwen + 20 GPT-3 já julgados pelos avaliadores do paper; `montar_leitura_cega.py`, gabarito `leitura-50-gabarito.csv`) em Google Forms (`criar_formulario.gs`), respondida pelo Pedro e amigos, sem resultado ainda; termo `docs/residencia/termo-de-entrega-Semana-8.md` rascunhado (29/10) — `resultados/lote-35B/` (`lote.py`, `rodar.sh`, saída `racionalizacoes-F-35B.csv`)**; candidatos abertos em `docs/2026-10-20-professores-abertos.md` (nível 3); (2) estudar as perdas: `docs/2026-10-20-perdas-o-que-e-I-gradiente.md` (I, ∇θ L, ΔL; checagem "nomeia o rótulo" trocada por I(R;X|Y) por braço + cosseno g_c·g_a no treino).

**Entregas:** `docs/residencia/termo-de-entrega-Semana-1.md` **já foi entregue** e **o gate da Semana 1 já passou**
(declarado 15/09) — não editar o termo; `docs/residencia/preparacao-arguicao-gate.md` está encerrado (só registro).
`docs/residencia/termo-de-entrega-Semana-2.md` (19/09) é a versão final escrita pelo Pedro para o gate 2 (3 docs de
`entrega/` linkados) — **gate 2 passou (declarado 19/09), sem feedback, sem apresentação**; termo
fechado, não editar. **Semana 3 (23/09):** rascunho em `docs/residencia/termo-de-entrega-Semana-3.md` (pedido dele), links `entrega/Arvore de Citacao.docx` e `entrega/Desenho da Leitura por Agentes.docx`; roteiro de fala em `docs/residencia/apresentacao-gate-3.md` (gate = termo no projetor, sem slides; entregável sempre .docx). **F1 da camada C executada** (árvore de citação S2 + OpenAlex): relatório `docs/screening/fase1/2026-09-23-camadaC-F1-relatorio.md`, coluna `camada_C_F1`, página em `docs/screening/fase1/figs/arvore-citacao-F1.html`. **24/09:** decisões da F1 dadas (desceram: só as 1.214 com palavra de tipo vão à F2; sem dado de citação vai; 50–99 = 30%); **lista de leitura de destilação** (17 obras, nível 3) por funil sobre a árvore externa (referências), a pedido do Pedro, para ler já — `docs/screening/fase1/2026-09-24-kd-lista-leitura.md`; outras divisões esperam o mapa v1 (forma em T). Scripts em `scripts/screening/`. **26–27/09: calibração dos agentes (M4) passou** (`docs/screening/fase1/2026-09-26-calibracao-agentes-relatorio.md`) e **F2 executada** (962 obras, cadeia Haiku->Haiku->Sonnet; relatório `docs/screening/fase1/2026-09-27-F2-relatorio.md`, checkpoint `docs/screening/fase1/F2/ESTADO.md`): 55 relevante · 157 dúvida (quase toda regra (c)); **só 1 grupo desceu, ~11,5 mil seguem, ~1.400 relevantes estimadas** — **erro de desenho da F2** (grupo = área; ver Rejected). **Plano novo, nada rodou:** `docs/screening/fase1/2026-09-27-plano-classificador.md` — classificador SPECTER2 + regressão logística sobre os 797 vereditos, contrato de funil, e a etapa C3 (de ~1.100 relevantes para ~50) **ainda não existe**; decisões D1–D5 do Pedro. **Riscos medidos (27/09):** `docs/screening/fase1/C1-diagnostico/2026-09-27-riscos-classificador.md` — classificador bate todas as linhas de base (72% das relevantes em 25% da lista × 28% ao acaso) mas K95 = 67%, não 25%; causa: 55 positivos (n efetivo 20), gabarito 21/28 no grupo 2, **hardware só 56% e ferramentas 0** — proposta: critério por cobertura de subárea + aprendizado ativo em rodadas de ~200; decisões R-D1–R-D5. Vetores copiados para `docs/screening/fase1/emb/`. **Critérios de relevância (27/09):** `docs/criterios-de-relevancia.md` (literatura + dois níveis: A tópico, B situacional por perguntas P1–P4b, V, A, R; P6 e acréscimo fora da triagem; P5 nas notas) e **método de baixo para cima** `docs/screening/fase1/2026-09-27-metodo-bottom-up.md` — camada 1 (critérios) em correção pelo Pedro: D-1, D-A (atualidade), D-N. Tabela-mestra NÃO tocada pela F2. **27/09 — MUDANÇA DE RUMO (Pedro): sem tempo para bottom-up; lista de alta qualidade rápida.** Surveys viram **júri** (91 com referências + reserva de hardware só para hardware, 'hardware é bem importante'); co-citação -> **lista v2 com 56 obras** em 4 blocos (13 mapas · 31 fundadores · 7 conceitos · 5 sistemas; 11 divisões pelo título; 18 ajustes do Claude declarados): `docs/screening/fase1/2026-09-27-lista-rapida-v2.md` + `lista-rapida/lista-v2.csv`. **Fichas de leitura por agentes (27/09):** 56 fichas (Sonnet, texto completo em 53, só abstract em Deng 2020 e LSTM) -> `docs/screening/fase1/2026-09-27-lista-v2-fichas.md` (síntese §0: 55 manter; redundância real só entre mapas 02/04/05; P3 história contada fraca; 4 introdutórias para começar). **Espera a revisão do Pedro** (§6 do relatório da lista). Pausados: F2, classificador como triagem, método por camadas. **Semana 4 (01/10):** rascunho `docs/residencia/termo-de-entrega-Semana-4.md` (formato 'fiz isso por esse motivo', regra nova da skill) + entregáveis `entrega/Selecao das Obras.docx` e `entrega/Metodo de Leitura.docx` (fontes .md ao lado); escolhas abertas no fim do termo. Termos seguintes saem da skill do projeto `/termogate` (`.claude/skills/termogate/`),
que codifica o tom dele a partir da reescrita que fez do rascunho. A `docs/residencia/proposta-de-tema.md` (rev. 2, 15/09)
é o documento vivo do tema, com a especialização na abertura.

**MODO DE TRABALHO (Pedro, 08/11):** 2 semanas de atraso; o PC (RTX 5060) perdeu o slot NVMe e roda com outro SSD
(SATA); o SSD do projeto está no notebook (`WKST-001`, GTX 1650). (1) **IA liberada para acelerar**: o veto do gate 4
abaixo não guia mais o trabalho (continua: não disfarçar LLM nas entregas). (2) **Notebook = contexto e exploração;
PC = tudo que precisa de GPU.** (3) **Tudo compartilhável entre as duas máquinas** (GitHub, HF Hub, Drive).
**Repo (08/11): `PedroMundel/RaDi-BERT`, privado, branch `main`.** Fora do git: `dados/esnli/` (baixar pela
`dados/README.md`), `amostra-treino.csv` (regenera com `lote.py amostra`), `docs/screening/fase1/raw|emb`, GGUF e
checkpoints (HF Hub privado). Ponte entre as máquinas (09/11): **`ssh pc`** (LAN,
`192.168.1.14` por DHCP) ou **`ssh pc-h`** (Hamachi, `25.11.204.231` fixo, fora de casa), do notebook, chave
`~/.ssh/radibert_pc` sem senha; PC `DESKTOP-2VBC5EC`, shell remoto = PowerShell 5.1 (script bash: `ssh pc '& "C:\Program
Files\Git\bin\bash.exe" -s' <<EOF`; `ssh` dentro dele com `</dev/null`). **Repo no PC: `D:\RaDi-BERT`** (SSD SATA 1 TB),
GitHub por deploy key read-write só deste repo (`~/.ssh/github_radibert` no PC); uv sync, ganchos, e-SNLI (md5 igual
ao notebook), 46 testes e I1–I5 ok. llama.cpp b11770 e o GGUF do 35B (SHA-256 igual
ao notebook) em `D:\tools`, `config/maquina.env` apontando para lá; llama-server testado na 5060 (09/11: ~30 tok/s
num pedido, 7,1 GB de VRAM). O 9B não foi copiado.

**REPLICAÇÃO DO AGRAWAL NO RTE (Pedro, 09/11):** RTE primeiro, e-SNLI depois. Decisões D0–D6 (professor Qwen 35B,
prompt, aquecimento cópia + proporcional, leitura literal das fases, métricas, 5–10 sementes, teste na CPU) em
`docs/2026-11-09-treino-agrawal-rte-explicado.md`. **O Pedro quer entender o código do treino antes de ele ser
escrito.** Justificativas do RTE geradas com a variante **FA** (FP3 + 20 exemplos de RTE) em
`resultados/rte-35B/racionalizacoes-FA.csv` (2.470 pares); a limpeza C (`clean_opening`) entra na montagem do dado.
Lote no PC pelo túnel SSH (`ssh -L 8080:127.0.0.1:8080 pc`) porque o código só estava no notebook; o `llama-server`
**sobrevive à queda da sessão SSH** e precisa de `Stop-Process -Name llama-server` no PC.
**NOITE DE 10/11 (modo autônomo, `AUTONOMIA.md`; estado no `HANDOFF.md`; código sem commit, PC igual por scp):
três nulos medidos** — RTE BERT cru 0,736 × decoder −0,028 (`resultados/rte-treino/leitura-grade.md`); T5 v1.1 como
encoder 0,636, com decoder 0,522 por desequilíbrio de gradiente (`resultados/rte-t5enc/`); e-SNLI 4 mil pares −0,007
(`resultados/esnli-treino/`). **Professor (via Pedro, 10/11): "sem conseguir repetir, nem seu nulo eu considero"** —
falta controle positivo; próximo = repetir a condição do Agrawal (BERT base MS-MARCO no RTE, cópia da Tabela 4),
checkpoint a escolher pelo Pedro (`nboost/pt-bert-base-uncased-msmarco` × `Capreolus/bert-base-msmarco`). Gate na
quarta 11/11. **DIA 10/11 (código sem commit, PC igual por scp; hipóteses e checagens em
`docs/2026-11-10-hipoteses-do-nulo.md`):** (1) **MS-MARCO (nboost, escolha do Pedro) NÃO reproduziu o Agrawal:**
baseline 0,767 (paper 0,4754), decoder −0,049 fora do ruído, sem treino 0,58–0,62
(`resultados/rte-msmarco/leitura-grade.md`); Capreolus não rodado. (2) **Não é erro de código, até onde se checou:**
equivalência I17 (decoder com peso 0 = BERT cru), corte de gradiente (<1% na fase C) e **controle de calendário**
(`bert_calendar` 0,746 ≈ BERT cru: a hipótese "menos treino" do Claude caiu; a queda vem da L_aux).
(3) **Marcas na atenção do [CLS]** (ideia do Pedro; `src/radibert/rte_marcas.py`, `--encoder marcas`, sem decoder):
marca real (palavras que a justificativa copia) **+0,055 sobre marca aleatória, 5/5, fora do ruído**, mas +0,006
sobre o BERT sem marcas (nulo); com 500 e 1.000 pares (`--pares`, teste também nos 1.470 pares de treino não usados,
ideia do Pedro) não há ganho (`resultados/rte-marcas/leitura-grade.md`). (4) Pesquisa nível 3 sobre combinar os
sinais: `docs/pesquisa/2026-11-10-combinar-sinais-racionalizacao-encoder.md` (sem ganho consistente dentro da
distribuição na literatura). Fila do Pedro: B (pares de contraste pelo Qwen) e A (rótulo por token), adiadas;
ledger `docs/claude/ledger/2026-11-10-fila-marcas-B-A.md`. Código do treino
(09/11; 116 testes, auditado 2×, lote em 2×16 por causa da VRAM): `docs/2026-11-09-codigo-treino-rte.md` (4 módulos,
`RationaleBert` com `encoder_outputs` do T5, fases A 39 / B 1–187 / C 188–624, invariantes I1–I14; **E1–E8 aceitas
pelo Pedro na recomendação**; **medida de gradiente em três grupos de tokens (S rótulo · C copiada do par · N nova, Pedro 09/11) + cosseno
g_c·g_a a cada 25 passos; F (gramaticais) virou 4º grupo, Pedro 09/11** e **influência por palavra no encoder** (`measure_words`: perda no decoder, ‖g‖ nos pesos do
BERT e alinhamento com g_c, por ocorrência, em 3 pontos e 1 semente por aquecimento; pedido do Pedro), com esboço de
código aprovado e escrito; no RTE "not/never/no" está em 90% das justificativas de not_entailment
e em 4% das de entailment. **Wadhwa 2024 conferido (09/11): o método deles é Integrated Gradients rótulo ← token da
justificativa, que não transfere para encoder; a medida aqui é outra e não se cita como "do Wadhwa"**). **Lote FA lido pelo Claude, veredito "serve para treinar"**:
`resultados/rte-35B/analise-lote-FA.md` (30/30 defendem o rótulo, 2/30 com fato trocado, ~1% discorda do gabarito;
**a limpeza C quebra ≥ 96 frases**, corrigir antes de montar o dado).

**NOITE DE 10/11 (2) — encoders pequenos (ideia do Pedro; código sem commit, PC igual por scp; leitura única em
`resultados/rte-pequenos/leitura-grade.md`):** BERT small (`google/bert_uncased_L-4_H-512_A-8`) e tiny. (1) **Decoder
nulo** nos dois (small −0,004). (2) **Marcas: o +0,017 de 5 sementes era falso positivo** (sementes 6–15: +0,002);
o mesmo treino na GPU difere em até 0,026 entre rodadas. (3) **Teste fora da distribuição** (dev do e-SNLI, 15
sementes, regra de parada escrita antes em `docs/2026-11-10-plano-teste-fora-da-distribuicao.md`): −0,004, intervalo
cruza o zero → **hipótese das marcas para ganho de nota ENCERRADA**. (4) **Medida de atenção:** sem marcas o `[CLS]`
põe 0,285 da atenção nas palavras marcadas, com marca real 0,805 em pares nunca treinados, e a nota não muda. (5)
**Destaque (único positivo, critério escrito antes):** as palavras de maior atenção coincidem com as que o LLM copia
com AP 0,724 contra 0,555 da melhor regra sem treino; com 2.000 pares, AP 0,731 e classificação empatada. Exemplos
em `resultados/rte-pequenos/destaque-exemplos.html` (não lidos pelo Pedro). Cabeça por token treinada direto nas marcas: AP 0,748, só +0,017 sobre a
atenção (critério: 0,05). Lacuna: utilidade para pessoa não testada. Ideias de tarefa para depois do gate
(reranqueador, pronunciamento, outros usos) em `docs/ideias-de-desenho.md`. Tiny fica no piso e não informa. **10/11: um professor de fora da
Residência chamou o tema de "péssimo" para final de curso, sem dar o motivo; a exigência de resultado positivo para a
nota é leitura do Pedro, a conferir com o coordenador.**

**SEMANA 9 EM DOCUMENTOS (11/11) E SEMANA 10:** rascunho `docs/residencia/termo-de-entrega-Semana-9.md` (7 itens; o
primeiro, a pedido do Pedro, declara a placa-mãe queimada, as rodadas por SSH no computador de um amigo e o "auxílio
pesado de LLM") e seis `.docx` novos em `entrega/`, cada um com o `.md` fonte: `O que Mudou em Relacao ao Agrawal`,
`Criterios Escritos Antes dos Testes`, `Exemplos do Destaque`, `Marcas de Atencao e Destaque`, `Replicacao do Agrawal
no RTE` e `Manual do Treino` (este fora da tabela do termo). **O Pedro faltou ao gate de 11/11 por doença: não houve
feedback. Agora é a Semana 10, a última.** O termo da Semana 9 foi entregue (Pedro, 12/11); o `.docx` entregue ainda
não está em `entrega/termos-entregues/`. Rumo da Semana 10 não decidido. Conversão para `.docx`: `md2docx_plain.py` com
`uv run --frozen --with pillow`. Estado no `HANDOFF.md`.

**12 A 15/11 — SEM EXPERIMENTO NOVO; RUMO DA SEMANA 10 AINDA NÃO DECIDIDO.** Três pesquisas de viabilidade por
agente, **nível 3, números não conferidos na fonte**, em `docs/pesquisa/2026-11-15-*.md`: (1) filtro de evidência na
frente de um LLM: possível com cortes, risco alto de empatar com busca por palavras, ideia já existente (Provence
2025 e outros); (2) limpeza de rótulos por discordância: não realista para mostrar ganho; (3) atenção e decisão:
**em tarefas de par, mexer na atenção muda a decisão**; Stacey et al. (2022) supervisionam o `[CLS]` da última camada
de um BERT em NLI com destaque humano e relatam ganho pequeno (+0,4 dentro, +0,8 a +1,6 fora), invisível no RTE com
o nosso ruído. Arquivadas pelo Pedro em `docs/ideias-de-desenho.md`: o filtro de evidência e "o small aponta, o maior
lê só o apontado". **Pedro (15/11): "não sei o que fazer, e não quero uma sugestão sua de novo"; "você precisaria
confirmar 10 informações pra poder afirmar algo com certeza, e afirma depois de confirmar 2".** Daí a memória
`afirmar-so-o-conferido` e a skill global `assertion-check`. **Não propor rumo; rodar `assertion-check` antes de
qualquer conclusão.** **Dia final: quinta 19/11. Decisão do Pedro (16/11): medir "o modelo decide pelo motivo certo?"
(apagar e manter as palavras que a justificativa aponta, com palavras sorteadas como controle), "só por medir";
desenho no `HANDOFF.md`, nada escrito nem rodado ainda.**

**16/11 — SEIS EXPERIMENTOS NO BERT SMALL (critérios em `docs/2026-11-10-plano-teste-fora-da-distribuicao.md`,
seções 10 e 11; leitura em `resultados/rte-pequenos/leitura-grade.md`; código sem commit, PC igual por scp):**
(1) tapar a atenção do `[CLS]` por camada sem treinar: a decisão depende dela nas camadas 3 e 4, não nas 1 e 2;
(2) marca cobrada em outras camadas (11 combinações), RTE: **nulo**; (3) o mesmo no e-SNLI: nulo, small 73,9% contra
79,7% do base; (4) destilar a atenção do BERT base no small (ideia do Pedro): **nulo**; (5) com professor que não viu
os pares do aluno, **imitar as respostas dá +1,6 ponto (passa no critério; primeiro positivo do projeto)** e a
atenção segue nula; (6) temperatura e professor com mais dados não sobem o ganho; controles mostram que ele vem do
que o professor diz sobre cada par. **É destilação padrão (Hinton 2015), sem LLM nem justificativa** (o Pedro
perguntou e foi dito). MiniLM e TinyBERT só por resumo de página (nível 3). **Próximo (Pedro): rodar os 3 jeitos de
juntar atenção com as respostas** (em sequência; atenção mais conteúdo; atenção como guia), ainda sem desenho.
Tabelas para o Pedro sempre com legenda (memória `tabela-com-legenda`). Estado no `HANDOFF.md`.

**17/11 — JUNTAR O INTERIOR DO PROFESSOR COM AS RESPOSTAS (plano, seção 11.5; leitura em
`resultados/rte-pequenos/leitura-grade.md`, linha 561; ledger `docs/claude/ledger/2026-11-16-juntar-atencao-e-respostas.md`;
código sem commit, PC igual por scp):** MiniLM (Wang et al., 2020) e TinyBERT (Jiao et al., 2020) **lidos pelo Claude,
nível 2** (`docs/artigos/notas-minilm-wang-2020.md`, `notas-tinybert-jiao-2020.md`; o Pedro não leu). Decisões do
Pedro: sem jeito 3; os dois pacotes; média das cabeças; fase 1 "como no TinyBERT"; perda de atenção "dos dois
jeitos". 14 braços x 5 sementes (`medir_juntar.py`, `juntar-esnli-4000.csv`). **Só a sequência (20 épocas imitando
embeddings, atenção e estados internos do professor, depois classificação + respostas) passa: com 15 sementes, +0,93
ponto sobre "respostas" no conjunto de escolha (intervalo de 95% +0,70 a +1,17, acima nas 15) e +0,45 no dev (+0,25
a +0,65).** O controle (fase 1 com BERT base sem tarefa) não ganha; juntar tudo num treino só não ajudou. **Achado
de auditoria:** a atenção que o BERT devolve em treino já passou pelo dropout, e `attention_kl` e `mark_loss` usam
essa desde 10/11; rodado dos dois jeitos, nenhuma diferença chega a 0,5 ponto neste desenho (os nulos de 16/11 não
foram rodados de novo). Continua sendo destilação entre BERTs, sem LLM nem justificativa. Brute-test em
`docs/claude/brute-test-juntar.md`. **Tarde de 17/11, hipótese do Pedro: levar as palavras novas da justificativa
(grupo N) ao `[CLS]`** (plano, seções 11.6 a 11.8; nada treinado): só com elas uma regressão acerta 76,4% do rótulo
(acaso 33,5%; palavras do par 46,6%); UMAP + HDBSCAN (ideia dele) dá 1 grupo de argumentar e 28 de assunto, e sem o
de argumentar ainda são 70,4%; a etapa 1 da 11.8 passa na regra de parada (os grupos dependem do par além do
rótulo), mas quase tudo é o assunto do par. **Etapa 2 rodada em 17–18/11 (plano 11.8; cinco seções novas no fim de
`leitura-grade.md`; ledger `docs/claude/ledger/2026-11-17-etapa2-grupos-cls.md`): NULO pelo critério escrito antes.**
Alvo restrito de sete grupos, recorte de 1.249 pares do conjunto de escolha, baseline de 15 sementes (respostas do
professor +2,34 no recorte), 8 braços com a cabeça: nenhum passa de 0,64 ponto. A cabeça treina, mas uma sonda linear
dá 0,765 no BERT pré-treinado e 0,760 no aluno com a cabeça: **o `[CLS]` já tinha a informação dos grupos** (é o
assunto do par). Exceção pedida pelo Pedro (sete grupos, 15 sementes): +0,17 sobre o aluno sem nada, cruza o zero;
+0,28 sobre o controle trocado. Olhar exploratório dele ("a ideia era ajudar em labels difíceis"): o ganho fica em
pares difíceis e contradição, cerca de 2 pares, sem critério prévio. **Pedro (18/11): "posso mudar de tema até a
última semana"; quer fazer hoje as duas frentes (fechar o porquê do nulo; uma melhoria na destilação, depois o
tiny), sem ter confirmado qual melhoria nem a troca de tema.** Estado
no `HANDOFF.md`.

**18/11 — GAPS DA REPLICAÇÃO (pedido do Pedro: "fechar esses gaps e melhorar nossa argumentação"; tudo em
`docs/2026-11-18-gaps-da-argumentacao.md`, critérios escritos antes de cada rodada; ledger
`docs/claude/ledger/2026-11-18-gaps-da-replicacao.md`; código sem commit, PC igual por scp):** (1) pares difíceis no
dev (plano 11.9): o padrão do olhar exploratório **não se repete**, fecha como acaso. (2) Tabela 2 do Agrawal
conferida no PDF: o +0,112 do RTE ficaria visível nas quatro grades e não aparece; com baseline forte (QNLI, QQP,
SST-2) **os intervalos do próprio artigo se sobrepõem**. (3) O 0,4754: encoder congelado 0,590, uma época 0,635 e
0,741 (nboost); `Capreolus/bert-base-msmarco` 0,743 com decoder −0,022 (intervalo fora do zero): **nenhuma condição
tentada dá o número, em dois checkpoints**. (4) **Decoder com os 16.000 pares do e-SNLI** (a receita da Tabela 4
cabe): ROC-AUC +0,003 cruzando o zero, acurácia −0,006; a perda do decoder cai em todos os grupos e a classificação
não ganha, então a escala curta (H2) deixa de explicar o nulo (**regra de leitura proposta pelo Claude, ainda sem a
confirmação do Pedro**). (5) **Controle de calendário nos 16.000 pares (decisão do Pedro):** o calendário do braço
com decoder, sozinho, **ajuda** (+0,007 de ROC-AUC, 5 de 5; caso não previsto no critério); com o mesmo calendário
dos dois lados o decoder é nulo no ROC-AUC e perde 0,9 ponto de acurácia (intervalo fora do zero). O +0,003 do
decoder era do calendário. Com 4.000 pares o calendário não se distingue (+0,004 cruzando o zero). (6) **Justificativa
embaralhada nos 16.000 pares (decisão do Pedro; braço `bert_decoder_shuffled`, outro par do mesmo rótulo): o conteúdo
importa.** Real menos embaralhado +0,016 de ROC-AUC e +2,1 pontos de acurácia, 5 de 5, fora do zero; o embaralhado
fica 3,0 pontos abaixo do calendário e o real 0,9. Não mostra que a justificativa certa ajuda (segue abaixo do
calendário), nem separa "ensina o motivo" de "tarefa impossível atrapalha como ruído". Suíte toda verde (191).
Dropout na atenção avaliado sem rodar (opinião do Claude: não vale), sem decisão do Pedro. (7) **Curva de arranque
(pergunta do Pedro: o decoder faz treinar mais rápido?):** o braço com decoder começa 15 pontos na frente no passo
1.225, empata no 1.300 e termina 0,9 atrás; em relógio não há vantagem (a fase B custa mais que o treino inteiro
sem decoder). **Terceira máquina desde 18/11: `ssh amigo`** (PC de um amigo, RTX 5060 Ti 16 GB, tudo em
`C:\RaDi-BERT`; cada semente roda os braços de uma comparação na mesma máquina). Leituras em `resultados/rte-msmarco/`,
`resultados/rte-capreolus/` e `resultados/esnli-treino-16k/`. O Pedro quer depois "algo novo com os professores" na
destilação, ainda sem desenho. Estado no `HANDOFF.md`.

**18/11, NOITE — PROFESSOR QUE LÊ A JUSTIFICATIVA E O QUE O DECODER GERA (critérios escritos antes; código sem
commit):** (1) professor BERT base lendo par + justificativa acerta 96,7% e não precisa do par
(`docs/2026-11-18-professor-que-le-a-justificativa.md`); imitar o interior dele na fase 1 da "sequência" **atrapalha**
(−2,7, 0 de 5; `## Rejected`). (2) O decoder (BERT + T5, 16.000 pares) gera justificativas usáveis em 22 de 50 lidas;
contra um T5 sozinho, sem diferença visível pelo juiz (+2,0, −5 a +9) (`docs/2026-11-18-o-que-o-decoder-gera.md`).
(3) EIDRR lido pelo Claude (nível 2, `docs/artigos/notas-eidrr-wang-wu-2026.md`); busca "justificativa em encoder
que deu certo": nada sólido (nível 3). **Pedro: "acho que é isso então"; nota do Claude como pesquisa 7/10, falta
escrever a entrega (termo da Semana 10 e documento de 12 a 18/11).** Estado no `HANDOFF.md`.

**19/11, MADRUGADA — FORA DE DOMÍNIO, PAINEL E PESO DO DECODER (o gate fecha 19/11 às 12h; critérios escritos antes
em `docs/2026-11-18-gaps-da-argumentacao.md`, Gaps 7, 8 e 9; leitura no fim de
`resultados/esnli-treino-16k/leitura-grade.md`; ledger `docs/claude/ledger/2026-11-18-fora-de-dominio-decoder.md`;
código sem commit):** (1) avaliação da pesquisa pedida pelo Pedro (`docs/2026-11-18-avaliacao-da-pesquisa.md`:
rigor alto, contribuição baixa; parte é de como está contado). (2) **Decoder fora de domínio: atrapalha.** No MNLI
(conjunto que decide) −1,5 ponto contra o calendário (−2,3 a −0,7), 0 de 5; RTE cruza o zero; HANS no piso. Fecha a
pendência 10 do `tema-v3` para esta receita. (3) **Painel de quatro medidas escolhido pelo Pedro** (robustez,
calibração, predição seletiva, pior classe): três do lado ruim, uma nula, nenhum candidato; as três andam junto com
a acurácia. Fora do critério: o calendário sozinho melhora calibração e predição seletiva. (4) O treino agora salva
os classificadores (`--salvar-pesos`) e avalia fora (`--fora`, `avaliar_fora.py`, `painel_pesos.py`, `ler_fora.py`);
MNLI e HANS baixados com o OK do Pedro. (5) **Braço embaralhado fora de domínio (PC do Marcelo, com calendário de
âncora):** a conferência do instrumento não passou por 0,03 ponto, números só descritos (real menos embaralhado no
MNLI +2,9). **Varredura do peso da perda do decoder (0, 0,05 e 0,5, valores do Pedro; 3 sementes, exploratória):
nenhum peso passa** (dev 82,8% a 83,2% nos quatro pesos, abaixo do calendário em todas as sementes); com peso 0 a
perda é a mesma, então o custo parece estar na fase só do decoder (leitura de 3 sementes, sem teste). Nada no ar às
07:35. (6) Rascunhos para o gate: `docs/residencia/termo-de-entrega-Semana-10.md` e
`entrega/controles-do-decoder-e-destilacao.md` (agente em Opus, números conferidos por agente; **o Pedro não leu**).
**TERMO DA SEMANA 10 ENTREGUE (Pedro, 19/11, ~11:35).** Tema: "Destilação de Racionalização de LLM para Encoders:
controles e limites", subtítulo "A supervisão por justificativas vale o custo em encoders para implantação?"
(decisão dele). Documentos em `entrega/`: `Trilha das Semanas 9 e 10.docx`, `Figuras e Evidencias.docx` (11 figuras,
tabela de onde sai cada número, hipótese das justificativas), `Criterios Escritos Antes dos Testes - Semana 10.docx`,
`Marcas de Atencao e Destaque v2.docx`. Não vi o que ele colou no formulário. **Pedro, depois de entregar: "Não sei
explicar nada do que foi feito" — é o próximo trabalho: ensinar com o termo e as figuras na mão, ele explicando com
as palavras dele.** Os documentos servem também ao TCC (memória `docs-de-entrega-servem-ao-tcc`). Nada commitado.
**Pedro: "queria muito, muito um positivo"; desconfia de erro no meio; considera a moldura "problemas e padrões
descobertos", com eficiência de modelos para implantação como área, título não decidido. Limite de Fable acabando:
"Usa o Opus pra coisa que n precisa do Fable".** Estado no `HANDOFF.md`.

**19/11, GATE 10 E RUMO PÓS-GATE (Pedro):** termo entregue e apresentado. **O professor criticou a escolha do
artigo** (Agrawal: "pouco descritivo, sem código, com baselines quebrados, poucas sementes"); **não elogiou o método**
(isso é inferência do Pedro, dito por ele; não registrar como fala do professor). **Decisão do Pedro: "modelar tudo
daqui pra frente baseado nesse cerne de custo"** — a pergunta do trabalho é "essa técnica compensa o custo 7x maior?",
não "deixar um modelo melhor com justificativa"; a destilação comum é a régua de comparação. **"As experimentações
acabaram, só pode fazer pontuais"**: a pontual já nomeada é pôr decoder e destilação no mesmo cenário (hoje o custo
do decoder é BERT base/16 mil pares e o da destilação é BERT small/4.000), ainda sem desenho. Limite de honestidade
combinado: os critérios escritos antes medem o **benefício** (acurácia); o custo vem dos tempos gravados; não escrever
que os critérios nasceram da pergunta de custo. Quatro imprecisões nos documentos entregues (o "21,8%" vem de uma
sonda de 63 pares; a regra geral e a do Gap 4 nos Critérios; detalhes das Figuras) ficam para corrigir na versão do
TCC, com pedido dele. Pesos do PC do Marcelo **copiados em 19/11** para
`resultados/<pasta>/amigo/pesos/` (13 arquivos, SHA-256 igual ao original; fora do git). Os 21 do PC do Pedro seguem
só em `D:\RaDi-BERT`. **21/11: tudo de 10 a 19/11 commitado no `feat/treino-rte`** em 15 commits por pasta; ficaram
fora, por passarem do limite de 2 MB do gancho, `entrega/Manual do Treino.docx` e `resultados/rte-treino/pc/palavras.csv`.
**21/11 (Pedro): o SSD do projeto voltou para o PC da RTX 5060.** Esta instalação (hostname `WKST-001`, o nome que
era do notebook) agora roda com a 5060 de 8 GB: o projeto e a GPU estão na mesma máquina, e `ssh pc` / `ssh pc-h`
deixam de ser o caminho para treinar. A cópia antiga do PC aparece como **`E:\RaDi-BERT`** (com os 21 pesos em
`resultados/*/pesos/`) e as ferramentas em `E:\tools`; o `config/maquina.env` daqui aponta para
`C:\Users\Pedro\Documents\Projects\tools` (não testei o `llama-server` nesta configuração). O que vale no bloco
"MODO DE TRABALHO" de 08/11 sobre notebook × PC está superado por isto. README com a estrutura atualizada (21/11); a
parte de narrativa do README espera a remodelagem pelo custo e os infográficos (decisão do Pedro).

**GATE 4 — FEEDBACK DO PROFESSOR (01/10, transmitido em 05/10; texto e abertos F1–F5 em `docs/feedback-gate-4.md`):**
(1) história não dá base agora — foco em obras **recentes, com métodos e ferramentas atuais**; (2) das 91 surveys só
3–5 servem, e **não refazer a pesquisa** — o screening fecha; (3) **daqui pra frente, nada de Claude/Gemini/ChatGPT
salvo necessidade real**. **O Pedro discorda (05/10) e segue usando LLM:** leitura e extração são dele; o Claude é
interlocutor e redige o que ele explicou. Não propor agentes nem fichas por LLM; não pôr no texto ideia que ele não
disse; nunca disfarçar o uso de LLM nas entregas. **Adendo (05/10):** em pessoa o professor foi mais tranquilo (a
fala era obrigação de quem argui), e **o termo do gate fica fora do veto**: o Claude redige a partir do registro da
semana, e o Pedro sempre adapta, nunca cola. **Sem mapa (Pedro, 05/10).** Semana 5 = escolher mais obras, as
melhores possíveis, entre as 56: `docs/screening/fase1/2026-10-05-lista-56-para-selecao.md` (selos ✔/◐/✗ = leitura do
Claude do critério "recente"). **Seleção do Pedro (05/10): saíram as 17 ✗, ficam 39 para o gate da semana 5.**
Lacunas sugeridas no fim do arquivo (ModernBERT, GQA, Orca, survey de KD de LLM, MobileLLM; metadados conferidos),
esperando a decisão dele. **07/10: lista com 50 obras** (39 + 7 lidas + e-SNLI, Ho 2023, survey de CoT de Chu 2024,
CoK de Wang 2024): `docs/screening/fase1/Lista de Obras.docx`. **Semana 5 fechada (07/10):** `docs/residencia/termo-de-entrega-Semana-5.md`
+ `entrega/Obras Lidas v4.docx`; leituras dele em `Downloads/Leituras Semana 5.docx`. **O desenho do tema NÃO está
decidido** (Pedro, 07/10: "vou decidindo mais pra frente"). Estado completo no `HANDOFF.md`.

**Leitura do Pedro (declarado 10/09):** apenas **Distilling Step-by-Step** e **DHRD** — dos dois ele escreveu resumo próprio, que são entregáveis. Nenhum outro artigo do projeto foi lido por ele. **Atualização 23/09:** terminou **Petersen et al. 2008** (nível 1). **Atualização 01/10:** declarou ter lido também **Agrawal, Ahemad & Sembium 2025** (nível 1; entra em `entrega/Obras Lidas v3`). **Arksey & O'Malley 2005 e Kitchenham & Charters 2007: leu o resumo preparado pelo Claude, não a fonte** (declarado 01/10) — no Obras Lidas v3 ficam numa seção separada "lidos por resumo"; não contam como nível 1. **01/10:** Hinton 2015, Yuan 2024 e Kwon 2023 (leitura dirigida). **06/10: DistilBERT (Sanh 2019)**, com extração dele em `docs/leituras/fichas/distilbert-sanh-2019.md`; recusou MobileBERT e Gou 2020 por "6+ anos, só para história". Necessidades que a leitura levantou → `docs/2026-10-06-destilacao-surveys-losses-bert.md` (nível 3). **⚠️ Wadhwa et al. 2024 (EMNLP, arXiv:2406.14511)** já testou racionalização embaralhada com aluno decoder: é o controle que o tema v3 dava como lacuna. A pergunta passa a ser "vale para encoder?".

**CRITÉRIO DO PROGRAMA (declarado pelo professor/coordenador em 11/09, e ele é por quem tudo passa):**
a Residência **não avalia inovação nem produto final — avalia o processo**. "O produto final é você, não o
seu TCC." O tema v3 foi considerado **"muito produto"** (o elogio "ótimo e explorável" registrado aqui em 11/09 **não foi
dito**: correção do Pedro em 10/11; ninguém avalizou o tema): ele não conseguiu ver
**qual especialização** o Pedro está construindo. A pergunta que precisa de resposta antes de qualquer
outra é **"você vai ser o quê?"** — e o tema entra como veículo dessa resposta, não como fim. Toda
proposta e todo documento de entrega deve tornar a especialização visível; o tema é instância dela.
**Consequência (interpretação do que ele disse, não fala dele; Pedro, 10/11):** novidade deixa de ser critério. Um método já publicado (Agrawal) é **blueprint
para aprender**, não ameaça. Nulo bem controlado e documentado é ciclo completo — conta.

**O PROCESSO DO PROFESSOR (transmitido pelo Pedro em 15/09, palavras do professor):** três Momentos/Etapas
para virar especialista em qualquer área — **Etapa 1: história, fundamentos, ferramentas** (divisões da
área, vocabulário) · **Etapa 2: "frameworks" de apoio** · **Etapa 3: trilhas ou campos de aplicação**.
A pesquisa bibliográfica pedida é **"screening", em contraposição à Revisão Sistemática**: o objetivo
é *"encontrar artigos relevantes e que suportem o início da Etapa 1: levantando a história da área, as
suas divisões, fundamentos, vocabulário e etc."* **Consequência:** o levantamento feito até 10/09
(`docs/pesquisa/artigos-verificados.md`, ~50 artigos em 7 frentes) foi busca de fronteira a serviço do tema — serve
para a Etapa 3, não para a Etapa 1. **A Etapa 1 da especialização nomeada ainda não foi feita.** A seção
de "fundacionais" de `docs/pesquisa/metodo-busca-artigos.md`, descartada em 09/09, pode voltar a ter função — decisão
do Pedro.

**DEFINIÇÃO DE FUNDAMENTOS DO PROFESSOR (transmitida pelo Pedro em 22/09, da última aula, palavras
do professor):** *"Os FUNDAMENTOS de qualquer Área ('porção') de Conhecimento é construído ao longo do
TEMPO (história), reunindo FERRAMENTAS que auxiliam na execução de toda e qualquer ATIVIDADE que seja
necessária dentro de uma TRILHA relacionada à Área. Toda Trilha também tem seus próprios fundamentos!
Um(a) especialista conhece 'o que forma' (ou compõe) a sua área de especialização ATUALMENTE
(fundamentos)."* **Leitura a confirmar pelo Pedro (pendências B1–B4):** história, fundamentos e ferramentas
não são três pilares paralelos — fundamentos é o produto, história e ferramentas são como ele se
constrói; a unidade das ferramentas é a **atividade** (não a divisão), e o método ainda não tem eixo de
atividade; cada trilha (Etapa 3 — o tema v3 é uma) terá fundamentos próprios, fora da Etapa 1;
"atualmente" confirma a janela 2020+ para o mapa e sem janela para história. Consequências para o
método: decisão do Pedro, depois do Petersen.

**PENDÊNCIAS PÓS-PETERSEN:** `docs/pendencias-pos-petersen.md` (aberto 22/09) — tudo que surgiu enquanto o
Pedro lia o Petersen 2008 (RQs, definição de fundamentos, filtro-tipo × Petersen, loop do pool, funil por
voltas, critérios de inclusão, start set, rótulos). **Nada decidido; cada item é uma pergunta para ele.**
Regra (22/09): decisão que falta é perguntada — nunca preenchida e rotulada como "do Claude".

**ESPECIALIZAÇÃO NOMEADA PELO PEDRO (15/09), com as palavras dele:**
- *"Você vai ser o quê?"* → **"eficiência de modelos para implantação"** — e o tema v3 é "só uma análise
  dentro dessa área", não a área.
- *"O que quer saber fazer que hoje não sabe?"* → **"conhecimento profundo sobre a arquitetura de
  encoders, decoders e encoder-decoders"** — é o que este ciclo ensina.
- Encaixe (observação do Claude, não do Pedro): a trilha de leitura já cruza as três famílias — DSbS
  (encoder-decoder, T5) → DHRD (decoder-only) → Agrawal (BERT + decoder T5) → v3 (encoder-only). A
  narrativa da proposta é essa.

**DEFINIÇÃO DE FRAMEWORK (Etapa 2; trazida pelo Pedro em 30/09, origem a confirmar):** estrutura flexível de diretrizes, práticas e ferramentas pré-definidas que serve de **esqueleto** (base, arquitetura, funções essenciais) para um projeto, para não reinventar a roda. Teste e consequências em `docs/criterios-de-relevancia.md` §7.1: **vale nos dois sentidos (Pedro, 30/09: 'é os dois')**: software (esqueleto de código) **e** conceitual/metodológico (diretrizes e práticas que prescrevem decisões num projeto: roofline, pipeline do Deep Compression, métricas de Sze, text-to-text do T5); taxonomia só conta se disser quando usar cada ramo.

**MÉTODO DE LEITURA DO PEDRO (rápido, 01/10 — 'mais rápida mas com os mesmos ganhos'):** `docs/metodo-de-leitura.md` — **caça dirigida em 5 paradas** (promessa · origem · núcleo · Ctrl+F · fecho), ~35 min/obra, colhendo os **mesmos 13 ganhos** da versão detalhada (v1, 30/09, guardada em `docs/metodo-de-leitura-v1-*.md`); escreve direto nos 4 arquivos acumulados de `docs/leituras/` (= material do gate); ficha do agente só como guia de ONDE ler (páginas), nunca de O QUE. Página em toda anotação.

**OS TRÊS OBJETIVOS DAS OBRAS (Pedro, 26/09):** as obras servem a **saber** (conhecimento, compreensão
profunda), **saber fazer** (prática em contextos diferentes) e **saber ser** (domínio visto no comportamento;
*"obras não ensinam isso"*), ou a uma combinação. Como vira regra nos agentes está em aberto:
`docs/screening/fase1/2026-09-26-plano-agentes-F2.md` §5.

**Régua de decisão do Pedro (anterior; em revisão após 11/09):** o tema tem que gritar para um empregador "eu resolvo um problema seu" + carregar professional improvement + ser inovador sem ser fronteira + caber no orçamento. O professor inverteu a ênfase: *professional improvement* vira o critério primário, "gritar para empregador" é secundário, e "inovador" sai. A especialização está nomeada (acima); a régua nova o Pedro ainda não escreveu por extenso. Ele decide; Claude é apoio à decisão, não executor — exceto escrever arquivos, que é sempre autorizado (documentação não é execução).

**PROCEDÊNCIA (regra permanente):** todo arquivo de pesquisa deve declarar quem leu o quê, em três níveis — (1) Pedro leu, (2) Claude leu o texto completo, (3) agente verificou página e resumo apenas. Nível 3 serve para triagem, **nunca para citação**: metadados são confiáveis, interpretação de método e resultado pode ter erro de sumarização. Nada entra em texto assinado pelo Pedro sem que ele tenha lido o original.

## Arquivos

- `docs/residencia/semana-1-topicos/topicos-csce2026.md` — os 289 tópicos extraídos das 3 CfPs (IDs A01–Q44), com análise crítica das CfPs no topo. Fonte da verdade.
- `docs/residencia/semana-1-topicos/clusters.md` — síntese: clusters nomeados, âncora + satélites, teste do elevador. PREENCHIDO 18/08.
- `docs/pesquisa/interesses-estudos-futuros.md` (raiz) — todos os 3/2.5 que caíram nas podas, por área; NÃO é parte da especialização.
- `docs/residencia/semana-1-topicos/artigos/` — notas de leitura da Fase 4 (surveys + papers dos finalistas).
- `docs/residencia/semana-1-topicos/objecoes-e-respostas.md` — objeções à config (O1 BIA≠CD, O2 assimetria ML/dados, O3 1/80, O4 empregador, O5 salário, O6 gap-de-ML≠âncora) com respostas prontas + regra R1 anti-atrofia.
- `docs/residencia/semana-1-topicos/temas-candidatos.md` — 20 temas propostos (10 âncora C2 + 10 âncora ML c/ satélites dados+segurança), com pares espelhados e critérios de escolha. TODOS rejeitados (ver `## Rejected`).
- `.docx` correspondentes: gerar SÓ ao finalizar cada .md (placeholders já existem).

**Arquivos do ciclo de tema (28/08–10/09):**

- `entrega/` — **versões de entrega do gate 2 (17/09), md + .docx gerados:** `metodo-screening.md`
  → `Metodo de Screening.docx` · `fundamentacao-metodo-screening.md` → `Fundamentacao do Metodo de
  Screening.docx` · `pool-termos.md` → `Pool de Termos.docx`. Regras da versão de entrega: primeira
  pessoa, sem metacomentários/versões/citações do Pedro, sem "Pedro", sem caracteres fora do teclado
  (— · § ⟨⟩ ≥ → × ² viram - / cap. / (rev-N) / >= / -> / x / ^2), numeração própria (Procedimento =
  cap. 10; sem seção de orçamento de tempo). Formatação "feia" de propósito: Arial 12, headings padrão
  pretos, Table Grid; código do pool como imagem. Conversor em scratchpad (`md2docx_plain.py`) — se
  precisar regerar, reescrever a partir do md. **Os documentos de trabalho na raiz continuam sendo a
  fonte; a entrega é derivada.** A Fundamentação declara níveis de leitura do Pedro (Petersen [1],
  Arksey & O'Malley [2], Tricco [3]) que **ainda não aconteceram** — ler antes de entregar.
  **Leituras nível 4 feitas (19/09):** Wohlin 2014 e Kitchenham & Charters 2007 lidos na fonte
  (PDFs em `docs/artigos/`, notas `notas-wohlin-2014.md`, `notas-kitchenham-charters-2007.md`);
  tabela §1 do método-do-método conferida, sem divergência. Glaser & Strauss 1967 **só por fonte
  secundária** (Saunders et al. 2018) — `notas-glaser-strauss-1967.md`; o `[4]` declarado na
  Fundamentação entregue está acima do real para essa fonte; corrigir se o doc for reentregue.
- `docs/metodo-de-construcao-do-metodo.md` — **o método do método (17/09).** Responde "como você criou
  isso?": as dez decisões mapeadas aos componentes-padrão de protocolo de revisão (Kitchenham 2007,
  Arksey & O'Malley 2005, Petersen 2008, Wohlin 2014, saturação de Glaser & Strauss — **nível 3, a
  confirmar na fonte antes de citar**), o que o método muda e por quê, trilha datada de quem decidiu o
  quê, e o script de resposta para a arguição — incluindo "usou IA?".
- `docs/screening/` (renomeada de `screening/` em 22/09, pedido do Pedro) — `papers/volta-N/` recebe os PDFs de cada volta, depois movidos por cluster; **apagar só com pedido dele, e avisar o que virou lixo ao fim de cada volta**. Execução 3: plano em `fase1/2026-09-22-plano-fase1-exec3.md`, passo 0 (contagens) em `fase1/2026-09-22-exec3-passo0.md`.
- `docs/screening/fase1/` — **Fase 1 em andamento (disparada pelo Pedro em 21/09).** `raw/` = retorno bruto
  das bases em JSON, sem filtro (K&C §6.1.4). **23/09, a pedido do Pedro:** o bruto das execuções 1 e 2 (`raw/2026-09-21-*`) e o `edge` antigo da execução 3 foram para a **Lixeira do Windows** (recuperáveis até ele esvaziar); as leituras em .md continuam. **Floresta final:** `2026-09-22-floresta.md` + `-obras.csv` (118.659 obras); limpeza em camadas A->B->C em `2026-09-23-proposta-metodo-limpeza.md`. **Execução 1** (string v0, piso 100): 1.721/1.734/409,
  legível em `2026-09-21-string-mae-retorno-bruto.md` — ~94% era ruído de `resource-constrained`/
  `on-device`. **Calibração do Pedro (21/09):** esses termos viraram filha `edge` (pool, emenda 1); piso
  em teste a 60. **Execução 2** (string regenerada): 100/103/89 → **154 obras únicas**, com decisão por
  obra em `2026-09-21-candidatos-string-mae-exec2.md` (58 entra · 9 sem filtro · **36 borda, decisão do
  Pedro** · 40 fora · 12 não é survey) — **saída da Fase 1 da string-mãe; nível 3, nada lido.** Registro
  nível 3 (Fase 2) espera o Pedro ler Petersen 2008. Filhas e Google Scholar não rodados. Decisão
  ⟨rev-22⟩ (21/09): veredito por termo do pool a cada rodada de saturação.
- `docs/screening/pool-termos-etapa1.md` — **vocabulário versionado do screening (v0, 17/09; execução 1 em 21/09).** 34 termos do Pedro +
  8 do Claude em 7 grupos, com origem; as strings de busca são composições dele (mãe + filhas, por
  base), como texto — **nenhuma executada**. Regras de entrada/aposentadoria, **revisão por evidência de retorno** (§3) e versões/emendas no arquivo.
- `docs/screening/metodo-screening-etapa1.md` — **o método vivo (v3.7, 22/09; v2.4 de 17/09 era o fechado).** ⟨rev-33⟩ (bloco N): leitura para **classificar** é **escada** abstract -> introdução -> conclusão (a escada é o limite, sem teto de 5 min; dúvida só no topo); leitura para **extrair** (taxonomia, ferramentas, referências, glossário) é fixa em todo survey que entrou; abstract ausente -> buscar por arXiv id/DOI, senão introdução; §1.4 declara o screening como mapa que também extrai, sem avaliar resultado. ⟨rev-34⟩ (bloco G): §1.2.1 pertencimento **por survey** — parcial entra como base; CNN/GNN/difusão fora; aplicação específica só sem survey geral; infraestrutura de implantação dentro; hardware é divisão ("pra saber que existe"); §3.4 exclusão **não é survey** (primário fica no bruto e volta como seminal; paper de sistema -> ferramentas); G4: treino puro fora. ⟨rev-35⟩ fecha as pendências pós-Petersen (só restam F3 e o teste da bimodalidade, que dependem de dado): `filtro-tipo` declarado como restrição; lacuna do pool também pelas perguntas de §1.4; relato de funil por volta; esquema evolui na extração; registro `screening/registro-etapa1.md` + `.csv`; **05/10 = até o mapa v1**. **A execução 2 foi calibração — a Fase 1 roda de novo, e o Pedro quer o plano antes de qualquer execução.** ⟨rev-23⟩: três facetas do mapa (divisão × pilar × **arquitetura**, eixo §1.2 anotado no Y) como colunas do §8 e bubble plot em §9.1. ⟨rev-24⟩: plot **A** (unidade survey) a cada rodada como instrumento do loop, **B** (unidade paper referenciado) no fim; a extração passa a registrar a **seção citante** de cada referência (§6, §7) — precondição de B. ⟨rev-25⟩: o pool muda **por evidência de retorno** (uma regra, duas direções — ruído sobre o bruto, lacuna sobre o plot A), com cláusula anti-viés (termo movido é obrigado a rodar em filha; **filha `edge` obrigatória**) e vocabulário versão × emenda; + checkpoint do nome da área antes de consolidar, até saturar, só antes do v1. ⟨rev-26⟩: **gate de relevância** no checkpoint (candidato rodado sozinho antes de ganhar volta), parada em "mais da metade já no pool", **teto de 8 voltas** (ampliável por ele) e voltas como métrica de gate. ⟨rev-27⟩ §5.3: **conjunto inicial com diversidade obrigatória** (autores disjuntos, venues distintos, >= 1 por pico de ano — os 8 mais citados das 58 são todos de 2020-21, e a distribuição é bimodal com vale em 2022), **detector de cluster** (divisões novas por survey tem de cair; se não cair, cluster perdido) e **teste da bimodalidade marcado como instrumento nosso**, não de Wohlin. ⟨rev-28⟩ **os termos passam a ser os do professor**: *fundamentos* é o **produto** (o que forma a área hoje) e o antigo "fundamentos" de §1.1/§6 vira **conceitos** — renomeado em todo o método, inclusive no valor da coluna *pilar*; **§1.4 nova** com a hierarquia, as **cinco perguntas do screening** (todas de *onde encontrar*, nenhuma de *o que é verdade* — a linha que separa screening de RSL) e os limites de escopo (fundamentos da trilha ficam fora); **§3.3 nova: eixo de atividade** (ferramenta serve atividade, bottom-up, só o que a fonte declara; mapeamento completo é da Etapa 2); colunas `atividade` e `era` no §8; **era é atributo da divisão, não divisão** (escolha delegada ao Claude pelo Pedro). ⟨rev-29⟩: **ferramenta se pesquisa fora de survey** — filha `ferramentas` sem `filtro-tipo` (paper de sistema), ferramentas nomeadas pela fonte viram item de extração, e registros de ecossistema (HF/ONNX/MLPerf) entram como descoberta nível 3 não citável. Achado que motivou: termo preciso de ferramenta devolve 0-3 surveys — a área documenta as ferramentas, não as pesquisa. ⟨rev-30⟩: **população = surveys sem piso de citação** (opção b) — o piso sai da busca e vira critério de registro (§3.2, valor **60**), porque piso na busca é idade disfarçada de qualidade. Medição 22/09 no S2 com a string limpa: com piso 103 · **sem piso 863** · sem palavras de tipo 16.821 · papers com >=60 citações 793. Os 41.412 da execução 1 eram string suja, não esta população. ⟨rev-31⟩ §11.1: **loop por voltas** na Fase 1, cada volta terminando em decisão do Pedro; o filtro **ordena, não apaga** (descartado fica no bruto e volta se uma rodada abrir grupo novo); alvo **provisório** de ~50 documentos — ele só fecha o número depois de ver gráficos e tabelas das primeiras voltas. ⟨rev-32⟩: **proposta de agrupamento** por volta é artefato do Claude, datado, **fora do registro** (`screening/fase1/<data>-volta-N-agrupamento.md`), com quatro salvaguardas — ordena e não apaga; mostra sempre os membros; marcada como proposta nível 3; **agrupamento não é divisão** e morre na volta seguinte. Motivo da cautela: a cicatriz do Agrawal (§7). Decididos pelo Pedro em 22/09, pós-Petersen. Screening da Etapa 1
  da especialização: dez decisões ditadas pelo Pedro + 21 correções de revisão marcadas `⟨rev-N⟩`,
  todas decididas por ele em 16/09 (defaults de §3.2/§4 por omissão, com calibração). Trilha:
  `docs/formulario-metodo-screening.md` (perguntas) e `docs/revisao-metodo-screening-2026-09-15.md`
  (achados). **Ler antes de qualquer busca.** Abertos só: nome do registro, data-alvo da Etapa 1,
  divisão de horas. **A Fase 1 (screening geral) só dispara com ordem do Pedro.**
- `docs/pesquisa/mapa-do-terreno.md` — **ler primeiro em sessão nova sobre tema/pesquisa.** Como julgar pesquisa em IA: os 5 tipos de alegação, o que torna pergunta difícil, os 6 instrumentos (baseline, confundidor, ablação, ruído, teto/piso, validade externa), o regime do Pedro, referência de arquiteturas e de destilação sem GPU grande, e as 7 perguntas para decidir.
- `docs/pesquisa/artigos-verificados.md` — registro único dos ~50 artigos verificados na fonte, em 7 frentes, + taxonomia de métodos (11 de 18 usam o mesmo) + lista de leitura deduplicada de 8.
- `docs/pesquisa/tema-v3-racionalizacao-encoder.md` — o tema vivo: pergunta, H1/H2 com verificação, ponte teórica, desenho de estudo, **aplicações industriais e o que NÃO é aplicação**, pendências.
- `docs/datasets-nli-verificacao.md` — **ler antes de qualquer conversa sobre tarefa/dataset.**
  Números verificados de ASSIN2 e e-SNLI na fonte primária, com procedência por nível. Três achados
  que mudam o quadro: o ASSIN2 é **binário** e foi feito de propósito com "fatos simples" e sem
  contradição (vem de legendas de imagem via SICK-BR); o **SICK-BR está queimado** como conjunto
  fora de domínio porque é a fonte do ASSIN2; o único par OOD em pt-BR é ASSIN2 → ASSIN 1.
- `docs/artigos/notas-herrewijnen-eacl2026.md` — notas da primeira leitura integral de paper do projeto.
- `docs/artigos/notas-dhrd-xu2025.md` · `notas-distilling-step-by-step.md` · `notas-li-icd-2508.16777.md`
  — as outras leituras de nível 2, com PDFs na mesma pasta. **Só estas quatro são citáveis.**
- `docs/pesquisa/secao-dsbs-cabeca-auxiliar.md` e `docs/pesquisa/secao-dhrd-transferencia-encoder.md` (raiz) — seções de
  entregável derivadas dos resumos que o Pedro escreveu dos dois papers: o que cada um **licencia**
  no desenho (cabeça auxiliar descartada; transferência para encoder) e o que **não** licencia, com
  nível 1 (Pedro) e nível 2 (Claude) marcados item por item. A do DHRD traz três correções ao resumo.
- `docs/pesquisa/metodo-busca-artigos.md` — método de busca (funil, snowball por citação, filtros, saturação). Contém seções de string e de fundacionais que o Pedro mandou desconsiderar em 09/09.
- `docs/residencia/semana-1-topicos/dinamica-preferencias.md` — 36/42 respostas de preferência revelada; é o que mostrou que a âncora real do Pedro é ML, não dados.
- `docs/residencia/semana-1-topicos/tema-escolhido.md` (v1) e `docs/residencia/semana-1-topicos/tema-v2-fusao-slm.md` — temas anteriores, superados. Mantidos como trilha de decisão.
- `docs/residencia/semana-1-topicos/titulos-alternativos-100.md` e `docs/residencia/semana-1-topicos/dominios-f10-descricoes.md` — 136 títulos e 110 domínios candidatos, todos reprovados; úteis como registro do que já foi descartado.

## Método de seleção — funil macro → meso → micro

Os 289 tópicos foram agrupados em **16 macro-temas** (M1–M16), cada um subdividido em **meso-grupos** temáticos, contendo os **micro-tópicos** (IDs originais da CfP).

**Processo acordado (iterativo, um macro por vez):**
1. Claude apresenta o macro da vez como **painel interativo no menu lateral** (widget com botões 0/1/2/3/?), estruturado macro → meso → micro com mini-explicação de cada item. SEMPRE usar o painel para pontuação — inclusive para pontuar os próprios macros; explicações longas e discussão ficam no chat.
2. Pedro pontua no painel e levanta dúvidas; decidimos juntos os casos ambíguos antes de seguir.
3. Só então passamos ao próximo macro. Notas registradas no `topicos-csce2026.md`.
4. Tópicos idênticos repetidos entre conferências (ex.: A02 = B44 = J03 = Q34) aparecem como UMA linha no painel; a nota replica para os IDs equivalentes.

**Escala de notas:**
| Nota | Significado |
|---|---|
| 0 | Ignoro |
| 1 | Curiosidade — leria um post |
| 2 | Quero estudar de verdade |
| 2.5 | Indeciso entre 2 e 3 — candidato a âncora/satélite, resolver na consolidação |
| 3 | Quero ser **reconhecido** nisso |
| ? | Não sei do que se trata — Claude explica, Pedro repontua |

**Macro-temas:** M1 LLMs/GenAI/NLP · M2 Fundamentos ML/DL · M3 Agentes/RL/autônomos · M4 Grafos · M5 Bayesianos/estatísticos · M6 Otimização/meta-heurísticas · M7 Fuzzy/rough sets · M8 IA simbólica/conhecimento · M9 Processo/qualidade de dados · M10 Infra big data · M11 Busca/IR/recomendação · M12 Privacidade/segurança · M13 Séries temporais · M14 Visão/sinal/multimídia · M15 Cognição/neuro-inspirados · M16 Aplicações de domínio

**Progresso:** FUNIL COMPLETO (M1–M16 ✔, 18/08/2026) · Ranking: C2 › C1 › C6 · PODAS 1 e 2 aplicadas (critério final: pipeline de dados INTEIRO, ênfase em estruturação; trilha completa na seção "Poda" do topicos-csce2026.md) · Consolidação preenchida: 29 conceitos nota 3 (21 C2 + 4 C1 + 4 C6) · clusters.md escrito · Pendente: Pedro revisar elevador + colunas pessoais da consolidação; conferir rebaixamento de I30/N08 (C4, faltaram no painel de veto) · Próxima etapa: FASE 4 — surveys (começar por Zha et al., data-centric AI, dossiê C2)

**Fase de leitura (Fase 4):** 1 survey por ETAPA do pipeline, não por tópico de CfP — ~8 leituras no total (plano numerado no clusters.md). Depois 2–3 papers apontados por cada survey, lendo título + abstract + figuras. Notas em `docs/residencia/semana-1-topicos/artigos/`.

## Fatos verificados (17/08/2026)

- TCCs das turmas anteriores (80 itens no repositório UFG, verificado 19/08): ~8 têm dados como núcleo (não 1), frequência crescendo; pool saturado é LLM/agentes (~25%); estruturação de dados é território virgem. Análise em `docs/residencia/semana-1-topicos/analise-tccs-anteriores.md`.

- As CfPs de 2026 quase não mencionam LLM/GenAI (1 item: E01; bloco C do ICDATA). Nenhum track de LLM entre as 21 conferências do congresso. Listas recicladas de anos anteriores — detalhes no topo do `topicos-csce2026.md`.
- Teste pendente para validar o venue: olhar proceedings reais na Springer (https://link.springer.com/conference/csce-1) e contar papers de LLM.
- ICDATA: aceitação ~40–50%, deadline estendido 18/06/2026, proceedings Springer Nature.

## Rejected

- **"O decoder ajuda fora de domínio" e "o sinal aparece em outra medida que não a acurácia"** (19/11, medido
  contra critério escrito antes) — MNLI −1,5 ponto; calibração e pior classe do lado ruim, predição seletiva nula.
  O painel é fechado: nenhuma medida nova nem troca de corte sem decisão do Pedro (regra de parada do Gap 8).
- **"A falta de ganho vem de o peso da perda do decoder estar fixo em 0,1"** (19/11, varredura exploratória de 3
  sementes pedida pelo Pedro) — com 0, 0,05 e 0,5 o braço fica abaixo do calendário em todas as sementes. Não propor
  outro valor de peso; o que ficou sem teste é a duração da fase só do decoder, e só com pedido dele.
- **Atalho da hipótese e resistência à compressão como medidas do painel** (19/11, Pedro: o atalho "n é tão
  atrativo de gastar tempo"; na compressão "eu tbm acho que não" há motivo para esperar efeito).
- **Lançar teste que o Pedro quer muito sem checar piso, poder e sem salvar os pesos** (19/11, Pedro: "corrige esses
  erros ... e pensa mais no desenho") — antes de rodada longa: medir o piso num modelo que já existe, estimar o que
  as sementes enxergam, salvar os pesos, fumaça em todos os braços.
- **Rodar script avulso a partir de `%TEMP%`** (19/11, incidente) — o Python importou um `h2.py` antigo de lá.
  Scripts avulsos rodam do scratchpad com `python -I`.
- **Etapa com justificativa só para o treino arrancar mais rápido** (18/11, Pedro: "n consigo pensar numa situação
  que seja util treinar por menos tempo") — a curva de arranque mostrou vantagem só nos primeiros ~100 passos e
  nenhuma em relógio; não propor ganho de velocidade de treino como objetivo.
- **Fase 1 da "sequência" imitando, nas posições do par, o interior de um professor que lê o par + a justificativa**
  (18/11, critério escrito antes em `docs/2026-11-18-professor-que-le-a-justificativa.md`) — 2,7 pontos abaixo da
  "sequência" no conjunto de escolha, 0 de 5 sementes, e a justificativa de outro par dá o mesmo. A causa não foi
  separada (renormalização da atenção, rótulo no interior). Não repetir este desenho; variação só com pedido do Pedro.
- **"A cabeça de grupos ajuda os pares difíceis" (olhar exploratório de 18/11)** (18/11, critério escrito antes na
  seção 11.9 do plano) — no dev o ganho não se repete (−0,08 e −0,03 ponto, cruzando o zero). Não trocar faixa,
  braço de dificuldade nem subconjunto para procurar de novo.
- **"A escala curta explica o nulo do decoder" (H2 do Claude, 10/11)** (18/11, derrubada por medida) — com os
  16.000 pares do e-SNLI a receita cabe, a perda do decoder cai em todos os tipos de palavra e a nota não sobe; com
  o mesmo calendário o decoder perde 0,9 ponto. Não propor "mais dados" como saída para o decoder.
- **"O classificador não usa o porquê" e "o sinal do decoder é fraco demais para mexer na nota"** (18/11,
  derrubadas pela justificativa embaralhada) — trocar a justificativa pela de outro par do mesmo rótulo custa 2,1
  pontos a mais que a certa. O que não se sustenta é o contrário também: a certa não fica acima do calendário.
- **Ler "decoder menos sem decoder" sem o controle de calendário** (18/11, medido) — nos 16.000 pares o calendário
  sozinho vale +0,007 de ROC-AUC e escondia o efeito do decoder. Toda comparação com decoder leva o braço
  `bert_calendar` junto.
- **Cabeça no `[CLS]` prevendo os grupos de palavras novas da justificativa (UMAP + HDBSCAN), para ganhar nota**
  (18/11, nulo pelo critério escrito antes, com 15 sementes no melhor braço) — o alvo é o assunto do par, que o BERT
  small já tem no `[CLS]` sem treino (sonda 0,765 × 0,760). Não propor variação (peso, outro corte de grupos) sem
  alvo novo que não esteja já no `[CLS]`.
- **Viés por rótulo nascendo em zero numa cabeça auxiliar treinada a 5e-5** (17/11, auditoria de treino) — não sai
  do lugar em 1.000 passos; nasce no logit da taxa de cada rótulo.
- **Jeito 3, atenção como guia das respostas (marcas do LLM ou linha do `[CLS]` do professor nas camadas 3 e 4)**
  (17/11, Pedro: "Sem jeito 3 então") — reabriria a regra de parada das marcas, e as marcas nas camadas 3 e 4 juntas
  já davam −1,3 ponto sozinhas no e-SNLI.
- **Estados internos no jeito 2 por ser "menos código" (recomendação do Claude de 16/11)** (17/11, derrubada pela
  leitura do MiniLM) — a diferença de código não existe; não repetir a justificativa.
- **"Mudar a atenção não muda a decisão" (frase do Claude, 10/11)** (15/11, derrubada pela literatura, nível 3, e
  pelo próprio controle) — a medida só cobre a última camada do `[CLS]`, média das cabeças, BERT small, RTE; em
  tarefas de par a atenção afeta a predição (Stacey et al. 2022; Vashishth et al. 2019) e a marca sorteada derruba a
  nota. Não repetir a frase sem esse escopo.
- **O Claude propor o rumo da Semana 10** (15/11, Pedro: "não quero uma sugestão sua de novo, já caí nesse erro") —
  responder o que ele perguntar e fazer o que ele pedir; opções só se ele pedir, sem ordenar nem recomendar.
- **Variação nova das marcas de atenção para ganhar nota (peso, camada, outro conjunto de teste)** (10/11, regra de
  parada aceita pelo Pedro antes do teste fora da distribuição) — o teste deu −0,004 com intervalo cruzando o zero.
  O destaque (apontar as palavras do LLM) é outra pergunta e segue aberta. **REABERTO EM PARTE (16/11, Pedro):**
  testar se mexer na atenção das outras camadas "muda alguma coisa (ablação)", e depois medir o (d). Só a camada foi
  reaberta; peso e outro conjunto de teste continuam fora. **Rodado em 16/11, nulo pelo critério escrito antes** (11
  combinações de camadas, maior diferença para o sem marcas +0,011; `leitura-grade.md`): a camada volta à regra de
  parada.
- **"As marcas empatam porque o modelo já olha para as palavras certas" (redundância, hipótese do Claude)** (10/11,
  derrubada por medida) — sem marcas a atenção do `[CLS]` nas palavras marcadas é 0,285; com marca real 0,805.
- **Ler ganho de 5 sementes abaixo de ~0,03 de ROC-AUC como sinal** (10/11, medido) — o mesmo treino na GPU varia
  até 0,026 entre rodadas; o +0,017 das marcas no small sumiu em 10 sementes novas.
- **Quantização como veículo novo agora** (10/11, Pedro: "isso n faz sentido, meter quantização no meio dessa
  bagunça") — ele quer resultado positivo com o trabalho atual, não trocar de técnica na véspera do gate.
- **Decoder fraco com gargalo no `[CLS]`** (10/11, Pedro: "parece só um monte de suposições, nada disso parece
  realmente concreto e worth it") — aposta sem evidência; a pesquisa de 10/11 também não achou obra que faça isso com
  justificativa de rótulo.
- **"O braço com decoder perde por ter menos treino de classificação" (H1 do Claude)** (10/11, derrubada por
  medida) — o controle de calendário deu 0,746 contra 0,736 do BERT cru; não propor de novo como explicação.
- **Entregar o nulo do decoder sem ter repetido o Agrawal** (10/11, professor via Pedro: "sem conseguir repetir, nem
  seu nulo eu considero") — nulo sem controle positivo pode ser bug; a condição original (BERT MS-MARCO) vem antes.
- **`google-t5/t5-base` como encoder classificador** (10/11, decisão do modo autônomo, registrada) — pré-treinado
  com RTE e MNLI supervisionados (cartão do HF); usar `google/t5-v1_1-base`.
- **Variante FC (premissa como turno de conversa) para o RTE** (09/11, Pedro: "descarta o FC") — não tirou a
  abertura "The text" (14/20, pior que a FP3) e piorou dois pares; a FA ficou.
- **Proibir no prompt a frase que se repete ("The text states")** (09/11, Pedro: "a solução não é proibir, como a gente
  já mediu") — a E4 do e-SNLI mostrou troca por sinônimo e erros de fato; tira-se o gatilho ou limpa-se depois (C).
- **Claude como gerador das justificativas do RTE** (09/11) — a Usage Policy proíbe saída como alvo de treino; espera a
  pergunta à Anthropic (`docs/2026-11-09-pergunta-anthropic-decoder.md`, não enviada).
- **Git Flow com `develop`** (08/11, proposta aceita pelo Pedro) — demais para uma pessoa em 3 semanas; fica `main`
  + branch `tipo/descricao` com PR.
- **mypy, `ruff format`, Docker, dependabot e cobertura mínima no repo** (08/11, proposta aceita pelo Pedro) — escala
  do ABIGS (sistema em produção); aqui é repo de pesquisa de uma pessoa. `ruff format` reescreveria o código antigo
  inteiro.
- **Distilling Step-by-Step como obra-base da replicação** (31/10, Pedro: "minha base *É* o Agrawal") — a replicação
  pedida pelo professor (aula de 31/10) sai do Agrawal 2025; o DSbS fica como origem do tema, não como base.
- **Contraste do SCOTT (Wang et al. 2023) para gerar ou pontuar as justificativas** (28/10, Pedro: "overcomplicate things") — exige outra passada do Qwen sobre o lote e só serviria para as opções pós-geração (filtro por template, reescrita). Registro em `docs/ideias-de-desenho.md`.
- **Variante D pura (uma frase, ≤ 25 palavras) como prompt final do Qwen** (21/10, Pedro: A/B "muito verbosas", mas na
  D "a qualidade caiu") — quer meio-termo puxando para a D; caminho em aberto: variante E com exemplos à la Wiegreffe 2022.
- **Circularidade como veto ou critério de aceite da justificativa** (20/10, Pedro: "preferência de veto minha, mas
  também 100% infundada") — nenhum paper mede dano ao aluno; sai da régua da rodada 0 e da hipótese da variante D.
- **Ajuste fino de BERT "por fazer" como trabalho da semana** (13/10, Pedro) — já fez várias vezes, não entrega
  nada; e só planejamento numa semana também não basta (o projeto já tinha 5 semanas de preparação).
- **Professor de pesos abertos (Qwen3) no lugar do Claude** (14/10, Pedro) — mantém o Claude, sem publicar pesos nem
  dataset; o argumento que sustenta é "o classificador NLI não é modelo concorrente" (Commercial Terms §D.4).
  Detalhe em `docs/2026-10-13-custo-racionalizacao-llm.md` §8. **REABERTO (20/10, Pedro):** o argumento do §D.4 caiu
  com a Usage Policy; o Claude como gerador fica arquivado por ora e o `Qwen/Qwen3.5-9B` vai a piloto.
- **Dataset do Agrawal como base do experimento** (14/10) — e-commerce proprietário; ESCI e GLUE sem justificativa
  humana. ESCI só como possível 2º conjunto de replicação.
- **Encoder já ajustado para NLI como ponto de partida** (14/10) — teto e contaminação com o SNLI; partir só do
  pré-treinado.
- **Item de termo descrevendo o rigor do método em vez do achado** (14/10, Pedro: "explicar demais a coisa errada") —
  regra 11 da skill `termogate`.

- **Montar mapa da área (mapa v1)** (05/10, Pedro) — "não é pra montar nenhum mapa"; a semana pede obras.
- **MobileBERT (2020) e Knowledge Distillation: A Survey (Gou, 2020) como leitura** (06/10, Pedro) — "6+ anos,
  muito desatualizado, serve apenas pra história quando eu quiser consultar".
- **História como pilar de leitura agora** (01/10, professor no gate 4) — não dá base neste ponto; foco em obras
  recentes com métodos e ferramentas atuais. Ver `docs/feedback-gate-4.md`.
- **Ampliar ou refazer o screening** (01/10, professor) — "você tem muito mais do que precisa"; das 91 surveys, 3–5 servem.
- **Agentes e LLM como método visível do processo** (01/10, professor) — "não quero ver mais nada de claude, gemini,
  chatgpt a não ser que seja uma necessidade real".

- **Método de leitura de 5 perguntas** (01/10) — o Pedro pediu "mais simples" querendo dizer **mais rápido com os
  mesmos ganhos**, não menos ganhos. Substituído pela caça dirigida em 5 paradas (`docs/metodo-de-leitura.md`).
- **Framework só como software (teste estreito do Claude)** (30/09) — Pedro: "é os dois". Diretriz/prática que
  prescreve decisão também é framework (§7.1 dos critérios).
- **Mapa por extração de taxonomias antes de ter a lista** (27/09) — sem tempo para o bottom-up completo. A lista sai
  do júri de surveys; o bottom-up do mapa foi movido para a leitura (`docs/leituras/mapa-divisoes.md`).

- **Regra do três por grupo (F2) quando o grupo é a própria área** (27/09) — só derruba grupo com 0 relevantes;
  com ~7% de relevância, 0 em 50 acontece 2,6% das vezes, e o grupo 2 (3.988 obras) contém 21/28 do gabarito.
  Resultado: 962 leituras e ~800 obras a menos de 12,5 mil. **Era calculável antes de rodar.** Regra nova:
  **contrato de funil** — toda etapa declara entrada, saída prevista com a conta, custo, sucesso e parada antes de
  rodar (`docs/screening/fase1/2026-09-27-plano-classificador.md` §1). Substituída por classificador obra a obra.

- **Endpoint em lote do Semantic Scholar (`/paper/batch`) como fonte única de referências** (23/09) —
  devolveu listas vazias para 63% das obras da camada C; obra a obra recupera parte, e as de editora
  (IEEE/Elsevier/ACM) seguem ocultas. Substituído pela união S2 (obra a obra) + OpenAlex.
- **Slides para o gate** (23/09) — Pedro: "nunca tem slides, sempre só o termo no projetor". Roteiro é
  fala sobre o termo; entregáveis sempre .docx.

- **Filtro de título por termo exato do pool como corte da floresta** (22/09) — recuperou só 36/58 do
  gabarito (62%): títulos usam formas curtas ("Transformer Compression", "Edge LLMs") e 8 surveys da
  área nem têm palavra de tipo no título. Radicais subiram para 79% no teste, mas dobraram o volume
  com ruído (`quant`->quantum); Pedro mandou "deixar tudo igual". Substituído pela limpeza em camadas.
- **Camada A "excluir quem não é Ciência da Computação"** (23/09) — inócuo: a busca já filtrou CS
  (118.637/118.659 têm CS). **E excluir Medicina/Educação/Matemática** — derrubaria cajuzeiros (4, 2 e 5
  dos 28 de ajuste têm esses campos).
- **Abstract como corte por palavra** (22/09) — 3.794 obras com termo núcleo no abstract, e as mais
  citadas eram ruído (*Vision Transformer*, *YOLOv11*, *Industry 5.0*). Abstract serve para julgar
  (escada), não para cortar 100 mil obras.
- **Aplicar classificação de grupos sem o Pedro revisar grupo a grupo** (23/09) — erro de processo do
  Claude na camada B (inclusive o ViT pendurado como pendente). Regra: proposta detalhada por grupo antes
  de qualquer marcação.
- **Amostra fixa de 30 por grupo na F2** (23/09) — a regra do três limita a proporção, não o número
  escondido, que cresce com o grupo (Hanley & Lippman-Hand 1983, sem tratamento de população finita).
  Substituída pela amostra por tamanho de grupo (50/40/30/proporcional/tudo).

- **Excluir paper cujo termo aparece só nas frases de abertura do resumo** (22/09) — técnica do
  Petersen et al. 2008 (§ sobre *variability*), testada sobre os 89 resumos do arXiv da execução 2:
  dos 7 nessa condição, **6 estavam dentro da área** e 1 fora. O mecanismo do nosso ruído é o inverso
  — survey de outro assunto com uma seção de eficiência cita o termo no **meio** do resumo. Não adotada. (Correção 22/09: o bulk do S2 **devolve** resumo quando o campo é pedido — a execução 2 não o pedia.)
- **`machine learning systems`, `benchmarking`, `toolkit` e `inference framework` no pool** (22/09) —
  medidos em 22/09: 56, 1.374, 116 e 3 retornos, todos ruído (o último devolve só *causal inference* —
  "inference" é ambíguo). Ficaram fora do grupo `ferramentas`.
- **Era (pré-LLM × pós-LLM) como divisão do mapa** (22/09) — escolha delegada pelo Pedro ao Claude
  para evitar viés dele. Divisão só existe se um survey aprovado a declarar (§9); "pré-LLM" é
  **periodização**, não técnica, e como divisão o mapa passaria a misturar dois eixos. Entra como
  **atributo** (coluna `era`) e, se o teste confirmar, como fato do **pilar história**.
- **Petersen puro como população do screening** (22/09) — 16.821 papers (área sem as palavras de
  tipo). É mapping study de verdade: mudaria §2, §6 e §7 inteiros e faria o mapa vir de keywording de
  papers primários em vez de taxonomia de survey. Fora por orçamento; a restrição fica declarada
  (pendência C1). Adotada a opção (b): surveys **sem piso de citação** (863 no S2).
- **Piso de citação como parâmetro de busca** (22/09) — é **idade disfarçada de qualidade**: os 8
  surveys mais citados das 58 da Fase 1 são todos de 2020–21. O piso passa a valer só no **registro**
  (§3.2, valor 60), depois da triagem de relevância.
- **Lista a priori de termos como taxonomia top-down** (17/09) — o próprio Pedro: "muito vaga para
  top-down literal; só palavras que vieram na cabeça, e eu não conheço da área". Virou pool de termos:
  vocabulário e registro de ponto de partida, não divisões. Top-down só no contorno (§1), bottom-up no
  conteúdo (§9 do método).
- **String de busca decretada (string-mãe fixa)** (17/09) — substituída pelo pool de termos versionado;
  a string é composição do pool, regenerada a cada versão. Motivo: a string v0 congelaria o vocabulário
  que o Pedro ainda não tem.
- **Espinha dorsal do mapa = taxonomia do survey mais recente (ou mais citado)** (16/09) — derrubada
  pelo Pedro: recência não garante qualidade e citação envelhece. Substituída por união com
  consolidação (§9 do método): ≥ 2 surveys consolidam, singular fica marcada, o Pedro mescla com motivo.
- **Degrau intermediário de procedência ("S — lido em nível de screening")** (15/09) — Pedro manteve a
  escala 3 → 2 → 1: o screening *é* o nível 3 (agente extrai), Claude lê inteiro (2), Pedro lê (1).
- **Interseção como regra do mapa (só divisão em que ≥ 2 surveys concordam desde o início)** (16/09)
  — perderia as divisões recentes, que só um survey cobre; nesta área o recente é o serving.
- **Novidade como critério de escolha ou defesa de tema** (11/09) — o professor/coordenador declarou
  que a Residência avalia processo, não inovação. A análise de 10/09 ("o que sobra de inédito após o
  Agrawal", a tabela de opções ranqueada por "risco de novidade" em `docs/pesquisa/tema-v4-opcoes-pos-agrawal.md`, a
  Parte 0 da `docs/residencia/preparacao-arguicao-gate.md`) foi feita sob a régua errada. O conteúdo factual (leituras,
  números, lacunas) continua válido; **o ranking e a moldura precisam ser refeitos** com a pergunta
  "qual opção ensina mais da especialização?" — depois que o Pedro nomear a especialização.
- **Apresentar o tema como fim** (11/09) — "muito produto", nas palavras do professor. O tema é veículo
  de uma especialização nomeada; a proposta precisa abrir por "o que estou me tornando", não por "de
  onde veio o tema".
- **H2, cabeça decodificadora auxiliar descartada na inferência, COMO CONTRIBUIÇÃO DE MECANISMO**
  (10/09) — **ocupada por Agrawal, Ahemad & Sembium, COLING 2025 Industry Track**
  (`aclanthology.org/2025.coling-industry.12`, Amazon): BERT base 110M + decoder T5 base como cabeça
  auxiliar, `L_total = L_cls + 0,1·L_aux`, decoder descartado na entrega; +6% em GLUE. A variante
  "Embedding-based Reasoning" deles ocupa também o H1. Eles ainda resolvem a pendência 9b (warmup em
  duas fases, decoder pré-treinado). **Sobrevive a pergunta do CONTROLE** — eles não rodaram
  racionalização embaralhada nem aleatória, nem avaliação fora de domínio. Ver
  `docs/artigos/notas-agrawal-coling2025.md` e a pendência 5 do `tema-v3`.
- **Triagem nível 3 como base para julgar novidade** (10/09) — o Agrawal estava em nível 3,
  classificado como "incógnita"; a triagem não pegou o mecanismo, e o mecanismo era o do tema. **Causa real, contada pelo Pedro em 23/09:** o agente **não conseguiu acessar** o paper, o aviso virou pendência solta e ficou parado até o Claude insistir — falha de processo. Regra nova: estado `sem acesso` com rotas automáticas e lista por volta (`docs/screening/fase1/2026-09-23-desenho-agentes.md`, M6). Nível 3
  serve para saber que o artigo existe, nunca para decidir se o espaço está livre.
- **NER como tarefa principal do tema v3** (10/09) — não é impedimento arquitetural (encoder rotula token nativamente), mas a maior parte das decisões de NER é superfície (maiúscula, contexto, formato); o efeito ficaria diluído nos poucos casos inferenciais, e a racionalização passaria a ser por span, elevando as partes móveis. Descartado por custo de detecção.
- **Geração de insight em prosa sobre documentos como aplicação do tema** (10/09) — é trabalho de decoder. Encoder produz rótulo ou trecho, não parágrafo. Sobrevive o vetor do H1 (agrupar, ordenar por confiança, sinalizar OOD), que é estrutura sobre acervo, não texto explicativo.
- **Narrar a troca de temas nos documentos de entrega** (10/09) — decisão de moldura do Pedro. Os critérios que saíram dos descartes entram declarados como critérios. A trilha permanece em `tema-escolhido.md` e `tema-v2-fusao-slm.md`.
- **Popular a proposta de tema com análise que o Pedro não leu** (10/09) — regra que passou a valer para todo documento assinado por ele: se ele não leu, não entra. Saíram da proposta a lista de aplicações industriais, a fórmula α/β/γ, o Herrewijnen, a tabela de riscos e a comparação metodológica com o time do Google.
- **Seção "os pesos da perda são busca de verdade"** na `docs/pesquisa/secao-dhrd-transferencia-encoder.md` (10/09) — não licenciava nada sobre a transferência para encoder, e duplicava conteúdo já registrado no `tema-v3`. Sobreviveu só a correção factual (α=β=1 vale para três modelos, não só os 8B).
- **Citar Li et al. (arXiv:2508.16777) como EACL 2026** (10/09) — o venue não se sustenta na fonte: o arXiv não traz campo *Comments* e o PDF usa template ACL genérico. Conferir na ACL Anthology antes de atribuir venue.
- **Rodapé de PDF como evidência de venue** (10/09) — a linha "39th Conference on NeurIPS 2025" no DHRD é o texto padrão do `neurips_2025.sty` e sai em qualquer submissão. O venue real (Efficient Reasoning Workshop) está no campo *Comments* do arXiv. Vale como regra geral.

- **Reanálise de resultado publicado como OBJETO de pesquisa próprio** (10/09) — exige julgar as premissas e análises de outros pesquisadores, o que demanda precisão extrema e não cabe numa primeira pesquisa. Continua válida como *interferência anterior* para ler e citar.
- **Tema v2, fusão de especialistas** (10/09) — o próprio Pedro derrubou o argumento de mercado: servidores já carregam vários adaptadores LoRA sobre uma base única, então fundir perde para trocar em quase todo cenário empresarial. Sobrevive só em borda, simultaneidade e organizações sem nuvem.
- **H1, regressão para o embedding da racionalização, COMO HIPÓTESE ISOLADA** (10/09) — mecanismo já ocupado: LRKD (arXiv:2601.21611, WWW'26) faz exatamente isso sobre um cross-encoder BERT. Lacuna restante é incremental. **Sobrevive como braço da ablação mesclada com H2** (ver `docs/pesquisa/tema-v3-racionalizacao-encoder.md`).
- **Lista de leitura deduplicada de 8 artigos** (10/09) — servia ao tema v2 (SLM/fusão); papers de eficiência de memória de modelo grande perderam função quando o tema foi para encoders. Nova lista em `docs/pesquisa/artigos-verificados.md`.
- **Seções de string de busca e de identificação de fundacionais** em `docs/pesquisa/metodo-busca-artigos.md` (09/09) — Pedro mandou desconsiderar para a busca de fronteira. Permanecem no arquivo, não foram removidas. **Reabertas pelo Pedro para outro propósito** — a Fase 2B (fundacionais) volta como critério de seminal no `docs/screening/metodo-screening-etapa1.md` §4 (15/09), e a string de busca volta como composição do `docs/screening/pool-termos-etapa1.md` (17/09), para mapa da área, não fronteira.
- Os 20 temas do `temas-candidatos.md` como estão (28/08) — nenhum passa na régua nova do Pedro: o tema precisa "gritar" para um empregador (mercado abstrato) "eu resolvo um problema seu" + carregar professional improvement (critério pessoal, não do edital). Temas pesquisa-primeiro (gap sintético→real etc.) reprovados por serem legíveis só para revisor.
- Usar o tema estacionado (datasets pt-BR jurídico) como critério de poda/decisão — era ideia solta; o foco é o pipeline de dados INTEIRO, com ênfase em estruturação/engenharia.
- Inverter âncora para ML (dados como satélite) — âncora ≠ plano de estudos; gap de ML se fecha via R1 (ver O6 em objecoes-e-respostas.md). Reabrir SÓ se Pedro preferir a lista B dos temas-candidatos.

- Pontuar os 289 tópicos linha a linha num painel único — rejeitado por custo; substituído pelo funil iterativo por macro.
- Config b2 (C9×C2 sem C1) — dominada pela config c (C9×C2×C1) em todos os critérios.
- Iniciar consolidação direto após o funil — excesso de notas altas (53 conceitos =3); poda vem primeiro.
- Dossiês de área para C3/C5/C7/C8 — sinal fraco no funil (amplo demais / perfil ferramenta); só sob demanda.
