# Lista rápida v2: ~50 obras para a base da área, escolhidas pelo júri de surveys (27/09)

**Procedência: nível 3.** Ninguém leu as obras. Os votos são metadado (quem cita quem), e metadado é confiável; as
divisões e os ajustes são classificação do Claude a partir do título. **A decisão final é sua** (§6). Plano aprovado em
27/09: `2026-09-27-plano-lista-rapida.md`.

## 1. O que foi feito

1. **Júri:** 57 surveys do gabarito + 55 relevantes da F2 (**91 com referências**), mais uma **reserva de hardware**
   (133 surveys com termo de hardware e contexto de modelo/IA no título, 115 com referências), porque hardware "é bem
   importante" (Pedro, 27/09). **Os votos da reserva só contam para hardware**: sem essa trava, ela seria maior que o
   júri validado e dominaria a lista.
2. **Votos:** cada jurado vota nas obras que cita (S2 obra a obra + OpenAlex, unificados por DOI ou título).
   **1.458 obras** receberam 3 ou mais votos; 648 receberam 5 ou mais; 213, 10 ou mais.
3. **Divisões:** os grupos do pool eram grossos demais. O consenso mostrou divisões que o pool não nomeia (NAS e
   arquitetura eficiente, atenção eficiente, computação condicional). Ficaram **11 divisões**, atribuídas pelo
   **título**, porque o abstract gerou ruído (o BERT saiu como "hardware").
4. **Seleção por regras** (`l3_seleciona.py`): o survey mais votado de cada divisão (mapas); os mais votados por
   divisão, espalhados por época (fundadores); listas nomeadas de conceitos e de sistemas, escolhidas pelos votos.
5. **Revisão do Claude** (`l4_lista_v2.py`): **18 dos 56 itens são ajustes** sobre a regra, cada um com motivo (§4).

## 2. A lista (56 obras)

### A mapas

| # | Ano | Título | Divisão | Votos do júri | Origem |
|---|---|---|---|---|---|
| 1 | 2017 | Efficient Processing of Deep Neural Networks: A Tutorial and Survey | hardware | 14 (+25 reserva) | **ajuste** |
| 2 | 2020 | Model Compression and Hardware Acceleration for Neural Networks: A Comprehensive Survey | compressão (geral) | 14 | regra |
| 3 | 2020 | Knowledge Distillation: A Survey | destilação | 15 | regra |
| 4 | 2021 | A Survey of Quantization Methods for Efficient Neural Network Inference | quantização | 13 | regra |
| 5 | 2021 | Pruning and Quantization for Deep Neural Network Acceleration: A Survey | poda e esparsidade | 8 | **ajuste** |
| 6 | 2022 | A Review of Sparse Expert Models in Deep Learning | computação condicional | 4 | **ajuste** |
| 7 | 2020 | Efficient Transformers: A Survey | atenção e sequência eficientes | 9 | regra |
| 8 | 2020 | A Comprehensive Survey of Neural Architecture Search | arquitetura eficiente e NAS | 5 | regra |
| 9 | 2024 | Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey | ajuste eficiente (PEFT) | 4 | regra |
| 10 | 2023 | Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems | inferência e serving | 6 | regra |
| 11 | 2023 | A Survey on Model Compression for Large Language Models | compressão de LLM | 7 | regra |
| 12 | 2024 | LLM Inference Unveiled: Survey and Roofline Model Insights | inferência e serving | 5 | regra |
| 13 | 2025 | Empowering Edge Intelligence: A Comprehensive Survey on On-Device AI Models | edge e on-device | (jurado; 2025) | regra |

### B fundadores

| # | Ano | Título | Divisão | Votos do júri | Origem |
|---|---|---|---|---|---|
| 1 | 2006 | Model compression | destilação | 20 | **ajuste** |
| 2 | 2015 | Distilling the Knowledge in a Neural Network | destilação | 40 | regra |
| 3 | 2019 | DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter | destilação | 18 | regra |
| 4 | 2016 | XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks | quantização | 22 | **ajuste** |
| 5 | 2022 | GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers | quantização | 15 | **ajuste** |
| 6 | 2022 | SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models | quantização | 18 | regra |
| 7 | 1989 | Optimal Brain Damage | poda e esparsidade | 24 | regra |
| 8 | 2015 | Deep Compression: Compressing Deep Neural Network with Pruning, Trained Quantization and Huffman Coding | poda e esparsidade | 22 | **ajuste** |
| 9 | 2018 | The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks | poda e esparsidade | 21 | regra |
| 10 | 2023 | SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot | poda e esparsidade | 14 | regra |
| 11 | 2014 | Exploiting Linear Structure Within Convolutional Networks for Efficient Evaluation | fatoração de baixo posto | 12 | regra |
| 12 | 2013 | Low-rank matrix factorization for Deep Neural Network training with high-dimensional output targets | fatoração de baixo posto | 10 | **ajuste** |
| 13 | 2021 | LoRA: Low-Rank Adaptation of Large Language Models | ajuste eficiente (PEFT) | 12 | **ajuste** |
| 14 | 2023 | QLoRA: Efficient Finetuning of Quantized LLMs | ajuste eficiente (PEFT) | 16 | **ajuste** |
| 15 | 2017 | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | computação condicional | 7 | **ajuste** |
| 16 | 2021 | Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity | computação condicional | 12 | regra |
| 17 | 2020 | DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference | computação condicional | 11 | **ajuste** |
| 18 | 2020 | Reformer: The Efficient Transformer | atenção e sequência eficientes | 12 | regra |
| 19 | 2023 | Mamba: Linear-Time Sequence Modeling with Selective State Spaces | atenção e sequência eficientes | 10 | regra |
| 20 | 2019 | Fast Transformer Decoding: One Write-Head is All You Need | inferência e serving | 6 | regra |
| 21 | 2022 | FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness | inferência e serving | 12 | regra |
| 22 | 2022 | Fast Inference from Transformers via Speculative Decoding | inferência e serving | 9 | **ajuste** |
| 23 | 2017 | MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications | arquitetura eficiente e NAS | 21 | regra |
| 24 | 2018 | FBNet: Hardware-Aware Efficient ConvNet Design via Differentiable Neural Architecture Search | arquitetura eficiente e NAS | 16 | **ajuste** |
| 25 | 2020 | MobileBERT: a Compact Task-Agnostic BERT for Resource-Limited Devices | arquitetura eficiente e NAS | 12 | **ajuste** |
| 26 | 2014 | DianNao: a small-footprint high-throughput accelerator for ubiquitous machine-learning | hardware | 6 (+13 reserva) | **ajuste** |
| 27 | 2016 | Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks | hardware | 7 (+30 reserva) | regra |
| 28 | 2016 | EIE: Efficient Inference Engine on Compressed Deep Neural Network | hardware | 10 (+17 reserva) | regra |
| 29 | 2017 | In-datacenter performance analysis of a tensor processing unit | hardware | 5 (+27 reserva) | **ajuste** |
| 30 | 2024 | FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs | hardware | 4 (+6 reserva) | regra |
| 31 | 2017 | Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference | edge e on-device | 14 | **ajuste** |

### C conceitos

| # | Ano | Título | Divisão | Votos do júri | Origem |
|---|---|---|---|---|---|
| 1 | 2017 | Attention is All you Need |  | 35 | regra |
| 2 | 2019 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding |  | 27 | regra |
| 3 | 2019 | Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer |  | 18 | regra |
| 4 | 2020 | Language Models are Few-Shot Learners |  | 30 | regra |
| 5 | 2023 | LLaMA: Open and Efficient Foundation Language Models |  | 14 | regra |
| 6 | 1997 | Long Short-Term Memory |  | 12 | regra |
| 7 | 2023 | A Survey of Large Language Models |  | 9 | regra |

### D sistemas

| # | Ano | Título | Divisão | Votos do júri | Origem |
|---|---|---|---|---|---|
| 1 | 2019 | PyTorch: An Imperative Style, High-Performance Deep Learning Library |  | 12 | regra |
| 2 | 2018 | TVM: An Automated End-to-End Optimizing Compiler for Deep Learning |  | 8 | regra |
| 3 | 2023 | Efficient Memory Management for Large Language Model Serving with PagedAttention | inferência e serving | 12 | regra |
| 4 | 2020 | TensorFlow Lite Micro: Embedded Machine Learning on TinyML Systems | edge e on-device | 3 | regra |
| 5 | 2016 | FINN: A Framework for Fast, Scalable Binarized Neural Network Inference | hardware | 3 (+11 reserva) | regra |

## 3. Conferência contra o critério de sucesso do plano

| Critério | Resultado |
|---|---|
| Toda divisão com >= 1 mapa | **10 de 11**; **fatoração de baixo posto não tem survey co-citado** (lacuna real do consenso) |
| Toda divisão com >= 2 fundadores | **10 de 11**; edge tem 1 fundador, mas conta com MobileNets (NAS), TFLite Micro (sistema) e um mapa de 2025 |
| Toda pergunta coberta | P1 mapa: 13 mapas · P3/P6 história: 14 fundadores até 2017 · P2 conteúdo: tutorial de Sze e os mapas · P4a como fazer: 5 sistemas · P4b destilação: 3 fundadores + mapa (a lista de 24/09 aprofunda) · V vocabulário: os mapas · A atualidade: 5 mapas de 2023–25 · **R arquitetura: BERT (encoder), T5 (encoder-decoder), GPT-3 e LLaMA (decoder), multi-query attention (KV cache de decoder), MobileBERT e DistilBERT (encoder compacto)** |
| Consistência com a lista de destilação de 24/09 | bate: Buciluă, Hinton, DistilBERT e o survey de Gou estão nas duas |
| Você aprova >= 80% | **a medir na sua revisão** |

## 4. Os 18 ajustes, com motivo

Os ajustes corrigem erros das regras automáticas (palavra casando por acaso, divisão errada, obra sem palavra-chave) e
aplicam o critério de **acréscimo** (tirar a segunda obra que repete a primeira). Os votos continuam valendo: nenhum
ajuste pôs uma obra com poucos votos no lugar de uma com muitos sem dizer por quê.

- **Efficient Processing of Deep Neural Networks: A Tutorial and Survey** — a regra não achou divisão pelo título; é o survey mais votado de hardware (14 + 25 da reserva)
- **Pruning and Quantization for Deep Neural Network Acceleration: A Surve** — a regra pôs 'Sparse Expert Models' (é MoE) como mapa de poda
- **A Review of Sparse Expert Models in Deep Learning** — movido de poda para computação condicional; substitui o survey de early exiting (mesmos 4 votos, MoE pesa mais na era LLM)
- **Model compression** — Buciluă 2006 (20 votos) perdeu a vaga para a cota de época; é a origem da destilação
- **XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Ne** — excluído pela regra por ter 'ImageNet' no título (22 votos)
- **GPTQ: Accurate Post-Training Quantization for Generative Pre-trained T** — substitui HAWQ; GPTQ tem mais votos (15 × 13) e é base da quantização de LLM
- **Deep Compression: Compressing Deep Neural Network with Pruning, Traine** — movido de quantização para poda (o título começa por pruning; é o pipeline clássico)
- **Low-rank matrix factorization for Deep Neural Network training with hi** — segundo fundador exigido pelo critério de sucesso (10 votos; o mais votado depois de Denton)
- **LoRA: Low-Rank Adaptation of Large Language Models** — a regra pôs LoRA em baixo posto; é o fundador do PEFT
- **QLoRA: Efficient Finetuning of Quantized LLMs** — a regra pôs em PEFT um paper de FPGA ('exp-LORA-tion' casou com LoRA)
- **Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Expe** — origem do MoE moderno (7 votos); substitui o paper de Bengio 2013, citado pelo estimador straight-through da quantização, não por computação condicional
- **DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference** — early exit, a outra metade da divisão
- **Fast Inference from Transformers via Speculative Decoding** — substitui FlashAttention-2 (redundante com FlashAttention; critério de acréscimo)
- **FBNet: Hardware-Aware Efficient ConvNet Design via Differentiable Neur** — substitui MobileNetV2 (redundante com MobileNets); NAS ciente de hardware, 16 votos
- **MobileBERT: a Compact Task-Agnostic BERT for Resource-Limited Devices** — encoder compacto (12 votos); liga a divisão às arquiteturas de linguagem
- **DianNao: a small-footprint high-throughput accelerator for ubiquitous ** — origem da família DianNao (6 + 13 = 19 votos, empate prático com DaDianNao, 20)
- **In-datacenter performance analysis of a tensor processing unit** — TPU (5 + 27 = 32 votos) não casou com a regra por falta de palavra-chave; substitui Eyeriss v2 (redundante)
- **Quantization and Training of Neural Networks for Efficient Integer-Ari** — inferência inteira em dispositivo (14 + 10 votos); substitui um paper de 4 votos

## 5. Limites

- **O consenso favorece o que é antigo e o que é central.** Mesmo com a cota por época, 14 dos 31 fundadores são de até
  2017, e boa parte da história da compressão é de CNN. Pelo §1.3 isso vale como **história**, não como técnica em uso.
- **Hardware é quase todo CNN-era** (DianNao, Eyeriss, EIE, TPU); a exceção é FlightLLM (2024). O hardware para LLM
  ainda não tem consenso de citação.
- **Divisões de cima para baixo e por título:** podem esconder uma divisão que os surveys declaram e esta lista não nomeia.
- **18 ajustes em 56 (32%)** é muito: as regras sozinhas não bastaram. Cada ajuste está justificado, mas são julgamento
  do Claude sobre título e votos.
- **Os 21 jurados sem referências não votaram** (a maioria é de editora fechada).

## 6. Decisões do Pedro

1. **Revisar a lista por título:** marque o que sai, o que muda de bloco e o que falta. O critério de sucesso é 80% de
   aprovação.
2. **Os 18 ajustes:** aceitar em bloco ou olhar um por um?
3. **Lacunas:** fatoração de baixo posto sem mapa e hardware para LLM sem consenso. Aceitar e declarar, ou buscar
   (um survey recente de baixo posto para LLM; um de aceleradores para LLM)?
4. **Tamanho:** 56 está um pouco acima de ~50. Cortar, e onde (candidatos: o segundo fundador de fatoração de baixo
   posto, LLaMA, TFLite Micro)?

## 7. Arquivos

`docs/screening/fase1/lista-rapida/`: `juri.csv` · `candidatas.csv` (1.458 obras com >= 3 votos; **ordena, não apaga**) ·
`candidatas-marcadas.csv` · `lista-v1.csv` (só regras) · **`lista-v2.csv`** · caches do S2 e do OpenAlex. Scripts em
`scripts/screening/lista/` (`l1_votos.py` -> `l4_lista_v2.py`).
