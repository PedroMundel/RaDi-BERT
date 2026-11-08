# Camada B — proposta detalhada por grupo (23/09/2026)

**PROPOSTA DO CLAUDE, NÍVEL 3 — nada decidido.** Pedido do Pedro: *"me manda a proposta com as categorias mais detalhado"*. Substitui a classificação aplicada na seção 7 do relatório da camada B, que foi feita sem ele revisar grupo a grupo (erro de processo meu). A coluna `camada_B` do CSV é provisória e será reescrita com as decisões dele. Nada foi apagado.

## Como ler

- **obras**: tamanho do grupo depois que as obras sem grupo foram postas no grupo mais parecido.
- **cajuzeiros**: quantas das 28 obras da metade de ajuste do gabarito caíram no grupo.
- **surveys**: obras com palavra de tipo (survey, review…) no título.
- **salvaguarda**: obras com palavra de tipo **e** termo núcleo do pool no título. Em todo grupo marcado "fora", **essas obras não saem** — vão para a camada C. É a mesma regra que você escolheu na camada A.
- **exemplos**: as mais citadas do grupo; **salvas pela salvaguarda**: as mais citadas entre as que a salvaguarda segura.

## Resumo

| categoria | grupos | obras | o que acontece |
|---|---|---|---|
| 1. Núcleo — a área em si | 2 | 5682 | segue inteiro para a camada C |
| 2. Pilar arquiteturas (§1.1 do método) | 1 | 554 | segue inteiro |
| 3. Dentro por regra já decidida | 1 | 767 | segue inteiro |
| 4. Misto — a área está dentro, misturada com outra coisa | 3 | 5752 | segue inteiro para a camada C (lá você separa obra por obra) |
| 5. A testar (grupo `uso?` do pool) | 1 | 1194 | segue para a camada C, marcado |
| 6. Fora por regra já decidida (§1.2.1 b: difusão e GNN) | 2 | 890 | fora, com a salvaguarda do título |
| 7. Outra área | 56 | 59952 | fora, com a salvaguarda do título |

**Mudança em relação à versão anterior — grupos 6 (imagem médica) e 12 (detecção de objetos):** antes
estavam como "regra §1.2.1 c, espera divisão". Olhando os grupos inteiros, eles são **IA aplicada**
(diagnóstico, direção autônoma), não eficiência aplicada: dos 2.905 do grupo 6, só 48 têm termo núcleo
no título. Proponho tratá-los como outra área; os 48 + 45 que são eficiência aplicada (*efficient deep
neural networks for medical image analysis*…) são segurados pela salvaguarda e, na camada C, você os
marca como "espera divisão" pela regra (c).

Nas categorias 6 e 7, a salvaguarda segura **952** obras (vão para a camada C).

---

## 1. Núcleo — a área em si

**Destino proposto:** segue inteiro para a camada C.  
**Por quê:** É onde estão 23 dos 28 cajuzeiros conhecidos da metade de ajuste. Não há o que discutir aqui.

### Grupo 2 — inferência eficiente, serving, compressão (o coração da área)

obras **4805** · cajuzeiros **21** · surveys 988 · salvaguarda 290 · palavras: *serving, inference, efficient, llm, edge, memory, hardware, neural*

- exemplos: *Efficient Memory Management for Large Language Model Serving with PagedAttention* (8424) · *Memory devices and applications for in-memory computing* (2137) · *A Survey of Quantization Methods for Efficient Neural Network Inference* (1717)
- salvas pela salvaguarda: *A Survey of Quantization Methods for Efficient Neural Network Inference* · *Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey* · *Pruning and Quantization for Deep Neural Network Acceleration: A Survey*

### Grupo 36 — destilação de conhecimento

obras **877** · cajuzeiros **2** · surveys 335 · salvaguarda 66 · palavras: *distillation, knowledge distillation, knowledge, shot, learning, adaptation, survey, continual*

- exemplos: *Knowledge Distillation: A Survey* (4643) · *A Survey on Contrastive Self-supervised Learning* (1812) · *Revisiting Deep Learning Models for Tabular Data* (1773)
- salvas pela salvaguarda: *Knowledge Distillation: A Survey* · *Knowledge Distillation and Student-Teacher Learning for Visual Intelligence: A Review and New Outlooks* · *Distilling Knowledge via Knowledge Review*

---

## 2. Pilar arquiteturas (§1.1 do método)

**Destino proposto:** segue inteiro.  
**Por quê:** O pilar de arquiteturas (transformer, encoder, decoder) é parte fixa da Etapa 1 e é o que você disse que quer aprender. O grupo de Vision Transformer contém *Efficient Transformers: A Survey*, que é cajuzeiro. Corrigindo o meu erro: ele não devia ter ficado pendente de pergunta nenhuma.

### Grupo 49 — visão computacional e Vision Transformer

obras **554** · cajuzeiros **0** · surveys 285 · salvaguarda 23 · palavras: *vision, computer vision, image classification, image, transformers, vision transformers, attention, computer*

- exemplos: *A Survey on Vision Transformer* (3920) · *Image Segmentation Using Deep Learning: A Survey* (3915) · *Transformers in Vision: A Survey* (3843)
- salvas pela salvaguarda: *Efficient Transformers: A Survey* · *Parameter-Efficient Fine-Tuning for Pre-Trained Vision Models: A Survey* · *Review of Lightweight Deep Convolutional Neural Networks*

---

## 3. Dentro por regra já decidida

**Destino proposto:** segue inteiro.  
**Por quê:** §1.2.1 (d), decidido por você em 22/09: infraestrutura de implantação (edge, offloading) está dentro — "ajuda a mapear a área".

### Grupo 46 — edge computing e offloading (infraestrutura)

obras **767** · cajuzeiros **0** · surveys 364 · salvaguarda 19 · palavras: *edge computing, computing, edge, offloading, mobile edge, computation, cloud, task*

- exemplos: *An Overview on Edge Computing Research* (974) · *A Full Dive Into Realizing the Edge-Enabled Metaverse: Visions, Enabling Technologies, and Challenges* (483) · *Communication-Efficient Edge AI: Algorithms and Systems* (454)
- salvas pela salvaguarda: *Empowering Edge Intelligence: A Comprehensive Survey on On-Device AI Models* · *Pervasive AI for IoT Applications: A Survey on Resource-Efficient Distributed Artificial Intelligence* · *A Survey on Edge Intelligence and Lightweight Machine Learning Support for Future Applications and Services*

---

## 4. Misto — a área está dentro, misturada com outra coisa

**Destino proposto:** segue inteiro para a camada C (lá você separa obra por obra).  
**Por quê:** Grupo 5: surveys de PEFT e de destilação de LLM convivem com tradução e PLN geral (5 cajuzeiros de ajuste estão aqui). Grupo 16: federado, com vários surveys de federado para dispositivo restrito. Grupo 43: não é assunto — é onde caíram editoriais e obras de metadado ruim, e junto caíram cajuzeiros (*A comprehensive survey on model compression and acceleration*, *A Survey on Mixture of Experts*).

### Grupo 5 — modelos de linguagem e PLN em geral

obras **3709** · cajuzeiros **5** · surveys 1372 · salvaguarda 66 · palavras: *language, language models, models, large language, large, translation, natural language, natural*

- exemplos: *Survey of Hallucination in Natural Language Generation* (5953) · *Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing* (5795) · *A Survey of Large Language Models* (5013)
- salvas pela salvaguarda: *Parameter-Efficient Fine-Tuning Methods for Pretrained Language Models: A Critical Review and Assessment* · *A Survey on Knowledge Distillation of Large Language Models* · *A Comprehensive Survey of Small Language Models in the Era of Large Language Models: Techniques, Enhancements, Applications, Collaboration with LLMs, and Trustworthiness*

### Grupo 43 — METADADO RUIM: editoriais, prefácios, capítulos (não é assunto)

obras **1171** · cajuzeiros **0** · surveys 336 · salvaguarda 47 · palavras: *note, ii, journal, designing, 2021, information, preface, international*

- exemplos: *Digital twin paradigm: A systematic literature review* (810) · *A comprehensive survey on model compression and acceleration* (542) · *Physical unclonable functions* (406)
- salvas pela salvaguarda: *A comprehensive survey on model compression and acceleration* · *An updated survey of variants and extensions of the resource-constrained project scheduling problem* · *A Survey on Mixture of Experts*

### Grupo 16 — aprendizado federado e privacidade

obras **872** · cajuzeiros **0** · surveys 383 · salvaguarda 28 · palavras: *federated, federated learning, privacy, privacy preserving, preserving, learning, survey federated, survey*

- exemplos: *Federated Learning for Internet of Things: A Comprehensive Survey* (1495) · *A survey on security and privacy of federated learning* (1453) · *Federated Learning on Non-IID Data: A Survey* (1443)
- salvas pela salvaguarda: *A Survey on Federated Learning for Resource-Constrained IoT Devices* · *A Review on Federated Learning Architectures for Privacy-Preserving AI: Lightweight and Secure Cloud–Edge–End Collaboration* · *Small models, big impact: A review on the power of lightweight Federated Learning*

---

## 5. A testar (grupo `uso?` do pool)

**Destino proposto:** segue para a camada C, marcado.  
**Por quê:** MLOps: você marcou em 22/09 para testar contra §1.2 — descreve atividades de implantação, mas não reduz custo de modelo. O teste é na camada C.

### Grupo 52 — MLOps e engenharia de software de ML

obras **1194** · cajuzeiros **0** · surveys 325 · salvaguarda 34 · palavras: *mlops, software, requirements, software development, development, literature review, literature, learning operations*

- exemplos: *Machine Learning Operations (MLOps): Overview, Definition, and Architecture* (706) · *AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges* (552) · *Agile Software Development: Methodologies and Trends* (336)
- salvas pela salvaguarda: *Embedded fuzzing: a review of challenges, tools, and solutions* · *Lightweight Software Architecture Evaluation for Industry: A Comprehensive Review* · *Advanced Digital Technologies in the Post-Disaster Reconstruction Process—A Review Leveraging Small Language Models*

---

## 6. Fora por regra já decidida (§1.2.1 b: difusão e GNN)

**Destino proposto:** fora, com a salvaguarda do título.  
**Por quê:** Você decidiu em 22/09 que técnica da área aplicada a difusão ou GNN fica fora.

### Grupo 34 — modelos de difusão (geração de imagem)

obras **488** · cajuzeiros **0** · surveys 186 · salvaguarda 5 · palavras: *diffusion, generation, diffusion models, image generation, image, text image, generative, text*

- exemplos: *Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding* (8877) · *Palette: Image-to-Image Diffusion Models* (2395) · *Diffusion Models in Vision: A Survey* (2339)
- salvas pela salvaguarda: *Lightweight diffusion models: a survey* · *Diffusion Model Quantization: A Review* · *A Survey on Recent Advancements in Lightweight Generative Adversarial Networks, their Applications and Datasets*

### Grupo 40 — grafos e GNN

obras **402** · cajuzeiros **0** · surveys 210 · salvaguarda 9 · palavras: *graph, graph neural, representation learning, representation, networks, graphs, embedding, survey graph*

- exemplos: *Graph Learning: A Survey* (524) · *A Survey on Heterogeneous Graph Embedding: Methods, Techniques, Applications and Sources* (475) · *A Comprehensive Survey on Community Detection With Deep Learning* (474)
- salvas pela salvaguarda: *A Survey of Community Detection in Complex Networks Using Nonnegative Matrix Factorization* · *Knowledge Distillation on Graphs: A Survey* · *Survey of Knowledge Distillation in Federated Edge Learning*

---

## 7. Outra área

**Destino proposto:** fora, com a salvaguarda do título.  
**Por quê:** Grupos cujo assunto é outro (educação, segurança, medicina, fuzzy, redes…). Muitos casam com o pool por **homônimo**: *lightweight cryptography*, **LoRa** (rádio) × **LoRA** (adaptação), *sparse FFT*, *resource-constrained project scheduling*, *embedded sensors*.

### Grupo 0 — IA na educação

obras **7288** · cajuzeiros **0** · surveys 1289 · salvaguarda 15 · palavras: *education, students, teaching, digital, teachers, learning, higher, student*

- exemplos: *Artificial Intelligence in Education: A Review* (2979) · *Embracing the future of Artificial Intelligence in the classroom: the relevance of AI literacy, prompt engineering, and critical thinking in modern education* (1044) · *New Era of Artificial Intelligence in Education: Towards a Sustainable Multifaceted Revolution* (960)
- salvas pela salvaguarda: *The Teacher-Student Relationship in the Use of Social Network Sites for Educational Purposes: A Systematic Review* · *Key considerations for implementing mobile learning in resource-constrained nations: a scoping review* · *Investigating the effects of SOLO taxonomy with reflective practice on university students’ meta-cognitive strategies, problem-solving, cognitive flexibility, spatial anxiety: an embedded mixed-method study on 3D game development*

### Grupo 1 — cibersegurança e IoT

obras **5629** · cajuzeiros **0** · surveys 2471 · salvaguarda 239 · palavras: *security, iot, intrusion, intrusion detection, detection, cybersecurity, authentication, cyber*

- exemplos: *Deep learning for cyber security intrusion detection: Approaches, datasets, and comparative study* (1185) · *Status report on the third round of the NIST post-quantum cryptography standardization process* (687) · *Deep learning approaches for anomaly-based intrusion detection systems: A survey, taxonomy, and open issues* (564)
- salvas pela salvaguarda: *Lightweight Cryptography Algorithms for Resource-Constrained IoT Devices: A Review, Comparison and Research Opportunities* · *Lightweight cryptography in IoT networks: A survey* · *Lightweight Cryptographic Protocols for IoT-Constrained Devices: A Survey*

### Grupo 3 — análise de sentimento

obras **3189** · cajuzeiros **0** · surveys 1273 · salvaguarda 23 · palavras: *sentiment, sentiment analysis, analysis, reviews, aspect, based sentiment, aspect based, classification*

- exemplos: *Relational Graph Attention Network for Aspect-based Sentiment Analysis* (713) · *ABCDM: An Attention-based Bidirectional CNN-RNN Deep Model for sentiment analysis* (691) · *Multimodal sentiment analysis: A systematic review of history, datasets, multimodal fusion methods, applications, challenges and future directions* (675)
- salvas pela salvaguarda: *Bert Distillation to Enhance the Performance of Machine Learning Models for Sentiment Analysis on Movie Review Data* · *Comprehensive Sentiment Analysis of Polish Book Reviews Using Large and Small Language Models* · *A Multi-Scale Feature Fusion Linear Attention Model for Movie Review Sentiment Analysis*

### Grupo 4 — LLMs em medicina/clínica

obras **3136** · cajuzeiros **0** · surveys 899 · salvaguarda 14 · palavras: *large language, language, large, language models, clinical, models, chatgpt, medical*

- exemplos: *SRplot: A free online platform for data visualization and graphing* (2263) · *ChatGPT in medicine: an overview of its applications, advantages, limitations, future prospects, and ethical considerations* (1060) · *Chatting about ChatGPT: How May AI and GPT Impact Academia and Libraries?* (1060)
- salvas pela salvaguarda: *The Rise of Small Language Models in Healthcare: A Comprehensive Survey* · *Is embedded indexing a worthwhile pursuit for indexers? A qualitative survey of current practices and thoughts for the future* · *JSON-ASR: A lightweight data storage and exchange format for automatic systematic reviews of TCM*

### Grupo 6 — imagem médica (câncer, segmentação)

obras **2905** · cajuzeiros **0** · surveys 1203 · salvaguarda 48 · palavras: *cancer, segmentation, deep learning, deep, breast, image, tumor, imaging*

- exemplos: *Transformers in Medical Imaging: A Survey* (1298) · *A survey of loss functions for semantic segmentation* (1098) · *A review of deep learning in medical imaging: Imaging traits, technology trends, case studies with progress highlights, and future promises* (1079)
- salvas pela salvaguarda: *Literature review: efficient deep neural networks techniques for medical image analysis* · *Knowledge distillation and teacher-student learning in medical imaging: Comprehensive overview, pivotal role, and future directions* · *Knowledge Distillation In Medical Data Mining: A Survey*

### Grupo 10 — saúde digital

obras **2275** · cajuzeiros **0** · surveys 867 · salvaguarda 13 · palavras: *health, digital health, digital, care, mobile, scoping, patient, scoping review*

- exemplos: *Reliability and Validity of Commercially Available Wearable Devices for Measuring Steps, Energy Expenditure, and Heart Rate: Systematic Review* (611) · *Wearable Health Devices in Health Care: Narrative Systematic Review* (600) · *Artificial Intelligence–Based Chatbots for Promoting Health Behavioral Changes: Systematic Review* (576)
- salvas pela salvaguarda: *Switching away: Exploring on-device media multitasking in web surveys* · *Sequential On-Device Multitasking within Online Surveys: A Data Quality and Response Behavior Perspective* · *Segmenting Clinicians’ Usage Patterns of a Digital Health Tool in Resource-Limited Settings: Clickstream Data Analysis and Survey Study*

### Grupo 8 — realidade virtual/aumentada

obras **2045** · cajuzeiros **0** · surveys 630 · salvaguarda 8 · palavras: *reality, augmented reality, virtual, augmented, virtual reality, impaired, visually, visually impaired*

- exemplos: *A research agenda for augmented and virtual reality in architecture, engineering and construction* (416) · *Personal LLM Agents: Insights and Survey about the Capability, Efficiency and Security* (380) · *Metaverse for Healthcare: A Survey on Potential Applications, Challenges and Future Directions* (313)
- salvas pela salvaguarda: *QButterfly: Lightweight Survey Extension for Online User Interaction Studies for Non-Tech-Savvy Researchers* · *A Review of Lightweight Object Detection Algorithms for Mobile Augmented Reality* · *A review of augmented reality in embedded systems for smart farming: innovations, applications and future directions*

### Grupo 9 — redes 5G/6G e comunicação sem fio

obras **1750** · cajuzeiros **0** · surveys 793 · salvaguarda 55 · palavras: *5g, 6g, wireless, communication, networks, communications, mimo, wireless networks*

- exemplos: *A Comprehensive Survey on Internet of Things (IoT) Toward 5G Wireless Systems* (1447) · *An Overview of Signal Processing Techniques for Joint Communication and Radar Sensing* (1232) · *Foundations of User-Centric Cell-Free Massive MIMO* (863)
- salvas pela salvaguarda: *Recent Advances in LoRa: A Comprehensive Survey* · *Embedded Sensors, Communication Technologies, Computing Platforms and Machine Learning for UAVs: A Review* · *A Survey on Resource Management in Joint Communication and Computing-Embedded SAGIN*

### Grupo 11 — LLM para engenharia de software

obras **1750** · cajuzeiros **0** · surveys 427 · salvaguarda 9 · palavras: *code, software, engineering, llm, automated, generation, software development, software engineering*

- exemplos: *Software Testing With Large Language Models: Survey, Landscape, and Vision* (745) · *A Survey on Automated Log Analysis for Reliability Engineering* (406) · *Fuzzing: A Survey for Roadmap* (364)
- salvas pela salvaguarda: *LLaMA-Reviewer: Advancing Code Review Automation with Large Language Models through Parameter-Efficient Fine-Tuning* · *Improving the Learning of Code Review Successive Tasks with Cross-Task Knowledge Distillation* · *A Systematic Literature Review of Parameter-Efficient Fine-Tuning for Large Code Models*

### Grupo 38 — IA em dispositivos médicos e regulação

obras **1663** · cajuzeiros **0** · surveys 492 · salvaguarda 8 · palavras: *medical devices, artificial intelligence, intelligence, artificial, regulatory, medical, healthcare, fda*

- exemplos: *Foundation models for generalist medical artificial intelligence* (2156) · *Algorithm fairness in artificial intelligence for medicine and healthcare* (601) · *Real-world data: a brief review of the methods, applications, challenges and opportunities* (449)
- salvas pela salvaguarda: *The Role of Lightweight AI Models in Supporting a Sustainable Transition to Renewable Energy: A Systematic Review* · *A Review on Artificial Intelligence and Point-of-Care Diagnostics to Combat Antimicrobial Resistance in Resource-Limited Healthcare Settings like Nigeria* · *Ethical Design of Data-Driven Decision Support Tools for Improving Cancer Care: Embedded Ethics Review of the 4D PICTURE Project*

### Grupo 7 — sistemas de recomendação

obras **1393** · cajuzeiros **0** · surveys 477 · salvaguarda 30 · palavras: *recommendation, recommender, recommender systems, filtering, recommendation systems, systems, collaborative, recommendations*

- exemplos: *A Survey on Knowledge Graph-Based Recommender Systems* (1039) · *Recommendation as Language Processing (RLP): A Unified Pretrain, Personalized Prompt & Predict Paradigm (P5)* (1008) · *A survey on large language models for recommendation* (990)
- salvas pela salvaguarda: *EDMF: Efficient Deep Matrix Factorization With Review Feature Learning for Industrial Recommender System* · *A systematic literature review of sparsity issues in recommender systems* · *Combining review-based collaborative filtering and matrix factorization: A solution to rating's sparsity problem*

### Grupo 12 — detecção de objetos e direção autônoma

obras **1320** · cajuzeiros **0** · surveys 556 · salvaguarda 45 · palavras: *object, object detection, detection, driving, traffic, driver, autonomous, autonomous driving*

- exemplos: *YOLOv11: An Overview of the Key Architectural Enhancements* (3615) · *A Comprehensive Review of YOLO Architectures in Computer Vision: From YOLOv1 to YOLOv8 and YOLO-NAS* (2945) · *A Survey of Modern Deep Learning based Object Detection Models* (939)
- salvas pela salvaguarda: *A comprehensive survey of deep learning-based lightweight object detection models for edge devices* · *Investigations of Object Detection in Images/Videos Using Various Deep Learning Techniques and Embedded Platforms—A Comprehensive Review* · *Real-Time Human Detection Using Deep Learning on Embedded Platforms: A Review*

### Grupo 19 — lógica fuzzy (inferência fuzzy)

obras **1171** · cajuzeiros **0** · surveys 80 · salvaguarda 7 · palavras: *fuzzy, fuzzy inference, inference, neuro fuzzy, neuro, anfis, adaptive, adaptive neuro*

- exemplos: *Differential Evolution: A review of more than two decades of research* (894) · *An Overview of Variants and Advancements of PSO Algorithm* (681) · *Major Advances in Particle Swarm Optimization: Theory, Analysis, and Application* (424)
- salvas pela salvaguarda: *A survey of hybrid metaheuristics for the resource-constrained project scheduling problem* · *Exploring potential for residential energy saving in New York using developed lightweight prototypical building models based on survey data in the past decades* · *The potential use of lightweight cellular concrete in pavement application: a review*

### Grupo 17 — ataques a LLM, agentes, prompt injection

obras **1132** · cajuzeiros **0** · surveys 229 · salvaguarda 6 · palavras: *attacks, prompt, llm, prompt injection, agents, injection, adversarial, large language*

- exemplos: *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (2002) · *How Johnny Can Persuade LLMs to Jailbreak Them: Rethinking Persuasion to Challenge AI Safety by Humanizing LLMs* (724) · *Should ChatGPT be Biased? Challenges and Risks of Bias in Large Language Models* (408)
- salvas pela salvaguarda: *Small Language Models for Agentic Systems: A Survey of Architectures, Capabilities, and Deployment Trade offs* · *Small Language Models for Edge AI: A Survey on Privacy-Preserving Toxicity and Grooming Detection* · *GTR-SQL: Graph Pruning, Tournament Selection, and Taxonomy Repair for Text-to-SQL*

### Grupo 22 — IoT em saúde

obras **1067** · cajuzeiros **0** · surveys 483 · salvaguarda 15 · palavras: *healthcare, iot, monitoring, things, internet, internet medical, medical things, smart healthcare*

- exemplos: *Artificial Intelligence (AI) and Internet of Medical Things (IoMT) Assisted Biomedical Systems for Intelligent Healthcare* (473) · *Remote patient monitoring using artificial intelligence: Current state, applications, and challenges* (405) · *A Survey on Wearable Technology: History, State-of-the-Art and Current Challenges* (400)
- salvas pela salvaguarda: *Data compression techniques in IoT-enabled wireless body sensor networks: A systematic literature review and research trends for QoS improvement* · *Embedded Machine Learning Using Microcontrollers in Wearable and Ambulatory Systems for Health and Care Applications: A Review* · *A review of on-device machine learning for IoT: An energy perspective*

### Grupo 18 — reabilitação, exoesqueleto, esporte

obras **1011** · cajuzeiros **0** · surveys 448 · salvaguarda 7 · palavras: *rehabilitation, limb, sports, exoskeleton, wearable, gait, upper, upper limb*

- exemplos: *Review of wearable thermoelectric energy harvesting: From body temperature to electronic systems* (524) · *The exoskeleton expansion: improving walking and running economy* (365) · *Wearable Sensor-Based Real-Time Gait Detection: A Systematic Review* (338)
- salvas pela salvaguarda: *A Review of Smart Technologies Embedded in Shoes* · *A Review of Pruning and Harvesting Manipulators* · *An overview of pruning and harvesting manipulators*

### Grupo 14 — processamento de imagem/vídeo (compressão de sinal, denoising)

obras **1006** · cajuzeiros **0** · surveys 479 · salvaguarda 57 · palavras: *image, compression, denoising, image denoising, video, super resolution, super, compressed*

- exemplos: *Deep learning models for digital image processing: a review* (621) · *Methods for image denoising using convolutional neural network: a review* (356) · *Multi-focus image fusion: A Survey of the state of the art* (303)
- salvas pela salvaguarda: *Low-Rank and Sparse Representation for Hyperspectral Image Processing: A review* · *Robust and sparsity-aware adaptive filters: A Review* · *A structured review of sparse fast Fourier transform algorithms*

### Grupo 13 — blockchain

obras **967** · cajuzeiros **0** · surveys 423 · salvaguarda 20 · palavras: *blockchain, iot, security, internet, technology, things, secure, internet things*

- exemplos: *Non-Fungible Token (NFT): Overview, Evaluation, Opportunities and Challenges* (723) · *Federated Learning Meets Blockchain in Edge Computing: Opportunities and Challenges* (613) · *Survey on IoT security: Challenges and solution using machine learning, artificial intelligence and blockchain technology* (399)
- salvas pela salvaguarda: *A survey on consensus methods in blockchain for resource-constrained IoT networks* · *Public Blockchains for Resource-Constrained IoT Devices—A State-of-the-Art Survey* · *A Survey on Secure and Private Federated Learning Using Blockchain: Theory and Application in Resource-Constrained Computing*

### Grupo 26 — modelos preditivos clínicos

obras **915** · cajuzeiros **0** · surveys 437 · salvaguarda 1 · palavras: *machine learning, machine, prediction, predicting, risk, systematic review, systematic, meta analysis*

- exemplos: *Prediction models for diagnosis and prognosis of covid-19: systematic review and critical appraisal* (2502) · *Comparison of machine learning and logistic regression models in predicting acute kidney injury: A systematic review and meta-analysis* (273) · *Machine learning approaches in COVID-19 diagnosis, mortality, and severity risk prediction: A review* (178)
- salvas pela salvaguarda: *Clinical Implementation of Predictive Models Embedded within Electronic Health Record Systems: A Systematic Review*

### Grupo 31 — aprendizado por reforço

obras **898** · cajuzeiros **0** · surveys 324 · salvaguarda 15 · palavras: *reinforcement learning, reinforcement, deep reinforcement, embodied, learning, action, manipulation, robot*

- exemplos: *Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey* (1114) · *Exploration in Deep Reinforcement Learning: A Survey* (632) · *Deep Reinforcement Learning for Robotics: A Survey of Real-World Successes* (455)
- salvas pela salvaguarda: *A Survey of On-Policy Distillation for Large Language Models* · *深度强化学习中稀疏奖励问题研究综述 (Survey on Sparse Reward in Deep Reinforcement Learning)* · *Integration of Mixture of Experts and Multimodal Generative AI in Internet of Vehicles: A Survey*

### Grupo 25 — fatoração de matrizes, estatística, incerteza

obras **894** · cajuzeiros **0** · surveys 269 · salvaguarda 49 · palavras: *matrix, factorization, tensor, matrix factorization, bayesian, clustering, data, dimensionality*

- exemplos: *A survey of uncertainty in deep neural networks* (2008) · *Interpretable Machine Learning: Fundamental Principles and 10 Grand Challenges* (1047) · *Modern Koopman Theory for Dynamical Systems* (783)
- salvas pela salvaguarda: *Sparse Polynomial Chaos Expansions: Literature Survey and Benchmark* · *A Survey on Sparse Learning Models for Feature Selection* · *Hyperspectral Unmixing Based on Nonnegative Matrix Factorization: A Comprehensive Review*

### Grupo 15 — fake news, discurso de ódio

obras **869** · cajuzeiros **0** · surveys 425 · salvaguarda 14 · palavras: *fake, detection, news, review detection, hate, hate speech, detection using, reviews*

- exemplos: *HateCheck: Functional Tests for Hate Speech Detection Models* (398) · *A Comprehensive Review on Fake News Detection With Deep Learning* (225) · *ChatGPT or Human? Detect and Explain. Explaining Decisions of Machine Learning Model for Detecting Short ChatGPT-generated Text* (202)
- salvas pela salvaguarda: *An Ensemble Model for Fake Online Review Detection Based on Data Resampling, Feature Pruning, and Parameter Optimization* · *Detecting Evasive Answers in Financial Q&A: A Psychological Discourse Taxonomy and Lightweight Baselines* · *Interpretable Review Spammer Group Detection Model Based on Knowledge Distillation and Counterfactual Generation*

### Grupo 32 — manutenção preditiva e falhas

obras **860** · cajuzeiros **0** · surveys 376 · salvaguarda 26 · palavras: *predictive maintenance, maintenance, fault, predictive, fault diagnosis, diagnosis, machine, prognostics*

- exemplos: *A Survey on Anomaly Detection for Technical Systems using LSTM Networks* (421) · *Machine Learning Applied to Electrified Vehicle Battery State of Charge and State of Health Estimation: State-of-the-Art* (402) · *Machine learning paradigm for structural health monitoring* (333)
- salvas pela salvaguarda: *A comprehensive survey of sparse regularization: Fundamental, state-of-the-art methodologies and applications on fault diagnosis* · *Machine learning-assisted design of lightweight refractory high-entropy alloys: a comprehensive review* · *Intelligent methods for optimization design of lightweight fiber-reinforced composite structures: A review and the-state-of-the-art*

### Grupo 63 — indústria 4.0/5.0 e gêmeos digitais

obras **831** · cajuzeiros **0** · surveys 241 · salvaguarda 38 · palavras: *manufacturing, industry, industrial, industrial internet, digital twin, twin, control, digital*

- exemplos: *Industry 5.0: A survey on enabling technologies and potential applications* (1469) · *Cyber-physical systems architectures for industrial internet of things applications in Industry 4.0: A literature review* (383) · *Artificial Intelligence Applications for Industry 4.0: A Literature-Based Study* (372)
- salvas pela salvaguarda: *A Survey on LoRa for Smart Agriculture: Current Trends and Future Perspectives* · *Embedded Sensors for Structural Health Monitoring: Methodologies and Applications Review* · *Fiber Optic Sensors Embedded in Textile-Reinforced Concrete for Smart Structural Health Monitoring: A Review*

### Grupo 27 — ECG e cardiologia

obras **831** · cajuzeiros **0** · surveys 354 · salvaguarda 5 · palavras: *ecg, cardiovascular, fibrillation, heart, atrial, atrial fibrillation, electrocardiogram, cardiac*

- exemplos: *A review on deep learning methods for ECG arrhythmia classification* (466) · *Review of noise removal techniques in ECG signals* (320) · *Deep learning for ECG Arrhythmia detection and classification: an overview of progress for period 2017–2023* (300)
- salvas pela salvaguarda: *A systematic review of ECG arrhythmia classification: embedded feasibility, adherence to standards, and fair evaluation* · *Survey, Analysis and Comparison of Radar Technologies for Embedded Vital Sign Monitoring* · *Women’s Cardiovascular Disease and Stroke Risk Stratification Using a Precision and Personalized Framework Embedded with an Explainable Artificial Intelligence Paradigm: A Narrative Review*

### Grupo 30 — fuzzy em otimização de engenharia

obras **779** · cajuzeiros **0** · surveys 74 · salvaguarda 12 · palavras: *fuzzy, fuzzy inference, inference, neuro fuzzy, neuro, adaptive neuro, adaptive, using adaptive*

- exemplos: *Consensus in multi-agent systems: a review* (466) · *Neuro-inspired electronic skin for robots* (287) · *Applications of Nonlinearity in Passive Vibration Control: A Review* (245)
- salvas pela salvaguarda: *A review of Pareto pruning methods for multi-objective optimization* · *A novel low-power high speed accurate and precise DAQ with embedded artificial intelligence for long term biodiversity survey* · *PRISMA-Guided Systematic Review on the Adoption of Artificial Intelligence and Embedded Systems for Smart Irrigation*

### Grupo 20 — controle fuzzy de motores

obras **768** · cajuzeiros **0** · surveys 51 · salvaguarda 4 · palavras: *control, fuzzy, controller, adaptive, anfis, motor, neuro fuzzy, neuro*

- exemplos: *Networked control systems: a survey of trends and techniques* (870) · *Dynamic Event-triggered Control and Estimation: A Survey* (269) · *Model predictive control design for linear parameter varying systems: A survey* (184)
- salvas pela salvaguarda: *Data-based modeling and control of nonlinear process systems using sparse identification: An overview of recent results* · *Advancements in hybrid controllers and new era models of distillation column: A review* · *Review on Embedded Methods in Parameter Estimation and Auto-tuning of Permanent Magnet Synchronous Servo Machine Driven Industrial Systems*

### Grupo 35 — revisão por pares e produção científica

obras **670** · cajuzeiros **0** · surveys 211 · salvaguarda 5 · palavras: *scientific, peer, peer review, reviewer, paper, research, patent, automated*

- exemplos: *The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery* (1151) · *Benchmarking and survey of explanation methods for black box models* (364) · *Towards Human-Centered Explainable AI: A Survey of User Studies for Model Explanations* (277)
- salvas pela salvaguarda: *TreeReview: A Dynamic Tree of Questions Framework for Deep and Efficient LLM-based Scientific Peer Review* · *Densifying Knowledge Hypergraphs with LLM-based review distillation for conversational consumer decision support* · *EGTR-Review: Efficient Evidence-Grounded Scientific Peer Review Generation via Multi-Agent Teacher Distillation*

### Grupo 37 — fuzzy em diagnóstico

obras **642** · cajuzeiros **0** · surveys 67 · salvaguarda 1 · palavras: *fuzzy, fuzzy inference, neuro fuzzy, neuro, inference, diagnosis, anfis, adaptive neuro*

- exemplos: *COVID-19 Outbreak Prediction with Machine Learning* (441) · *Optimization Method for Forecasting Confirmed Cases of COVID-19 in China* (369) · *Evaluation of artificial intelligence techniques in disease diagnosis and prediction* (364)
- salvas pela salvaguarda: *Simple and Compound Leaf Taxonomy Embedded Machine Learning Approach for Ayurveda Plants Recognition*

### Grupo 21 — reconhecimento de fala

obras **608** · cajuzeiros **0** · surveys 253 · salvaguarda 12 · palavras: *speech, speech recognition, recognition, automatic speech, automatic, audio, speaker, voice*

- exemplos: *Self-Supervised Speech Representation Learning: A Review* (529) · *A Survey on Neural Speech Synthesis* (499) · *Recent Advances in End-to-End Automatic Speech Recognition* (472)
- salvas pela salvaguarda: *A Review of On-Device Fully Neural End-to-End Automatic Speech Recognition Algorithms* · *Sparsity-Based Audio Declipping Methods: Selected Overview, New Algorithms, and Large-Scale Evaluation* · *Voice Activation Systems for Embedded Devices: Systematic Literature Review*

### Grupo 24 — análise de sentimento (2)

obras **586** · cajuzeiros **0** · surveys 283 · salvaguarda 8 · palavras: *sentiment, sentiment analysis, aspect, analysis, reviews, based sentiment, aspect based, lstm*

- exemplos: *Sentiment Analysis* (993) · *Transformer models for text-based emotion detection: a review of BERT-based approaches* (630) · *A Review on Word Embedding Techniques for Text Classification* (216)
- salvas pela salvaguarda: *A Novel Multi-Layer Sparse Regularizer based GRU Model for Consumer Reviews Summarization* · *Domain Generalization via Switch Knowledge Distillation for Robust Review Representation* · *An innovative word embedded and optimization based hybrid artificial intelligence approach for aspect-based sentiment analysis of app and cellphone reviews*

### Grupo 47 — diagnóstico point-of-care e biossensores

obras **538** · cajuzeiros **0** · surveys 197 · salvaguarda 5 · palavras: *point care, point, diagnostics, biosensors, chip, sleep, smartphone, care*

- exemplos: *Electrochemical glucose sensors in diabetes management: an updated review (2010-2020).* (557) · *Biosensors applications in medical field: A brief review* (456) · *Future smart battery and management: Advanced sensing from external to embedded multi-dimensional measurement* (332)
- salvas pela salvaguarda: *A mini-review of embedded 3D printing: supporting media and strategies.* · *Lightweight and Low-Cost Deployable Origami Antennas—A Review* · *RETRACTED: Embedded Sensors with 3D Printing Technology: Review*

### Grupo 29 — interface cérebro-computador

obras **535** · cajuzeiros **0** · surveys 244 · salvaguarda 4 · palavras: *brain computer, brain, computer, computer interfaces, computer interface, interfaces, interface, eeg*

- exemplos: *Current Status, Challenges, and Possible Solutions of EEG-Based Brain-Computer Interface: A Comprehensive Review* (437) · *Transfer Learning for EEG-Based Brain–Computer Interfaces: A Review of Progress Made Since 2016* (422) · *EEG-Based Emotion Recognition: A State-of-the-Art Review of Current Trends and Opportunities* (334)
- salvas pela salvaguarda: *Electromyography Signals in Embedded Systems: A Review of Processing and Classification Techniques* · *Lightweight deep learning models for EEG decoding: a review* · *Overview of the EEG-Based Classification of Motor Imagery Activities Using Machine Learning Methods and Inference Acceleration with FPGA-Based Cards*

### Grupo 55 — redes definidas por software (SDN)

obras **498** · cajuzeiros **0** · surveys 199 · salvaguarda 3 · palavras: *defined, software defined, networking, defined networking, software, sdn, defined networks, network*

- exemplos: *“A Survey of Software Defined Networking”* (678) · *The rise of traffic classification in IoT networks: A survey* (249) · *A Survey on Data Plane Programming with P4: Fundamentals, Advances, and Applied Research* (218)
- salvas pela salvaguarda: *Survey on LoRa Technology: Solution for Internet of Things* · *Overview of Embedded Rust Operating Systems and Frameworks* · *A Literature Survey on Various Streaming Protocol and Compression Techniques in Multimedia Transmission with Internet of Things*

### Grupo 33 — reconhecimento de atividade humana

obras **483** · cajuzeiros **0** · surveys 246 · salvaguarda 8 · palavras: *human activity, activity recognition, human, activity, recognition, action, action recognition, pose*

- exemplos: *Deep Learning for Sensor-based Human Activity Recognition* (894) · *Sensor-based and vision-based human activity recognition: A comprehensive survey* (665) · *Deep Learning in Human Activity Recognition with Wearable Sensors: A Review on Advances* (577)
- salvas pela salvaguarda: *Review on Human Action Recognition in Smart Living: Sensing Technology, Multimodality, Real-Time Processing, Interoperability, and Resource-Constrained Processing* · *A systematic survey on human pose estimation: upstream and downstream tasks, approaches, lightweight models, and prospects* · *AI-Enabled FET Sensors: Data Modalities, Learning Tasks, and Edge Deployment—A Review*

### Grupo 23 — retinopatia diabética

obras **470** · cajuzeiros **0** · surveys 184 · salvaguarda 5 · palavras: *retinopathy, diabetic retinopathy, diabetic, retinal, artificial intelligence, artificial, intelligence, images*

- exemplos: *Digital Eye Strain- A Comprehensive Review* (303) · *Deep Learning Techniques For Diabetic Retinopathy Classification: A Survey* (197) · *Refractive surgery beyond 2020* (171)
- salvas pela salvaguarda: *Computationally efficient deep learning models for diabetic retinopathy detection: a systematic literature review* · *Advancing Sparse Vegetation Monitoring in the Arctic and Antarctic: A Review of Satellite and UAV Remote Sensing, Machine Learning, and Sensor Fusion* · *Lightweight Deep Learning Models for Retinal Disease Classification: A Survey*

### Grupo 64 — casa inteligente e automação

obras **459** · cajuzeiros **0** · surveys 183 · salvaguarda 27 · palavras: *home, home automation, automation, smart, smart home, automation using, raspberry, raspberry pi*

- exemplos: *A review on microstrip patch antenna and feeding techniques* (96) · *Comparative Performance Study of ESP-NOW, Wi-Fi, Bluetooth Protocols based on Range, Transmission Speed, Latency, Energy Usage and Barrier Resistance* (76) · *HeadFi: bringing intelligence to all headphones* (70)
- salvas pela salvaguarda: *An Overview of AI-Enabled Remote Smart- Home Monitoring System Using LoRa* · *A Review of Fully Integrated and Embedded Power Converters for IoT* · *Energy saving on IoT using LoRa: a systematic literature review*

### Grupo 39 — localização indoor e Wi-Fi

obras **449** · cajuzeiros **0** · surveys 166 · salvaguarda 14 · palavras: *indoor, localization, positioning, wi, wi fi, fi, fingerprinting, sensing*

- exemplos: *Cross-Domain WiFi Sensing with Channel State Information: A Survey* (804) · *A Review on Challenges of Autonomous Mobile Robot and Sensor Fusion Methods* (489) · *A Review of Radio Frequency Fingerprinting Techniques* (353)
- salvas pela salvaguarda: *A Review of Sparse Sensor Arrays for Two-Dimensional Direction-of-Arrival Estimation* · *A Survey of Sparse Mobile Crowdsensing: Developments and Opportunities* · *GNSS-Free Outdoor Localization Techniques for Resource-Constrained IoT Architectures: A Literature Review*

### Grupo 50 — educação médica

obras **449** · cajuzeiros **0** · surveys 121 · salvaguarda 0 · palavras: *education, medical education, nursing, medical, artificial, artificial intelligence, intelligence, students*

- exemplos: *Virtual reality simulations in nurse education: A systematic mapping review.* (320) · *ChatGPT prompts for generating multiple-choice questions in medical education and evidence on their validity: a literature review.* (139) · *Educational Strategies for Clinical Supervision of Artificial Intelligence Use.* (137)

### Grupo 44 — Alzheimer e Parkinson

obras **429** · cajuzeiros **0** · surveys 207 · salvaguarda 2 · palavras: *alzheimer, alzheimer disease, disease, parkinson, parkinson disease, diagnosis, early, disease using*

- exemplos: *Current advances in digital cognitive assessment for preclinical Alzheimer's disease* (222) · *Artificial Intelligence and Acute Stroke Imaging* (216) · *Deep learning for Alzheimer's disease diagnosis: A survey* (194)
- salvas pela salvaguarda: *Comprehensive Review of Deep Learning Algorithms for Embedded Healthcare Applications* · *Lightweight Deep Learning-Based Alzheimer’s Detection Using MobileNetV2 and Grad-CAM: A Comprehensive Review*

### Grupo 45 — eletrônica de potência e fuzzy

obras **427** · cajuzeiros **0** · surveys 130 · salvaguarda 3 · palavras: *power, anfis, fuzzy, control, voltage, fault, dc, controller*

- exemplos: *The most used MPPT algorithms: Review and the suitable low-cost embedded board for each algorithm* (350) · *An Overview of Soft Open Points in Electricity Distribution Networks* (231) · *Voltage Source Multilevel Inverters With Reduced Device Count: Topological Review and Novel Comparative Factors* (218)
- salvas pela salvaguarda: *The most used MPPT algorithms: Review and the suitable low-cost embedded board for each algorithm* · *A Comprehensive Review of Artificial Neural Network Techniques Used for Smart Meter-Embedded forecasting System* · *Physically consistent ultra-lightweight AI for real-time harmonics and stability in converter-dominated grids: Systematic review, evidence synthesis, and deployment gaps*

### Grupo 28 — marca d'água e ocultação de dados

obras **418** · cajuzeiros **0** · surveys 228 · salvaguarda 10 · palavras: *watermarking, image, hiding, data hiding, techniques, reversible, video, digital image*

- exemplos: *Watermarking techniques for medical data authentication: a survey* (147) · *Data Hiding With Deep Learning: A Survey Unifying Digital Watermarking and Steganography* (128) · *A Review on Text Steganography Techniques* (114)
- salvas pela salvaguarda: *A comparative review and analysis of medical image encryption and compression techniques* · *Developed Lightweight Cryptographic Algorithms for The Application of Image Encryption: A Review* · *Review of image encryption and compression techniques*

### Grupo 59 — séries temporais e previsão

obras **392** · cajuzeiros **0** · surveys 208 · salvaguarda 15 · palavras: *series, time series, forecasting, series forecasting, time, stock, recurrent, series data*

- exemplos: *A review on the attention mechanism of deep learning* (3150) · *A review on the long short-term memory model* (1800) · *Transformers in Time Series: A Survey* (1675)
- salvas pela salvaguarda: *Pruning Deep Neural Networks for Green Energy-Efficient Models: A Survey* · *A Comprehensive Survey on Model Quantization for Deep Neural Networks* · *Machine learning approaches for LoRa networks:a survey*

### Grupo 51 — nuvem de pontos 3D e profundidade

obras **371** · cajuzeiros **0** · surveys 139 · salvaguarda 10 · palavras: *3d, point, point cloud, depth, reconstruction, depth estimation, point clouds, cloud*

- exemplos: *Review: deep learning on 3D point clouds* (323) · *Monocular depth estimation based on deep learning: An overview* (301) · *Fiducial Markers for Pose Estimation* (233)
- salvas pela salvaguarda: *Deep Depth Completion From Extremely Sparse Data: A Survey* · *A Survey of Label-Efficient Deep Learning for 3D Point Clouds* · *A Survey on Data Compression Techniques for Automotive LiDAR Point Clouds*

### Grupo 41 — sumarização de texto

obras **344** · cajuzeiros **0** · surveys 131 · salvaguarda 0 · palavras: *summarization, text, abstractive, summarization using, extractive, automatic, document, using*

- exemplos: *Topic Modeling Using Latent Dirichlet allocation* (325) · *A comparison of ChatGPT-generated articles with human-written articles* (151) · *The Factual Inconsistency Problem in Abstractive Text Summarization: A Survey* (132)

### Grupo 58 — redes de sensores sem fio

obras **341** · cajuzeiros **0** · surveys 110 · salvaguarda 5 · palavras: *wireless sensor, routing, wireless, sensor networks, sensor, fuzzy, clustering, networks*

- exemplos: *Distributed Event-Triggered Estimation Over Sensor Networks: A Survey* (435) · *Fuzzy based enhanced cluster head selection (FBECS) for WSN* (145) · *Performance Enhancement in Wireless Body Area Networks with Secure Communication* (96)
- salvas pela salvaguarda: *Resource-efficient and secure distributed state estimation over wireless sensor networks: a survey* · *Revolutionary of secure lightweight energy efficient routing protocol for internet of medical things: a review* · *Peer Review #3 of "A novel air quality monitoring and improvement system based on wireless sensor and actuator networks using LoRa communication (v0.2)"*

### Grupo 42 — deepfake

obras **337** · cajuzeiros **0** · surveys 164 · salvaguarda 1 · palavras: *deepfake, detection, video, face, deep, techniques, detection using, image*

- exemplos: *Backdoor Learning: A Survey* (887) · *A survey on adversarial attacks and defences* (473) · *ASVspoof 2021: Towards Spoofed and Deepfake Speech Detection in the Wild* (432)
- salvas pela salvaguarda: *Lightweight Hybrid Deep Learning Models for Real-Time Deepfake Video Detection: A Comprehensive Survey*

### Grupo 54 — descoberta de fármacos

obras **316** · cajuzeiros **0** · surveys 68 · salvaguarda 1 · palavras: *drug, drug discovery, discovery, protein, target, prediction, computational, graph*

- exemplos: *Computational Approaches in Preclinical Studies on Drug Discovery and Development* (373) · *Attention is all you need: utilizing attention in AI-enabled drug discovery* (296) · *Computers and viral diseases. Preliminary bioinformatics studies on the design of a synthetic vaccine and a preventative peptidomimetic antagonist against the SARS-CoV-2 (2019-nCoV, COVID-19) coronavirus* (195)
- salvas pela salvaguarda: *Matrix factorization for biomedical link prediction and scRNA-seq data imputation: an empirical survey*

### Grupo 48 — odontologia

obras **313** · cajuzeiros **0** · surveys 170 · salvaguarda 1 · palavras: *dental, dentistry, artificial intelligence, artificial, intelligence, narrative, review artificial, narrative review*

- exemplos: *Accuracy and practicality of intraoral scanner in dentistry: A literature review.* (276) · *Artificial intelligence in dentistry—A review* (208) · *Deep learning for cephalometric landmark detection: systematic review and meta-analysis* (179)
- salvas pela salvaguarda: *A review of the Application of Additive Manufacturing in Endodontic access opening using SLM process*

### Grupo 56 — epilepsia e EEG

obras **299** · cajuzeiros **0** · surveys 117 · salvaguarda 4 · palavras: *seizure, eeg, epileptic, epileptic seizure, epilepsy, detection, eeg based, signals*

- exemplos: *EEG-based emotion recognition: Review of commercial EEG devices and machine learning techniques* (193) · *Development of Expert-Level Automated Detection of Epileptiform Discharges During Electroencephalogram Interpretation.* (174) · *Machine learning and wearable devices of the future* (144)
- salvas pela salvaguarda: *From Seizure Detection to Smart and Fully Embedded Seizure Prediction Engine: A Review* · *A Survey of Methods and Architectures for Parkinson's Disease Recognition from EEG Using Attention-Based Sparse Graph Convolutional Neural Networks* · *A Comprehensive Review of Parkinson's Disease Recognition from EEG Using Attention-Based Sparse Graph Convolutional Neural Networks*

### Grupo 60 — reconhecimento de emoção

obras **265** · cajuzeiros **0** · surveys 105 · salvaguarda 1 · palavras: *emotion, emotion recognition, recognition, speech, multimodal emotion, recognition using, multimodal, audio*

- exemplos: *Speech emotion recognition: Emotional models, databases, features, preprocessing methods, supporting modalities, and classifiers* (633) · *Multimodal Alignment and Fusion: A Survey* (202) · *A Review on Speech Emotion Recognition Using Deep Learning and Attention Mechanism* (200)
- salvas pela salvaguarda: *A Comprehensive Review of Lightweight Audio-Visual Emotion Recognition: Architectures, Fusion Techniques, and the Efficiency Trade-off*

### Grupo 65 — fuzzy aplicado (qualidade, avaliação)

obras **247** · cajuzeiros **0** · surveys 9 · salvaguarda 1 · palavras: *fuzzy, fuzzy inference, mamdani, fuzzy logic, student, logic, inference, performance*

- exemplos: *AI different approaches and ANFIS data mining: A novel approach to predicting early employment readiness in middle eastern nations* (51) · *Pembelajaran Text Preprocessing berbasis Simulator Untuk Mata Kuliah Information Retrieval* (41) · *Evaluating critical success factors in the permanence in Higher Education using multi-criteria decision-making* (35)
- salvas pela salvaguarda: *Analyzing Healthcare and Wellness Products’ Quality Embedded in Online Customer Reviews: Assessment with a Hybrid Fuzzy LMAW and Fermatean Fuzzy WASPAS Method*

### Grupo 57 — reconhecimento facial

obras **210** · cajuzeiros **0** · surveys 84 · salvaguarda 7 · palavras: *face, face recognition, recognition, face detection, mask, facial, masked, deep*

- exemplos: *LightFace: A Hybrid Deep Face Recognition Framework* (413) · *Appearance-Based Gaze Estimation With Deep Learning: A Review and Benchmark* (271) · *Design of Deep Learning Algorithm for IoT Application by Image based Recognition* (106)
- salvas pela salvaguarda: *Sparse representation for face recognition: A review paper* · *Lightweight Deep Learning Models for Face Mask Detection in Real-Time Edge Environments: A Review and Future Research Directions* · *A Comprehensive Survey of Lightweight Neural Networks for Face Recognition*

### Grupo 62 — legenda de imagem (captioning)

obras **188** · cajuzeiros **0** · surveys 109 · salvaguarda 0 · palavras: *captioning, image, caption, review image, deep learning, deep, video, description*

- exemplos: *The multi-modal fusion in visual question answering: a review of attention mechanisms* (295) · *A Survey of Vision-Language Pre-Trained Models* (285) · *Referring Expression Comprehension: A Survey of Methods and Datasets* (141)

### Grupo 53 — língua de sinais

obras **173** · cajuzeiros **0** · surveys 78 · salvaguarda 1 · palavras: *sign language, sign, language recognition, recognition, language, gesture, translation, gesture recognition*

- exemplos: *Weakly Supervised Learning with Multi-Stream CNN-LSTM-HMMs to Discover Sequential Parallelism in Sign Language Videos* (379) · *Including Signed Languages in Natural Language Processing* (157) · *Gestures Controlled Home Automation using Deep Learning: A Review* (130)
- salvas pela salvaguarda: *A Review of the Embedded Deployment of Sign Language Detection Models: Metrics, Tradeoffs and Perspectives*

### Grupo 61 — reconhecimento de escrita (OCR)

obras **153** · cajuzeiros **0** · surveys 76 · salvaguarda 1 · palavras: *handwritten, recognition, character recognition, character, ocr, text recognition, handwriting, optical*

- exemplos: *Neural Text Segmentation and its Application to Sentiment Analysis* (48) · *Towards efficient unconstrained handwriting recognition using Dilated Temporal Convolution Network* (45) · *A survey on handwritten mathematical expression recognition: The rise of encoder-decoder and GNN models* (34)
- salvas pela salvaguarda: *A Comparative Review of Lightweight Machine Learning Approaches for Handwriting-Based Dyslexia Detection*

---

## Decisão sua

Para cada categoria (ou grupo, se quiser mudar algum): **concordo** ou **muda para ___**. Depois disso reescrevo a coluna `camada_B` e meço a perda no teste de novo.

---

## DECIDIDO pelo Pedro (23/09): "pode deixar assim" — proposta aceita inteira

Aplicada: colunas `camada_B` e `para_camada_C` reescritas no `2026-09-22-floresta-obras.csv`.

| destino | obras |
|---|---|
| fora (outra área) | 59.014 |
| fora (§1.2.1 b — difusão, GNN) | 876 |
| núcleo | 5.682 |
| misto | 5.752 |
| a testar (`uso?`) | 1.194 |
| dentro (§1.2.1 d) | 767 |
| arquiteturas (§1.1) | 554 |
| salva pela salvaguarda do título | 952 |
| **para a camada C** | **14.901** (12.446 com abstract; 5.340 com palavra de tipo no título) |

**Recuperação do gabarito (camadas A + B juntas):** ajuste 28/28 · **teste 28/29 (97%)** — a única
perda continua sendo *A Survey on Green Deep Learning*, na camada A.
