# Fase do prompt: o que a literatura diz para gerar racionalizações de NLI / e-SNLI (19/10/2026)

**Escopo.** Pesquisa externa a pedido do Pedro, antes da rodada grande (~100 mil pares). Só informa; **não decide**. Termina em perguntas abertas.

## Aviso de procedência (ler primeiro)

**Nada deste arquivo é citável pelo Pedro sem ele ler a fonte.** Tudo aqui é nível 3 (agente). Etiquetas usadas na coluna "Proc.":

- **N3-abs**: nível 3, só abstract / página de metadados (arXiv, ACL Anthology, resultado de busca).
- **N3-txt**: nível 3, texto completo processado pelo agente por ferramenta de extração (ar5iv / HTML do arXiv), com as seções indicadas. **Números e formatos de prompt vêm do extrator e não foram conferidos linha a linha no PDF.** Podem ter erro de sumarização.
- **N2-proj**: nota nível 2 já existente no projeto (Claude leu o texto), usada só onde indicado.

**Conferência do Claude no PDF (19/10, só os trechos citados, não o paper inteiro):**
- **Wiegreffe 2022, Tab. 4 (p. 4):** e-SNLI, prompts crowd 30,8% · empate 26,8% · prompts dos autores 42,4%. São 250
  explicações e α = 0,5. É GPT-3 contra GPT-3, mudando só os exemplos do prompt. Bate com a §3.8.
- **Hase 2020, p. 5:** as explicações humanas vazam "about 97% of the time for e-SNLI" (pelo simulador T5). Bate com a
  §3.3. **Nuance que o relatório não trouxe:** a frase anterior diz que os autores *não* acham que vazamento torne
  uma explicação ruim, e o que importa para eles é o conteúdo semântico.

Convenções: "**Diz**" = o que o paper afirma (com seção/tabela quando o extrator deu). "**Inferência do agente**" = minha leitura, sem apoio direto no paper. Citações literais têm menos de 15 palavras.

**Não recomendado nem avaliado aqui (rejeitados no CLAUDE.md do projeto):** professor de pesos abertos no lugar do Claude; dataset do Agrawal; encoder já ajustado em NLI/SNLI. Artigos que usam professor aberto aparecem só como evidência sobre o prompt.

---

## 1. Verificação de existência (EXISTS-FIRST)

Todos conferidos em arXiv e/ou ACL Anthology nesta sessão. Venue vem da Anthology ou do campo *Comments* do arXiv, nunca de rodapé de PDF.

| Obra | Autores | Venue / ano | Como confirmei | Proc. |
|---|---|---|---|---|
| Reframing Human-AI Collaboration for Generating Free-Text Explanations | Wiegreffe, Hessel, Swayamdipta, Riedl, Choi | NAACL 2022, pp. 632-658 | Anthology 2022.naacl-main.47; arXiv 2112.08674 | N3-txt (§2, §3, §4, Apêndices A, E, F) |
| Few-Shot Self-Rationalization with Natural Language Prompts | Marasović, Beltagy, Downey, Peters | Findings of NAACL 2022, pp. 410-424 | Anthology 2022.findings-naacl.31; arXiv 2111.08284 | N3-txt (§2-§4, Tab. 1-5) |
| e-SNLI: Natural Language Inference with Natural Language Explanations | Camburu, Rocktäschel, Lukasiewicz, Blunsom | NeurIPS 2018 (campo *Comments*) | arXiv 1812.01193 | N3-txt (§3 = regras de anotação resumidas; Apêndice A = só os moldes filtrados. O texto integral das instruções do AMT não é público: nem no paper, nem no GitHub dos autores, conferido pelo Claude em 19/10) |
| Distilling Step-by-Step! | Hsieh et al. | Findings of ACL 2023 (*Comments*) | arXiv 2305.02301 | N3-txt (§3-§4, Tab. 1-2) |
| Large Language Models Are Reasoning Teachers | Ho, Schmid, Yun | ACL 2023 (Long), pp. 14852-14882 | Anthology 2023.acl-long.830; arXiv 2212.10071 | N3-txt (§3-§4, Tab. 1) |
| Investigating Mysteries of CoT-Augmented Distillation | Wadhwa, Amir, Wallace | EMNLP 2024 (*Comments* do arXiv 2406.14511) | arXiv | N3-txt (§2, RQ1-RQ3, Apêndices B-C) |
| NILE: Natural Language Inference with Faithful Natural Language Explanations | Kumar, Talukdar | ACL 2020, pp. 8730-8742 | Anthology 2020.acl-main.771; arXiv 2005.12116 | N3-txt (método e faithfulness) |
| SCOTT: Self-Consistent Chain-of-Thought Distillation | Wang, Wang, Li, Gao, Yin, Ren | ACL 2023 (Long), pp. 5546-5558 | Anthology 2023.acl-long.304; arXiv 2305.01879 | N3-txt (método, Tab. de avaliação humana) |
| Leakage-Adjusted Simulatability: Can Models Generate Non-Trivial Explanations of Their Behavior in Natural Language? | Hase, Zhang, Xie, Bansal | Findings of EMNLP 2020, pp. 4351-4367 | Anthology 2020.findings-emnlp.390; arXiv 2010.04119 | N3-txt (definição, custo, Tab. 3) |
| Measuring Association Between Labels and Free-Text Rationales | Wiegreffe, Marasović, Smith | EMNLP 2021 (main), pp. 10266-10284 | Anthology 2021.emnlp-main.804; arXiv 2010.12762 | **N3-abs** |
| REV: Information-Theoretic Evaluation of Free-Text Rationales | Chen, Brahman, Ren, Ji, Choi, Swayamdipta | ACL 2023 (Long), pp. 2007-2030 | Anthology 2023.acl-long.112; arXiv 2210.04982 | N3-txt (método, modelos, datasets) |
| RORA: Robust Free-Text Rationale Evaluation | Jiang, Lu, Chen, Khashabi, Van Durme, Liu | ACL 2024 (Long), pp. 1070-1087 | Anthology 2024.acl-long.60; arXiv 2402.18678 | N3-txt (método, Tab. 3) |
| The Unreliability of Explanations in Few-shot Prompting for Textual Reasoning | Ye, Durrett | NeurIPS 2022 (*Comments*) | arXiv 2205.03401 | N3-txt (usa e-SNLI) |
| Explanations from Large Language Models Make Small Reasoners Better | Li et al. (12 autores) | **venue não confirmado** (só arXiv 2210.06726, out/2022) | arXiv | N3-txt (§3-§4) |
| Can LLM-Generated Textual Explanations Enhance Model Classification Performance? An Empirical Study | Dhaini, Vladika, Erdogan, Attaoui, Kasneci | ICANN 2025 (*Comments* da v2); v1 13/08/2025, v2 11/11/2025 | arXiv 2508.09776 | N3-txt (lido a **v1** em HTML) + abstract v2 |
| Towards Efficient CoT Distillation: Self-Guided Rationale Selector (MoRSD) | Yan, Liu, Pan, Chen, Xiang, Tang | **venue não confirmado** (arXiv 2509.23574, 28/09/2025) | arXiv | **N3-abs** |
| Does Rationale Quality Matter? Enhancing Mental Disorder Detection via Selective Reasoning Distillation | Song, Lee, Shin, Cho, Ko, Park | **venue não confirmado** (arXiv 2505.20014, 26/05/2025) | arXiv | **N3-abs** |
| Concise Reasoning, Big Gains: Pruning Long Reasoning Trace with Difficulty-Aware Prompting | Wu et al. | **venue não confirmado** (arXiv 2505.19716, 26/05/2025) | arXiv | **N3-abs** |
| Rationale-Guided Distillation for E-Commerce Relevance Classification | Agrawal, Ahemad, Sembium | COLING 2025 Industry, pp. 136-148 | Anthology 2025.coling-industry.12 | **N2-proj** (`docs/artigos/notas-agrawal-coling2025.md`); Pedro leu |
| Evaluating Human Alignment and Model Faithfulness of LLM Rationale | Fayyaz, Yin, Sun, Peng | **venue não confirmado** (arXiv 2407.00219, jun/2024, v2 out/2024) | arXiv | N3-txt (só o prompt de e-SNLI, Tab. A.3) |

**Observações de existência.**
- O pedido listava Hase et al. como "Findings EMNLP 2020": confirmado. O título completo é o da tabela, e o 4º autor é Harry Xie.
- O arXiv 2406.14511 (Wadhwa) é o que o CLAUDE.md já cita; venue EMNLP 2024 vem do *Comments*.
- O abstract do Wiegreffe 2021 muda de redação entre a versão do arXiv (v4) e a da Anthology; citar a versão que ele ler.

---

## 2. Como os trabalhos promptaram LLMs para explicar NLI (Q1)

### 2.1 Quadro comparativo dos formatos

"Rótulo dado" = o prompt já contém o rótulo-ouro (racionalização pós-hoc). "Rótulo previsto" = o LLM prevê o rótulo e explica (CoT / predict-then-explain).

| Trabalho | Professor | Tarefa | Rótulo | Exemplos (nº, escolha) | Detalhes do prompt | Proc. |
|---|---|---|---|---|---|---|
| Wiegreffe 2022 | GPT-3 (versão exata não extraída) | **e-SNLI**, CSQA | **Dado** (chamado de "controle metodológico", §2 nota 3) | 12, 18 ou 24; tirados de 115 instâncias de treino aleatórias; **igual por rótulo**; ordem embaralhada; teto de 24 pelo limite de 2049 tokens (Apênd. A) | Abre com "Let's explain classification decisions."; formato de pergunta (hipótese como pergunta, "true, false, or neither?", "why?"). O enquadramento QA "achieved the best performance" (Apênd. A) | N3-txt |
| Marasović 2022 (FEB) | T5 / UnifiedQA / GPT-3 | **e-SNLI** + 3 | **Previsto**: saída "rótulo because explicação" (§3.1) | 16 por rótulo (48), balanceado (Tab. 1); no GPT-3, 28-45 demonstrações sorteadas dos 48 (§4) | Prompt final "explain nli hypothesis: ... premise: ..."; tags "premise:"/"hypothesis:" são "crucial" no e-SNLI (§3.1) | N3-txt |
| Hsieh 2023 (DSbS) | PaLM 540B | **e-SNLI**, ANLI, CQA, SVAMP | **Previsto**, racionalização **antes** do rótulo (Fig. 3) | ~10 por tarefa (Limitações); "when available" segue Wei et al., senão exemplos próprios; critério de escolha não dito | Tripla (entrada, racionalização, rótulo). O extrator **não achou** o texto do prompt de e-SNLI nem filtro por acerto; **ambos não verificados** | N3-txt |
| Li 2022 | GPT-3 text-davinci-002, guloso | CSQA, StrategyQA, OBQA (**sem e-SNLI**) | Três modos: **COTE** (previsto, só guarda se acertou), **RP** (rótulo dado, sem filtro), **CROP** (COTE, com RP de reserva) (§3) | 7 escritos por humanos por dataset | Rótulo antes da explicação no RP | N3-txt |
| Ho 2023 (Fine-tune-CoT) | InstructGPT text-davinci-002 | 12 tarefas, **sem NLI** (aritmética, CSQA, StrategyQA...) | **Previsto**; guarda se a resposta final bate com o ouro | zero-shot ("Let's think step by step") | **Várias amostras por pergunta**: T=0,7, D=8 (D=64 em MultiArith/SVAMP) | N3-txt |
| SCOTT 2023 | GPT-NeoX-20B | CSQA, StrategyQA, CREAK, QASC (**sem e-SNLI**) | **Dado** (resposta-ouro no contexto) + decodificação contrastiva | nº não extraído | Contraste entre gerar com a resposta-ouro e com resposta vazia/errada | N3-txt |
| Wadhwa 2024 | Mistral-7B-Instruct | CSQA, OBQA, QuaRel (**sem NLI**) | **Dado** ("elicited to support the correct answer", §2 nota 1) | 2 escritos à mão pelos autores (Apênd. B) | A racionalização de exemplo começa com "The answer is B because..." (restata o rótulo) | N3-txt |
| Ye & Durrett 2022 | OPT-175B, GPT-3, InstructGPT, text-davinci-002 | **e-SNLI**, Synth, AdvHotpot | E-P (explica→prevê) vs P-E (prevê→explica) | até 32 no e-SNLI, aleatórios, vários grupos; **vizinho mais próximo não ajudou** no e-SNLI com poucos dados | só o text-davinci-002 ganhou com explicação nas três tarefas | N3-txt |
| Dhaini 2025 | Gemma2-9B, Mistral-7B, Llama3-70B, GPT-4o mini; T=0 | **e-SNLI**, HealthFC | **Dado** (número do rótulo); instrução para **não revelar** o rótulo | zero-shot e few-shot de **4** exemplos do dataset | "Provide exactly one sentence that directly connects the premise to the hypothesis." Few-shot deu ganho "minor" nas métricas | N3-txt (v1) |
| Agrawal 2025 | Mixtral 8x7B Instruct | relevância de e-commerce (+GLUE) | **Dado** (query, produto, rótulo) + "Explain why" | nº de exemplos não registrado nas notas | ver notas do projeto | N2-proj |
| Camburu 2018 | humanos (AMT) | e-SNLI | rótulo dado | n/a | protocolo abaixo | N3-txt |
| NILE 2020 | GPT-2 medium treinado em e-SNLI | e-SNLI | **um gerador por rótulo** (3 explicações candidatas por par) | n/a (não é prompt) | ver §2.3 | N3-txt |

### 2.2 O protocolo humano do e-SNLI (Camburu 2018), que o prompt espelha

**Diz** (N3-txt, §3; os moldes estão no Apênd. A):
- Os anotadores deviam focar nos elementos "non-obvious" que induzem a relação e **não repetir** partes da premissa que aparecem idênticas na hipótese.
- Regras por rótulo: em **implicação**, justificar toda parte da hipótese que não está na premissa; em **neutro** e **contradição**, citar um elemento que contribui já basta.
- A explicação devia ser **autossuficiente** (fazer sentido sem reler o par).
- Primeiro **destacavam palavras** essenciais, depois escreviam usando-as; metade das palavras destacadas tinha de aparecer escrita igual. O navegador rejeitava explicação com menos de 3 tokens ou copiada da premissa/hipótese.
- 1 explicação por par no treino; 3 por par no dev/teste. 6.325 anotadores.
- Controle de qualidade: amostra de 1.000 explicações corrigidas à mão (nota 0-1); taxa de erro 9,62% (entailment 19,55%, neutro 7,26%, contradição 9,38%). **Explicações em formato de template foram refeitas (11% dos dados)**; templates listados no Apênd. A (por exemplo "Just because [premissa] doesn't mean [hipótese]").
- O paper **não** reporta comprimento médio, nem proíbe explicitamente repetir o rótulo (segundo o extrator).

**Inferência do agente.** (a) A instrução "diga o fato da premissa que decide" da variante D é parente da regra "elementos não óbvios" de Camburu. (b) O fluxo "destacar palavras, depois escrever" é um prompt em dois passos que ninguém, nos trabalhos lidos, usou com LLM para e-SNLI. (c) As definições de rótulo do prompt do piloto **não têm paralelo** em nenhum prompt acima; a instrução por rótulo existe só no protocolo humano de Camburu (regras de cobertura, não definições lógicas).

### 2.3 NILE e SCOTT: explicação por rótulo / contrafactual

- **NILE (diz, N3-txt):** um gerador por rótulo; no teste, os três geram explicação antes de qualquer decisão. Os autores observam que "the form for explanations of different labels is discriminative", ou seja, a forma da explicação entrega o rótulo, e tentam neutralizar isso com amostras negativas de mesma forma.
- **SCOTT (diz, N3-txt):** a decodificação contrastiva elevou, em 100 racionalizações de StrategyQA, "New Info" de 0,65 (guloso) para 0,77 (contraste com vazio) e 0,82 (contraste com resposta errada); "Supports Answer" de 0,48 para 0,58 e 0,63; gramática caiu pouco (0,99 para 0,97). Kappa de Fleiss 0,26. O aluno também treina com racionalizações contrafactuais (para resposta errada).
- **Inferência do agente:** o contraste exige acesso a probabilidades por token, que a API de mensagens do Claude não oferece; o análogo implementável seria só "gerar uma explicação para cada um dos 3 rótulos" (3x o custo), sem o contraste.

### 2.4 Trabalhos de 2024-2026 sobre destilação de racionalização com estudo de prompt ou qualidade

- **Dhaini 2025 (ICANN):** o mais próximo do desafio, mas as explicações entram como **texto de entrada** (anexadas à hipótese), não como alvo auxiliar. **Diz (v1, N3-txt):** PLMs (BERT, DeBERTa, RoBERTa, ModernBERT) com explicação de LLM ganham de 0,08 a 0,19 de acurácia sobre sem explicação, mas ficam 0,10-0,21 abaixo da explicação humana, "especialmente no e-SNLI". **Contradição:** o abstract da v2 diz que as automáticas são "tão boas quanto" as humanas. Li a v1; a v2 pode ter outros números. Conferir as duas.
- **MoRSD 2025 (N3-abs):** seleciona racionalizações por acerto, diversidade e "dificuldade" (quão bem o aluno acerta com aquela racionalização); relata +4,6% médio em 7 datasets com menos racionalizações. Não li método nem datasets.
- **Song et al. 2025 (N3-abs):** seleção de racionalizações por alinhamento com raciocínio clínico de especialista melhora o aluno em saúde mental. Domínio distante.
- **Wu et al. 2025, Concise Reasoning (N3-abs):** em raciocínio longo de matemática (decoder, 720 tokens médios), traços podados rendem aluno igual ou melhor com 8x menos dados. Regime diferente do e-SNLI, só indicativo.
- **Henrichsen & Krebs 2025, arXiv 2507.00214 (N3-txt, verificado):** Llama-3.2-1B gera "raciocínio + rótulo" e ganha +8,7 pontos em emoção, mas o aluno é **decoder** e o raciocínio vem de um gerador que vê o rótulo-ouro; os autores não discutem vazamento. Citado só como beco: não testa encoder nem prompt.
- **Não encontrei** estudo de racionalização de LLM como alvo auxiliar de **encoder-only** em NLI com variação de prompt. (Busca em arXiv/web; ausência não é prova.)

---

## 3. Quais propriedades da racionalização ajudam o ALUNO (Q2)

Distinção: a maior parte da literatura mede qualidade **para o leitor humano** (plausibilidade, gramática). O que importa aqui é o efeito na acurácia do aluno. **Não achei paper que valide que uma métrica de qualidade humana ou de vazamento prevê o ganho do aluno** (inferência do agente, por ausência).

### 3.1 Comprimento

- **Wadhwa 2024 (diz, N3-txt, RQ1-RQ3):** com a racionalização **depois** do rótulo, embaralhar os tokens quase não muda (Tab. 2: por exemplo GPT-2 CSQA 70,92 → 69,56); mascarar só derruba o ganho acima de 60%; **15 tokens de maior atribuição** igualam a racionalização inteira de ~36,3 tokens (Tab. 3). Preencher com `<unk>` ajuda um pouco e satura em ~11 tokens, sem passar do CoT. Conclusão deles: não precisa ser coerente, mas os tokens têm de "offer additional signal"; palavras similares por Word2Vec ficam no nível de sem-CoT.
- **Importante (diz):** esses resultados valem para aluno **decoder-only** que gera a racionalização depois do rótulo, em QA de múltipla escolha, sem NLI. O CLAUDE.md já registra que isso é o controle que o tema v3 pergunta se vale para encoder.
- **Camburu 2018:** a referência humana tem ~12 palavras (medida do projeto, não do paper) e é parte da definição do dataset; nenhum paper lido varia o comprimento da racionalização de e-SNLI e mede o aluno.
- **Inferência do agente:** pelo Wadhwa, o conteúdo semântico pode importar menos que o esperado quando o alvo vem após o rótulo; então o comprimento seria sobretudo alavanca de **custo** (dois terços do custo do Sonnet é saída, `docs/2026-10-19-geracao-dataset-prompt-e-licenca.md` §1.1). Risco inverso: se todas as variantes empatarem no aluno, a escolha do prompt vira escolha de custo e de qualidade para leitor.

### 3.2 Especificidade / informação nova

- **Wiegreffe 2022 (diz, §3, Fig. 3):** as explicações do GPT-3 eram boas em factualidade e gramática, mas fracas em "New Info" e em "Supports Label". Isso motivou o filtro.
- **Wadhwa (diz):** vale só o que carrega sinal adicional (controle Word2Vec).
- **Camburu (diz):** explicações em template eram tratadas como não informativas e refeitas.
- **Inferência do agente:** a paráfrase da definição do rótulo no piloto é, em tese, o caso de "forma sem informação nova"; mas nenhum paper testa se isso piora o aluno.

### 3.3 Vazamento do rótulo / circularidade

- **Hase 2020 (diz, N3-txt):** as explicações **humanas** do e-SNLI vazam o rótulo "about 97% of the time" (simulador T5). Ou seja, o vazamento no e-SNLI é praticamente a norma, inclusive no ouro. Isso reforça o NILE ("a forma entrega o rótulo").
- **RORA (diz):** as métricas anteriores ficam inflacionadas por racionalizações que repetem o rótulo ou a pergunta; REV deu a racionalização "leaky" 0,147 contra -0,038 do ouro em StrategyQA (Tab. 3 do RORA).
- **Wadhwa (diz):** a racionalização do professor já restata a resposta ("The answer is B because...") e mesmo assim melhora o aluno. O paper não discute vazamento.
- **Contradição entre literaturas.** Avaliação (Hase, RORA, REV) trata vazamento como defeito da **métrica**; destilação (DSbS, Wadhwa, Agrawal) nunca remove o rótulo da racionalização e ganha. Nenhum paper lido mede se vazamento prejudica um aluno que usa a racionalização como alvo auxiliar.
- **Inferência do agente (hipótese, não testada):** como o decoder é treinado com forçamento do professor e a perda é só sobre os tokens da racionalização, um alvo que carrega o rótulo pode funcionar como sinal de rótulo redundante, e não como sinal novo. Esse é o motivo teórico para medir vazamento, mas o dano real é desconhecido.

### 3.4 Fidelidade / factualidade

- **Ye & Durrett 2022 (diz):** no e-SNLI, explicação não factual é sinal de resposta errada; com um calibrador simples, P-E chegou a 68,5% com 128 exemplos (~12 pontos acima do few-shot sem calibrar). Explicações eram consistentes com a resposta prevista em mais de 80% dos casos.
- **SCOTT (diz):** aluno treinado com racionalização contrastiva + contrafactual fica mais fiel (LAS); acurácia comparável. Só valia para aluno que gera racionalização **na inferência**.
- **Inferência do agente:** com a cabeça descartada na inferência, fidelidade "da racionalização ao raciocínio do aluno" não é o alvo; o que importa é a racionalização ser **correta e informativa sobre o par** (factualidade). Nenhum paper isola isso para aluno encoder.

### 3.5 Diversidade (várias racionalizações por par)

- **Ho 2023 (diz, Tab. 1):** D=8 amostras por pergunta (T=0,7), todas as que acertam viram exemplos. Em GPT-3 6,7B: MultiArith 33,33 → 53,33; SVAMP 12,67 → 30,33 (D=64). É aritmética e aluno gerador; **não é classificação com cabeça auxiliar**.
- **MoRSD (abstract):** seleção que inclui diversidade reduz o volume e melhora o aluno. Método não lido.
- **Wiegreffe 2022 (diz, §3):** no SNLI, 3/3 anotadores aceitaram 31,5% das explicações **gulosas** e só 11,3% das **amostradas**; pelo menos uma aceitável entre as 5 candidatas: 51,2%. Ou seja, amostrar mais barato custa qualidade média, e a seleção importa.

### 3.6 Pós-hoc (rótulo dado) vs pré-hoc (previsto)

- **Wadhwa (diz):** a posição da racionalização **depois do rótulo** vence a de antes em todos os modelos e datasets (Tab. 1, por exemplo Gemma-2B QuaRel 74,90 antes → 78,16 depois). Isso é ordem de saída de um decoder, não "rótulo no prompt do professor".
- **Ye & Durrett (diz):** explicar→prever vs prever→explicar: só o text-davinci-002 teve ganho consistente; efeito depende do modelo.
- **Li 2022 (diz):** os três modos (COTE, RP, CROP) vencem o ajuste fino simples; melhor resultado CSQA 64,50 (MT-Ra com CROP) contra 63,05. **Não extraí a comparação direta RP vs COTE.**
- **Wiegreffe 2022 (diz):** deram o rótulo-ouro de propósito, para avaliar a explicação mesmo quando o modelo erraria. É a justificativa metodológica do modo "rótulo dado".
- **Inferência do agente:** no modo "rótulo dado" o professor explica um rótulo ouro possivelmente ruidoso do SNLI sem poder discordar; no modo "previsto + filtro por acerto" (COTE, Ho) os pares difíceis tendem a sair do treino. Nenhum dos papers mede esse viés em e-SNLI.

### 3.7 Tamanho do professor

- **DSbS (diz, Tab. 1, T5-base, dados completos):** e-SNLI: ajuste fino 88,38; DSbS com racionalização do PaLM 540B 89,51; com GPT-NeoX 20B 89,12. ANLI: 43,58 / 49,58 / 48,15. Treino single-task (racionalização+rótulo numa saída) pior que multitarefa nos quatro datasets. Os autores só **hipotetizam** que o PaLM dá racionalizações melhores (sem ablação).
- **Inferência do agente:** no e-SNLI a diferença entre um professor de 20B e um de 540B foi ~0,4 ponto, de um só experimento; sugere pouca sensibilidade ao professor, mas não responde Haiku vs Sonnet.

### 3.8 Referência humana como alvo

- **Wiegreffe 2022 (diz, Tab. 3-5):** com exemplos crowd do e-SNLI no prompt, crowd 63,6% vs GPT-3 24,8% (empate 11,6%); com exemplos reescritos pelos autores, o prompt dos autores bate o crowd 42,4% a 30,8% (Tab. 4) e, contra o ouro, GPT-3 40,7% vs ouro 49,6% (Tab. 5). **O e-SNLI foi o dataset mais difícil.** Ou seja, **exemplos de e-SNLI humano no prompt rendem explicações piores que exemplos reescritos com cuidado.**
- **Marasović (diz, Tab. 5):** plausibilidade humana: ouro 77,4; GPT-3 42,4; para implicação o GPT-3 fica em ~27 vs 63,5 do ouro.
- **Contexto do piloto (do Pedro):** o piloto achou 7/20 humanas "ruins" e preferiu Sonnet em 14/20. Os dois trabalhos acima eram com GPT-3; não é contradição direta, mas os números de 2022 não valem para um professor de 2026.

---

## 4. Métricas de vazamento / circularidade para comparar variantes (Q3)

Todas existem nos nomes e venues da §1. Tabela de uso prático. "Laptop" é **inferência do agente** sobre RTX 5060 8GB; **nada foi testado**.

| Métrica | O que mede (diz) | O que exige | Custo / hardware citado no paper | Cabe no laptop? (inferência) | Proc. |
|---|---|---|---|---|---|
| **LAS** (Hase 2020) | Quanto a explicação ajuda um observador a prever a saída do modelo, separando os casos em que a explicação sozinha já revela a resposta. LAS = ½(LAS₀ + LAS₁), com grupos "vaza" e "não vaza" | Simulador **T5-base** treinado para prever ŷ de (x, e), com dropout de x ou e. O próprio indicador de vazamento é "o simulador acerta ŷ só com a explicação" | Paper treinou modelos de tarefa em uma **T4**: ~24h a 5 dias, só 10% do SNLI nos principais. O custo era dos modelos da tarefa, não do simulador. Código no GitHub dos autores (peterbhase/LAS-NL-Explanations, citado pela busca) | Só o simulador T5-base **provavelmente** cabe; mas LAS foi definido para explicar o **comportamento de um modelo**, e aqui há um professor gerando racionalização do rótulo-ouro. Exigiria adaptar. Valores não são comparáveis entre datasets (diz) | N3-txt |
| **Indicador de vazamento isolado** (parte do LAS e do 1º estágio do RORA) | O rótulo é recuperável **só da racionalização** | Qualquer classificador rótulo-a-partir-da-racionalização: no RORA é um modelo pequeno (FastText) com Integrated Gradients | RORA: T5-base nos demais estágios | **Sim, com folga**: TF-IDF + regressão logística treina em segundos em CPU; ou BERT pequeno. É a versão mais barata. Para comparar variantes entre si, não em valor absoluto: o ouro humano do e-SNLI já vaza ~97% pelo T5 | N3-txt (parte) |
| **Wiegreffe 2021** (associação rótulo-racionalização) | Se um modelo conjunto "prevê e racionaliza" tem rótulo e racionalização associados: *robustness equivalence* e *feature importance agreement* | Modelos T5 treinados para prever e racionalizar | não extraído (só abstract) | **Não serve para comparar prompts**: avalia um modelo treinado, não a racionalização do professor (inferência do agente) | **N3-abs** |
| **REV** (Chen 2023) | Informação **nova** e relevante ao rótulo na racionalização, além da entrada e do rótulo (V-informação condicional). Média de -log g′[b](y) + log g[r,b](y) | **Dois avaliadores T5-Large** ajustados em exemplos com racionalização humana (no e-SNLI, 10% do treino), mais uma "racionalização vazia" (baseline) construída por template e paráfrase | Uma NVIDIA RTX 8000; até 20 épocas, lr 5e-6, batch 8 | **Dificilmente**: T5-Large ×2 em 8GB só com truncamento agressivo/quantização/LoRA (inferência não testada). Limites declarados: pode premiar racionalização de predição errada; não mede factualidade; depende da qualidade da racionalização humana usada para treinar o avaliador | N3-txt |
| **RORA** (Jiang 2024) | Informação nova do rótulo, **robusta a vazamento**: detecta tokens que vazam, gera contrafactuais por infilling (MICE, T5-base) e treina o avaliador com IRM | 3 estágios (detector, infiller, avaliador T5-base) | hardware não relatado; lr, épocas e λ=10 dados | **Pipeline pesado de montar** para o benefício. Correlação instância-a-instância com humanos: RORA r=0,36, REV r=0,05 (Tab. 3, StrategyQA). Datasets: StrategyQA, ECQA, CoS-E; **o extrator não viu e-SNLI**. Disponibilidade do código **não verificada** | N3-txt |

**Observações.**
- O RORA mostra que, com racionalização com vazamento, o **LAS fica indefinido** (NaN em StrategyQA) ou premia o vazamento (ECQA: 0,506 vs 0,365 do ouro). Cuidado ao usar LAS num cenário em que o vazamento é alto.
- **Inferência do agente.** A rota barata é a do indicador isolado: um classificador rótulo-pela-racionalização treinado nas racionalizações da própria variante, mais as checagens já planejadas (nome do rótulo, paráfrase de definição, taxa de cópia). O ponto do `docs/2026-10-19-geracao-dataset-prompt-e-licenca.md` §1.3 (Haiku adivinha o rótulo só pela racionalização) é a mesma ideia com um classificador de LLM; a citação "Hase et al. 2020, Findings of EMNLP" **foi conferida aqui e existe**.
- Todas essas métricas medem a racionalização **para o leitor ou para um avaliador**. Nenhuma foi correlacionada, nos papers lidos, ao ganho de um aluno que usa a racionalização como alvo auxiliar.

---

## 5. Protocolo para comparar variantes antes da rodada grande (Q4)

### 5.1 Tamanhos de amostra usados na literatura (avaliação humana)

| Trabalho | Amostra | Anotadores | Proc. |
|---|---|---|---|
| Camburu 2018 | 1.000 explicações do próprio dataset, nota 0-1 com crédito parcial, por controle de qualidade | os autores | N3-txt |
| Marasović 2022 | 360 exemplos (6 por divisão × 60 divisões; 2 por rótulo no e-SNLI), plausibilidade | 3 por exemplo; kappa de Fleiss 0,54-0,73 por modelo | N3-txt |
| Wiegreffe 2022 | ~1.241 instâncias SNLI, ~6.200 pares instância-explicação, ~19 mil notas binárias de aceitabilidade; avaliação por atributos em **91** instâncias de NLI | 3 por par; exame de qualificação NLI (≥7/8) | N3-txt |
| NILE 2020 | primeiros 100 exemplos do teste SNLI | 5 não especialistas | N3-txt |
| Li 2022 | 100 exemplos de CSQA (preferência) | n/d | N3-txt |
| SCOTT 2023 | 100 racionalizações de StrategyQA; kappa 0,26 | n/d | N3-txt |
| REV 2023 | 230 exemplos de ECQA | n/d | N3-txt |
| RORA 2024 | 229 instâncias de StrategyQA | 3 por racionalização | N3-txt |

**Inferência do agente.** Nos papers lidos, 90-360 itens é o intervalo comum; o piloto do Pedro (n=20, cego) está abaixo dele. Com n=20, o intervalo de 95% de uma proporção (normal, p≈0,5) tem ±22 pontos; só diferenças enormes como 14/20 vs 3/20 se sustentam. Para variantes próximas, 20 itens não discriminam. O plano de 3-4 variantes sobre ~300 pares, com checagem automática em todos e avaliação cega em ~20 por finalista, já está no documento de 19/10; este achado só mostra a distância para o que os papers fizeram.

### 5.2 Filtro automático / seleção

- **Filtro de aceitabilidade (Wiegreffe 2022, diz):** T0-3B ajustado com 5 sementes em ~6,2 mil pares anotados 3x. No SNLI, seleção de 1 explicação entre 5: acurácia 38,7% (3/3) no teste, contra 32,0% pelo NLL do GPT-3 e 14,7% ao acaso, com teto (oráculo) de 52,4%. Após filtro, na comparação com o ouro: ouro 49,9% vs GPT-3 43,2% (Tab. 9). O ganho **no SNLI foi pequeno**: só 36,4% das explicações mudaram.
- **Inferência do agente:** esse filtro depende de ~19 mil anotações humanas e de um T0-3B; não é reproduzível aqui. O análogo barato nos papers lidos é: (a) filtrar por acerto do rótulo previsto (Li COTE, Ho); (b) regras por script (comprimento, cópia, nome do rótulo); (c) juiz-LLM. **Não achei neste levantamento um estudo validando juiz-LLM de explicação de NLI**; não afirmo que funcione.
- **Amostragem múltipla + seleção:** Wiegreffe (1 gulosa + 4 amostradas) e Ho (D=8). Nos dois, amostrar é um passo **de seleção posterior**, não um ganho grátis: no SNLI as amostradas eram muito piores em média que a gulosa (11,3% vs 31,5% aceitáveis).
- **Teto metodológico do piloto (Ye & Durrett, diz):** a estrutura do prompt altera o resultado por modelo; só um dos quatro modelos testados ganhou com explicação nas três tarefas. Resultado de prompt não se transfere de professor para professor.

### 5.3 O gargalo: proxy vs resultado do aluno

**Inferência do agente.** Nenhum paper lido mostra que a ordem das variantes por qualidade de leitor ou por vazamento coincide com a ordem pela acurácia do aluno. Em Wadhwa, racionalização embaralhada (conteúdo destruído) iguala a original para aluno decoder. Se o mesmo valer para encoder, as variantes empatariam no aluno apesar de diferenças grandes de qualidade. Isso não pode ser concluído da literatura para encoder; é a pergunta do tema v3 (H2 + controle embaralhado).

---

## 6. O que isso muda no protocolo (Q5)

Apresentado como opções com evidência, **não como decisão**.

### 6.1 Mapeamento das variantes planejadas

| Variante | O que a literatura lida diz | O que ela **não** diz |
|---|---|---|
| **A**: prompt do piloto | Rótulo-ouro no prompt é a prática de Wiegreffe, Wadhwa, Agrawal, Dhaini. Dhaini também manda não revelar o rótulo e limita a uma frase. | Nenhum paper lido põe definições de rótulo no prompt. |
| **B**: sem definições | Combina com Wiegreffe (formato de pergunta, sem definições), Marasović (só tags), Dhaini (zero-shot sem definição). Remove a fonte da paráfrase circular observada. | Ninguém mediu se a definição melhora a correção em NLI. Esse é um teste que só o piloto pode dar. |
| **C**: B + exemplos escolhidos pelo Pedro | Wiegreffe: exemplos escritos com cuidado venceram os crowd do e-SNLI (42,4 vs 30,8%, Tab. 4), e exemplos crowd do e-SNLI no prompt rendiam explicações piores. Nº de exemplos usados: 2 (Wadhwa), 4 (Dhaini), 7 (Li), ~10 (DSbS), 12-24 (Wiegreffe), 16 por rótulo (Marasović). Norma: **balanceado por rótulo**, ordem embaralhada. Ye & Durrett: escolher por vizinhança **não ajudou** no e-SNLI. Dhaini: few-shot trouxe só ganho "minor" nas métricas. | Ninguém comparou exemplos escolhidos à mão com aleatórios no mesmo número de exemplos. Risco (inferência): os exemplos fixam tom e comprimento, e o Wiegreffe sugere que exemplos de 12 palavras em template podem ensinar o vazamento por forma (Hase: 97%). |
| **D**: C + limite de comprimento + "o fato da premissa que decide" | A instrução espelha a regra de Camburu de focar no "non-obvious" e a de uma frase de Dhaini. Comprimento como alavanca de custo (ver §3.1). | Nenhum paper isola o efeito do comprimento sobre aluno **encoder** em e-SNLI; Wadhwa (decoder) sugere pouca sensibilidade após o rótulo. Agrawal usou ~12 tokens sem estudo de comprimento (N2-proj). |

### 6.2 Variantes que a literatura sugere e que não estão no plano

1. **Prever e explicar, filtrando por acerto (COTE, Li 2022; Ho 2023; DSbS).** O professor recebe só o par, prevê o rótulo e explica; fica o que bate com o ouro. Custo: nenhum extra relevante. Ganho possível: a racionalização não nasce condicionada ao rótulo. Perde os pares que o modelo erra (viés para pares fáceis, inferência). Há também o desenho CROP (previsto, com reserva em rótulo dado).
2. **Várias racionalizações por par (Ho 2023, D=8, T=0,7).** Custa D vezes. Pelo documento de 19/10, o Haiku sai ~US$ 3,50 por 100 mil, então ~US$ 28 com D=8 (conta do agente a partir desses números). Evidência só em aritmética e aluno gerador; seleção posterior importa (Wiegreffe: amostradas pioram a média).
3. **Racionalização por rótulo / contrafactual (NILE, SCOTT).** Gerar uma por rótulo (3×). Serve ao aluno que usa a racionalização para discriminar; para uma cabeça auxiliar descartada, **o uso não é claro** (inferência). O contraste de SCOTT depende de probabilidades por token, indisponíveis na API de mensagens (inferência a verificar).
4. **Destacar e explicar (Camburu).** Dois passos como no protocolo humano; o Wadhwa mostra que 15 tokens de maior atribuição igualam a racionalização inteira. Combina com alvo curto. Nenhum paper usou isso com LLM em e-SNLI.
5. **Portão de vazamento por classificador rótulo-pela-racionalização** (§4), aplicado igual a todas as variantes e ao e-SNLI humano como referência (que vaza ~97%). Barato e sem treinar nada pesado.
6. **Controles no aluno, não no prompt** (já no tema v3): racionalização embaralhada (Wadhwa) e **alvo humano do e-SNLI** como braço (Dhaini v1: humano ganha da LLM como entrada). Citados porque o proxy da §5.3 não substitui o teste no aluno.
7. **Seleção por utilidade ao aluno (MoRSD)**, que pontua a racionalização pela facilidade com que o aluno acerta com ela. É a única idéia de "medir a racionalização pelo aluno" que encontrei; só li o abstract.

---

## 7. Becos sem saída e limites desta pesquisa

- **DSbS: texto do prompt de e-SNLI** e se há filtro por acerto: o extrator não achou em HTML nem em ar5iv. Os PDFs vieram binários; `pdftoppm` não está instalado, então não li PDF direto. Isso **não foi verificado**.
- **NILE e Wiegreffe PDFs**: lidos só via ar5iv (HTML). Wiegreffe: o apêndice sobre instruções de aceitabilidade não apareceu.
- **Hase 2020, Camburu 2018, Marasović 2022, DSbS**: números dos extratores; podem conter erro de sumarização.
- **Fayyaz 2024** usa racionalização extrativa (palavras destacadas), não texto livre; só ajudou a mostrar o formato do prompt de e-SNLI com rótulo-ouro. Fora do núcleo.
- **MDPI Information 17(2):119 (Wang & Liu, jan/2026, "EGM-PM", dataset ExNLI)**: existe (Crossref DOI 10.3390/INFO17020119, por busca), mas a página devolveu 403. Resumo só por snippet de busca, **não usei como evidência**.
- **Busca de aluno encoder com cabeça auxiliar e racionalização de LLM em NLI**: não achei. Achei RAKSHAK (arXiv 2607.20450, DeBERTa multitarefa para intenção tóxica, ShriNep@EEUCA 2026), mas o PDF veio ilegível: **só o título e autores foram verificados**, o conteúdo não.

---

## 8. Perguntas abertas para o Pedro

1. As definições de rótulo (A vs B) são mais um teste do **piloto** que de literatura. Que métrica define "melhor" aqui: menor paráfrase, menos erro, menos vazamento?
2. Vazamento é defeito para o aluno ou não? A literatura lida não responde, e o ouro humano já vaza ~97%. O objetivo é igualar o humano ou ficar abaixo?
3. Rótulo dado (pós-hoc) ou previsto com filtro por acerto: o prompt de rótulo previsto muda quais pares chegam ao treino. Entra como variante?
4. Quantas racionalizações por par (1 ou várias), considerando que o ganho publicado é em aritmética e aluno gerador?
5. O limite de comprimento é decisão de custo ou de efeito no aluno? A evidência só sustenta custo.
6. Tamanho da avaliação cega: 20 por finalista basta para o que ele quer decidir?
7. Quer um teste curto no aluno (por exemplo, treino pequeno por variante) para validar o proxy, ou aceita decidir só pelas métricas do texto?

---

## 9. Fontes

Metadados e venues (Anthology / arXiv):
- Wiegreffe et al. 2022: https://aclanthology.org/2022.naacl-main.47/ · https://arxiv.org/abs/2112.08674
- Marasović et al. 2022: https://aclanthology.org/2022.findings-naacl.31/ · https://arxiv.org/abs/2111.08284
- Camburu et al. 2018: https://arxiv.org/abs/1812.01193
- Hsieh et al. 2023: https://arxiv.org/abs/2305.02301
- Ho et al. 2023: https://aclanthology.org/2023.acl-long.830/ · https://arxiv.org/abs/2212.10071
- Wadhwa et al. 2024: https://arxiv.org/abs/2406.14511 · https://arxiv.org/html/2406.14511v2
- Kumar & Talukdar 2020 (NILE): https://aclanthology.org/2020.acl-main.771 · https://arxiv.org/abs/2005.12116
- Wang et al. 2023 (SCOTT): https://aclanthology.org/2023.acl-long.304/ · https://arxiv.org/abs/2305.01879
- Hase et al. 2020 (LAS): https://aclanthology.org/2020.findings-emnlp.390 · https://arxiv.org/abs/2010.04119
- Wiegreffe et al. 2021: https://aclanthology.org/2021.emnlp-main.804 · https://arxiv.org/abs/2010.12762
- Chen et al. 2023 (REV): https://aclanthology.org/2023.acl-long.112 · https://arxiv.org/abs/2210.04982
- Jiang et al. 2024 (RORA): https://aclanthology.org/2024.acl-long.60 · https://arxiv.org/abs/2402.18678
- Ye & Durrett 2022: https://arxiv.org/abs/2205.03401
- Li et al. 2022: https://arxiv.org/abs/2210.06726
- Dhaini et al. 2025: https://arxiv.org/abs/2508.09776
- Yan et al. 2025 (MoRSD): https://arxiv.org/abs/2509.23574
- Song et al. 2025: https://arxiv.org/abs/2505.20014
- Wu et al. 2025: https://arxiv.org/abs/2505.19716
- Henrichsen & Krebs 2025: https://arxiv.org/abs/2507.00214
- Fayyaz et al. 2024: https://arxiv.org/abs/2407.00219
- Agrawal et al. 2025: https://aclanthology.org/2025.coling-industry.12/
- Wang & Liu 2026 (MDPI, só existência por busca): https://www.mdpi.com/2078-2489/17/2/119
- RAKSHAK (só título/autores): https://arxiv.org/abs/2607.20450

Arquivos do projeto usados: `docs/artigos/notas-agrawal-coling2025.md`; `docs/2026-10-19-geracao-dataset-prompt-e-licenca.md`.
