# As 56 obras da lista v2 — para você escolher (05/10)

**De onde vêm as descrições:** cada uma resume a ficha que um agente escreveu em 27/09 depois de ler a obra (nível 2
por agente). Em duas obras o agente só teve o abstract, e isso está marcado. Você não leu nenhuma delas, exceto as
três marcadas **[lido]**.

**Selo (é a minha leitura do critério do professor, "obras recentes, métodos e ferramentas atuais"; quem decide é você):**
- **✔ atual**: método ou ferramenta em uso hoje.
- **◐ base vigente**: obra antiga, mas o que ela introduziu ainda é usado (o Transformer, por exemplo).
- **✗ histórico**: superado ou fora do foco de LLM e implantação. Serve só como contexto.

**Placar:** 22 ✔ · 17 ◐ · 17 ✗.

---

## A. Mapas (surveys), 13 obras: o professor disse que 3 a 5 servem

- **01. Efficient Processing of Deep Neural Networks: A Tutorial and Survey** (Sze et al. 2017) · intermediário · ◐
  Explica como o hardware executa uma rede (MAC, dataflow, movimento de dados) e por que energia e memória mandam no
  custo. Também cobre quantização, poda e destilação do ponto de vista do hardware. Todos os exemplos são CNN, de antes
  do Transformer. É a única obra que ensina vocabulário de hardware.

- **02. Model Compression and Hardware Acceleration for Neural Networks: A Comprehensive Survey** (Deng et al. 2020) · intermediário · ◐ · *só abstract*
  Promete unir quatro famílias de compressão (modelo compacto, decomposição tensorial, quantização, esparsidade) e
  ligá-las ao desenho de aceleradores. É o único mapa que trata baixo posto como categoria própria, mas se sobrepõe a
  01, 04 e 05.

- **03. Knowledge Distillation: A Survey** (Gou et al. 2020) · intermediário · ◐
  Organiza a destilação em três eixos: que conhecimento se transfere, como se treina e qual a relação professor-aluno.
  Tem uma seção de NLP (DistilBERT, TinyBERT). Retrata a área antes dos LLMs, então não cobre destilação de modelos de
  bilhões de parâmetros.

- **04. A Survey of Quantization Methods for Efficient Neural Network Inference** (Gholami et al. 2021) · intermediário · ✔
  O vocabulário-padrão da quantização (uniforme ou não, simétrica ou não, granularidade, QAT × PTQ, precisão mista),
  que continua valendo. Os exemplos são quase todos de visão, com algo de BERT.

- **05. Pruning and Quantization for Deep Neural Network Acceleration: A Survey** (Liang et al. 2021) · intermediário · ✗
  Poda (estática e dinâmica) e quantização sobre CNNs, com tabelas de resultado e recomendações práticas. O próprio
  texto admite que não olha para outras arquiteturas, e ela se sobrepõe muito à 04.

- **06. A Review of Sparse Expert Models in Deep Learning** (Fedus, Zoph & Dean 2022) · avançado · ◐
  Mixture-of-Experts escrito pelos criadores do Switch: roteador, instabilidade de treino e quando compensa usar
  esparso no lugar de denso. É anterior à onda de MoE nos LLMs abertos de 2023 em diante.

- **07. Efficient Transformers: A Survey** (Tay et al. 2020) · intermediário · ◐
  Taxonomia de nove famílias de atenção mais barata. Explica bem os modos encoder, decoder e encoder-decoder e por que
  a máscara causal limita o decoder. Os próprios autores dizem que nenhuma variante virou padrão, e boa parte delas
  foi abandonada.

- **08. A Comprehensive Survey of Neural Architecture Search** (Ren et al. 2020) · avançado · ✗
  Busca automática de arquitetura (células, DARTS, compartilhamento de pesos), com o alvo em CNN para classificação de
  imagem. Sem linguagem e sem Transformer.

- **09. Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey** (Han et al. 2024) · intermediário · ✔
  O mapa do ajuste eficiente (adapters, prompts, LoRA e derivados, híbridos), com as equações de cada família, e uma
  parte de sistemas reais (serving e treino com vários adaptadores).

- **10. Towards Efficient Generative LLM Serving: A Survey from Algorithms to Systems** (Miao et al. 2023, rev. 2025) · avançado · ✔
  Serving de LLM decoder-only em duas frentes: algoritmo (decodificação, arquitetura, compressão) e sistema
  (paralelismo, memória, escalonamento, kernels). Tem uma tabela comparando vLLM, TensorRT-LLM, DeepSpeed e outros. É
  o mais "ferramenta atual" dos mapas.

- **11. A Survey on Model Compression for Large Language Models** (Zhu et al. 2023, rev. 2024) · intermediário · ✔
  Quantização, poda, destilação e baixo posto já para LLM (GPTQ, AWQ, SparseGPT, QLoRA, MiniLLM), com métricas e
  benchmarks. Cada método leva um a três parágrafos: é largo e raso. Não distingue encoder de decoder.

- **12. LLM Inference Unveiled: Survey and Roofline Model Insights** (Yuan et al. 2024) · intermediário · ✔ · **[lido]**
  Usa o roofline para dizer se cada técnica ataca gargalo de memória ou de computação (o decode é limitado por
  memória, o prefill por computação). Traz a ferramenta LLM-Viewer.

- **13. Empowering Edge Intelligence: A Comprehensive Survey on On-Device AI Models** (Wang et al. 2025) · introdutório · ✔
  IA em dispositivo: sete famílias de otimização, hardware de borda e benchmark em cinco celulares. É o mais recente,
  mas funciona como catálogo (centenas de obras com uma ou duas frases cada) e o núcleo ainda é CNN.

---

## B. Fundadores, 31 obras

### Destilação
- **14. Model Compression** (Buciluă, Caruana & Niculescu-Mizil 2006) · intermediário · ✗
  O precursor da destilação: comprime um ensemble num modelo pequeno que imita os rótulos dele. Gera dados
  sintéticos (MUNGE) quando faltam dados.
- **15. Distilling the Knowledge in a Neural Network** (Hinton, Vinyals & Dean 2015) · introdutório · ◐ · **[lido]**
  Cunhou a destilação por soft targets com temperatura, o mecanismo base de quase toda a linha.
- **16. DistilBERT** (Sanh et al. 2019) · introdutório · ◐
  Destila o BERT já no pré-treino com uma perda tripla e metade das camadas: 40% menor, 60% mais rápido, 97% do
  desempenho. É destilação de **encoder**, a ponte direta com o tema v3.

### Quantização
- **17. XNOR-Net** (Rastegari et al. 2016) · intermediário · ✗
  Binarização (1 bit) de CNN no ImageNet. A acurácia cai em redes profundas. Tem valor histórico como quantização
  extrema.
- **18. GPTQ** (Frantar et al. 2022) · avançado · ✔
  Quantização pós-treino de pesos para 3 ou 4 bits em LLMs de até 175B, em horas de GPU, usando a Hessiana. É um
  método-base que continua em uso nas ferramentas.
- **19. SmoothQuant** (Xiao et al. 2022) · intermediário · ✔
  Resolve os outliers das ativações de LLM passando a dificuldade para os pesos, o que permite W8A8 sem retreino.
  Integrado a um framework de produção.
- **44. Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference** (Jacob et al. 2017) · avançado · ✔
  Define o esquema int8 afim (escala e ponto-zero) e o treino com quantização simulada (QAT). É o esquema que os
  frameworks de borda usam até hoje.

### Poda
- **20. Optimal Brain Damage** (LeCun, Denker & Solla 1989) · intermediário · ✗
  Poda por saliência de segunda ordem (Hessiana) no lugar de magnitude. O critério volta na poda de LLMs (SparseGPT),
  mas a obra em si é histórica.
- **21. Deep Compression** (Han, Mao & Dally 2015) · intermediário · ✗
  O pipeline poda, depois quantização treinada, depois Huffman, que levou o VGG de 552 MB para 11 MB e mediu o ganho
  em hardware. Foi um marco da era CNN, mas o pipeline não é usado assim hoje.
- **22. The Lottery Ticket Hypothesis** (Frankle & Carbin 2018) · intermediário · ✗
  Redes densas contêm sub-redes esparsas treináveis desde a inicialização. Tem peso teórico, mas sem ganho em hardware
  e só com visão em escala pequena.
- **23. SparseGPT** (Frantar & Alistarh 2023) · avançado · ✔
  Poda de LLMs de 175B em uma passada, sem retreino, a 50–60% de esparsidade (inclusive 2:4). Combina com GPTQ.

### Baixo posto e ajuste eficiente
- **24. Exploiting Linear Structure Within Convolutional Networks** (Denton et al. 2014) · intermediário · ✗
  Fatoração SVD de camadas convolucionais para acelerar a inferência de CNN.
- **25. Low-rank Matrix Factorization for DNN Training** (Sainath et al. 2013) · intermediário · ✗
  Fatora a camada final de uma DNN de fala. O foco é acelerar o treino.
- **26. LoRA** (Hu et al. 2021) · intermediário · ✔
  Congela os pesos e treina duas matrizes de baixo posto que depois se somam aos pesos, sem latência extra na
  inferência. É a técnica mais usada para ajustar LLM em hardware limitado.
- **27. QLoRA** (Dettmers et al. 2023) · avançado · ✔
  LoRA sobre um modelo quantizado em 4 bits (NF4, quantização dupla, otimizadores paginados), o que permite ajustar
  um modelo de 65B numa GPU. Testa as três famílias: encoder, encoder-decoder e decoder.

### Computação condicional (MoE, saída antecipada)
- **28. Outrageously Large Neural Networks: Sparsely-Gated MoE** (Shazeer et al. 2017) · avançado · ◐
  A origem do MoE moderno (roteador top-k e perdas de balanceamento), ainda sobre LSTM.
- **29. Switch Transformers** (Fedus, Zoph & Shazeer 2021) · avançado · ✔
  MoE com um único especialista por token sobre o T5, chegando à escala de trilhão. É o elo com o MoE dos LLMs de
  hoje.
- **30. DeeBERT** (Xin et al. 2020) · intermediário · ◐
  Saída antecipada no BERT: uma amostra sai na camada em que o classificador já está confiante. Corta até ~40% do
  tempo. É **encoder** e é nicho.

### Atenção e sequência eficientes
- **31. Reformer** (Kitaev, Kaiser & Levskaya 2020) · avançado · ✗
  Atenção por hashing (LSH) e camadas reversíveis. Foi uma variante que não pegou.
- **32. Mamba** (Gu & Dao 2023) · avançado · ✔
  Uma alternativa ao Transformer sem atenção (espaço de estados seletivo), linear no comprimento e sem KV cache. É
  atual, mas a maturidade em escala grande ainda é questão aberta.
- **33. Fast Transformer Decoding: One Write-Head is All You Need** (Shazeer 2019) · intermediário · ✔
  Multi-query attention: as cabeças compartilham chave e valor, o que encolhe o KV cache. Explica com contas simples
  por que o decode é limitado por memória. É a raiz do GQA usado nos LLMs atuais.
- **34. FlashAttention** (Dao et al. 2022) · avançado · ✔
  Atenção exata feita em blocos para não ir à memória lenta da GPU. Está embutida em quase todo stack de LLM.
- **35. Fast Inference from Transformers via Speculative Decoding** (Leviathan, Kalman & Matias 2022) · avançado · ✔
  Um modelo pequeno propõe tokens e o grande verifica, com 2–3× de ganho e a mesma saída. É base de sistemas de
  serving atuais.

### Arquitetura eficiente e NAS
- **36. MobileNets** (Howard et al. 2017) · introdutório · ✗
  Convolução separável em profundidade para celular. É CNN, fora do foco de LLM.
- **37. FBNet** (Wu et al. 2018) · intermediário · ✗
  NAS diferenciável com a latência real do celular dentro da perda. É CNN.
- **38. MobileBERT** (Sun et al. 2020) · intermediário · ◐
  Um BERT estreito com gargalos e destilação camada a camada, medido em celular real. Mostra que FLOPs não é o mesmo
  que latência. É **encoder**.

### Hardware
- **39. DianNao** (Chen et al. 2014) · avançado · ✗
  O primeiro ASIC dedicado a redes neurais. Marco histórico.
- **40. Eyeriss** (Chen et al. 2016) · avançado · ✗
  Chip de CNN com o dataflow row-stationary (reaproveitar dados para mover menos). É histórico, mas a ideia aparece
  em Sze (01).
- **41. EIE** (Han et al. 2016) · avançado · ✗
  Hardware que executa a rede já comprimida pelo Deep Compression. Decompõe o ganho de energia em fatores.
- **42. In-Datacenter Performance Analysis of a TPU** (Jouppi et al. 2017) · avançado · ◐
  A TPU v1: array sistólico int8 e roofline aplicado a hardware, com medição real contra CPU e GPU. Conta a origem da
  indústria de ASIC de IA.
- **43. FlightLLM** (Zeng et al. 2024) · avançado · ✔
  Acelerador FPGA completo (hardware, ISA e compilador) para inferência de LLM comprimido. Mostra que o decode é
  limitado por banda. É a única obra de hardware da era LLM na lista.

---

## C. Conceitos (as arquiteturas), 7 obras

- **45. Attention Is All You Need** (Vaswani et al. 2017) · intermediário · ◐
  O Transformer: atenção multi-cabeça e encoder-decoder. É a fonte de tudo que vem depois e a base do seu objetivo de
  15/09.
- **46. BERT** (Devlin et al. 2019) · intermediário · ◐
  Encoder bidirecional pré-treinado por mascaramento. É a arquitetura que DistilBERT, MobileBERT e DeeBERT comprimem,
  e a família do tema v3.
- **47. T5: Exploring the Limits of Transfer Learning** (Raffel et al. 2019) · intermediário · ◐
  Tudo como texto-para-texto. A §3.2 compara encoder-decoder, decoder-only e prefix LM com custo igualado. É a obra
  que mais responde ao seu objetivo.
- **48. GPT-3: Language Models are Few-Shot Learners** (Brown et al. 2020) · intermediário · ◐
  Decoder de 175B e aprendizado por exemplos no prompt. É o marco que transforma eficiência de LLM em problema. As
  limitações já citam destilação.
- **49. LLaMA** (Touvron et al. 2023) · intermediário · ✔
  Decoder aberto (RMSNorm, SwiGLU, RoPE) com o argumento de que treinar menor por mais tempo sai mais barato na
  inferência. É o alvo de GPTQ, SmoothQuant, SparseGPT e QLoRA.
- **50. Long Short-Term Memory** (Hochreiter & Schmidhuber 1997) · intermediário · ✗ · *só abstract*
  A rede recorrente que o Transformer substituiu.
- **51. A Survey of Large Language Models** (Zhao et al. 2023) · avançado · ✔
  144 páginas sobre pré-treino, adaptação, uso e avaliação de LLMs, leis de escala e as três famílias de arquitetura.
  Diz que a pesquisa recente quase só treina decoder. É obra de consulta, não de leitura corrida.

---

## D. Sistemas e ferramentas, 5 obras

- **52. PyTorch** (Paszke et al. 2019) · intermediário · ✔
  Por dentro do framework: execução imediata, autograd e gerência de memória da GPU. É a ferramenta sobre a qual quase
  tudo é feito.
- **53. TVM** (Chen et al. 2018) · avançado · ◐
  Compilador que gera código otimizado para CPU, GPU, FPGA e aceleradores, com busca guiada por um modelo de custo
  aprendido. Avaliado em CNN e RNN.
- **54. vLLM / PagedAttention** (Kwon et al. 2023) · intermediário · ✔ · **[lido]**
  KV cache paginado como memória virtual, com 2 a 4× de vazão. É a referência de serving.
- **55. TensorFlow Lite Micro** (David et al. 2020) · intermediário · ◐
  Inferência em microcontrolador (TinyML) sem alocação dinâmica de memória. É a implantação no extremo pequeno.
- **56. FINN** (Umuroglu et al. 2016) · avançado · ✗
  Gera aceleradores FPGA para redes totalmente binarizadas. É nicho.

---

## Seleção do Pedro (05/10)

**Saíram as 17 obras ✗**: 05, 08, 14, 17, 20, 21, 22, 24, 25, 31, 36, 37, 39, 40, 41, 50 e 56. **Ficam 39**, que
entram no gate da semana 5.

## Lacunas que o Claude vê nas 39 (opinião; você decide)

**Procedência:** título, ano e identificador foram conferidos no arXiv e na USENIX em 05/10. As descrições vêm do que
o Claude sabe dessas obras; nenhuma foi lida no projeto. As 39 são fortes em **técnica**, mas fracas em três pontos
que o critério do professor pega: o **encoder atual** (o mais novo é de 2020), o **serving atual** (só o vLLM) e o
**LLM em dispositivo** (o lado edge é quase todo CNN).

**As 5 que eu colocaria, em ordem:**

| # | Obra | Lacuna que fecha |
|---|---|---|
| 1 | **Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder...** (ModernBERT; Warner et al. 2024, arXiv:2412.13663) | É o encoder atual. Junta num BERT de 2024 as técnicas da lista (FlashAttention, RoPE, atenção local e global, remoção de padding) para ficar rápido e com pouca memória. É a família do tema v3 e o seu objetivo de arquitetura, em versão recente. |
| 2 | **GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints** (Ainslie et al. 2023, arXiv:2305.13245) | O MQA (33) é a raiz, mas o que os LLMs de hoje usam é o GQA: grupos de cabeças compartilhando chave e valor. É curto e mostra como converter um modelo já treinado. |
| 3 | **Orca: A Distributed Serving System for Transformer-Based Generative Models** (Yu et al., OSDI 2022) | A origem do *continuous batching* (escalonamento por iteração), que todo motor de serving usa, o vLLM incluído (ele se compara ao Orca). Sem ele, o vLLM fica pela metade. |
| 4 | **A Survey on Knowledge Distillation of Large Language Models** (Xu et al. 2024, arXiv:2402.13116) | O survey de destilação da lista (03) é de antes dos LLMs, e destilação é a sua trilha. Este é o mapa recente, e pode **substituir** o 03 nos 3 a 5 surveys. |
| 5 | **MobileLLM: Optimizing Sub-billion Parameter Language Models for On-Device Use Cases** (Liu et al. 2024, arXiv:2402.14905) | LLM pequeno para celular: decisões de arquitetura (profundo e estreito, compartilhamento de embeddings, GQA) com abaixo de 1B de parâmetros. Fecha o lado edge com LLM, não com CNN. |

**Se sobrar espaço:** AWQ (arXiv:2306.00978, quantização de pesos muito usada nas ferramentas, par do GPTQ) ·
DistServe (arXiv:2401.09670, separa prefill e decode em máquinas diferentes, serving de 2024) · MiniLLM
(arXiv:2306.08543, destilação de LLM gerador) · SGLang (arXiv:2312.07104, reaproveitamento de prefixo no KV cache).

**Lacuna que não vira obra:** as ferramentas de implantação mais usadas hoje (llama.cpp, TensorRT-LLM, ONNX Runtime)
se documentam em repositório e manual, não em paper. Se o gate pedir ferramentas, elas entram como ferramentas, não
como obras.

## Obras adicionadas pelo Pedro (07/10)

A lista passa de 39 para **50 obras**. Tabela com nome, autor e link: `docs/screening/fase1/Lista de Obras.docx`.
Identificadores conferidos no arXiv, no Semantic Scholar e na ACL Anthology.

- Já lidas por ele: Distilling Step-by-Step (Hsieh et al., 2023); DHRD (Xu et al., 2025); Agrawal, Ahemad e Sembium
  (2025); Wadhwa et al. (2024); Chen et al. (2025, adaptive thinking); KPOD (Feng et al., 2024); EasyDistill (Wang et
  al., 2025). DistilBERT, Hinton, Yuan e Kwon já estavam na lista.
- Pedidas por ele: e-SNLI (Camburu et al., 2018); Large Language Models Are Reasoning Teachers (Ho et al., 2023);
  survey de CoT de Chu et al. (2024); Chain-of-Knowledge Prompting (Wang et al., 2024).
