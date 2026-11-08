# Camada B — mapa de tópicos: relatório (23/09/2026)

**Status: tópicos calculados, NENHUM grupo marcado como lixo ainda — decisão do Pedro.** Nível 3:
agrupamento automático por semelhança de título + abstract; ninguém leu as obras. A coluna
`camada_B_topico` foi acrescentada ao `2026-09-22-floresta-obras.csv` (só nas 74.791 mantidas pela A).

## 1. O que foi feito

Cada uma das 74.791 obras virou um vetor pelo **SPECTER2** (modelo treinado em papers científicos,
aprendendo que papers que se citam tratam do mesmo assunto). O **BERTopic** agrupou os vetores
parecidos (UMAP para reduzir, HDBSCAN para agrupar, grupo mínimo de 100 obras, semente 42 —
parâmetros declarados antes de rodar) e descreveu cada grupo pelas palavras mais típicas dos títulos.
Resultado: **66 grupos + o grupo -1**, que é o das obras que o algoritmo não conseguiu pôr em grupo
nenhum ("ruído" no vocabulário do HDBSCAN — não quer dizer lixo, quer dizer "sem vizinhança clara").

## 2. Onde estão os cajuzeiros conhecidos

Das 28 obras da metade de ajuste do gabarito: **21 no grupo 2** (serving, inference, efficient, llm,
edge, memory, hardware), **4 no grupo 5** (language models), **2 no grupo 36** (knowledge
distillation) e **1 no grupo -1**. Nenhuma foi perdida pela camada A. É um sinal forte de que o
agrupamento separa a área: três grupos concentram 27 das 28.

## 3. O que o mapa mostra sobre o lixo (exemplos reais)

- **Homônimos, como você previu com *quantum*:** o grupo 1 (segurança de IoT) tem *"Lightweight
  Cryptography… for Resource-Constrained IoT Devices"* — "lightweight" de criptografia, não de modelo;
  o grupo 9 (redes 5G/6G) tem vários surveys de **LoRa** (rádio) casando com **LoRA** (adaptação);
  o grupo 14 tem *sparse FFT* e *compressão de vídeo fractal* casando com "sparsity" e "compression".
- **Aplicações específicas** (regra §1.2.1 c, "espera divisão"): o grupo 6 (imagem médica) tem
  *"Literature review: efficient deep neural networks techniques for medical image analysis"* — é
  eficiência, mas numa aplicação.

## 4. Proposta de classificação dos grupos (PROPOSTA DO CLAUDE — você decide cada linha)

Quatro categorias:
- **núcleo** — onde estão os cajuzeiros; seguem.
- **regra** — uma regra do método que você já decidiu diz o destino (aplicação específica espera
  divisão; difusão e GNN fora; infraestrutura dentro; MLOps é `uso?`; ViT depende da P2).
- **verificar** — grupo grande ou misto que pode esconder cajuzeiro; não dá para descartar em bloco.
- **proposta: fora** — outra área ou homônimo, pelo que as palavras e os exemplos mostram.

| grupo | obras | cajuzeiros (ajuste) | surveys com termo núcleo no título | palavras-chave | proposta | exemplos (mais citados) |
|---|---|---|---|---|---|---|
| -1 | 25158 | 1 | 523 | review, intelligence, artificial, based, data, artificial intelligence | verificar | Image Segmentation Using Deep Learning: A Survey · Don’t Stop Pretraining: Adapt Language Models to Domains and Tasks · Foundation models for generalist medical artificial intelligence |
| 0 | 6469 | 0 | 13 | education, students, teaching, digital, teachers, learning, higher, st | proposta: fora | Artificial Intelligence in Education: A Review · Embracing the future of Artificial Intelligence in the classroom: the relevance  · New Era of Artificial Intelligence in Education: Towards a Sustainable Multiface |
| 1 | 5140 | 0 | 215 | security, iot, intrusion, intrusion detection, detection, cybersecurit | proposta: fora | Deep learning for cyber security intrusion detection: Approaches, datasets, and  · Status report on the third round of the NIST post-quantum cryptography standardi · Deep learning approaches for anomaly-based intrusion detection systems: A survey |
| 2 | 4315 | 21 | 267 | serving, inference, efficient, llm, edge, memory, hardware, neural | núcleo | Efficient Memory Management for Large Language Model Serving with PagedAttention · Memory devices and applications for in-memory computing · A Survey of Quantization Methods for Efficient Neural Network Inference |
| 3 | 3080 | 0 | 23 | sentiment, sentiment analysis, analysis, reviews, aspect, based sentim | proposta: fora | Relational Graph Attention Network for Aspect-based Sentiment Analysis · ABCDM: An Attention-based Bidirectional CNN-RNN Deep Model for sentiment analysi · Multimodal sentiment analysis: A systematic review of history, datasets, multimo |
| 4 | 2716 | 0 | 13 | large language, language, large, language models, clinical, models, ch | verificar | SRplot: A free online platform for data visualization and graphing · ChatGPT in medicine: an overview of its applications, advantages, limitations, f · Chatting about ChatGPT: How May AI and GPT Impact Academia and Libraries? |
| 5 | 2421 | 4 | 43 | language, language models, models, large language, large, translation, | verificar | Survey of Hallucination in Natural Language Generation · Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natu · A Survey of Large Language Models |
| 6 | 2238 | 0 | 35 | cancer, segmentation, deep learning, deep, breast, image, tumor, imagi | regra: §1.2.1 c (aplicação — espera divisão) | Transformers in Medical Imaging: A Survey · A survey of loss functions for semantic segmentation · A review of deep learning in medical imaging: Imaging traits, technology trends, |
| 7 | 1320 | 0 | 29 | recommendation, recommender, recommender systems, filtering, recommend | proposta: fora | A Survey on Knowledge Graph-Based Recommender Systems · Recommendation as Language Processing (RLP): A Unified Pretrain, Personalized Pr · A survey on large language models for recommendation |
| 8 | 1292 | 0 | 6 | reality, augmented reality, virtual, augmented, virtual reality, impai | proposta: fora | A research agenda for augmented and virtual reality in architecture, engineering · Metaverse for Healthcare: A Survey on Potential Applications, Challenges and Fut · A Survey on Measuring Cognitive Workload in Human-Computer Interaction |
| 9 | 1224 | 0 | 44 | 5g, 6g, wireless, communication, networks, communications, mimo, wirel | proposta: fora | A Comprehensive Survey on Internet of Things (IoT) Toward 5G Wireless Systems · An Overview of Signal Processing Techniques for Joint Communication and Radar Se · Foundations of User-Centric Cell-Free Massive MIMO |
| 10 | 1190 | 0 | 4 | health, digital health, digital, care, mobile, scoping, patient, scopi | proposta: fora | The Recent Progress and Applications of Digital Technologies in Healthcare: A Re · Challenges of Telemedicine during the COVID-19 pandemic: a systematic review · Perceptions and Needs of Artificial Intelligence in Health Care to Increase Adop |
| 11 | 1005 | 0 | 9 | code, software, engineering, llm, automated, generation, software deve | verificar | Software Testing With Large Language Models: Survey, Landscape, and Vision · Unit Test Case Generation with Transformers · Using Pre-Trained Models to Boost Code Review Automation |
| 12 | 941 | 0 | 26 | object, object detection, detection, driving, traffic, driver, autonom | regra: §1.2.1 c (aplicação — espera divisão) | YOLOv11: An Overview of the Key Architectural Enhancements · A Comprehensive Review of YOLO Architectures in Computer Vision: From YOLOv1 to  · A Survey of Modern Deep Learning based Object Detection Models |
| 13 | 915 | 0 | 20 | blockchain, iot, security, internet, technology, things, secure, inter | proposta: fora | Non-Fungible Token (NFT): Overview, Evaluation, Opportunities and Challenges · Federated Learning Meets Blockchain in Edge Computing: Opportunities and Challen · Survey on IoT security: Challenges and solution using machine learning, artifici |
| 14 | 852 | 0 | 48 | image, compression, denoising, image denoising, video, super resolutio | verificar | Deep learning models for digital image processing: a review · Methods for image denoising using convolutional neural network: a review · A review on medical image denoising algorithms |
| 15 | 767 | 0 | 7 | fake, detection, news, review detection, hate, hate speech, detection  | proposta: fora | HateCheck: Functional Tests for Hate Speech Detection Models · A Comprehensive Review on Fake News Detection With Deep Learning · ChatGPT or Human? Detect and Explain. Explaining Decisions of Machine Learning M |
| 16 | 653 | 0 | 24 | federated, federated learning, privacy, privacy preserving, preserving | verificar | Federated Learning for Internet of Things: A Comprehensive Survey · A survey on security and privacy of federated learning · Federated Learning on Non-IID Data: A Survey |
| 17 | 636 | 0 | 0 | attacks, prompt, llm, prompt injection, agents, injection, adversarial | proposta: fora | Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applicatio · How Johnny Can Persuade LLMs to Jailbreak Them: Rethinking Persuasion to Challen · Unleashing the potential of prompt engineering for large language models |
| 18 | 551 | 0 | 0 | rehabilitation, limb, sports, exoskeleton, wearable, gait, upper, uppe | proposta: fora | The exoskeleton expansion: improving walking and running economy · Wearable Sensor-Based Real-Time Gait Detection: A Systematic Review · Soft Robotic Suits: State of the Art, Core Technologies, and Open Challenges |
| 19 | 549 | 0 | 0 | fuzzy, fuzzy inference, inference, neuro fuzzy, neuro, anfis, adaptive | proposta: fora | An efficient optimization approach for designing machine learning models based o · Compressive Strength Prediction of Lightweight Concrete: Machine Learning Models · Prediction Model of Shield Performance During Tunneling via Incorporating Improv |
| 20 | 453 | 0 | 0 | control, fuzzy, controller, adaptive, anfis, motor, neuro fuzzy, neuro | proposta: fora | Direct torque control improvement of a variable speed DFIG based on a fuzzy infe · Adaptive neuro-fuzzy PID controller based on twin delayed deep deterministic pol · Design of a PID optimized neural networks and PD fuzzy logic controllers for a t |
| 21 | 435 | 0 | 11 | speech, speech recognition, recognition, automatic speech, automatic,  | verificar | Self-Supervised Speech Representation Learning: A Review · A Survey on Neural Speech Synthesis · Recent Advances in End-to-End Automatic Speech Recognition |
| 22 | 423 | 0 | 7 | healthcare, iot, monitoring, things, internet, internet medical, medic | proposta: fora | Remote patient monitoring using artificial intelligence: Current state, applicat · An intelligent healthcare monitoring framework using wearable sensors and social · Internet of Medical Things (IoMT): Overview, Emerging Technologies, and Case Stu |
| 23 | 406 | 0 | 2 | retinopathy, diabetic retinopathy, diabetic, retinal, artificial intel | proposta: fora | Deep Learning Techniques For Diabetic Retinopathy Classification: A Survey · Refractive surgery beyond 2020 · Fundus-controlled perimetry (microperimetry): Application as outcome measure in  |
| 24 | 402 | 0 | 3 | sentiment, sentiment analysis, aspect, analysis, reviews, based sentim | proposta: fora | Sentiment Analysis · Transformer models for text-based emotion detection: a review of BERT-based appr · State of the art: a review of sentiment analysis based on sequential transfer le |
| 25 | 395 | 0 | 30 | matrix, factorization, tensor, matrix factorization, bayesian, cluster | verificar | A survey of uncertainty in deep neural networks · Modern Koopman Theory for Dynamical Systems · Interpretable Machine Learning - A Brief History, State-of-the-Art and Challenge |
| 26 | 389 | 0 | 0 | machine learning, machine, prediction, predicting, risk, systematic re | proposta: fora | Prediction models for diagnosis and prognosis of covid-19: systematic review and · Comparison of machine learning and logistic regression models in predicting acut · Machine learning based prediction models for cardiovascular disease risk using e |
| 27 | 379 | 0 | 2 | ecg, cardiovascular, fibrillation, heart, atrial, atrial fibrillation, | proposta: fora | A review on deep learning methods for ECG arrhythmia classification · Review of noise removal techniques in ECG signals · Deep learning for ECG Arrhythmia detection and classification: an overview of pr |
| 29 | 379 | 0 | 3 | brain computer, brain, computer, computer interfaces, computer interfa | proposta: fora | Current Status, Challenges, and Possible Solutions of EEG-Based Brain-Computer I · Transfer Learning for EEG-Based Brain–Computer Interfaces: A Review of Progress  · Intra- and Inter-subject Variability in EEG-Based Sensorimotor Brain Computer In |
| 28 | 379 | 0 | 5 | watermarking, image, hiding, data hiding, techniques, reversible, vide | proposta: fora | Watermarking techniques for medical data authentication: a survey · Data Hiding With Deep Learning: A Survey Unifying Digital Watermarking and Stega · A Review on Text Steganography Techniques |
| 30 | 364 | 0 | 1 | fuzzy, fuzzy inference, inference, neuro fuzzy, neuro, adaptive neuro, | proposta: fora | Multiobjective Design Optimization of an IPMSM for EVs Based on Fuzzy Method and · Fuzzy inference system with interpretable fuzzy rules: Advancing explainable art · Short-term building electrical load forecasting using adaptive Neuro-Fuzzy Infer |
| 31 | 335 | 0 | 8 | reinforcement learning, reinforcement, deep reinforcement, embodied, l | proposta: fora | Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey · Exploration in Deep Reinforcement Learning: A Survey · Deep Reinforcement Learning for Robotics: A Survey of Real-World Successes |
| 32 | 326 | 0 | 8 | predictive maintenance, maintenance, fault, predictive, fault diagnosi | proposta: fora | Machine learning paradigm for structural health monitoring · Recent advances in the application of deep learning for fault diagnosis of rotat · State-of-the-art on research and applications of machine learning in the buildin |
| 33 | 310 | 0 | 5 | human activity, activity recognition, human, activity, recognition, ac | proposta: fora | Deep Learning for Sensor-based Human Activity Recognition · Sensor-based and vision-based human activity recognition: A comprehensive survey · Deep Learning in Human Activity Recognition with Wearable Sensors: A Review on A |
| 34 | 309 | 0 | 4 | diffusion, generation, diffusion models, image generation, image, text | regra: §1.2.1 b (difusão — fora) | Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding · Palette: Image-to-Image Diffusion Models · Diffusion Models in Vision: A Survey |
| 35 | 298 | 0 | 0 | scientific, peer, peer review, reviewer, paper, research, patent, auto | proposta: fora | ResearchAgent: Iterative Research Idea Generation over Scientific Literature wit · ReviewerGPT? An Exploratory Study on Using Large Language Models for Paper Revie · AutoSurvey: Large Language Models Can Automatically Write Surveys |
| 36 | 297 | 2 | 35 | distillation, knowledge distillation, knowledge, shot, learning, adapt | núcleo | Knowledge Distillation: A Survey · A Survey on Contrastive Self-supervised Learning · Revisiting Deep Learning Models for Tabular Data |
| 37 | 283 | 0 | 0 | fuzzy, fuzzy inference, neuro fuzzy, neuro, inference, diagnosis, anfi | proposta: fora | Optimization Method for Forecasting Confirmed Cases of COVID-19 in China · A Healthcare Monitoring System for the Diagnosis of Heart Disease in the IoMT Cl · An efficient clinical support system for heart disease prediction using TANFIS c |
| 38 | 279 | 0 | 0 | medical devices, artificial intelligence, intelligence, artificial, re | proposta: fora | Artificial intelligence in healthcare and medicine: clinical applications, thera · Global Regulatory Frameworks for the Use of Artificial Intelligence (AI) in the  · Opportunities and challenges of artificial intelligence and distributed systems  |
| 39 | 269 | 0 | 5 | indoor, localization, positioning, wi, wi fi, fi, fingerprinting, sens | proposta: fora | Cross-Domain WiFi Sensing with Channel State Information: A Survey · Survey on WiFi-based indoor positioning techniques · A Survey of Machine Learning for Indoor Positioning |
| 40 | 259 | 0 | 4 | graph, graph neural, representation learning, representation, networks | regra: §1.2.1 b (GNN — fora) | Graph Learning: A Survey · A Survey on Heterogeneous Graph Embedding: Methods, Techniques, Applications and · A Comprehensive Survey on Community Detection With Deep Learning |
| 41 | 249 | 0 | 0 | summarization, text, abstractive, summarization using, extractive, aut | proposta: fora | The Factual Inconsistency Problem in Abstractive Text Summarization: A Survey · Deep Learning Based Abstractive Text Summarization: Approaches, Datasets, Evalua · Abstractive text summarization: State of the art, challenges, and improvements |
| 42 | 247 | 0 | 1 | deepfake, detection, video, face, deep, techniques, detection using, i | proposta: fora | ASVspoof 2021: Towards Spoofed and Deepfake Speech Detection in the Wild · Generative adversarial networks (GANs): Introduction, Taxonomy, Variants, Limita · A Survey on Speech Deepfake Detection |
| 43 | 232 | 0 | 1 | note, ii, journal, designing, 2021, information, preface, internationa | proposta: fora | Physical unclonable functions · Overleaf Example · Journal of Applied Learning & Teaching |
| 44 | 216 | 0 | 1 | alzheimer, alzheimer disease, disease, parkinson, parkinson disease, d | proposta: fora | Deep learning for Alzheimer's disease diagnosis: A survey · Alzheimer's disease multiclass diagnosis via multimodal neuroimaging embedding f · Functional magnetic resonance imaging, deep learning, and Alzheimer's disease: A |
| 45 | 205 | 0 | 1 | power, anfis, fuzzy, control, voltage, fault, dc, controller | proposta: fora | The most used MPPT algorithms: Review and the suitable low-cost embedded board f · Overview of SOGI-Based Single-Phase Phase-Locked Loops for Grid Synchronization  · Optimal placement and sizing of multi-type FACTS devices in power systems using  |
| 46 | 202 | 0 | 2 | edge computing, computing, edge, offloading, mobile edge, computation, | regra: §1.2.1 d (infraestrutura — dentro) | An Overview on Edge Computing Research · A survey on the computation offloading approaches in mobile edge computing: A ma · A survey on computation offloading modeling for edge computing |
| 47 | 197 | 0 | 1 | point care, point, diagnostics, biosensors, chip, sleep, smartphone, c | proposta: fora | Recent progress, challenges, and prospects of fully integrated mobile and wearab · Machine learning in point-of-care testing: innovations, challenges, and opportun · Recent advances in lab-on-a-chip technologies for viral diagnosis |
| 48 | 190 | 0 | 1 | dental, dentistry, artificial intelligence, artificial, intelligence,  | proposta: fora | Accuracy and practicality of intraoral scanner in dentistry: A literature review · Artificial intelligence in dentistry—A review · Deep learning for cephalometric landmark detection: systematic review and meta-a |
| 49 | 167 | 0 | 2 | vision, computer vision, image classification, image, transformers, vi | regra: P2 (`arquiteturas`/ViT) | A Survey on Vision Transformer · Transformers in Vision: A Survey · Attention mechanisms in computer vision: A survey |
| 50 | 159 | 0 | 0 | education, medical education, nursing, medical, artificial, artificial | proposta: fora | Educational Strategies for Clinical Supervision of Artificial Intelligence Use. · Mapping the use of artificial intelligence in medical education: a scoping revie · The application of Chat Generative Pre-trained Transformer in nursing education. |
| 51 | 156 | 0 | 8 | 3d, point, point cloud, depth, reconstruction, depth estimation, point | proposta: fora | Review: deep learning on 3D point clouds · Monocular depth estimation based on deep learning: An overview · Comprehensive Review of Deep Learning-Based 3D Point Cloud Completion Processing |
| 52 | 151 | 0 | 8 | mlops, software, requirements, software development, development, lite | regra: `uso?` (MLOps — testar §1.2) | Machine Learning Operations (MLOps): Overview, Definition, and Architecture · Who Needs MLOps: What Data Scientists Seek to Accomplish and How Can MLOps Help? · Towards MLOps: A Framework and Maturity Model |
| 53 | 146 | 0 | 1 | sign language, sign, language recognition, recognition, language, gest | proposta: fora | Weakly Supervised Learning with Multi-Stream CNN-LSTM-HMMs to Discover Sequentia · Including Signed Languages in Natural Language Processing · Gestures Controlled Home Automation using Deep Learning: A Review |
| 54 | 145 | 0 | 0 | drug, drug discovery, discovery, protein, target, prediction, computat | proposta: fora | Computational Approaches in Preclinical Studies on Drug Discovery and Developmen · Attention is all you need: utilizing attention in AI-enabled drug discovery · Advanced machine-learning techniques in drug discovery. |
| 55 | 142 | 0 | 0 | defined, software defined, networking, defined networking, software, s | proposta: fora | “A Survey of Software Defined Networking” · An Exhaustive Survey on P4 Programmable Data Plane Switches: Taxonomy, Applicati · Scalability, Consistency, Reliability and Security in SDN Controllers: A Survey  |
| 56 | 139 | 0 | 1 | seizure, eeg, epileptic, epileptic seizure, epilepsy, detection, eeg b | proposta: fora | Development of Expert-Level Automated Detection of Epileptiform Discharges Durin · Machine learning and wearable devices of the future · Transformers in EEG Analysis: A Review of Architectures and Applications in Moto |
| 57 | 134 | 0 | 4 | face, face recognition, recognition, face detection, mask, facial, mas | proposta: fora | LightFace: A Hybrid Deep Face Recognition Framework · Fast Facial Landmark Detection and Applications: A Survey · Recent development in face recognition |
| 58 | 127 | 0 | 0 | wireless sensor, routing, wireless, sensor networks, sensor, fuzzy, cl | proposta: fora | Fuzzy based enhanced cluster head selection (FBECS) for WSN · A Survey on Energy-Efficient Strategies in Static Wireless Sensor Networks · Energy-Efficient, Cluster-Based Routing Protocol for Wireless Sensor Networks Us |
| 59 | 125 | 0 | 2 | series, time series, forecasting, series forecasting, time, stock, rec | proposta: fora | A review on the attention mechanism of deep learning · Transformers in Time Series: A Survey · A survey on long short-term memory networks for time series prediction |
| 60 | 123 | 0 | 1 | emotion, emotion recognition, recognition, speech, multimodal emotion, | proposta: fora | Speech emotion recognition: Emotional models, databases, features, preprocessing · A Review on Speech Emotion Recognition Using Deep Learning and Attention Mechani · Affective Image Content Analysis: Two Decades Review and New Perspectives |
| 61 | 117 | 0 | 0 | handwritten, recognition, character recognition, character, ocr, text  | proposta: fora | Towards efficient unconstrained handwriting recognition using Dilated Temporal C · A survey on handwritten mathematical expression recognition: The rise of encoder · Online handwriting recognition systems for Indic and non-Indic scripts: a review |
| 62 | 112 | 0 | 0 | captioning, image, caption, review image, deep learning, deep, video,  | proposta: fora | An Overview of Image Caption Generation Methods · Dual Graph Convolutional Networks with Transformer and Curriculum Learning for I · Visuals to Text: A Comprehensive Review on Automatic Image Captioning |
| 63 | 105 | 0 | 4 | manufacturing, industry, industrial, industrial internet, digital twin | proposta: fora | Industry 5.0: A survey on enabling technologies and potential applications · Artificial Intelligence Applications for Industry 4.0: A Literature-Based Study · Artificial-Intelligence-Driven Customized Manufacturing Factory: Key Technologie |
| 64 | 104 | 0 | 4 | home, home automation, automation, smart, smart home, automation using | proposta: fora | A Review Paper on Raspberry Pi and its Applications · IoT-Cognizant cloud-assisted energy efficient embedded system for indoor intelli · A Systematic Analysis on Raspberry Pi Prototyping: Uses, Challenges, Benefits, a |
| 65 | 100 | 0 | 0 | fuzzy, fuzzy inference, mamdani, fuzzy logic, student, logic, inferenc | proposta: fora | AI different approaches and ANFIS data mining: A novel approach to predicting ea · Evaluating critical success factors in the permanence in Higher Education using  · A neuro-fuzzy model for predicting and analyzing student graduation performance  |

## 5. O que acontece com cada escolha

| categoria da proposta | obras |
|---|---|
| núcleo | 4612 |
| regra | 4267 |
| verificar | 33635 |
| proposta: fora | 32277 |

Se você aceitar **todos** os "fora" da proposta, sobram 42514 obras —
das quais 25158 estão no grupo -1 (sem grupo). A camada C (ASReview) partiria desse número, e o
grupo -1 provavelmente precisa de tratamento próprio antes (ex.: reatribuir cada obra ao grupo mais
próximo, função do próprio BERTopic).

**Salvaguarda antes de descartar qualquer grupo:** sortear uma amostra dele e conferir que não há
cajuzeiro; e medir a perda na metade de teste do gabarito (só depois da sua decisão).

---

## 7. Aplicação (Pedro, 23/09: "pode seguir" — proposta aceita)

**Passo 1 — reatribuição do grupo -1.** As 25.158 obras sem grupo foram postas no grupo cujo centro (média dos vetores dos membros) é mais parecido com elas — é o que a função `reduce_outliers` do BERTopic faz na estratégia por embeddings. Similaridade mediana 0,94 (10% abaixo de 0,90). Foram para: fora 17.227 · verificar 3.498 · núcleo 1.070 · regras 3.363.

**Passo 2 — marcação.** Coluna `camada_B` no CSV da floresta (e `camada_B_grupo_final`, `camada_B_reatribuido`).

| categoria | obras |
|---|---|
| fora | 49504 |
| verificar | 11975 |
| núcleo | 5682 |
| regra §1.2.1 c | 4225 |
| regra uso? | 1194 |
| regra §1.2.1 b | 890 |
| regra §1.2.1 d | 767 |
| regra P2 | 554 |

**Passo 3 — perda na metade de teste (29):** 25 no núcleo · 1 em *regra §1.2.1 d* (dentro) · 1 em *regra P2* — **"Efficient Transformers: A Survey"**, que caiu no grupo 49 (Vision Transformer): a P2 decide se ele fica · 1 excluída na camada A (*Green Deep Learning*) · **1 perdida em "fora": "A comprehensive survey on model compression and acceleration"** (542 citações).

## 8. O problema achado: o grupo 43 e as suspeitas nos grupos "fora"

A obra perdida estava sem grupo e foi reatribuída ao **grupo 43** — que não é um assunto: é o grupo de **metadado ruim** (editoriais, prefácios, capítulos; palavras-chave *note, ii, journal, preface*). Ele absorveu 939 obras sem grupo, e junto vieram cajuzeiros: *A comprehensive survey on model compression and acceleration*, *A Survey on Mixture of Experts* (196 cit.), *The Prompt Report*. **O grupo 43 não deveria estar em "fora".**

Além dele, **751 obras nos grupos "fora" têm palavra de tipo + termo núcleo no título**. A maioria é homônimo (512 casam só por termos de `edge`: *lightweight cryptography*, *resource-constrained project scheduling*, *embedded sensors*; LoRa como rádio), mas há cajuzeiros reais, ex.: *A Survey of On-Policy Distillation for LLMs* (grupo 31, aprendizado por reforço).

**Proposta de correção:** (a) grupo 43 -> **verificar**; (b) a **mesma salvaguarda pelo título que você escolheu na camada A**: obra de grupo "fora" com palavra de tipo + termo núcleo no título vai para **verificar**. Efeito: +1.171 (grupo 43) + 704 = **27.162 obras** não-fora. *Ressalva:* estou propondo isto depois de ver o teste; a salvaguarda é a regra que já estava decidida na camada A, mas o teste desta camada fica parcialmente gasto.

## 9. Amostras dos grupos "verificar" (15 por grupo, sorteio semente 2309)

Para você decidir o grupo inteiro olhando títulos reais.

### Grupo 4 — LLM, clinical, ChatGPT (3136 obras após reatribuição)

- 2026 — From “Correct Translation” to “Great Translation”: Research on Human–Machine Collaborative Translation and Translators’ Digital Intelligence Literacy: A Comparative Analysis of Translations Produced by ChatGPT, DeepSeek, and Human Translators
- 2023 — Generative Artificial Intelligence for Clinical Communication: Implications for Non-Pharmacological Interventions in Health Care.
- 2024 — AI and Human Reasoning: Qualitative Research in the Age of Large Language Models
- 2025 — Evaluating a Multi-Modal Large Language Model for Ophthalmology Triage
- 2021 — PICO entity extraction for preclinical animal literature
- 2023 — The Amount of Errors in ChatGPT’s Responses is Indirectly Correlated with the Number of Publications Related to the Topic Under Investigation
- 2026 — Bibliometric, methodological and reporting characteristics of systematic reviews with explicit AI disclosure statements: an exploratory meta-research study
- 2020 — Writer’s uncertainty identification in scientific biomedical articles: a tool for automatic if-clause tagging
- 2025 — Generative AI vs. human expertise: a comparative analysis of case-based rational pharmacotherapy question generation
- 2026 — An Intelligent Conversational Healthcare System for Symptom-Based Disease Prediction and Location-Aware Hospital Recommendation Using Machine Learning
- 2026 — Performance of generative artificial intelligence in oral and maxillofacial radiology based on the board-certification examination of Japan.
- 2025 — Small Language Models in Healthcare: Capabilities, Challenges, and Future Directions
- 2024 — Automated Mass Extraction of Over 680,000 PICOs from Clinical Study Abstracts Using Generative AI: A Proof-of-Concept Study
- 2026 — AD-CARE: A Guideline-grounded, Modality-agnostic LLM Agent for Real-world Alzheimer's Disease Diagnosis with Multi-cohort Assessment, Fairness Analysis, and Reader Study
- 2026 — irAE-GPT: leveraging large language models to identify immune-related adverse events in electronic health records and clinical trial datasets

### Grupo 5 — language models, translation, NLP (3709 obras após reatribuição)

- 2026 — The Profiler-Agent: A Retrieval-Augmented and Latent-State Reasoning Framework for Complex Narrative Data
- 2020 — Syntax Representation in Word Embeddings and Neural Networks - A Survey
- 2020 — Lemmatization and morphological analysis for the Latin Dependency Treebank
- 2023 — Connecting Humanities and Social Sciences: Applying Language and Speech Technology to Online Panel Surveys
- 2025 — Classification of Greek News Articles by Text Type Using Open Large Language Models
- 2026 — Fine-Tuning T5 and BERT for Effective Question Answering and Document Retrieval: A Transfer Learning Approach
- 2025 — Multilingual Chatbot Development Using Pre-Trained Language Models: A Survey
- 2025 — Shifting AI Efficiency From Model-Centric to Data-Centric Compression
- 2025 — Bridging the linguistic divide: a survey on leveraging large language models for machine translation
- 2022 — An Introduction to Retrieval and Reminiscence from Lifelog Archives at NTCIR
- 2023 — Knowledge Graph Embedding: An Overview
- 2025 — Generalist Scanner Meets Specialist Locator: A Synergistic Coarse-to-Fine Framework for Robust GUI Grounding
- 2025 — Towards Fair User Modeling with Survey Guided Learning
- 2026 — Artificial Intelligence in Sacred Text Analysis: A Survey of Methodologies and Applications
- 2026 — GATES: Self-Distillation under Privileged Context with Consensus Gating

### Grupo 11 — code, software engineering, LLM (1750 obras após reatribuição)

- 2023 — Examining deep learning’s capability to spot code smells: a systematic literature review
- 2025 — SecureReviewer: Enhancing Large Language Models for Secure Code Review through Secure-aware Fine-tuning
- 2026 — SLBench: Evaluating How LLM Agents Follow Logical Relations in Skills
- 2023 — Empirical Study on Transformer-based Techniques for Software Engineering
- 2026 — From Intent to Execution: Composing Agentic Workflows with Agent Recommendation
- 2024 — Vulnerability Handling of AI-Generated Code - Existing Solutions and Open Challenges
- 2025 — Exploring ChatGPT as a Qualitative Research Assistant
- 2021 — Faults in Deep Reinforcement Learning Programs: A Taxonomy and A Detection Approach
- 2026 — Comparative Analysis of Security Vulnerabilities in Ai-Generated Versus Human-Written Python Code: an Automated Static Analysis Approach
- 2025 — A Design Science Blueprint for an Orchestrated AI Assistant in Doctoral Supervision
- 2026 — The Governance Gap in Contemporary LLM-Based Agentic Systems: A Structural Diagnostic Review
- 2023 — Automating Code-Related Tasks Through Transformers: The Impact of Pre-training
- 2026 — RustC4++: Improving Rust Code-Comment Inconsistency Detection via Hybrid LLM and Static Analysis
- 2022 — Effort-Aware Just-in-Time Bug Prediction for Mobile Apps Via Cross-Triplet Deep Feature Embedding
- 2023 — A Survey of Software Defects Research Based on Deep Learning

### Grupo 14 — image/video compression, denoising, sparse (1006 obras após reatribuição)

- 2025 — A survey on Deep Image Prior for image denoising
- 2023 — Video Coding for Machines using Object Analysis and Standard Video Codecs
- 2024 — A Review of Image Denoising Using Fuzzy and Wiener Filters in the Wavelet Domain
- 2024 — Compressive Sensing in Image/Video Compression: Sampling, Coding, Reconstruction, and Codec Optimization
- 2022 — Change Bit-Depth Procedure for Data Measured Preprocessing before Compression
- 2023 — An end-to-end deep convolutional neural network for image restoration of sparse aperture imaging system in geostationary orbit
- 2026 — Text Image Restoration: A Comprehensive Review of Multi-modal, Generative, and Adaptive Approaches
- 2024 — Video compression and optimization technologies - review
- 2021 — Adaptive Resolution-Based Tradeoffs for Energy-Efficient Visual Computing Systems
- 2025 — Diffusion Models for Low-Light Image Enhancement: A Multi-Perspective Taxonomy and Performance Analysis
- 2024 — A Review on FPGA-based Architectures for Noise Removal of Digital Images using High-Level Design
- 2025 — A Review of Efficient Contrast Enhancement Techniques in Computer Vision: From Histogram Equalization to Lightweight Deep Learning
- 2026 — Image Inpainting Methods: A Review of Deep Learning Approaches
- 2024 — Overview of Visual Signal Compression towards Machine Vision
- 2022 — Efficient feature based video retrieval and indexing using pattern change with invariance algorithm

### Grupo 16 — federated learning, privacy (872 obras após reatribuição)

- 2023 — A Comprehensive Study on Model Initialization Techniques Ensuring Efficient Federated Learning
- 2026 — VSCI: Verifiable Smooth Coded Inference Via Spline Reconstruction
- 2025 — Optimizing Privacy-Preserving Primitives to Support LLM-Scale Applications
- 2023 — A Systematic Literature Review on Client Selection in Federated Learning
- 2026 — Advancements and challenges of federated learning in medical imaging: a systematic literature review
- 2025 — FedBKD: Distilled Federated Learning to Embrace Gerneralization and Personalization on Non-IID Data
- 2025 — Privacy-preserving cyberbullying detection using federated learning: A comprehensive review of technologies, challenges and solutions
- 2022 — Federated Graph Neural Networks: Overview, Techniques and Challenges
- 2026 — Personalizing Federated Learning Models: Methods, Applications, and Challenges in Healthcare 5.0
- 2023 — TVFL: Tunable Vertical Federated Learning towards Communication-Efficient Model Serving
- 2026 — Validated Synthetic Data Generation from a Multicenter Spine Surgery Registry: Methodology and Benchmark
- 2026 — Privacy-Preserving Machine Learning for IoT: A Cross-Paradigm Survey and Future Roadmap
- 2023 — Limitations and Future Aspects of Communication Costs in Federated Learning: A Survey
- 2025 — Moving from Manual to Automated Sleep Staging with Federated Learning
- 2025 — Adaptive Embedded Machine Learning on IoT Devices: A Review

### Grupo 21 — speech recognition, audio (608 obras após reatribuição)

- 2025 — Voice-Enabled Local Language Translator Using Generative AI
- 2023 — Segment-Based Spotting of Bowel Sounds Using Pretrained Models in Continuous Data Streams
- 2022 — An Empirical Study on How People Perceive AI-generated Music
- 2022 — Category of speech system in modeling affective processes (based on the material of network communication)
- 2026 — SW-ASR: A Context-Aware Hybrid ASR Pipeline for Robust Single Word Speech Recognition
- 2025 — Adaptive Modality Gating: Explainable, Confidence-Guided Fusion for Source-Only Zero-Shot Deepfake Detection
- 2025 — From Waveforms to Pixels: A Survey on Audio-Visual Segmentation
- 2025 — The Sound of Syntax: Finetuning and Comprehensive Evaluation of Language Models for Speech Pathology
- 2020 — Review of existing text-to-speech algorithms
- 2022 — Robotic System Control using Embedded Machine Learning and Speech Recognition
- 2025 — On The Landscape of Spoken Language Models: A Comprehensive Survey
- 2026 — AfriVoices-KE: A Multilingual Speech Dataset for Kenyan Languages
- 2023 — Speech-to-Text and Text-to-Speech Recognition Using Deep Learning
- 2025 — Evolution and Perspectives of Speech Synthesis Technology: From Parametric Synthesis to the Era of Large Language Models
- 2025 — A Review on Sound Source Localization in Robotics: Focusing on Deep Learning Methods

### Grupo 25 — matrix/tensor factorization, bayesian, uncertainty (894 obras após reatribuição)

- 2026 — Hybrid Machine Learning and Fuzzy Inference System for University Admission Prediction
- 2022 — Population-Based Hierarchical Non-Negative Matrix Factorization for Survey Data
- 2024 — Inference with Sequential Monte-Carlo Computation of $p$-values: Fast and Valid Approaches
- 2020 — Sparse Methods for Automatic Relevance Determination
- 2021 — Numerical Matrix Decomposition
- 2024 — A tutorial on multi-view autoencoders using the multi-view-AE library
- 2025 — Towards Quantum Tensor Decomposition in Biomedical Applications
- 2020 — Population Total Estimation in a Complex Survey by Nonparametric Model Calibration Using Penalty Function Method with Auxiliary Information Known at Cluster Levels
- 2021 — Manifold Modeling in Machine Learning
- 2022 — Multigroup Analysis in Information Systems Research using PLS-PM
- 2025 — Attribute Filtering in Approximate Nearest Neighbor Search: An In-depth Experimental Study
- 2021 — Mining real-world high dimensional structured data in medicine and its use in decision support. Some different perspectives on unknowns, interdependency, and distinguishability
- 2024 — Review of Recent Advances in Gaussian Process Regression Methods
- 2023 — Rare Category Analysis for Complex Data: A Review
- 2024 — Techniques for Handling Missing Values in Customers Electricity Data: A Systematic Literature Review

## 10. Leitura das amostras e proposta final (PROPOSTA DO CLAUDE — decisão do Pedro)

Pelas amostras: **4** (LLM em clínica), **11** (engenharia de software), **14** (processamento de
imagem/vídeo), **21** (fala) e **25** (fatoração/estatística) são de outras áreas — o raro cajuzeiro
ali dentro é salvo pela salvaguarda do título. **5** (linguagem) e **16** (federado) são mistos
(ex.: *Shifting AI Efficiency From Model-Centric to Data-Centric Compression* no 5;
*Communication-Efficient Model Serving* no 16) e seguem.

**Efeito da proposta completa** (grupo 43 -> verificar; salvaguarda do título em todo grupo "fora";
4, 11, 14, 21, 25 -> fora):

| destino | obras | das quais com palavra de tipo no título |
|---|---|---|
| fora | 54.882 | — |
| núcleo | 5.682 | 1.323 |
| verificar (5, 16, 43) | 5.752 | 2.091 |
| salva pela salvaguarda | 845 | 845 |
| regra §1.2.1 c — aplicação, espera divisão | 4.225 | 1.759 |
| regra §1.2.1 b — difusão/GNN, fora pela regra | 890 | 396 |
| regra §1.2.1 d — infraestrutura, dentro | 767 | 364 |
| regra `uso?` (MLOps) | 1.194 | 325 |
| regra P2 (ViT; contém *Efficient Transformers: A Survey*) | 554 | 285 |

**Entrada da camada C (sem os grupos de regra b e c):** ~**14.800 obras**. O ASReview não obriga a
ler todas: ele ordena a fila e para pela regra SAFE; quantas você marca depende de quão cedo os
cajuzeiros se esgotam — não dá para prever antes de começar.
