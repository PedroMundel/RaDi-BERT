# Filtro de evidência com encoder pequeno na frente de um LLM leitor

Data: 15/11/2026. Pesquisa de literatura e viabilidade (uma semana, uma pessoa, RTX 5060 8 GB).

## Procedência

Pesquisa **nível 3**: um agente leu abstracts, páginas HTML de arXiv e tabelas extraídas por ferramenta de fetch. Serve para triagem, **nunca para citação**. Números abaixo vêm de extração automática de tabelas; conferir na fonte antes de usar em texto assinado.

| Item | Como foi aberto |
|---|---|
| Shi et al. 2023 (GSM-IC) | HTML ar5iv, tabelas 2 e 3 |
| Yoran et al. 2024 | HTML arXiv v2, tabelas 2, 6, 7 |
| Wu et al. 2024 (irrelevant inputs) | HTML arXiv v2 |
| Cuconasu et al. 2024 (Power of Noise) | HTML arXiv v4 |
| Chen et al. 2024 (RGB) | HTML arXiv, tabela de ruído |
| Liu et al. 2024 (Lost in the Middle) | HTML arXiv, tabela 1 e 6 |
| RECOMP | HTML arXiv v1, tabela principal de QA |
| FILCO | HTML arXiv v1, tabela 5 |
| Provence | HTML arXiv, tabelas e apêndice |
| EXIT | HTML arXiv v3, só os primeiros 100 mil caracteres (apêndices finais não lidos) |
| CompAct | HTML arXiv v2, tabela 2 |
| LLMLingua-2 | HTML arXiv v2 |
| CPC (arXiv:2409.01227) | HTML arXiv v1 |
| LLMLingua, Selective Context | **só resultado de busca** (título, autores, venue, resumo); tabelas não abertas |
| arXiv:2508.19282 (CORE-RAG) | **PDF ilegível** pela ferramenta; só metadados |
| Datasets e modelos | API ou página do Hugging Face Hub (ver tabelas) |

Nenhum artigo foi lido em texto completo por pessoa. Venues marcados "via busca" vêm de resultado de busca, não da página do artigo. **Não conferido** (nomeados na busca, não verificados): ver seção final.

## Q1. Contexto irrelevante piora a resposta do LLM leitor? O efeito é maior em modelos pequenos?

### O que as fontes dizem

| Artigo | Ano / venue | Modelos | Efeito medido |
|---|---|---|---|
| Shi, Chen et al., *Large Language Models Can Be Easily Distracted by Irrelevant Context* ([arXiv 2302.00093](https://arxiv.org/abs/2302.00093)) | 2023, ICML (PMLR 202) | code-davinci-002, text-davinci-003 (tamanhos não declarados no texto lido) | Aritmética GSM-IC, CoT: 95,0 original (100 problemas) para 72,4 micro e 6,0 macro (code-davinci-002); text-davinci-003 80,0 para 68,4 micro e 9,0 macro. **Sem comparação de tamanho** |
| Liu et al., *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)) | 2024, TACL 12 | GPT-3.5-Turbo, Claude-1.3, MPT-30B-Instruct, LongChat-13B | QA multi-documento: oráculo 88,3 (GPT-3.5) vs 56,1 sem contexto; com 20 documentos e gabarito no índice 9, GPT-3.5 cai para 53,8, abaixo do sem-contexto. Modelos de 13B e 30B perdem de forma parecida (LongChat 83,4 oráculo, 52,5 a 55,3 no meio). O paper diz que a curva em U só aparece em modelos grandes o bastante: Llama-2 7B tem só viés de recência |
| Yoran et al., *Making Retrieval-Augmented LMs Robust to Irrelevant Context* ([arXiv 2310.01558](https://arxiv.org/abs/2310.01558)) | 2024, ICLR | Llama-2-13B, Llama-2-70B (só NQ) | Contexto aleatório, prompt padrão: -1,4 (NQ) a -7,9 (Bamboogle) pontos; com prompt que obriga a usar o contexto: -7,6 a -21,1. 70B em NQ: -4,8 (padrão) e -7,4 (mix) contra -7,6 do 13B. O paper conclui que "aumentar o tamanho sozinho não basta" |
| Wu et al., *How Easily do Irrelevant Inputs Skew the Responses of LLMs?* ([arXiv 2404.03302](https://arxiv.org/abs/2404.03302)) | 2024, COLM | GPT-4 Turbo, GPT-3.5 Turbo, Gemini Pro, Llama2-7B | Razão de desvio para a opção enganosa (não é acurácia): Llama2-7B 57 a 85%; os três grandes 3 a 22%. Irrelevante **semanticamente próximo** é o pior. O texto não atribui a diferença ao tamanho (modelos diferem em família e treino) |
| Cuconasu et al., *The Power of Noise* ([arXiv 2401.14887](https://arxiv.org/abs/2401.14887)) | 2024, SIGIR | Llama2-7B, Falcon-7B, Phi-2 (2,7B), MPT-7B; NQ-open | Llama2: 0,564 só com o gabarito, 0,428 com 1 distrator relacionado, 0,378 com 18 distratores (gabarito perto da pergunta), 0,18 com gabarito no meio. Distratores *relacionados* machucam mais que aleatórios; aleatórios às vezes ajudam (MPT +0,08). Sem tendência de tamanho (Phi-2 2,7B empata com os 7B) |
| Chen et al., *Benchmarking LLMs in RAG* (RGB) ([arXiv 2309.01431](https://arxiv.org/abs/2309.01431)) | 2024, AAAI | ChatGPT, ChatGLM-6B, ChatGLM2-6B, Vicuna-7B, Qwen-7B-Chat, BELLE-7B | Acurácia em inglês, ruído 0 para 0,8: ChatGPT 96,3 para 76,0; Qwen-7B 94,3 para 73,7; ChatGLM2-6B 91,3 para 57,3; Vicuna-7B 87,7 para 60,3; BELLE-7B 83,3 para 64,7 |

### Veredito Q1

- **Estabelecido:** contexto irrelevante, sobretudo o semanticamente próximo da pergunta, reduz a acurácia de leitores de todos os tamanhos testados, em tamanhos de dezenas de pontos nos casos duros.
- **"Maior em modelos pequenos": misto e fraco.** A favor: Wu 2024 (Llama2-7B muito mais enganado que os grandes, mas a comparação mistura famílias) e RGB com ruído 0,8 (modelos de 6 a 7B perdem 20 a 34 pontos, ChatGPT perde 20; Qwen-7B perde 20,6, igual ao ChatGPT). Contra: Yoran 2024 (70B perde tanto quanto 13B), Cuconasu 2024 (sem tendência, Phi-2 de 2,7B resiste como os 7B), Liu 2024 (modelos de 13B a 30B e GPT-3.5 sofrem de forma parecida).
- Inferência do agente: não há na literatura lida um experimento controlado, mesma família, variando só o tamanho, com leitor de 3B a 9B. O argumento "o LLM pequeno ganha mais com o filtro" é **plausível mas não demonstrado**; teria de ser medido.
- Nenhum dos artigos acima testou Qwen3 ou Llama-3.x pequenos. Para esses, não há número publicado nas fontes lidas.

## Q2. Trabalho anterior: encoder pequeno treinado com sinal de LLM para selecionar ou comprimir contexto

Todos verificados por existência (página arXiv e/ou ACL Anthology / ICLR abertas por busca).

| Trabalho | Ano / venue | O que supervisiona o modelo pequeno | Tamanho do selecionador | Leitores | Datasets | Resultado principal (do próprio paper) |
|---|---|---|---|---|---|---|
| **RECOMP** extrativo ([2310.04408](https://arxiv.org/abs/2310.04408), Xu, Shi, Choi) | 2024, ICLR (via busca) | Contraste: positivo = frase que faz o leitor acertar; negativos = frases que fazem pior. **Sinal do próprio leitor, sem LLM professor** (o abstrativo destila GPT-3.5) | Dual encoder Contriever, ~110M | Flan-UL2 20B (LLaMA-13B na transferência) | NQ, TriviaQA, HotpotQA (500 ex.) | ~5% dos tokens em NQ/TQA, ~11% em HotpotQA, com perda pequena em TQA e HotpotQA, perda maior em NQ (ver Q3) |
| **FILCO** ([2311.08377](https://arxiv.org/abs/2311.08377), Wang et al.) | 2023 arXiv; venue **não conferido** | Rótulos oráculo: inclusão do string da resposta, sobreposição lexical (F1 unigrama > 0,5) ou CXMI. **Sem LLM professor** | Flan-T5 XL (3B) ou Llama-2 7B | Flan-T5 XL, Llama-2 7B | NQ, TQA, HotpotQA, ELI5, FEVER, WoW | Corta 44 a 64% do prompt; Flan-T5 top-5: NQ 47,6 para 61,8, HotpotQA 61,5 para 65,0. Limite oráculo ("Silver") 62,0 e 65,2 |
| **Provence** ([2501.16214](https://arxiv.org/abs/2501.16214), Chirkova et al., NAVER) | 2025, ICLR | Rótulos de frase vindos de **Llama-3-8B-Instruct** respondendo e citando frases; destilação de score de um reranker | DeBERTa-v3 (large; contagem não dada na página lida) | Llama-2-7B-chat; apêndice com 13B, SOLAR-10.7B, Mistral-7B-Instruct | Treino: MS MARCO, NQ. Teste: NQ, TyDi, PopQA, HotpotQA, BioASQ, SyllabusQA, RGB | Poda 50 a 80% do contexto; NQ 72,6 vs 71,8 (cheio) a 76% de poda; HotpotQA 56,0 vs 57,0 a 82%; PopQA e RGB melhoram. Pesos publicados com licença CC-BY-NC-ND (ver tabela de modelos) |
| **EXIT** ([2412.12559](https://arxiv.org/abs/2412.12559), Hwang et al.) | 2025, Findings of ACL (via busca) | Rótulos de frase da **anotação humana do HotpotQA**; GPT-4o zero-shot testado como pseudo-rotulador e pior (recall 54% nas relevantes) | Gemma-2B-it com LoRA (também 7B) | Llama-3.1-8B-Instruct e 70B | NQ, TriviaQA, HotpotQA, 2WikiMQA | Mantém ~31% dos tokens; média EM/F1 com leitor 8B: 34,4/44,8 (cheio) para 37,9/47,5 |
| **CompAct** ([2407.09014](https://arxiv.org/abs/2407.09014), Yoon et al.) | 2024; venue **não conferido** | SFT em ~28 mil exemplos sintetizados por **GPT-4o** (abstrativo, iterativo) | Mistral-7B-Instruct | LLaMA3-8B (principal), LLaMA2-13B, modelos de API | HotpotQA, MuSiQue, 2Wiki, NQ, TQA | 47x de compressão; HotpotQA F1 46,9 vs 40,3 do documento cheio |
| **LLMLingua-2** ([2403.12968](https://arxiv.org/abs/2403.12968), Pan et al.) | 2024, Findings of ACL | Classificação por token (manter/descartar) com rótulos obtidos de compressão do **GPT-4** sobre MeetingBank | XLM-RoBERTa-large (355M); versão small com mBERT (110M) | GPT-3.5-Turbo, Mistral-7B (alvo) | MeetingBank, LongBench, ZeroSCROLLS, GSM8K, BBH | MeetingBank QA EM 86,9 vs 87,8 original; LongBench 39,1 vs 44,0 a ~5x. **Agnóstico à tarefa**, não usa a pergunta |
| **LLMLingua** ([2310.05736](https://arxiv.org/abs/2310.05736), Jiang et al.) | 2023, EMNLP | Nenhum treino de seletor: perplexidade de um LM pequeno (GPT-2 small, LLaMA-7B) | LM de 124M a 7B | GPT-3.5, GPT-4 | GSM8K, BBH, ShareGPT, Arxiv | Até 20x com pouca perda (via busca; tabelas não abertas) |
| **Selective Context** ([2310.06201](https://arxiv.org/abs/2310.06201), Li et al.) | 2023, EMNLP | Nenhum treino: auto-informação de um LM base | LM base | vários | 4 aplicações | -50% de custo de contexto; BERTscore -0,023 (via busca; tabelas não abertas) |
| **CPC** ([2409.01227](https://arxiv.org/abs/2409.01227), Liskavets et al.) | 2024, arXiv; sem venue | Contraste com perguntas geradas por LLM sobre WikiText | Mistral-7B com LoRA (**não é pequeno**) | não especificado | LongBench, ZeroSCROLLS | LongBench 50,0 vs 48,8 (LongLLMLingua) a 3.000 tokens; BM25 40,6 |
| "Context pruning for RAG" como termo | Provence é o trabalho de referência com esse nome nos resultados | | | | | |

Trabalhos mais próximos que o agente achou mas **não abriu**: arXiv:2503.10720 (AttentionRAG), arXiv:2601.17532 (Information Gain Pruning), AACL 2026 long.39 (EnComp), arXiv:2508.19282 (CORE-RAG, PDF ilegível). Ver "não conferido".

### Já foi feito "supervisionar o seletor com as palavras que o LLM copia na justificativa"?

- **Não encontrei trabalho que faça exatamente isso.** Busca dirigida (rationale, explicação, token, destilação) não devolveu nenhum paper que treine highlighter com os tokens copiados pela justificativa de um LLM para podar contexto de outro leitor.
- **Vizinhos próximos:** Provence (rótulo de frase = o que o Llama-3-8B cita ao responder), LLMLingua-2 (rótulo por palavra = o que o GPT-4 manteve ao comprimir, mas sem pergunta), FILCO (rótulo por sobreposição lexical com a saída-alvo).
- Inferência do agente: a variante do projeto é uma **troca de sinal de supervisão** dentro de um desenho já bem coberto (selecionador pequeno + leitor LLM). O terreno é ocupado; a diferença está só em usar a justificativa em vez da citação (Provence) ou da compressão (LLMLingua-2). Espaço para uma semana: **é um estudo de replicação com um sinal alternativo, não um achado novo de método**. Isso é compatível com o critério do programa (processo, não novidade), mas não deve ser vendido como inédito.
- O encoder do projeto (BERT 29M) é menor que todos os selecionadores acima exceto o small do LLMLingua-2 (110M). Isso é fato verificável nas tabelas; ser menor e ainda competir seria um resultado, mas não há número publicado para encoder dessa escala em QA.

## Q3. Filtros desse tipo batem as linhas de base simples?

**Este é o principal risco.** O que os próprios papers mostram:

**RECOMP (Flan-UL2 20B, top-5 documentos, tabela principal)**

| Condição | NQ tokens | NQ EM/F1 | TQA EM/F1 | HotpotQA tokens | HotpotQA EM/F1 |
|---|---|---|---|---|---|
| Sem recuperação | 0 | 21,99 / 29,38 | 49,33 / 54,85 | 0 | 17,80 / 26,10 |
| Top-5 cheio | 660 | 39,39 / 48,28 | 62,37 / 70,09 | 684 | 32,80 / 43,90 |
| Frase aleatória | 32 | 23,27 / 31,09 | 50,18 / 56,24 | 61 | 21,00 / 29,86 |
| Frase por BM25 | 36 | 25,82 / 33,63 | 54,67 / 61,19 | 74 | 26,80 / 38,02 |
| Frase por Contriever (sem treino) | 36 | 30,06 / n.c. | 53,67 / 60,01 | 78 | 28,60 / 39,48 |
| Extrativo treinado | 37 | 36,57 / 44,22 | 58,99 / 65,26 | 75 | 30,40 / 40,14 |

- Em NQ o treinado bate BM25 por ~10 pontos de EM. Em HotpotQA a diferença é 3,6 EM e 2,1 F1 sobre 500 exemplos. Inferência do agente: com n=500 o erro padrão de uma EM de ~30% é ~2 pontos, então essa diferença está perto do ruído (um teste pareado seria necessário).
- O treinado fica **abaixo do top-5 cheio** em todos os conjuntos (30,4 vs 32,8 em HotpotQA), ao custo de ~11% dos tokens.

**Outros**

- **CPC (LongBench, 2.000 tokens):** BM25 23,6, SBERT 25,8, embeddings OpenAI 29,8, LLMLingua-2 39,1, CPC 49,5. Retriever lexical é a linha mais fraca, mas CPC usa um LLM de 7B.
- **FILCO:** só compara com cheio e com filtro por passagem; **não tem linha base BM25 nem aleatória**. Ganho sobre "cheio": NQ +13 a +14 (top-5 Flan-T5), HotpotQA +3,5.
- **Provence:** compara com RECOMP, LongLLMLingua, LLMLingua-2, DSLR; **não tem BM25 nem aleatório** no experimento de poda.
- **EXIT:** não inclui BM25 nem aleatório como baselines (verificado na tabela lida). Ganho médio sobre "cheio": +3,5 EM com leitor 8B.
- **Yoran 2024:** um filtro NLI de 407M (BART-large-MNLI) volta ao nível sem recuperação com contexto aleatório, mas **descarta relevantes**: NQ com top-1 cai de 40,6 para 37,0; 2Wiki de 53,1 para 39,0. Filtro de passagem inteira é arriscado.
- Inferência do agente: o ganho que filtros aprendidos mostram sobre BM25 é **grande quando a pergunta tem forte sobreposição lexical com a resposta** (NQ, TQA) e **pequeno em multi-salto** (HotpotQA). O projeto precisa de BM25, sobreposição lexical (a regra de AP 0,56), aleatório, oráculo e idealmente um reranker genérico como braços obrigatórios.

## Q4. Datasets

Verificação: API ou página do Hugging Face Hub aberta nesta sessão.

| Dataset (hub id verificado) | Tamanho | Contexto por pergunta | Frases de apoio anotadas | Métrica | Licença | Encaixe |
|---|---|---|---|---|---|---|
| **`hotpotqa/hotpot_qa`**, config `distractor` (verificado via API: 82.806 downloads) | treino 90.447, validação 7.405 | ~10 parágrafos (2 de apoio + 8 distratores) | **Sim** (`supporting_facts`: título + índice da frase) | EM/F1 | CC BY-SA 4.0 | Melhor encaixe: tem tudo, é o dataset de EXIT, RECOMP, CompAct, Provence |
| `dgslibisey/MuSiQue` (verificado: 24.340 downloads) | treino ~19,9 mil, validação ~2,4 mil | ~20 parágrafos | Sim (`is_supporting` por parágrafo; decomposição) | EM/F1 | **Não declarada** na página do hub | Mais difícil (leitor 8B: F1 15,6 cheio, 23,6 oráculo, via CompAct). Granularidade é parágrafo, não frase |
| `xanhho/2WikiMultihopQA` (verificado; "espelho oficial" de Alab-NII/2wikimultihop; 10.569 downloads) | 100 mil a 1 milhão (categoria; 402 MB) | ~10 parágrafos | Sim segundo o paper (evidências em tripla e frases de apoio); **campos não visíveis** na página (viewer desligado) | EM/F1 | apache-2.0 na página do espelho; **licença do repo original não verificada** | Viável, mas estrutura precisa ser conferida baixando |
| `allenai/qasper` (verificado) | 5.049 perguntas, 1.585 artigos | Artigo inteiro, milhares de tokens | Sim (evidência) | F1 de resposta; muitas respostas livres | cc-by-4.0 | Respostas abstrativas e de difícil nota automática; contexto longo |
| `mandarjoshi/trivia_qa` (verificado) | >100 mil | Documentos web longos | Não, frase | EM/F1 | **unknown** | Sem anotação de frase de apoio, sem licença clara |
| `miracl/nomiracl` (verificado existir; 1.839 downloads) | não verificado | passagens multilíngues | rótulos de relevância por passagem | recusa/alucinação | **não verificada** | Mede alucinação e recusa, não acurácia de resposta; fora de escopo |

Não verificado: hub id de **RGB** (a busca por "rgb retrieval augmented benchmark" na API devolveu vazio; repo no GitHub: chen700564/RGB, **licença não declarada** na página lida). SQuAD com distratores: não procurei hub id; construir sinteticamente é trabalho extra.

**Recomendação de dataset: `hotpotqa/hotpot_qa`, config `distractor`.**

- Atende a (a) a (f): pergunta, ~10 parágrafos com 8 distratores, resposta curta com EM/F1, **frase de apoio anotada** (dá o filtro oráculo), cada par (pergunta + parágrafo) cabe em 512 tokens do BERT com folga (inferência do agente: parágrafos de poucas frases), licença CC BY-SA 4.0.
- Contra: distratores do HotpotQA já foram escolhidos por similaridade lexical com a pergunta (BM25) pelos criadores do dataset. Inferência do agente: isso torna BM25 uma linha de base **mais difícil de bater** aqui do que em NQ. Resultado de RECOMP em HotpotQA (diferença pequena sobre BM25) é consistente com isso.

## Q5. Leitores pequenos para 8 GB via GGUF

IDs verificados pela API do Hub nesta sessão. Existência de GGUF **não verificada** para estes ids exatos (os GGUF costumam ser publicados em repositórios de terceiros; conferir).

| Hub id | Parâmetros (safetensors) | Licença (tag) | Sensível a distratores segundo as fontes lidas? |
|---|---|---|---|
| `Qwen/Qwen3-4B` | 4,02 B | apache-2.0 | Não encontrei medida nas fontes lidas |
| `meta-llama/Llama-3.2-3B-Instruct` | 3,21 B | llama3.2 (gated manual) | Não encontrei medida; a família Llama-3.1-8B é leitor padrão em EXIT e CompAct |
| `microsoft/Phi-3.5-mini-instruct` | 3,82 B | mit | Não encontrei medida; Phi-2 (2,7B, outro modelo) resistiu como os 7B em Cuconasu 2024 |
| `meta-llama/Llama-3.1-8B-Instruct` | 8,03 B | llama3.1 (gated manual) | Leitor em EXIT e CompAct (LLaMA3-8B); HotpotQA: F1 40,3 com 30 documentos vs oráculo 51,2 (CompAct). **Sensível a distratores: sim**, ~11 pontos de F1 |
| `Qwen/Qwen3.5-9B` (já usado no projeto) | 9,65 B | apache-2.0 | Nenhuma medida encontrada em paper |

Para a variante 1 (leitor pequeno): `Qwen/Qwen3-4B` ou `meta-llama/Llama-3.2-3B-Instruct`. Recomendação do agente: **`Qwen/Qwen3-4B`** (Apache-2.0, sem fila de aprovação, cabe em Q4/Q8 em 8 GB). Ressalva: o Qwen3 tem modo de raciocínio; desligar para resposta curta.

Nota: o tamanho "pequeno" na literatura de 2024 a 2026 é quase sempre 7B a 8B (Llama-2-7B, Llama-3.1-8B, Mistral-7B). Leitor de 3B a 4B é menos comum; menos números para comparar.

## Q6. Veredito de viabilidade em uma semana

### Experimento mínimo comum (dia 1)

Checagem barata: acurácia do leitor com **contexto cheio vs só frases/parágrafos de apoio** (oráculo) no HotpotQA distractor, ~300 perguntas de validação. Se a diferença for pequena, os dois cenários morrem no dia 1.

- O que a literatura leva a esperar (todos com ressalva): CompAct com LLaMA3-8B em HotpotQA com 30 documentos *recuperados* dá F1 40,3 (cheio) vs 51,2 (oráculo), ou seja ~11 pontos. EXIT com Llama-3.1-8B: cheio 44,8 para 47,5 filtrado (média de 4 datasets). RECOMP com Flan-UL2: top-5 43,9 F1.
- Inferência do agente, **sem fonte direta**: no setting distractor (10 parágrafos, 2 de apoio) a diferença cheio vs oráculo deve ser menor que em 30 documentos recuperados, porque há menos texto, mas os distratores são difíceis. Não achei número publicado para Qwen3-4B nem Llama-3.2-3B nesse setting. **Medir**, não presumir.
- Regra de parada proposta: se oráculo - cheio < 5 pontos de F1 com o leitor de 4B, a variante 1 não tem margem.

### Variante 1: leitor pequeno, "o LLM pequeno responde melhor com o filtro"

**POSSÍVEL COM CORTES.**

- Razões a favor: a gerar (35B local, 1,2 a 1,7 s por resposta curta, mais com prompt longo de ~1.200 tokens: estimativa 2 a 4 s por exemplo) cerca de 1.500 justificativas leva ~1,5 h. Treinar o BERT pequeno em ~1.500 perguntas × ~40 frases = ~60 mil pares leva minutos. O leitor de 4B responde a ~0,3 a 0,5 s por exemplo (estimativa), então milhares de avaliações cabem em horas.
- Riscos: HotpotQA tem distratores difíceis (Q4); a margem sobre BM25 pode ser dentro do ruído (Q3); a premissa "pequeno ganha mais" é mista (Q1).
- **Experimento mínimo que ainda significa algo:**
  - Treino: 1.500 perguntas do `train` (justificativa do 35B, rótulo = palavras/frases copiadas). Sem treino do leitor.
  - Teste: **1.000 perguntas** de `validation` (n=500 deixa a margem de ±2 pontos grande demais para diferenças de 2 a 4 pontos).
  - Condições: (1) contexto cheio; (2) só oráculo (frases anotadas); (3) BM25 top-k frases; (4) sobreposição lexical (a regra de AP 0,56); (5) frases aleatórias; (6) o filtro do projeto; opcionalmente (7) `BAAI/bge-reranker-base` (verificado, MIT) como reranker genérico. Mesmo k de frases (ou mesmo orçamento de tokens) em todas.
  - Leitor: `Qwen/Qwen3-4B`. Métrica: EM e F1, com IC por bootstrap pareado.

### Variante 2: leitor grande (35B), "mais barato e talvez mais preciso"

**POSSÍVEL COM CORTES, mas com resultado provavelmente nulo ou só de custo.**

- Razões: o 35B a 1,2 a 1,7 s por resposta curta exige ~3 a 4 s com contexto cheio (estimativa); 1.000 exemplos × 3 a 4 condições ≈ 3 a 5 h na GPU. Cabe, mas disputa tempo com a variante 1 e com a geração dos rótulos (que usa o mesmo 35B).
- Evidência da literatura: leitores grandes também degradam com distratores (Q1), mas o ganho de filtros sobre "cheio" com leitor maior é menor (EXIT: +3,5 EM com 8B e +3,7 com 70B; ambos modestos). Inferência do agente: a afirmação "mais barato" é verificável (menos tokens de entrada, menos prefill); "mais preciso" tem teto baixo, e o 35B local é MoE, cuja sensibilidade a distratores não está na literatura lida.
- **Experimento mínimo:** 500 perguntas de teste (subconjunto das 1.000 da variante 1), condições cheio / oráculo / BM25 / filtro do projeto, mesmos k. Medir acurácia e tempo por exemplo.
- Atenção: usar o mesmo 35B como professor dos rótulos e como leitor mistura professor e leitor. Se o filtro foi treinado com o que o 35B copia, o ganho com o 35B como leitor é circular. Inferência do agente: declarar isso no texto, ou usar o 9B (`Qwen/Qwen3.5-9B`) como leitor "grande" da variante 2.

### Ordem sugerida (inferência do agente)

1. Dia 1: baixar HotpotQA distractor, rodar cheio vs oráculo com Qwen3-4B em 300 validação. Decidir.
2. Dias 2 e 3: gerar justificativas e rótulos (35B), treinar o filtro.
3. Dia 4: rodar as condições da variante 1.
4. Dia 5: variante 2 (500 exemplos).
5. Dias 6 e 7: texto.

## O que isto muda para a decisão

- A ideia **não é inédita no método**: Provence, FILCO, EXIT e LLMLingua-2 já cobrem selecionador pequeno supervisionado por sinal de LLM ou oráculo. O que não achei é a **supervisão pelas palavras copiadas na justificativa**. Pode ser apresentada como "outro sinal de supervisão", nunca como "primeiro filtro".
- O **risco principal é a linha de base lexical**. No HotpotQA, o treinado de RECOMP ficou perto do BM25 (3,6 EM). O filtro do projeto precisa bater BM25 e a regra de sobreposição de conteúdo; o AP de 0,73 contra 0,56 é a favor, mas é AP de palavras, não acurácia de resposta.
- A afirmação "LLM pequeno se beneficia mais" tem **evidência mista** (Q1). Formular como pergunta empírica, não como hipótese confirmada.
- O resultado negativo (filtro empata com BM25) é publicável como ciclo completo (conforme o critério do programa), desde que as condições e a regra de parada sejam escritas antes dos testes.
- O oráculo de frases do HotpotQA dá o teto: sem ele, não se sabe se um filtro fraco é fraco ou se o problema não tem margem.
- A variante 2 tem pouca margem de ganho de acurácia e risco de circularidade se o 35B for professor e leitor; o ganho defensável é custo (tokens, tempo).
- Tamanho amostral importa: 1.000 perguntas no teste, bootstrap pareado, e lembrar que o mesmo treino na GPU variou até 0,026 entre rodadas em medidas anteriores do projeto.
- Se o dia 1 mostrar oráculo - cheio < 5 pontos de F1 com o leitor pequeno, parar: não há o que filtrar.

## Limites desta pesquisa

- Nível 3: extração de tabelas por ferramenta automática, sem leitura humana; números podem conter erro (um valor, NQ F1 31,92 de RECOMP/Contriever, veio visivelmente inconsistente e não foi usado).
- Venues de FILCO, CompAct e de outros foram "não declarados na página"; RECOMP (ICLR 2024), EXIT (Findings of ACL 2025), LLMLingua-2 (Findings of ACL 2024), LLMLingua (EMNLP 2023), Selective Context (EMNLP 2023), Provence (ICLR 2025) vêm de resultados de busca.
- Tempos por exemplo do 35B e do leitor de 4B são **estimativas do agente** a partir dos 1,2 a 1,7 s informados para respostas curtas; prompts longos aumentam o prefill.
- Nenhum paper foi encontrado que reporte sensibilidade a distratores para Qwen3-4B, Llama-3.2-3B ou Phi-3.5-mini; a coluna correspondente da tabela de Q5 está vazia por isso.
- A busca de "mais próximo" foi feita por palavras-chave; pode haver trabalho de 2025 a 2026 que não apareceu.
- Não verifiquei se os GGUF dos leitores de Q5 existem nos ids de repositório exatos.

### Não conferido (nomes vistos, não verificados)

- RGB como dataset no Hugging Face Hub: hub id não encontrado; licença do GitHub não declarada.
- arXiv:2508.19282 (CORE-RAG, Cui et al.): PDF ilegível, só metadados; venue sugerido ICML 2026 pelo nome do repo, não confirmado.
- arXiv:2503.10720 (AttentionRAG), arXiv:2601.17532 (Information Gain Pruning), AACL 2026 long.39 (EnComp), arXiv:2605.30790: aparecem em resultados de busca, não abertos.
- Licença do repositório original 2WikiMultihopQA (Alab-NII/2wikimultihop); a página do espelho diz apache-2.0.
- Licença de `dgslibisey/MuSiQue` (sem cartão no hub).
- Venues de FILCO e CompAct.
- Contagem de parâmetros do Provence.
- SQuAD com distratores e NQ-open com passagens recuperadas: hub ids não procurados.

## Fontes

- Shi et al. 2023: https://arxiv.org/abs/2302.00093 · https://proceedings.mlr.press/v202/shi23a.html
- Liu et al. 2024: https://arxiv.org/abs/2307.03172 · https://aclanthology.org/2024.tacl-1.9
- Yoran et al. 2024: https://arxiv.org/abs/2310.01558
- Wu et al. 2024: https://arxiv.org/abs/2404.03302
- Cuconasu et al. 2024: https://arxiv.org/abs/2401.14887
- Chen et al. 2024 (RGB): https://arxiv.org/abs/2309.01431
- RECOMP: https://arxiv.org/abs/2310.04408
- FILCO: https://arxiv.org/abs/2311.08377
- Provence: https://arxiv.org/abs/2501.16214
- EXIT: https://arxiv.org/abs/2412.12559
- CompAct: https://arxiv.org/abs/2407.09014
- LLMLingua-2: https://arxiv.org/abs/2403.12968
- LLMLingua: https://arxiv.org/abs/2310.05736
- Selective Context: https://aclanthology.org/2023.emnlp-main.391
- CPC: https://arxiv.org/abs/2409.01227
- Datasets e modelos: https://huggingface.co/datasets/hotpotqa/hotpot_qa · https://huggingface.co/datasets/dgslibisey/MuSiQue · https://huggingface.co/datasets/xanhho/2WikiMultihopQA · https://huggingface.co/datasets/allenai/qasper · https://huggingface.co/datasets/mandarjoshi/trivia_qa · https://huggingface.co/datasets/miracl/nomiracl · https://huggingface.co/Qwen/Qwen3-4B · https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct · https://huggingface.co/microsoft/Phi-3.5-mini-instruct · https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct · https://huggingface.co/Qwen/Qwen3.5-9B · https://huggingface.co/naver/provence-reranker-debertav3-v1 · https://huggingface.co/BAAI/bge-reranker-base · https://huggingface.co/google/bert_uncased_L-4_H-512_A-8
