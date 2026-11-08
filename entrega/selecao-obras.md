# Seleção das Obras

## 1. Calibração dos agentes de leitura

Antes de usar agentes de LLM para ler obras, testei-os num conjunto em que eu já sabia a resposta: 28 surveys da metade de ajuste da minha referência e 30 obras que eu já tinha classificado como fora da área. Os agentes não eliminaram nenhum survey da área e marcaram como relevante ou dúvida 26 dos 27 que tinham resumo disponível (96%). Nenhuma obra de fora chegou a relevante. Fiz isso porque só posso confiar numa leitura automática depois de medir quanto ela erra.

## 2. Leitura por amostragem

Com os agentes calibrados, sorteei 962 obras dos grupos que sobraram da limpeza e pedi que os agentes lessem e classificassem cada uma. O objetivo era medir quanto do que sobrou é de fato da área. O resultado: cerca de metade das 11.544 obras restantes é da área pelo assunto. Ou seja, o corte por assunto já estava feito, e o que faltava era outra coisa: escolher, entre milhares de obras da área, as que servem para aprender a área.

## 3. O que conta como relevante

Ser do assunto não diz se uma obra serve para montar uma base. Por isso escrevi as perguntas que uma obra precisa responder para entrar:

- Ela mostra como a área se organiza (um mapa)?
- Ela me ensina como as técnicas funcionam?
- Ela conta como a área nasceu, ou é ela mesma o trabalho que abriu uma linha?
- Ela me ensina a fazer algo da área (ferramenta, framework, prática)?
- Ela me dá o vocabulário da área?
- Ela mostra a área como é hoje?
- Ela explica como encoder, decoder e encoder-decoder mudam o problema?

Para escrever essas perguntas, usei literatura sobre critérios de relevância levantada e lida com apoio de LLM (o guia de scoping review da JBI; Levac et al., 2010; Saracevic, 2007). A ideia que tirei dela: o critério sai das perguntas que se quer responder, e relevância de assunto é diferente de relevância para a tarefa.

## 4. Os surveys como júri

Em vez de ler surveys um a um para construir o mapa, usei os surveys como júri. Cada survey vota nas obras que cita, e as obras que muitos surveys citam em comum formam a lista. Fiz isso porque quem escreve survey é especialista, e o que muitos deles citam em comum é o consenso da área sobre o que importa.

- Júri: 57 surveys da minha referência e 55 surveys que os agentes marcaram como relevantes; 91 deles tinham a lista de referências disponível;
- Hardware: considero hardware uma parte importante da área. Por isso acrescentei 133 surveys de hardware como júri extra, mas os votos deles contam só para o grupo de hardware, para não dominar o resto da lista;
- Resultado: 1.458 obras receberam 3 ou mais votos;
- Divisões: as obras foram separadas em 11 divisões (quantização, poda, destilação, fatoração de baixo posto, ajuste eficiente, computação condicional, atenção eficiente, inferência e serving, arquitetura eficiente, hardware e edge). As divisões saíram dos próprios dados: o consenso mostrou divisões que a minha lista inicial de termos não tinha;
- Seleção: em cada divisão, as mais votadas, espalhadas por época (até 2017, 2018-21, 2022 em diante), para a lista não ficar só com obras antigas, que tiveram mais tempo de ser citadas.

A lista final tem 56 obras em quatro grupos:

- Mapas (13): surveys que organizam a área ou uma divisão;
- Fundadores (31): os trabalhos que abriram cada linha;
- Conceitos (7): o que todos assumem que o leitor sabe (Transformer, BERT, T5, GPT-3, LLaMA, LSTM);
- Sistemas (5): ferramentas (PyTorch, TVM, vLLM, TFLite Micro, FINN).

Uso de LLM: a contagem de votos, a separação em divisões e uma revisão das regras automáticas foram feitas com LLM. Dezoito obras da lista são ajustes dessa revisão sobre as regras (por exemplo, obras repetidas e palavras que casaram por acaso), cada um com motivo registrado.

## 5. Fichas das 56 obras

Pedi que agentes de LLM lessem as 56 obras, 53 delas no texto completo, e escrevessem uma ficha de cada uma: o que a obra traz para a base, as perguntas da seção 3 que ela responde, o nível (introdutório, intermediário ou avançado), os pré-requisitos e por onde começar a ler. Fiz isso porque preciso saber o que cada obra traz antes de decidir a ordem de leitura. As fichas mostram, por exemplo, que só 4 das 56 são introdutórias, e que a história da área é mais contada pelos trabalhos fundadores do que pelos surveys.

## 6. As 10 primeiras leituras

Com as fichas, escolhi as 10 primeiras leituras, em ordem de pré-requisito, cobrindo a área inteira, as três famílias de arquitetura e hardware, e sem obras que repetem a mesma coisa:

| Ordem | Obra | Por quê |
|---|---|---|
| 1 | Attention is All you Need (Vaswani et al., 2017) | a arquitetura que quase todas as outras assumem |
| 2 | Exploring the Limits of Transfer Learning, T5 (Raffel et al., 2019), só a parte de arquiteturas | compara encoder-decoder, decoder-only e prefix LM no mesmo experimento |
| 3 | Distilling the Knowledge in a Neural Network (Hinton et al., 2015) | a origem da destilação |
| 4 | DistilBERT (Sanh et al., 2019) | destilação aplicada a um encoder |
| 5 | Efficient Processing of Deep Neural Networks: A Tutorial and Survey (Sze et al., 2017) | mapa, história e hardware no mesmo texto |
| 6 | Deep Compression (Han et al., 2015) | o pipeline clássico de compressão |
| 7 | A Survey of Quantization Methods for Efficient Neural Network Inference (Gholami et al., 2021) | a maior divisão da área |
| 8 | Efficient Transformers: A Survey (Tay et al., 2020) | mapa da eficiência do transformer |
| 9 | LLM Inference Unveiled (Yuan et al., 2024) | mapa atual e o modelo roofline |
| 10 | Efficient Memory Management for LLM Serving with PagedAttention, vLLM (Kwon et al., 2023) | o motor de serving de referência |

## 7. Frameworks

Uso framework nos dois sentidos da definição: estrutura que oferece diretrizes, práticas e ferramentas prontas para orientar um projeto. Na lista aparecem os dois tipos:

- Ferramentas (software): vLLM, TensorRT-LLM e DeepSpeed-Inference (servir LLMs); TVM e TensorRT (compilar para hardware); TFLite Micro (rodar em microcontrolador); FINN (FPGA); PyTorch (desenvolver e treinar);
- Diretrizes (conceituais): o modelo roofline, que diz se o gargalo de um modelo é memória ou computação e onde otimizar; o pipeline poda, quantização e codificação; e as escolhas de quantização (quando quantizar depois do treino e quando treinar já quantizado).

As obras da lista servem para achar e situar os frameworks. Para aprender cada framework de software, a fonte é a documentação oficial dele.

## 8. A lista completa

| Nº | Grupo | Ano | Obra | Divisão |
|---|---|---|---|---|
| 1 | Mapas | 2017 | Efficient Processing of Deep Neural Networks: A Tutorial and Survey | hardware |
| 2 | Mapas | 2020 | Model Compression and Hardware Acceleration for Neural Networks: A Comprehensive Survey | compressão (geral) |
| 3 | Mapas | 2020 | Knowledge Distillation: A Survey | destilação |
| 4 | Mapas | 2021 | A Survey of Quantization Methods for Efficient Neural Network Inference | quantização |
| 5 | Mapas | 2021 | Pruning and Quantization for Deep Neural Network Acceleration: A Survey | poda e esparsidade |
| 6 | Mapas | 2022 | A Review of Sparse Expert Models in Deep Learning | computação condicional |
| 7 | Mapas | 2020 | Efficient Transformers: A Survey | atenção e sequência eficientes |
| 8 | Mapas | 2020 | A Comprehensive Survey of Neural Architecture Search | arquitetura eficiente e NAS |
| 9 | Mapas | 2024 | Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey | ajuste eficiente (PEFT) |
| 10 | Mapas | 2023 | Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems | inferência e serving |
| 11 | Mapas | 2023 | A Survey on Model Compression for Large Language Models | compressão de LLM |
| 12 | Mapas | 2024 | LLM Inference Unveiled: Survey and Roofline Model Insights | inferência e serving |
| 13 | Mapas | 2025 | Empowering Edge Intelligence: A Comprehensive Survey on On-Device AI Models | edge e on-device |
| 14 | Fundadores | 2006 | Model compression | destilação |
| 15 | Fundadores | 2015 | Distilling the Knowledge in a Neural Network | destilação |
| 16 | Fundadores | 2019 | DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter | destilação |
| 17 | Fundadores | 2016 | XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks | quantização |
| 18 | Fundadores | 2022 | GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers | quantização |
| 19 | Fundadores | 2022 | SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models | quantização |
| 20 | Fundadores | 1989 | Optimal Brain Damage | poda e esparsidade |
| 21 | Fundadores | 2015 | Deep Compression: Compressing Deep Neural Network with Pruning, Trained Quantization and Huffman Coding | poda e esparsidade |
| 22 | Fundadores | 2018 | The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks | poda e esparsidade |
| 23 | Fundadores | 2023 | SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot | poda e esparsidade |
| 24 | Fundadores | 2014 | Exploiting Linear Structure Within Convolutional Networks for Efficient Evaluation | fatoração de baixo posto |
| 25 | Fundadores | 2013 | Low-rank matrix factorization for Deep Neural Network training with high-dimensional output targets | fatoração de baixo posto |
| 26 | Fundadores | 2021 | LoRA: Low-Rank Adaptation of Large Language Models | ajuste eficiente (PEFT) |
| 27 | Fundadores | 2023 | QLoRA: Efficient Finetuning of Quantized LLMs | ajuste eficiente (PEFT) |
| 28 | Fundadores | 2017 | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | computação condicional |
| 29 | Fundadores | 2021 | Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity | computação condicional |
| 30 | Fundadores | 2020 | DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference | computação condicional |
| 31 | Fundadores | 2020 | Reformer: The Efficient Transformer | atenção e sequência eficientes |
| 32 | Fundadores | 2023 | Mamba: Linear-Time Sequence Modeling with Selective State Spaces | atenção e sequência eficientes |
| 33 | Fundadores | 2019 | Fast Transformer Decoding: One Write-Head is All You Need | inferência e serving |
| 34 | Fundadores | 2022 | FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness | inferência e serving |
| 35 | Fundadores | 2022 | Fast Inference from Transformers via Speculative Decoding | inferência e serving |
| 36 | Fundadores | 2017 | MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications | arquitetura eficiente e NAS |
| 37 | Fundadores | 2018 | FBNet: Hardware-Aware Efficient ConvNet Design via Differentiable Neural Architecture Search | arquitetura eficiente e NAS |
| 38 | Fundadores | 2020 | MobileBERT: a Compact Task-Agnostic BERT for Resource-Limited Devices | arquitetura eficiente e NAS |
| 39 | Fundadores | 2014 | DianNao: a small-footprint high-throughput accelerator for ubiquitous machine-learning | hardware |
| 40 | Fundadores | 2016 | Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks | hardware |
| 41 | Fundadores | 2016 | EIE: Efficient Inference Engine on Compressed Deep Neural Network | hardware |
| 42 | Fundadores | 2017 | In-datacenter performance analysis of a tensor processing unit | hardware |
| 43 | Fundadores | 2024 | FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs | hardware |
| 44 | Fundadores | 2017 | Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference | edge e on-device |
| 45 | Conceitos | 2017 | Attention is All you Need | - |
| 46 | Conceitos | 2019 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | - |
| 47 | Conceitos | 2019 | Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer | - |
| 48 | Conceitos | 2020 | Language Models are Few-Shot Learners | - |
| 49 | Conceitos | 2023 | LLaMA: Open and Efficient Foundation Language Models | - |
| 50 | Conceitos | 1997 | Long Short-Term Memory | - |
| 51 | Conceitos | 2023 | A Survey of Large Language Models | - |
| 52 | Sistemas | 2019 | PyTorch: An Imperative Style, High-Performance Deep Learning Library | - |
| 53 | Sistemas | 2018 | TVM: An Automated End-to-End Optimizing Compiler for Deep Learning | - |
| 54 | Sistemas | 2023 | Efficient Memory Management for Large Language Model Serving with PagedAttention | inferência e serving |
| 55 | Sistemas | 2020 | TensorFlow Lite Micro: Embedded Machine Learning on TinyML Systems | edge e on-device |
| 56 | Sistemas | 2016 | FINN: A Framework for Fast, Scalable Binarized Neural Network Inference | hardware |
