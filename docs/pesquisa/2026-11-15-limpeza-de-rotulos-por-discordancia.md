# Limpeza de rótulos por discordância de sinais: literatura e viabilidade (15/11/2026)

## Procedência

**Nível 3.** Um agente leu resumos e páginas, não artigos completos. Serve para triagem, nunca para citação. Nada aqui foi lido pelo Pedro nem pelo Claude (nível 1 e 2).

| Como foi aberto | Itens |
|---|---|
| Texto (HTML/ar5iv) lido em parte, números de tabela extraídos por um modelo pequeno | Chong, Hong & Manning 2022 (ar5iv); Zhu et al. 2022 (ar5iv, só a parte de ruído); Zuo, Plank & Peng (EVADE, HTML); Klie, Webber & Gurevych (ar5iv, só os primeiros ~100 mil de ~158 mil caracteres) |
| Só página de resumo (arXiv/ACL Anthology) | Northcutt, Jiang & Chuang 2021; Northcutt, Athalye & Mueller 2021; Nie, Zhou & Bansal 2020; Swayamdipta et al. 2020; Pleiss et al. 2020; Weber-Genzel et al. 2024 (VariErr NLI); Talukdar et al. 2021; Nahum et al. 2024; Agro & Aldarmaki 2023; Pavlick & Kwiatkowski 2019 |
| Só resultado de busca, sem abrir a fonte | Sorscher et al. 2022; Beigman & Beigman Klebanov 2009 e Beigman Klebanov & Beigman 2010; Bowman et al. 2020 (nada de útil nesta pergunta) |
| PDF inacessível | Versões em PDF de Zhu 2022, Chong 2022 e Klie 2022: o conteúdo veio comprimido e ilegível. Usei as versões HTML/ar5iv no lugar. |

Aviso: as tabelas vieram de um extrator automático; o próprio extrator avisou que a Tabela 3 de Chong 2022 estava "garbled em alguns pontos". Conferir no PDF antes de citar qualquer número.

Itens que não consegui conferir estão na seção "Não conferido".

## Resumo executivo (o que as fontes dizem, depois a inferência)

- Fontes: em NLI há discordância humana grande (ChaosNLI) e erro real menor; não achei taxa de erro de rótulo medida especificamente no RTE do GLUE.
- Fontes: com ruído de ~5%, a correção de rótulos mexeu no acerto verdadeiro de -0,2 a +0,9 ponto (Chong 2022, Tabela 4, 4 conjuntos).
- Fontes: BERT é pouco sensível a ruído injetado; métodos de tratamento de ruído "não melhoram o pico" (Zhu 2022).
- Fontes: existe trabalho que usa **explicações** para achar erro em NLI (VariErr NLI 2024; EVADE 2025/26). Não achei trabalho que use **discordância de atenção/destaque** para achar rótulo errado.
- Inferência do agente: o ganho esperado em RTE limpo a 1%–5% fica abaixo de 0,03 de ROC-AUC e dentro do ruído de sementes. Mostrar ganho nos dados reais não é realista em uma semana. O experimento com ruído injetado é viável, desde que o sinal do LLM seja regerado sob o rótulo trocado (ver Q5).

## Q1. Ruído de rótulo em RTE e em NLI

| Fonte | Autores, ano, venue | O que diz | Observação |
|---|---|---|---|
| What Can We Learn from Collective Human Opinions on NLI Data? (ChaosNLI) | Nie, Zhou, Bansal; 2020; EMNLP 2020 (pp. 9131–9143); arXiv 2010.03532 | 100 anotações por exemplo em 3.113 exemplos de SNLI/MNLI e 1.532 de αNLI. Busca secundária reporta que a nova maioria difere do rótulo original em cerca de 10% (αNLI), 20–25% (SNLI) e 30–31% (MNLI-m); varia entre versões do artigo. Modelos acertam quase tudo nos exemplos de alta concordância e ficam perto do acaso nos de baixa. | Só o resumo foi aberto; os percentuais vêm de resultado de busca, não da fonte. É discordância humana, não necessariamente erro. Não cobre RTE. |
| Inherent Disagreements in Human Textual Inferences | Pavlick & Kwiatkowski; 2019; TACL 7, pp. 677–694; DOI 10.1162/tacl_a_00293 | Discordância entre anotadores persiste com mais anotadores; não é só ruído. | Só confirmado por busca. |
| VariErr NLI: Separating Annotation Error from Human Label Variation | Weber-Genzel, Peng, de Marneffe, Plank; 2024; ACL 2024 (main); arXiv 2403.01931 | 500 itens do MNLI reanotados, 1.933 explicações, 7.732 julgamentos de validade (um snippet de busca diz 7.574). Métodos automáticos de detecção de erro ficam "significativamente abaixo" de GPTs e humanos; GPT-4 é o melhor sistema, ainda abaixo de humanos. | Percentuais de erro por item (ex.: 37,6% com ao menos um erro autoidentificado) vieram só de snippet de busca; não confiar sem abrir o artigo. |
| Learning with Annotation Noise; Some Empirical Evidence for Annotation Noise in a Benchmarked Dataset | Beigman & Beigman Klebanov, ACL-IJCNLP 2009 (P09-1032); Beigman Klebanov & Beigman, HLT-NAACL 2010 (N10-1067) | Evidência de ruído de anotação no RTE-1 e do viés de "caso difícil" (aprender dos casos fáceis). | Só resultado de busca. É RTE-1, não o RTE do GLUE. |
| Pervasive Label Errors in Test Sets Destabilize ML Benchmarks | Northcutt, Athalye, Mueller; 2021; NeurIPS 2021 Datasets and Benchmarks; arXiv 2103.14749 | Em 10 conjuntos (visão, texto, áudio), pelo menos 3,3% de erro nos conjuntos de teste (versão anterior: 3,4%); ~51% dos candidatos sinalizados por confident learning foram confirmados por humanos. | Por memória e sem abrir a lista, os 10 conjuntos não incluem NLI. Isto é inferência do agente, não conferida. |

Lacuna: **não encontrei taxa de erro medida para o RTE do GLUE** (treino ou dev). A tentativa de busca devolveu RTE-1 (2009/2010) e uma reanotação húngara (HuRTE), nenhuma delas uma correção do RTE em inglês. Os rótulos de teste do GLUE são ocultos, então qualquer checagem só vale para treino/dev.

Inferência do agente: a estimativa do próprio Pedro (~1% de justificativas contra o rótulo, ~7% com fato errado) é a única medida específica do RTE disponível; ela é consistente com "erro real baixo, ambiguidade alta", mas não é comparável com os 20–30% do ChaosNLI, que medem outra coisa.

## Q2. Métodos de detecção com sinal de modelo

| Método | Ano, venue | Como sinaliza | Resultado reportado | Observação |
|---|---|---|---|---|
| Confident learning / `cleanlab` | Northcutt, Jiang, Chuang; 2021; JAIR 70, pp. 1373–1411; arXiv 1911.00068 | Estima a conjunta entre rótulo ruidoso e verdadeiro com probabilidades fora da amostra e limiares por classe | Em texto (Chong 2022): AUPR 0,24 (IMDB), 0,31 (Amazon), 0,17 (SNLI-5) | Precisa de probabilidades por validação cruzada |
| Dataset Cartography | Swayamdipta et al.; 2020; EMNLP 2020 (pp. 9275–9293); arXiv 2009.10795 | Confiança média e variabilidade da confiança no rótulo ao longo das épocas | Região "difícil de aprender" costuma ter erros; região "ambígua" ajuda generalização fora da distribuição. Treinar em subconjuntos perde um pouco dentro da distribuição (relato secundário) | Não é um detector de erro validado, é um diagnóstico |
| Area Under the Margin (AUM) | Pleiss, Zhang, Elenberg, Weinberger; 2020; NeurIPS 2020; arXiv 2001.10528 | Margem média logit do rótulo dado contra o maior outro, ao longo do treino; limiar por classe sintética | Imagens: remover ~17% (WebVision50) reduz erro 1,6 ponto; ~13% (CIFAR-100) reduz 1,2 | Em NLP funciona pior (linha abaixo) |
| AUM em NLP | Talukdar, Dagar, Gupta, Menon; 2021; BlackboxNLP 2021 (pp. 296–302); arXiv 2109.09191 | Aplica AUM em conjuntos de NLP (CoLA, GLUE, SST segundo a Anthology) | Eficácia menor que em imagens; "remove muitos pontos corretamente rotulados" | Só resumo aberto, sem números |
| Perda de modelo de fundação (FML) | Chong, Hong, Manning; 2022; EMNLP 2022; arXiv 2205.12702 | Ordena exemplos pela perda de um modelo pré-treinado ajustado, fora da amostra | SNLI com 5% de ruído de origem humana: AUPR FML 0,54, ensemble (FME) 0,61, confident learning 0,17, H&G 0,20. IMDB 0,58 contra 0,24 do CL | Os baselines do CL e H&G usam classificadores fracos (FastText / vetores de palavras) |
| Comparação de 18 métodos | Klie, Webber, Gurevych; 2023; Computational Linguistics 49(1); DOI 10.1162/coli_a_00464; arXiv 2206.02280 | Reimplementa 18 detectores em 9 conjuntos (classificação e rotulagem; nenhum de NLI nos trechos lidos) | Ruído aleatório de 5% em ATIS/SST: Borda Count e Datamap Confidence ~0,98/0,50 de AP; em IMDB (erro natural) tudo fica em 0,33–0,35 | Erro injetado ao acaso é muito mais fácil que erro natural. Não mede acerto após limpar |
| LLM como verificador | Nahum, Calderon, Keller, Szpektor, Reichart; 2024 (v2 em 2025); arXiv 2410.18889 (sem venue) | Conjunto de LLMs como juízes sobre exemplos de consistência factual (TRUE, SummEval) | LLMs detectam 6–21% dos erros (busca secundária) e corrigi-los eleva o desempenho medido | Domínio diferente de NLI. Só resumo |
| Explicações em NLI: VariErr | Weber-Genzel et al.; 2024; ACL 2024 | Anotadores explicam o rótulo; outros julgam se a explicação sustenta o rótulo; rótulo sem explicação válida = erro | Métodos automáticos de detecção ficam abaixo de GPT e humanos | Usa explicação **escrita por humano** |
| Explicações em NLI: EVADE | Zuo, Plank, Peng; arXiv 2511.08949 (nov/2025, v2 mai/2026); página do arXiv não dá venue; uma página de busca indica Findings of ACL 2026 (não conferido) | LLMs (Llama-8B/70B, Qwen-7B/72B) geram explicações e as validam; rótulos sem explicação válida são marcados | Remover erros do LLM melhorou o ajuste mais que remover os humanos (relato do resumo). Tabela 5: VariErr rodada 1 F1 0,584 (BERT), 0,625 (RoBERTa); melhor EVADE direto 0,633 / 0,635; sem sementes nem testes de significância; linhas "antes" idênticas entre modelos (inconsistência apontada pelo extrator) | É o trabalho mais próximo da ideia. Treina em ~500 itens com rótulo-distribuição; não é RTE nem rótulo único |

### Biblioteca e dados verificados

| Item | Verificação | Resultado |
|---|---|---|
| `cleanlab` | JSON do PyPI (`https://pypi.org/pypi/cleanlab/json`) | Versão 2.9.0, publicada em 13/01/2026, Python >= 3.10, licença Apache-2.0. Releases anteriores eram AGPL-3.0 (snyk, nixpkgs); o ponto exato da troca não foi conferido. Conferir o LICENSE do GitHub antes de depender. |
| ChaosNLI | Repositório GitHub citado nos resultados (`easonnie/ChaosNLI`) | Existe, segundo o artigo e a busca; não clonei. Não contém RTE. |
| Dataset Cartography | Repositório `allenai/cartography` citado no resumo | Citado por busca, não clonado. |

### Explicações, atenção ou destaque para achar rótulo errado

Fontes: VariErr (explicações humanas) e EVADE (explicações de LLM) usam **explicação em texto que sustenta ou não o rótulo**. Isso é parente da ideia "justificativa contradiz o rótulo". Uma busca por "discordância de atenção/destaque para detectar rótulo errado" não achou nenhum trabalho. O único achado ligado a atenção foi contrário: o benchmark ERASER (DeYoung et al., arXiv 1911.03429, só lido por snippet) diz que pesos de atenção em geral não dão explicações fiéis.

Inferência do agente: a discordância atenção-versus-marcas provavelmente carrega pouca informação sobre o **rótulo**. As marcas (palavras que a justificativa copia) são palavras do par e dependem pouco do rótulo; a atenção do `[CLS]` já foi treinada para prevê-las. A discordância mede a qualidade do destaque, não a correção do rótulo. Os dois sinais que sobrevivem a esse argumento: (1) o LLM, sem ver o rótulo, prevê o rótulo; (2) um juiz pergunta se a justificativa sustenta o rótulo dado. Isto é hipótese e deve ser testada, não assumida.

## Q3. Ganho esperado com ruído baixo (1%–5%) e conjunto pequeno

Não achei estudo que meça exatamente "BERT-base ou menor, ~2,5 mil exemplos, 1–5% de ruído, limpar e medir". O mais próximo:

| Evidência | Números | Leitura |
|---|---|---|
| Chong et al. 2022, Tabela 4 (5% de ruído injetado de origem humana, acerto no teste "verdadeiro") | IMDB-5: ruidoso 94,2, corrigido 95,1, limpo 95,8. Amazon-5: 91,0 / 90,8 / 91,0. TweetNLP-5 (1.827 tweets): 92,8 / 93,0 / 93,8. TweetNLP-M: 82,0 / 82,0 / 82,1 | Corrigir deu -0,2 a +0,9 ponto. O teto (limpo contra ruidoso) já é só 0,0–1,0 ponto. O extrator avisou que a tabela pode estar truncada |
| Zhu et al. 2022 (Is BERT Robust to Label Noise?) | Workshop Insights from Negative Results in NLP 2022 (ACL), arXiv 2204.09371. Métodos de tratamento de ruído "não melhoram o pico" do BERT; maior ganho abaixo de 4 pontos com ruído injetado (20–70%), abaixo de 1,5 com supervisão fraca | Benefício só aparece com ruído alto. Ruído injetado a 20% em IMDB derruba BERT a ~86 contra ~94 limpo (leitura incerta da tabela) |
| Agro & Aldarmaki 2023 (Handling Realistic Label Noise in BERT Text Classification) | arXiv 2305.16337, sem venue | Ruído realista (dependente de atributos e de discordância de anotadores) degrada BERT bem mais que ruído aleatório |
| Resultado de busca sobre tratamento de ruído em corpora pequenos | Em conjuntos grandes com ruído baixo, filtrar não melhora; em pequenos e muito ruidosos, confident learning ajuda F1 | Não identifiquei a fonte; não citar |

Inferência do agente, com a conta: em RTE com ~2.470 pares e 1% de erro real são ~25 pares. A dev tem 277 pares, o erro padrão do acerto é ~2,9 pontos (raiz de 0,25/277 = 0,030). O ruído de GPU medido pelo Pedro (até 0,026 de ROC-AUC entre repetições) já tem o tamanho do efeito máximo esperado. O ganho esperado a 1%–5% de ruído fica em torno de 0 a 1 ponto de acerto, **abaixo de ~0,03 de ROC-AUC e de 2–3 pontos de acerto**. Mesmo um detector perfeito de 25 erros reais corrigiria 1% dos rótulos.

### Remover exemplos difíceis ou ambíguos pode piorar?

| Evidência | Fonte | Leitura |
|---|---|---|
| AUM em NLP remove muitos pontos corretos e muita informação linguística | Talukdar et al. 2021 (resumo) | Sim, há custo |
| Região ambígua do mapa dá melhor generalização fora da distribuição; treinar só no difícil é pior; perda pequena dentro da distribuição | Swayamdipta et al. 2020 (relato secundário) | Limpar por "difícil" tem custo dentro da distribuição |
| Com pouco dado, o melhor é manter os fáceis; com muito, os difíceis | Sorscher et al. 2022, NeurIPS 2022, arXiv 2206.14486 (teoria + visão, só busca) | Em 2,5 mil exemplos, podar difíceis é arriscado |
| Discordância é informação, não erro | Pavlick & Kwiatkowski 2019; Nie et al. 2020; Weber-Genzel et al. 2024 | Descartar o discordante em NLI tira variação legítima |
| Viés de caso difícil: ruído de anotação concentrado nos casos difíceis enviesa o aprendizado para os fáceis | Beigman & Beigman 2009 (só busca) | Ponto a favor de limpar, mas só com ruído concentrado |

Nenhum estudo que achei mede o dano de remover exemplos difíceis em um conjunto **sem ruído** de NLI; a conclusão "tem custo" é inferência a partir de evidências indiretas.

## Q4. Teste barato com ruído injetado

Protocolo usado na literatura:

| Fonte | Protocolo | Qualidade de detecção das linhas de base |
|---|---|---|
| Chong et al. 2022 | 5% de ruído de origem humana (80% de trocas pelo voto minoritário em 3–2, 20% de rótulo dissidente) em SNLI (subconjunto de 10% com 5 rótulos) e TweetNLP | SNLI-5, AUPR: H&G 0,20; CL 0,17; FML 0,54; FME 0,61; FME+CL 0,62 |
| Klie et al. 2023 | 5% de rótulos trocados ao acaso em ATIS e SST; erro natural em IMDb | Ruído aleatório é fácil (AP até 0,98 em ATIS); erro natural em IMDb fica em 0,33–0,35 de AP |
| Zhu et al. 2022 | Ruído uniforme (AG News 40–70%) ou por troca única (IMDB 20–45%); mede o acerto, não a detecção | Mostra o efeito do ruído, não a detecção |

Pontos que valem para o desenho:
- Fontes: ruído de origem humana é mais difícil de detectar que ruído aleatório (Chong 2022; Klie 2023). Com troca aleatória de 10% ou 20% o resultado vai parecer melhor do que será nos erros reais.
- Fontes: a linha de base mais forte nos números lidos é a **perda fora da amostra de um modelo pré-treinado ajustado** (FML), muito acima de confident learning com classificador fraco. Em RTE o BERT pequeno acerta pouco, então o detector por perda dele será pior que o de um modelo grande (inferência do agente).
- Não achei nenhuma publicação deste protocolo em RTE.

## Q5. Veredito de viabilidade para uma semana

| Item | Veredito | Por quê (inferência do agente) |
|---|---|---|
| (i) Limpar o RTE real e mostrar ganho | **NÃO REALISTA** | Ganho esperado 0–1 ponto, abaixo do piso de ruído (0,026 de ROC-AUC entre repetições; erro padrão da dev ~2,9 pontos). Só ~25 erros reais prováveis. Rodar o pipeline é possível e dá um resultado nulo legível, não um ganho demonstrável |
| (ii) Detecção com ruído injetado | **POSSÍVEL** (com um corte, abaixo) | 2.470 pares, encoder de 29M, RTX 5060: cada treino é curto. Não precisa de dev para medir detecção (precisão e recall contra os índices trocados) |

### Menor experimento que ainda significa algo

1. Trocar 10% e 20% dos rótulos (simétrico) em treino; 3 desenhos de ruído por taxa.
2. **Regerar a justificativa do LLM sob o rótulo trocado** (cerca de 250 e 500 pares, ~1,2 s/par no 35B). Sem isto o sinal vaza: a justificativa original foi escrita sob o rótulo verdadeiro e o juiz "justificativa contradiz o rótulo" acharia os trocados por construção (inferência do agente).
3. Sinais a comparar, todos produzindo um escore por par: (a) discordância atenção versus marcas; (b) LLM sem o rótulo prevê rótulo diferente do dado; (c) juiz "a justificativa sustenta o rótulo?"; (d) combinação.
4. Linhas de base obrigatórias: **aleatório**; **perda fora da amostra** do BERT pequeno por validação cruzada em K partes (FML do Chong); **confident learning** (`cleanlab` 2.9.0, `find_label_issues` com as mesmas probabilidades); **AUM ou confiança de Dataset Cartography** do próprio treino.
5. Métrica de detecção: AUPRC e precisão nos k primeiros (k = número de trocados), e recall com revisão limitada a 10% da lista.
6. Etapa de limpeza opcional: remover os k mais suspeitos, retreinar com 10 sementes, comparar contra ruidoso e contra limpo. Só interpretar "recupera X% da diferença" se a diferença ruidoso–limpo for maior que ~0,03; abaixo disso o resultado não diz nada.

### Principais formas de enganar

- Vazamento do rótulo verdadeiro na justificativa (item 2 acima).
- Ruído aleatório é fácil: acertar a 20% de troca não prova nada para o erro real de 1%. Se possível, adicionar troca "plausível" (pares em que o LLM sem rótulo discorda do gabarito) como ruído difícil.
- Precisão com prevalência baixa: com 1% de erro real (~25 pares), um detector que sinalize 10% (247 pares) e acerte metade dos erros tem ~5% de precisão. Remover 247 pares para corrigir ~12 rótulos tende a perder mais que ganhar (conta do agente).
- Os sinais (a) e (d) dependem do mesmo encoder treinado nos dados ruidosos; o juiz do LLM é independente. Misturar os dois e atribuir o mérito ao destaque seria enganoso.
- Treino na GPU não é determinístico: variação até 0,026 entre repetições; seguir a regra de 10 sementes, não 5.

## Não conferido

| Item | Motivo |
|---|---|
| Lista exata dos 10 conjuntos de Northcutt, Athalye & Mueller 2021 | A página só descreve "visão, linguagem natural e áudio"; a ausência de NLI é memória do agente |
| Percentuais exatos do ChaosNLI (10/20–25/30–31%) | Vieram de busca e de segunda mão (um artigo de 2024); o resumo aberto não os traz |
| Venue de EVADE (Findings of ACL 2026) | Só aparece como página de busca (`preview.aclanthology.org/ingest-acl/2026.findings-acl.65/`); o arXiv não lista venue |
| Resultados completos de Klie 2023, Zhu 2022 e Chong 2022 | PDFs ilegíveis; usei HTML/ar5iv, de leitura parcial |
| Snow et al. (concordância de 89,7% entre voto da multidão e especialistas no RTE-1) | Aparece só em resultado de busca; não achei nem abri o artigo |
| Mandal, estudo negativo de Dataset Cartography em SQuAD | Só aparece em resultado de busca; não identifiquei autor, ano nem venue |
| Verificação por LLM em ltzGLUE (~10% de rótulos falsos após tradução; arXiv 2604.17976) | Só resultado de busca; é conjunto traduzido, não RTE em inglês |
| Alegação de blog "5% de ruído tira 8–12% do BERT" | Fonte anônima, contradiz Zhu 2022; não usar |
| Ponto exato da troca de licença AGPL para Apache-2.0 no `cleanlab` | Só PyPI (2.9.0 = Apache-2.0) e relatos secundários de AGPL anterior |

## O que isto muda para a decisão

- Limpar o RTE real para "ganhar nota" repete o desenho que já falhou no projeto: efeito esperado menor que o ruído de repetição. Tratar como nulo provável, não como aposta.
- O que a literatura sustenta é medir **detecção**, não ganho de nota: o experimento com ruído injetado (Q5 ii) tem resultado legível seja qual for o resultado.
- A ideia original (discordância atenção versus marcas) não tem precedente que eu tenha achado, e há argumento de que ela mede qualidade do destaque, não correção do rótulo. Isto é hipótese a testar contra aleatório, não tese.
- O sinal mais plausível é o do LLM sem rótulo e o do juiz de justificativa; o precedente mais próximo é EVADE (e VariErr), que valida explicações geradas por LLM contra o rótulo. Citar como trabalho relacionado, com cautela sobre a falta de sementes nele.
- A linha de base a bater é a perda fora da amostra de um modelo ajustado (Chong 2022, AUPR 0,54–0,61 em SNLI com 5% de ruído), mais confident learning, AUM e aleatório.
- Regerar as justificativas sob o rótulo trocado é obrigatório; sem isso o resultado é falso positivo por vazamento.
- Remover exemplos "difíceis" em NLI pequeno pode custar (AUM em NLP, cartografia, Sorscher); ao limpar, preferir descartar poucos (k = ruído esperado) e comparar contra remover o mesmo número ao acaso.
- Conforme o rumo do trabalho, vale registrar o que o Pedro estimou (~1% contra o rótulo, ~7% com fato errado) como a única taxa de erro específica do RTE desta pesquisa.

## Limites desta pesquisa

- Nível 3: resumos e páginas; tabelas extraídas por um modelo pequeno, algumas com inconsistência declarada. Nenhum número aqui deve ir para texto assinado sem leitura do original.
- Não encontrei taxa de erro medida no RTE do GLUE, nem estudo de limpeza em NLI com conjunto de ~2,5 mil exemplos e 1–5% de ruído; o ganho esperado é inferência a partir de conjuntos próximos (sentimento e tweets, NLI de outro tamanho).
- A busca foi curta (uma passada por pergunta); "não achei" não prova que não existe. Em particular, trabalhos de 2025–2026 sobre detecção de erro com explicações de LLM podem existir além de EVADE.
- As inferências sobre vazamento de rótulo, precisão com prevalência baixa e baixo conteúdo de rótulo na discordância atenção-marcas são raciocínio do agente, não resultado medido.
- Nada foi executado: nenhum código, nenhum modelo, nenhuma instalação.

## Fontes

- Northcutt, Jiang, Chuang 2021, JAIR: https://arxiv.org/abs/1911.00068
- Northcutt, Athalye, Mueller 2021, NeurIPS D&B: https://arxiv.org/abs/2103.14749
- Nie, Zhou, Bansal 2020, EMNLP: https://arxiv.org/abs/2010.03532
- Pavlick & Kwiatkowski 2019, TACL: https://aclanthology.org/Q19-1043/
- Swayamdipta et al. 2020, EMNLP: https://arxiv.org/abs/2009.10795
- Pleiss et al. 2020, NeurIPS: https://arxiv.org/abs/2001.10528
- Talukdar et al. 2021, BlackboxNLP: https://aclanthology.org/2021.blackboxnlp-1.22 ; https://arxiv.org/abs/2109.09191
- Chong, Hong, Manning 2022, EMNLP: https://arxiv.org/abs/2205.12702
- Klie, Webber, Gurevych 2023, Computational Linguistics: https://arxiv.org/abs/2206.02280 ; https://aclanthology.org/2023.cl-1.4/
- Weber-Genzel et al. 2024, ACL: https://arxiv.org/abs/2403.01931
- Zuo, Plank, Peng, EVADE: https://arxiv.org/abs/2511.08949
- Nahum et al. 2024: https://arxiv.org/abs/2410.18889
- Zhu et al. 2022, Insights from Negative Results workshop: https://arxiv.org/abs/2204.09371
- Agro & Aldarmaki 2023: https://arxiv.org/abs/2305.16337
- Sorscher et al. 2022, NeurIPS: https://arxiv.org/abs/2206.14486
- Beigman & Beigman Klebanov 2009: https://aclanthology.org/P09-1032/ ; Beigman Klebanov & Beigman 2010: https://aclanthology.org/N10-1067
- cleanlab no PyPI: https://pypi.org/project/cleanlab/
