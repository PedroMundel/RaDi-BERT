# F2 — auditoria do Pedro (M4.3): 30 vereditos sorteados do agente 3

Para cada obra: o veredito, a regra e a frase que o agente usou, e o abstract completo para conferir. Marque na coluna da sua cabeça: **concordo / discordo**. Semente 2611.

## 1. F0581 — Disentangling generalization and memorization in large language models using chess (2026)

- **Veredito final:** fora · **regra:** §3.4 fora da área · **objetivo:** —
- **Frase usada:** "Large Language Models (LLMs) exhibit remarkable capabilities, yet it remains unclear to what extent these reflect sophisticated recall or genuine reasoning ability."
- **Motivo do agente:** não é survey (testbed/benchmark primário); tema é capacidade de raciocínio, não eficiência de implantação
- **Abstract:** Large Language Models (LLMs) exhibit remarkable capabilities, yet it remains unclear to what extent these reflect sophisticated recall or genuine reasoning ability. We introduce chess as a controlled testbed aimed at disentangling these faculties. Leveraging the game's structure and scalable engine evaluations, we construct a taxonomy of positions varying in density of relevant priors - ranging from common states solvable by memorization to completely novel ones requiring generalization. Crucially, our approach achieves this distinction without requiring explicit knowledge of the models'training data. Applying this taxonomy, we combine a longitudinal analysis of the GPT lineage with a rigorous evaluation of contemporary models, including Claude Opus and Gemini. Our analysis reveals a steep gradient: performance consistently degrades as the density of relevant priors decreases. Notably, for tasks with few relevant priors, base model performance regresses to the random-play baseline. While newer models improve, progress slows significantly for tasks with sparse priors. Furthermore, while reasoning-augmented inference improves performance, its relative marginal benefit per token decreases in the absence of relevant priors. These results suggest limitations in systematic generalization, highlighting the need for mechanisms beyond scale to achieve robust performance when deprived of relevant priors.

## 2. F0401 — A Review of Privacy Preserving Federated Learning for Private IoT Analytics (2020)

- **Veredito final:** fora · **regra:** §1.2 (sem eixo) · **objetivo:** —
- **Frase usada:** "This work reviews research around an alternative approach to machine learning known as federated learning"
- **Motivo do agente:** revisão de aprendizado federado; sem eixo de inferência, memória/hardware ou redução de rótulo para implantação
- **Abstract:** The Internet-of-Things generates vast quantities of data, much of it attributable to an individual's activity and behaviour. Holding and processing such personal data in a central location presents a significant privacy risk to individuals (of being identified or of their sensitive data being leaked). However, analytics based on machine learning and in particular deep learning benefit greatly from large amounts of data to develop high performance predictive models. Traditionally, data and models are stored and processed in a data centre environment where models are trained in a single location. This work reviews research around an alternative approach to machine learning known as federated learning which seeks to train machine learning models in a distributed fashion on devices in the user's domain, rather than by a centralised entity. Furthermore, we review additional privacy preserving methods applied to federated learning used to protect individuals from being identified during training and once a model is trained. Throughout this review, we identify the strengths and weaknesses of different methods applied to federated learning and finally, we outline future directions for privacy preserving federated learning research, particularly focusing on Internet-of-Things applications.

## 3. F0866 — A Survey on Secure and Private Federated Learning Using Blockchain: Theory and Application in Resource-Constrained Computing (2023)

- **Veredito final:** dúvida · **regra:** frases insuficientes para eixo de §1.2 · **objetivo:** —
- **Frase usada:** "this survey focuses on reviewing the challenges, solutions, and future directions for the successful deployment of blockchain in resource-constrained FL environments"
- **Motivo do agente:** foco aparente em segurança/blockchain; sinal de recurso-restrito insuficiente para confirmar eixo de implantação
- **Abstract:** Federated learning (FL) has gained widespread popularity in recent years due to the fast booming of advanced machine learning and artificial intelligence, along with emerging security and privacy threats. Federated learning (FL) enables efficient model generation from local data storage of the edge devices without revealing the sensitive data to any entities. While this paradigm partly mitigates the privacy issues of users’ sensitive data, the performance of the FL process can be threatened and reach a bottleneck due to the growing cyber threats and privacy violation techniques. To expedite the proliferation of the FL process, the integration of blockchain for FL environments has drawn increasing attention from academia and industry. Blockchain has the potential to prevent security and privacy threats with its decentralization, immutability, consensus, and transparency characteristics. However, if the blockchain mechanism requires costly computational resources, then the resource-constrained FL clients cannot be involved in the training. Considering that, this survey focuses on reviewing the challenges, solutions, and future directions for the successful deployment of blockchain in resource-constrained FL environments. We comprehensively review variant blockchain mechanisms suitable for the FL process and discuss their tradeoffs for a limited resource budget. Furthermore, we extensively analyze the cyber threats that could be observed in a resource-constrained FL environment, and how blockchain can play a key role in blocking those cyberattacks. To this end, we highlight some potential solutions for the coupling of blockchain and FL that can offer high levels of reliability, data privacy, and distributed computing performance.

## 4. F0801 — Automated Course-Program Outcome Mapping with Bloom's Taxonomy and DEI Classification Using Lightweight Transformer Models (2025)

- **Veredito final:** fora · **regra:** §3.4 não é survey · **objetivo:** —
- **Frase usada:** "This study employs transformer-based models, MiniLM-v2 and DistilBERT, to automate CO–PO mapping, Bloom's classification, and DEI categorization."
- **Motivo do agente:** não é survey; aplica modelos já leves a tarefa educacional, sem eixo de custo de implantação — fora da área
- **Abstract:** Effective alignment of Course Outcomes (COs) with Program Outcomes (POs) and Bloom’s Taxonomy levels is essential for accreditation and quality assurance in engineering education. This study employs transformer-based models, MiniLM-v2 and DistilBERT, to automate CO–PO mapping, Bloom’s classification, and DEI categorization. A dataset of over 1,000 CO–PO pairs from CHED guidelines was used to evaluate performance against Support Vector Classifier (SVC) baselines. For PO mapping, DistilBERT achieved the highest F1-score (0.22) and accuracy (0.25), outperforming MiniLM-v2 and SVC. In Bloom’s classification, both transformers scored F1 = 0.97, with MiniLM-v2 slightly surpassing DistilBERT in Macro-Average AUC (0.9910). For DEI mapping, MiniLM-v2 achieved the top Macro AUC (0.9909) due to its deeper architecture, balanced hidden size, and relational embedding mechanism, enabling superior semantic understanding. Integrated into a Flask-based web tool, these models provide an accessible, efficient system for curriculum development. Overall, MiniLM-v2 offers the best combination of accuracy, semantic understanding, and scalability for automated curriculum alignment.

## 5. F0019 — Survey of Knowledge Distillation in Federated Edge Learning (2023)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c), indefinido · **objetivo:** —
- **Frase usada:** "In this paper, we investigate the works that KD applies to FEL"
- **Motivo do agente:** KD é técnica da área, mas as frases não explicam o que é FEL nem se há eixo de implantação
- **Abstract:** The increasing demand for intelligent services and privacy protection of mobile and Internet of Things (IoT) devices motivates the wide application of Federated Edge Learning (FEL), in which devices collaboratively train on-device Machine Learning (ML) models without sharing their private data. Limited by device hardware, diverse user behaviors and network infrastructure, the algorithm design of FEL faces challenges related to resources, personalization and network environments. Fortunately, Knowledge Distillation (KD) has been leveraged as an important technique to tackle the above challenges in FEL. In this paper, we investigate the works that KD applies to FEL, discuss the limitations and open problems of existing KD-based FEL approaches, and provide guidance for their real deployment.

## 6. F0782 — Lightweight Convolutional Neural Networks for Wheat Disease Detection and Classification: A Review and Comparative Study From Field to Storage (2026)

- **Veredito final:** fora · **regra:** §1.2.1 (b) · **objetivo:** —
- **Frase usada:** "Lightweight Convolutional Neural Networks (LCNNs)"
- **Motivo do agente:** Survey restrita a CNNs leves (LCNN), técnica só-CNN (b), aplicada a análise de imagem de trigo.
- **Abstract:** The increasing adoption of Lightweight Convolutional Neural Networks (LCNNs) for agricultural applications has highlighted their potential for automated wheat disease detection and classification across both field (pre-harvest) and post-harvest storage environments. However, the effectiveness and deployability of such systems depend not only on model architecture but also critically on the quality and suitability of the datasets used for training and evaluation. In this paper, two complementary reviews are presented to address these intertwined challenges. First, a systematic review of LCNN architectures is conducted, focusing on models applied to wheat-related image analysis across both field and storage scenarios, with particular emphasis on classification performance, model compactness, computational efficiency, and compatibility with edge and embedded platforms, especially in the context of deployment under storage conditions. Second, a critical review of existing wheat grain image datasets is provided, examining dataset scale, acquisition conditions, annotation strategies, class diversity, and accessibility, with an emphasis on their relevance to storage-based disease detection tasks. The integrated analysis reveals a strong interdependence between architectural performance and dataset characteristics. Reported gains in LCNN accuracy are often influenced by dataset bias, controlled imaging conditions, and class imbalance, which can obscure real-world performance in storage environments. Lightweight models, while advantageous for deployment, are shown to be especially sensitive to limitations in data realism and annotation quality. Moreover, a mismatch is identified between current dataset acquisition practices and the operational conditions encountered in grain storage, including bulk aggregation, occlusion, dust, and uneven illumination. The findings highlight a fragmentation between model development and dataset construction in existing research. This study emphasizes the need for a co-design paradigm in which LCNN architectures and storage-realistic datasets are developed in tandem.

## 7. F0513 — KD2M: A Unifying Framework for Feature Knowledge Distillation (2025)

- **Veredito final:** fora · **regra:** §3.4 primário da área · **objetivo:** —
- **Frase usada:** "we propose an unifying framework, Knowledge Distillation through Distribution Matching (KD$^{2}$M)"
- **Motivo do agente:** framework primário de destilação de conhecimento, não é survey
- **Abstract:** Knowledge Distillation (KD) seeks to transfer the knowledge of a teacher, towards a student neural net. This process is often done by matching the networks'predictions (i.e., their output), but, recently several works have proposed to match the distributions of neural nets'activations (i.e., their features), a process known as \emph{distribution matching}. In this paper, we propose an unifying framework, Knowledge Distillation through Distribution Matching (KD$^{2}$M), which formalizes this strategy. Our contributions are threefold. We i) provide an overview of distribution metrics used in distribution matching, ii) benchmark on computer vision datasets, and iii) derive new theoretical results for KD.

## 8. F0849 — Lightweight HI source finding for next generation radio surveys (2022)

- **Veredito final:** fora · **regra:** §3.4 sistema/ferramenta · **objetivo:** —
- **Frase usada:** "We introduce LiSA, a set of python modules for the denoising, detection and characterization of HI sources in 3D spectral data"
- **Motivo do agente:** ferramenta de software para radioastronomia, não é survey nem trata eixo de implantação
- **Abstract:** Future deep HI surveys will be essential for understanding the nature of galaxies and the content of the Universe. However, the large volume of these data will require distributed and automated processing techniques. We introduce LiSA, a set of python modules for the denoising, detection and characterization of HI sources in 3D spectral data. LiSA was developed and tested on the Square Kilometer Array Science Data Challenge 2 dataset, and contains modules and pipelines for easy domain decomposition and parallel execution. LiSA contains algorithms for 2D-1D wavelet denoising using the starlet transform and flexible source finding using null-hypothesis testing. These algorithms are lightweight and portable, needing only a few user-defined parameters reflecting the resolution of the data. LiSA also includes two convolutional neural networks developed to analyse data cubes which separate HI sources from artifacts and predict the HI source properties. All of these components are designed to be as modular as possible, allowing users to mix and match different components to create their ideal pipeline. We demonstrate the performance of the different components of LiSA on the SDC2 dataset, which is able to find 95% of HI sources with SNR>3 and accurately predict their properties.

## 9. F0007 — Practical Lab Monitoring System (2020)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 10. F0748 — A survey of deep nonnegative matrix factorization (2022)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 11. F0705 — Knowledge distillation and teacher-student learning in medical imaging: Comprehensive overview, pivotal role, and future directions (2025)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c) · **objetivo:** —
- **Frase usada:** "comprehensively review the development and application of KD in the medical imaging field"
- **Motivo do agente:** aplicação específica (c): destilação de conhecimento aplicada a imagem médica, exemplo citado no método
- **Abstract:** Knowledge Distillation (KD) is a technique to transfer the knowledge from a complex model to a simplified model. It has been widely used in natural language processing and computer vision and has achieved advanced results. Recently, the research of KD in medical image analysis has grown rapidly. The definition of knowledge has been further expanded by combining with the medical field, and its role is not limited to simplifying the model. This paper attempts to comprehensively review the development and application of KD in the medical imaging field. Specifically, we first introduce the basic principles, explain the definition of knowledge and the classical teacher-student network framework. Then, the research progress in medical image classification, segmentation, detection, reconstruction, registration, radiology report generation, privacy protection and other application scenarios is presented. In particular, the introduction of application scenarios is based on the role of KD. We summarize eight main roles of KD techniques in medical image analysis, including model compression, semi-supervised method, weakly supervised method, class balancing, etc. The performance of these roles in all application scenarios is analyzed. Finally, we discuss the challenges in this field and propose potential solutions. KD is still in a rapid development stage in the medical imaging field, we give five potential development directions and research hotspots. A comprehensive literature list of this survey is available at https://github.com/XiangQA-Q/KD-in-MIA.

## 12. F0121 — OneLA: Scaling Linear-Attention Decoding to Large Beams in Generative Recommendation (2026)

- **Veredito final:** fora · **regra:** §3.4 primário da área · **objetivo:** —
- **Frase usada:** "we present OneLA, a linear-attention decoding framework that exploits the shared prompt and short divergent suffixes of GR workloads."
- **Motivo do agente:** framework primário para acelerar decodificação (inferência), não é survey
- **Abstract:** Generative recommendation (GR) relies on large-beam decoding to generate hundreds of candidate items, creating a new scaling challenge for recurrent linear attention. Existing linear attention serving systems either materialize a full recurrent state for every beam or repeatedly replay shared history, incurring substantial memory and traffic overhead. To address this, we present OneLA, a linear-attention decoding framework that exploits the shared prompt and short divergent suffixes of GR workloads. Specifically, OneLA represents all beam states using a single shared prompt-derived state and compact, append-only records of their divergent transitions. Using this representation, OneLA computes only the state information required at each decoding step, without reconstructing a full recurrent state for every beam. Furthermore, OneLA uses a lightweight ancestry index to track the transition records that make up each beam's history, allowing beams to be updated without moving or copying existing records. A fused GPU kernel further reuses the shared state across beams. Our analysis shows that OneLA achieves 1.54-2.46x end-to-end decode speedups while substantially reducing recurrent-state memory use and data movement.

## 13. F0426 — Advances in devices and on-device/edge computing algorithm for infrared machine vision and infrared thermography: a review (2026)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 14. F0589 — Essential-Web v1.0: 24T tokens of organized web data (2025)

- **Veredito final:** fora · **regra:** §3.4 fora da área · **objetivo:** —
- **Frase usada:** "We present Essential-Web v1.0, a 24-trillion-token dataset in which every document is annotated with a twelve-category taxonomy covering topic, format, content complexity, and quality."
- **Motivo do agente:** não é survey (artigo de dataset); tema é curadoria de dado de treino, não eficiência de implantação
- **Abstract:** Data plays the most prominent role in how language models acquire skills and knowledge. The lack of massive, well-organized pre-training datasets results in costly and inaccessible data pipelines. We present Essential-Web v1.0, a 24-trillion-token dataset in which every document is annotated with a twelve-category taxonomy covering topic, format, content complexity, and quality. Taxonomy labels are produced by EAI-Distill-0.5b, a fine-tuned 0.5b-parameter model that achieves an annotator agreement within 3% of Qwen2.5-32B-Instruct. With nothing more than SQL-style filters, we obtain competitive web-curated datasets in math (-8.0% relative to SOTA), web code (+14.3%), STEM (+24.5%) and medical (+8.6%). Essential-Web v1.0 is available on HuggingFace: https://huggingface.co/datasets/EssentialAI/essential-web-v1.0

## 15. F0198 — STARLESS'23: 2nd Workshop on Serverless computing for pervasive cloud-edge-device systems and services - Welcome and Committees *LESS 2023 welcome message (2023)

- **Veredito final:** dúvida · **regra:** §3.4 incerto · **objetivo:** —
- **Frase usada:** "the first in-person workshop on serverless computing for pervasive cloud-edge-device systems and services"
- **Motivo do agente:** parece introdução/anúncio de workshop sobre infraestrutura serverless (eixo d), mas frases não mostram se organiza/revisa literatura (survey)
- **Abstract:** After the successful kick-off of the *LESS workshop series in 2022 as a virtual event due to the lingering travel restrictions for the COVID-19 pandemic, we are very excited to host the first in-person workshop on serverless computing for pervasive cloud-edge-device systems and services. Serverless technologies have remained so far confined within the realm of cloud computing, but this is changing fast, with serverless/edgeless/deviceless paradigms being adopted more and more in decentralized and distributed systems thanks to the flexible Function-as-a-Service (FaaS) programming model and their ability to efficiently adapt to changing environments. Our ambition through *LESS 2023 is to raise awareness of serverless opportunities within pervasive computing and their associated open research challenges. We aim to lead the way for further research activities in this emerging area, with potentially high impact on the market of Internet of Things (IoT), smart cities, industrial automation, mobile health, and so on. We thank the TPC members for their timely and professional efforts in reviewing the submissions received, which resulted in a technical program with three very high quality papers covering the topics of performance evaluation, open source contributions, and Artificial Intelligence. Moreover, we would like to thank Gregor Schiele for his inspiring keynote speech on adaptive AI in holistic pervasive systems, as well as Gabriele Russo Russo for anticipating his main conference talk on decentralized edge-cloud FaaS in a meet-the-author session. We also thank the PerCom organizers and the PerCom workshop co-chairs, Carlo Vallati and Qi Han, for their continued support and assistance in all the organization phases. Finally, we thank all the authors and workshop attendees for their contributions and participation.

## 16. F0669 — Small Language Models for Phishing Website Detection: A Review of Cost, Performance, and Privacy Trade-Offs (2026)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c) · **objetivo:** —
- **Frase usada:** "empirical comparison of fifteen open small language models (SLMs) for phishing website detection"
- **Motivo do agente:** aplicação específica (c) - detecção de phishing
- **Abstract:** This review investigates Goldenits et al.'s (2025) empirical comparison of fifteen open small language models (SLMs) for phishing website detection, which aimed to evaluate whether locally hosted models can achieve the same accuracy as proprietary large language models (LLMs), without the prohibitive costs or privacy concerns. The authors test each model with a stratified sample of 1,000 labelled websites from a pool of 10,395 websites and measure the accuracy, precision, recall and F1 score of the results. The best local model, llama3.3:70b, achieves an F1 score of 0.893 and recall of 0.948, which is close to, but still lower than, the F1 scores above 0.95 achieved by the largest proprietary systems (Goldenits et al. 2025). This review restates the three research questions posed in this paper, assesses the evidence provided for each of the questions and situates the evidence in the context of the existing literature on cost-aware deployment (Irugalbandara et al. 2024; Kavya & Sumathi, 2024) and LLM-based phishing detection (Koide et al. 2024). It concludes that, besides the number of parameters, the deployability of an SLM depends on its architecture and on the reliability of its output format, which does not depend only on its classification skill.

## 17. F0097 — Comprehensive Review of Image Compression Techniques (2026)

- **Veredito final:** fora · **regra:** §1.2.1 sem eixo · **objetivo:** —
- **Frase usada:** "Image compression reduces storage requirements and transmission bandwidth while maintaining acceptable image quality."
- **Motivo do agente:** compressão de imagem (dado), não de modelo
- **Abstract:** The exponential growth of digital multimedia, cloud computing, medical imaging, remote sensing, and Internet of Things (IoT) applications has significantly increased the demand for efficient image compression techniques.Image compression reduces storage requirements and transmission bandwidth while maintaining acceptable image quality.Traditional methods such as Discrete Cosine Transform (DCT), Discrete Wavelet Transform (DWT), Huffman coding, and Arithmetic coding have been widely adopted for image compression.Recently, machine learning and deep learning approaches, particularly Convolutional Neural Networks (CNNs) and Autoencoders, have demonstrated superior performance in achieving higher compression ratios with improved reconstruction quality.This review presents a comprehensive analysis of contemporary image compression techniques, including lossless, lossy, hybrid, clustering-based, and deep learning-based methods.The paper also discusses current challenges, and future research directions.The findings indicate that adaptive and AI-driven compression frameworks are becoming increasingly important for next-generation.

## 18. F0572 — Generative Artificial Intelligence & Conversational Agents - Part of the problem or of the solution of HCI dark pattern (2026)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 19. F0472 — Optimizing Emotion Recognition in Indonesian Product Reviews Using LoRA on Transformer (2026)

- **Veredito final:** fora · **regra:** §3.4 primário da área · **objetivo:** —
- **Frase usada:** "This research evaluates the Low-Rank Adaptation (LoRA) technique for optimizing emotion recognition in Indonesian product reviews, with a focus on resource efficiency."
- **Motivo do agente:** estudo primário (não survey) comparando LoRA e fine-tuning completo; tema de eficiência (PEFT) mas não é survey
- **Abstract:** Emotion analysis in product reviews plays a crucial role in Indonesia’s e-commerce landscape, yet training advanced transformer models demands high computational resources, posing a significant constraint for small businesses. This research evaluates the Low-Rank Adaptation (LoRA) technique for optimizing emotion recognition in Indonesian product reviews, with a focus on resource efficiency. Indobert-large-p2, Indobert-base-uncased, and Indobertweet-base-uncased models were trained on the PRDECT-ID dataset, comparing the performance of full fine-tuning and LoRA. Results show LoRA provided competitive performance; on the Indobert-large-p2 model, the F1-score reached 67.81%, surpassing full fine-tuning’s 67.74%, despite training only about 1% of the total parameters. LoRA significantly reduced VRAM consumption by up to 17% and accelerated training duration by up to four minutes. Furthermore, the transformer models fine-tuned in this study, using both LoRA and full fine-tuning, consistently outperformed the results of previous research that employed complex architectures like CNN and BiLSTM, with the highest F1-score reaching 69.72% compared to the previous best of 66.13%. LoRA proves to be a practical and efficient solution for limited computational resources, enabling effective emotion analysis without expensive infrastructure.

## 20. F0333 — Review for "Fermentation process quality prediction using teacher student stacked sparse recurrent autoencoder" (2021)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 21. F0953 — A Survey of Single-Cell Clustering Methods Based on Encoder Types: Embedded, Topological, and Multi-Modal (2026)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 22. F0816 — Privacy-Preserving MLOps with Differential Privacy and AI-Guided Tuning (2026)

- **Veredito final:** fora · **regra:** §3.4 não é survey · **objetivo:** —
- **Frase usada:** "we propose a new Privacy-Preserving MLOps (PP-MLOps) framework that combines AI-aided adaptive tuning of differential privacy in the automated MLOps lifecycle."
- **Motivo do agente:** não é survey; framework de privacidade/MLOps, fora do eixo de custo de implantação — fora da área
- **Abstract:** When machine learning systems transition from being deployed within research environments to enterprise-scale deployment pipelines, protecting data privacy poses an increasing challenge while the model is being trained and/or used. Privacy-preserving techniques will predominantly rely on some form of static differential privacy (DP) constraint, with the challenge often being to balance privacy requirements with model performance, particularly with dynamic workloads. In this paper, we propose a new Privacy-Preserving MLOps (PP-MLOps) framework that combines AI-aided adaptive tuning of differential privacy in the automated MLOps lifecycle. These proposed agent approaches allow for a flexible way to continuously assess privacy risks, regulatory obligations to privacy and confidentiality, and the value of model utility metrics while adapting DP scale of noise, depth of clipping, and privacy budgets (ε, δ) in real-time to achieve optimal model utility. The continuous optimization of DP in CI/CD pipeline operations is actualized through also using reinforcement-learning based controllers to adjust for a range of privacy and performance tradeoff situations in real-time. Evaluation simulations show a 20% improvement in model accuracy retention in regulation compliant DP tuning and operational measures against traditional fixed DP configurations of varying distributions and operational risks. This study can lay the foundation for fully autonomous risk sensing and regulatory compliant MLOps while translating theoretical claims of privacy, application and assurance in a pragmatic framework machine learning deployment at scale.

## 23. F0117 — A comprehensive review of AI-driven plant stress monitoring and embedded sensor technology: Agriculture 5.0 (2025)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 24. F0840 — A Review of Lightweight Object Detection Algorithms for Mobile Augmented Reality (2022)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c) · **objetivo:** —
- **Frase usada:** "A Review of Lightweight Object Detection Algorithms for Mobile Augmented Reality"
- **Motivo do agente:** aplicação específica (c) — detecção de objetos para AR móvel, análoga a compressão para YOLO
- **Abstract:** org

## 25. F0672 — NETWORK-AWARE, PRIVACY-PRESERVING, AND RESOURCE-EFFICIENT FACE RECOGNITION FOR IOT, EDGE, AND CLOUD-BASED AUTHENTICATION: A SYSTEMATIC SURVEY (2026)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 26. F0604 — Lightweight Hybrid Deep Learning Models for Real-Time Deepfake Video Detection: A Comprehensive Survey (2026)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c) · **objetivo:** —
- **Frase usada:** "model compression techniques— including pruning and quantization — essential for resource-constrained deployment"
- **Motivo do agente:** aplicação específica (c): detecção de deepfake
- **Abstract:** The rapid advancement of Generative Artificial Intelligence (GAI) has led to the proliferation of deepfake media, posing significant threats to digital security, privacy, and information integrity. To overcome this challenge, substantial research efforts have been directed toward developing automated detection techniques using deep learning methodologies. This study presents a comprehensive survey of deep learning-based deepfake detection methods, emphasizing lightweight and hybrid architectures designed for real-time deployment. The survey systematically categorizes the landscape of deepfake generation techniques and evaluates state-of-the-art detection frameworks, including: classical CNNs, efficient backbone architectures (MobileNet, EfficientNet), and spatiotemporal models (CNN LSTM/GRU). Furthermore, this study examines model compression techniques— including pruning and quantization — essential for resource-constrained deployment, and provides a structured analysis of benchmark datasets, major detection architecture categories, and persistent research gaps. By critically examining the trade-off between detection accuracy and computational latency, this paper identifies key open challenges and concludes by highlighting a research gap for probabilistically robust, lightweight frameworks, offering a roadmap for future research toward reliable, real-time deepfake forensics in unconstrained environments.

## 27. F0754 — Real-time Pedestrian Detection Using Resource Constrained Embedded Platforms – A Review (2023)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c) · **objetivo:** —
- **Frase usada:** "Real-time Pedestrian Detection Using Resource Constrained Embedded Platforms – A Review"
- **Motivo do agente:** aplicação específica (c): detecção de pedestres com YOLO/CNN, exemplo citado no próprio roteiro.
- **Abstract:** Autonomous Vehicles (AV) are currently limited to the sensors fitted on the vehicle itself to detect pedestrians instead of working collaboratively with the road side units (RSUs). If Resource Constrained Embedded Platforms (RCEPs) were capable of achieving real-time pedestrian detection, they could be deployed at busy traffic intersections to assist AVs. Currently, high-end GPU platforms are required to achieve real-time performance, but their size and cost mean they are not viable for deployment at busy traffic intersections. Therefore, this study performs a comparative analysis as to the ability of RCEPs to achieve real-time pedestrian detection using Convolutional Neural Network (CNN) architectures. Several CNN architectures were trained on a custom pedestrian dataset, with Tiny Yolov4 achieving 62% mean average precision (mAP). When deployed, this analysis indicates that some RCEPs are capable of achieving real-time pedestrian detection, benchmarked at 30FPS, with Tiny YOLOv4 achieving 40.48FPS on the NVIDIA Jetson Nano. The Raspberry Pi 4 paired with the Google Edge TPU also exceeded the real-time threshold, achieving 51.22FPS using MobileNetV2-SSD. Both models were quantized at FP16 and UINT8, which inherently have lower accuracy in favour of faster inferencing. Our analysis evaluates the real-time performance of the selected embedded devices when hosting lightweight CNNs, as well as offering numerous future research directions to improve the pedestrian detection.

## 28. F0032 — A Comprehensive Survey on Vision Transformers, Few-Shot Learning, and Lightweight Clinical Deployment in Next-Generation Artificial Intelligence (2026)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c) · **objetivo:** —
- **Frase usada:** "This survey examines contemporary research trends in skin lesion analysis"
- **Motivo do agente:** aplicação específica (c): imagem médica (lesões de pele)
- **Abstract:** Early identification of malignant and pre-malignant skin lesions plays a decisive role in improving patient survival and treatment effectiveness. Despite notable progress in computeraided diagnosis, reliable skin lesion classification remains difficult due to subtle visual similarities between lesion types, severe class imbalance, and the limited availability of expert-annotated dermatological data. These challenges become even more pronounced in real-world clinical environments, where imaging conditions are often inconsistent and rare lesion categories are underrepresented. Recent advances in artificial intelligence have introduced promising alternatives to conventional convolutionbased models, particularly through the adoption of Vision Transformers, few-shot learning paradigms, and efficiencyoriented system designs. This survey examines contemporary research trends in skin lesion analysis, covering key developments in lesion preprocessing, segmentation-assisted representation learning, attention-based architectures, and data-efficient learning strategies. Each approach is critically discussed in terms of its diagnostic relevance, practical limitations, and suitability for clinical deployment. In addition, a unifying conceptual framework is presented that integrates global contextual understanding with adaptive learning from limited data. This perspective directly addresses persistent challenges related to scalability, interpretability, and generalization across diverse clinical settings. By systematically analyzing current methodologies, performance trade-offs, and open research gaps, this work provides a foundation for the development of next-generation dermatological imaging systems, with particular relevance to real-time screening, mobile platforms, and telemedicine-based healthcare applications.

## 29. F0677 — Internet of UAV Mounted RFID for Various Applications Using LoRa Technology: A Comprehensive Survey (2022)

- **Veredito final:** sem acesso · **regra:**  · **objetivo:** —
- **Frase usada:** ""
- **Motivo do agente:** 
- **Abstract:** (sem abstract)

## 30. F0374 — Teacher-Student Framework for Polyphonic Semi-supervised Sound Event Detection: Survey and Empirical Analysis (2024)

- **Veredito final:** dúvida · **regra:** §1.2.1 (c) · **objetivo:** —
- **Frase usada:** "[título] Teacher-Student Framework for Polyphonic Semi-supervised Sound Event Detection: Survey and Empirical Analysis"
- **Motivo do agente:** survey de aplicação específica (detecção de eventos sonoros) com técnica professor-aluno da área
- **Abstract:** Polyphonic sound event detection refers to the task of automatically identifying sound events occurring simultaneously in an auditory scene. Due to the inherent complexity and variability of real-world auditory scenes, building robust detectors for polyphonic sound event detection poses a significant challenge. The task becomes furthermore challenging without sufficient annotated data to develop sound event detection systems under a supervised learning regime. In this article, we explore the recent developments in polyphonic sound event detection, with a particular emphasis on the application of Teacher-Student techniques within the semi-supervised learning paradigm. Unlike previous works, we have consolidated and organized the fragmented literature on Teacher-Student techniques for polyphonic sound event detection. By examining the latest research, categorizing Teacher-Student approaches, and conducting an empirical study to assess the performance of each approach, this survey offers valuable insights and practical guidance for researchers and practitioners in the field. Our findings highlight the potential benefits of utilizing multiple learners, ensuring consistent predictions, and making thoughtful choices regarding perturbation strategies.

