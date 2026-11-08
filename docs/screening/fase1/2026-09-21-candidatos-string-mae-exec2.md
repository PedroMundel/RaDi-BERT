# Fase 1 — string-mãe, execução 2 — lista de candidatos (21/09/2026)

**Procedência: nível 3 (Claude, por título; arXiv também por resumo). Nenhum item lido. Serve para a Fase 3
(decisão do Pedro linha a linha), nunca para citação.**

**O que é isto.** Saída da Fase 1 (§11 do método): a união do retorno da string-mãe na execução 2 — pool v0
emenda 1 (sem `resource-efficient`/`on-device`, que viraram filha `edge`), piso de citação em teste a 60 —
com uma decisão por obra. Bruto sem filtro em `raw/2026-09-21-semanticscholar-{A2,C2}*.json` e
`raw/2026-09-21-arxiv-string-mae-exec2.json`; citação/venue dos só-arXiv em `raw/2026-09-21-s2-lookup-arxiv-exec2.json`.

**Números.** S2 A2 (Review, >= 60) = 100 · S2 C2 (sem tipo, >= 60) = 103, **A2 ⊂ C2** (a etiqueta *Review* é
redundante) · arXiv = 89, dos quais 37 já estavam no S2 · **155 linhas = 154 obras únicas** (uma duplicada no S2: "Efficient
Large Language Models: A Survey", registro arXiv + registro TMLR — as duas linhas ficam, marcadas). Comparação com
a execução 1 (string com os termos de `edge`, piso 100): 1.721 / 1.734 / 409 — os três termos eram ~94% do retorno,
e baixar o piso para 60 não devolveu volume. Efeito do piso 60 vs. 100 no S2: 38 obras entre 60 e 99 citações.

**Decisões (definição):**
- **entra** — dentro de §1.2 por título **e** passa §3.2 por (a) venue com revisão por pares **ou** (b) >= 60 citações no S2.
- **não entra — sem filtro de qualidade** — dentro de §1.2, mas só arXiv e < 60 citações. Não é descarte (§3.2): espera a
  perna (c), citado por >= 2 surveys registrados, que só pode rodar na Fase 2.
- **borda §1.2** — a relevância não se decide por título: eixo iii (menos rótulo) em tarefa de visão, §1.3 (CNN/GNN/difusão),
  treino vs. implantação, edge de redes vs. edge de modelo, aplicação específica. **Decisão do Pedro na Fase 3.**
- **fora da área** — não reduz custo de implantação por nenhum dos três eixos.
- **não é survey** — paper primário, software ou ferramenta (LightSeq marcado como candidato a ferramenta, §3.1).

| decisão | n |
|---|---|
| entra | 58 |
| não entra — sem filtro de qualidade | 9 |
| borda §1.2 | 36 |
| fora da área | 40 |
| não é survey | 12 |
| **total** | 155 |

**Alerta de calibração (§3.2):** 'entra' com 60+ obras antes de existir divisão. A regra '> 10 por divisão → subir para 200' só se aplica na Fase 3, quando o mapa v1 tiver divisões; até lá a lista fica como está.

## Tabela

Ordem: decisão, depois citação. `(a)` = venue com revisão por pares (S2 `venue` ≠ arXiv.org — heurística, conferir os estranhos). `fonte` = em que base a obra apareceu.

| # | decisão | cit | ano | título | venue | (a) | fonte | nota (nível 3) | id |
|---|---|---|---|---|---|---|---|---|---|
| 1 | entra | 4640 | 2020 | Knowledge Distillation: A Survey | International Journal of Computer Vision | sim | S2+arXiv | KD | 2006.05525 |
| 2 | entra | 1715 | 2021 | A Survey of Quantization Methods for Efficient Neural Network Inference | Low-Power Computer Vision | sim | S2 | quantização | 2103.13630 |
| 3 | entra | 1668 | 2020 | Efficient Transformers: A Survey | ACM Computing Surveys | sim | S2 | atenção eficiente | 2009.06732 |
| 4 | entra | 1019 | 2021 | Sparsity in Deep Learning: Pruning and growth for efficient inference and training in neural networks | Journal of machine learning research | sim | S2 | poda/esparsidade | 2102.00554 |
| 5 | entra | 991 | 2020 | Knowledge Distillation and Student-Teacher Learning for Visual Intelligence: A Review and New Outlooks | IEEE Transactions on Pattern Analysis and Mac | sim | S2+arXiv | KD; foco visão | 2004.05937 |
| 6 | entra | 973 | 2020 | Model Compression and Hardware Acceleration for Neural Networks: A Comprehensive Survey | Proceedings of the IEEE | sim | S2 | compressão + hardware | 10.1109/JPROC.2020.2976475 |
| 7 | entra | 694 | 2021 | Efficient Deep Learning: A Survey on Making Deep Learning Models Smaller, Faster, and Better | ACM Computing Surveys | sim | S2+arXiv | compressão geral | 2106.08962 |
| 8 | entra | 541 | 2020 | A comprehensive survey on model compression and acceleration | Artificial Intelligence Review | sim | S2 | compressão geral | 10.1007/s10462-020-09816-7 |
| 9 | entra | 511 | 2023 | A Survey on Model Compression for Large Language Models | Transactions of the Association for Computati | sim | S2+arXiv | compressão de LLM | 2308.07633 |
| 10 | entra | 378 | 2024 | A Survey on Knowledge Distillation of Large Language Models | arXiv.org | — | S2+arXiv | KD de LLM | 2402.13116 |
| 11 | entra | 355 | 2024 | Mobile Edge Intelligence for Large Language Models: A Contemporary Survey | IEEE Communications Surveys and Tutorials | sim | S2+arXiv | LLM em edge, eixo ii | 2407.18921 |
| 12 | entra | 331 | 2024 | Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding | Annual Meeting of the Association for Computa | sim | S2+arXiv | decodificação especulativa | 2401.07851 |
| 13 | entra | 302 | 2023 | Model Compression for Deep Neural Networks: A Survey | De Computis | sim | S2 | compressão; venue "De Computis" estranho — conferir | 10.3390/computers12030060 |
| 14 | entra | 300 | 2024 | Lightweight Deep Learning for Resource-Constrained Environments: A Survey | ACM Computing Surveys | sim | S2+arXiv | leve/edge | 2404.07236 |
| 15 | entra | 299 | 2024 | A Review on Edge Large Language Models: Design, Execution, and Applications | ACM Computing Surveys | sim | S2 | LLM em edge | 2410.11845 |
| 16 | entra | 276 | 2024 | A comprehensive review of model compression techniques in machine learning | Applied intelligence (Boston) | sim | S2 | compressão geral | 10.1007/s10489-024-05747-w |
| 17 | entra | 270 | 2024 | A Survey on Efficient Inference for Large Language Models | arXiv.org | — | S2+arXiv | inferência de LLM | 2404.14294 |
| 18 | entra | 265 | 2025 | Empowering Edge Intelligence: A Comprehensive Survey on On-Device AI Models | ACM Computing Surveys | sim | S2+arXiv | on-device AI | 2503.06027 |
| 19 | entra | 262 | 2023 | Efficient Large Language Models: A Survey | arXiv.org | — | S2+arXiv | LLM eficiente (duplicado no S2 com #100, TMLR) | 2312.03863 |
| 20 | entra | 242 | 2020 | Compressing Large-Scale Transformer-Based Models: A Case Study on BERT | Transactions of the Association for Computati | sim | S2 | compressão de BERT — encoder-only | 2002.11985 |
| 21 | entra | 226 | 2024 | LLM Inference Unveiled: Survey and Roofline Model Insights | arXiv.org | — | S2+arXiv | roofline de inferência | 2402.16363 |
| 22 | entra | 197 | 2023 | Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems | ACM Computing Surveys | sim | S2+arXiv | serving de LLM | 2312.15234 |
| 23 | entra | 178 | 2023 | Full Stack Optimization of Transformer Inference: a Survey | arXiv.org | — | S2+arXiv | inferência de transformer full-stack | 2302.14017 |
| 24 | entra | 175 | 2020 | Bringing AI To Edge: From Deep Learning's Perspective | Neurocomputing | sim | S2 | DL em edge, eixo ii | 2011.14808 |
| 25 | entra | 170 | 2022 | Efficient Methods for Natural Language Processing: A Survey | Transactions of the Association for Computati | sim | S2+arXiv | NLP eficiente | 2209.00099 |
| 26 | entra | 170 | 2021 | Adaptive Inference through Early-Exit Networks: Design, Challenges and Directions | EMDL@MobiSys | sim | S2 | early exit; workshop EMDL@MobiSys | 2106.05022 |
| 27 | entra | 158 | 2024 | A Survey of Resource-efficient LLM and Multimodal Foundation Models | arXiv.org | — | S2 | LLM/multimodal resource-efficient | 2401.08092 |
| 28 | entra | 153 | 2022 | Enable Deep Learning on Mobile Devices: Methods, Systems, and Applications | ACM Trans. Design Autom. Electr. Syst. | sim | S2 | DL em mobile | 2204.11786 |
| 29 | entra | 131 | 2024 | Lightweight Deep Learning: An Overview | IEEE Consumer Electronics Magazine | sim | S2 | DL leve | 10.1109/MCE.2022.3181759 |
| 30 | entra | 129 | 2021 | Hardware-Aware Neural Architecture Search: Survey and Taxonomy | International Joint Conference on Artificial  | sim | S2 | NAS hardware-aware: técnica de projeto com efeito na implantação | 10.24963/ijcai.2021/592 |
| 31 | entra | 126 | 2020 | An Overview of Neural Network Compression | arXiv.org | — | S2+arXiv | compressão geral | 2006.03669 |
| 32 | entra | 114 | 2024 | Beyond Efficiency: A Systematic Survey of Resource-Efficient Large Language Models | arXiv.org | — | S2+arXiv | LLM resource-efficient | 2401.00625 |
| 33 | entra | 110 | 2021 | A Survey on Green Deep Learning | arXiv.org | — | S2+arXiv | green DL — variante "green NLP" do pool; inclui treino | 2111.05193 |
| 34 | entra | 108 | 2024 | Model Compression and Efficient Inference for Large Language Models: A Survey | arXiv.org | — | S2+arXiv | compressão + inferência de LLM | 2402.09748 |
| 35 | entra | 103 | 2022 | A Survey on Model Compression and Acceleration for Pretrained Language Models | AAAI Conference on Artificial Intelligence | sim | S2+arXiv | compressão de PLM | 2202.07105 |
| 36 | entra | 98 | 2025 | Edge Intelligence: A Review of Deep Neural Network Inference in Resource-Limited Environments | Electronics | sim | S2 | inferência em edge | 10.3390/electronics14122495 |
| 37 | entra | 92 | 2024 | Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective | arXiv.org | — | S2 | aceleração de inferência, hardware | 2410.04466 |
| 38 | entra | 91 | 2024 | A Survey on Transformer Compression | arXiv.org | — | S2+arXiv | compressão de transformer | 2402.05964 |
| 39 | entra | 88 | 2025 | Efficient Reasoning Models: A Survey | Trans. Mach. Learn. Res. | sim | S2+arXiv | raciocínio eficiente — eixo i (menos tokens) | 2504.10903 |
| 40 | entra | 86 | 2025 | A survey of model compression techniques: past, present, and future | Frontiers Robotics AI | sim | S2 | compressão geral | 10.3389/frobt.2025.1518965 |
| 41 | entra | 84 | 2020 | Resource-Efficient Neural Networks for Embedded Systems | arXiv.org | — | S2 | embarcados | 2001.03048 |
| 42 | entra | 78 | 2025 | Vision Transformers on the Edge: A Comprehensive Survey of Model Compression and Acceleration Strategies | Neurocomputing | sim | S2 | ViT em edge: compressão | 2503.02891 |
| 43 | entra | 77 | 2020 | Deep Model Compression and Architecture Optimization for Embedded Systems: A Survey | Journal of Signal Processing Systems | sim | S2 | compressão p/ embarcados | 10.1007/s11265-020-01596-1 |
| 44 | entra | 75 | 2024 | LLM Inference Serving: Survey of Recent Advances and Opportunities | IEEE Conference on High Performance Extreme C | sim | S2+arXiv | serving de LLM | 2407.12391 |
| 45 | entra | 72 | 2024 | A Survey of Small Language Models | arXiv.org | — | S2+arXiv | SLMs | 2410.20011 |
| 46 | entra | 71 | 2025 | Efficient Inference for Large Reasoning Models: A Survey | IEEE Transactions on Pattern Analysis and Mac | sim | S2+arXiv | inferência de modelos de raciocínio | 2503.23077 |
| 47 | entra | 69 | 2024 | A Survey on Inference Optimization Techniques for Mixture of Experts Models | ACM Computing Surveys | sim | S2+arXiv | inferência de MoE | 2412.14219 |
| 48 | entra | 68 | 2020 | Pruning Algorithms to Accelerate Convolutional Neural Networks for Edge Applications: A Survey | arXiv.org | — | S2+arXiv | poda; CNN — §1.3 história, mas poda é técnica da área | 2005.04275 |
| 49 | entra | 62 | 2025 | Knowledge distillation and dataset distillation of large language models: emerging trends, challenges, and future directions | Artificial Intelligence Review | sim | S2 | KD + dataset distillation de LLM | 2504.14772 |
| 50 | entra | 62 | 2024 | Efficient Large Language Models: A Survey | Trans. Mach. Learn. Res. | sim | S2 | = #25 (TMLR) | d13adc935c02fa1ab7a714b6b92433a931679b60 |
| 51 | entra | 60 | 2021 | Data-Free Knowledge Transfer: A Survey | arXiv.org | — | S2+arXiv | KD sem dados; cit = 60, no piso | 2112.15278 |
| 52 | entra | 48 | 2024 | Faster and Lighter LLMs: A Survey on Current Challenges and Way Forward | International Joint Conference on Artificial  | sim | arXiv | LLM mais rápido e leve; IJCAI 2024 survey track | 2402.01799 |
| 53 | entra | 47 | 2021 | Resource-Efficient Deep Learning: A Survey on Model-, Arithmetic-, and Implementation-Level Techniques | ACM Computing Surveys | sim | arXiv | resource-efficient DL 3 níveis; ACM CSUR | 2112.15131 |
| 54 | entra | 29 | 2023 | Efficient Neural Networks for Tiny Machine Learning: A Comprehensive Review | ACM Transactions on Intelligent Systems and T | sim | arXiv | TinyML; ACM TIST | 2311.11883 |
| 55 | entra | 24 | 2024 | Efficient Deep Learning Infrastructures for Embedded Computing Systems: A Comprehensive Survey and Future Envision | ACM Transactions on Embedded Computing System | sim | arXiv | infraestrutura DL p/ embarcados; ACM TECS | 2411.01431 |
| 56 | entra | 22 | 2025 | Optimizing LLMs for Resource-Constrained Environments: A Survey of Model Compression Techniques | Annual International Computer Software and Ap | sim | arXiv | compressão de LLM; COMPSAC 2025 | 2505.02309 |
| 57 | entra | 19 | 2026 | Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization | Annual Meeting of the Association for Computa | sim | arXiv | KV cache; ACL 2026 Findings | 2607.08057 |
| 58 | entra | 18 | 2024 | From Algorithm to Hardware: A Survey on Efficient and Safe Deployment of Deep Neural Networks | IEEE Transactions on Neural Networks and Lear | sim | arXiv | implantação eficiente e segura; IEEE TNNLS | 2405.06038 |
| 59 | não entra — sem filtro de qualidade | 41 | 2023 | The Efficiency Spectrum of Large Language Models: An Algorithmic Survey | arXiv.org | — | arXiv | espectro de eficiência de LLM; arXiv, 41 cit — candidato à perna (c) | 2312.00678 |
| 60 | não entra — sem filtro de qualidade | 22 | 2025 | Speed Always Wins: A Survey on Efficient Architectures for Large Language Models | arXiv.org | — | arXiv | arquiteturas eficientes p/ LLM (atenção linear, MoE...); arXiv, 22 cit — forte candidato à perna (c) | 2508.09834 |
| 61 | não entra — sem filtro de qualidade | 7 | 2024 | Closer Look at Efficient Inference Methods: A Survey of Speculative Decoding | arXiv.org | — | arXiv | decodificação especulativa; arXiv, 7 cit | 2411.13157 |
| 62 | não entra — sem filtro de qualidade | 7 | 2024 | The CAP Principle for LLM Serving: A Survey of Long-Context Large Language Model Serving | arXiv.org | — | arXiv | serving de contexto longo; arXiv, 7 cit | 2405.11299 |
| 63 | não entra — sem filtro de qualidade | 7 | 2022 | Design Automation for Fast, Lightweight, and Effective Deep Learning Models: A Survey | arXiv.org | — | arXiv | design automation p/ modelos leves; arXiv, 7 cit | 2208.10498 |
| 64 | não entra — sem filtro de qualidade | 3 | 2024 | Geometry is All You Need: A Unified Taxonomy of Matrix and Tensor Factorization for Compression of Generative Language Models | arXiv.org | — | arXiv | fatoração matricial/tensorial p/ compressão; arXiv, 3 cit | 2410.03040 |
| 65 | não entra — sem filtro de qualidade | 3 | 2020 | A Selective Survey on Versatile Knowledge Distillation Paradigm for Neural Network Models | arXiv.org | — | arXiv | KD; arXiv, 3 cit | 2011.14554 |
| 66 | não entra — sem filtro de qualidade | 0 | 2026 | From Tensor Buffer to Distributed Memory Hierarchy: A Survey of KV Cache Management for LLM Serving | arXiv.org | — | arXiv | KV cache; arXiv, 0 cit — candidato à perna (c) | 2607.02574 |
| 67 | não entra — sem filtro de qualidade | 0 | 2023 | A Quantitative Review on Language Model Efficiency Research | arXiv.org | — | arXiv | revisão quantitativa de eficiência de LM; arXiv, 0 cit | 2306.01768 |
| 68 | borda §1.2 | 371 | 2020 | An Overview of Deep Semi-Supervised Learning | arXiv.org | — | S2+arXiv | eixo iii — semi-supervisionado; treino com menos rótulo, modelo servido igual | 2006.05278 |
| 69 | borda §1.2 | 235 | 2024 | End-Edge-Cloud Collaborative Computing for Deep Learning: A Comprehensive Survey | IEEE Communications Surveys and Tutorials | sim | S2 | end-edge-cloud: sistemas/redes; eixo ii só se tratar do modelo | 10.1109/COMST.2024.3393230 |
| 70 | borda §1.2 | 165 | 2024 | Understanding LLMs: A Comprehensive Overview from Training to Inference | Neurocomputing | sim | S2+arXiv | visão geral de LLM; tem seção de inferência | 2401.02038 |
| 71 | borda §1.2 | 156 | 2022 | A Survey on Label-Efficient Deep Image Segmentation: Bridging the Gap Between Weak Supervision and Dense Prediction | IEEE Transactions on Pattern Analysis and Mac | sim | S2 | eixo iii — label-efficient, mas segmentação de imagem | 2207.01223 |
| 72 | borda §1.2 | 153 | 2024 | The Ultimate Guide to Fine-Tuning LLMs from Basics to Breakthroughs: An Exhaustive Review of Technologies, Research, Best Practices, Applied Research Challenges and Opportunities | arXiv.org | — | S2+arXiv | fine-tuning geral; PEFT está dentro por §1.2, o resto não | 2408.13296 |
| 73 | borda §1.2 | 153 | 2023 | Review of Lightweight Deep Convolutional Neural Networks | Archives of Computational Methods in Engineer | sim | S2 | CNN leve — §1.3: CNN só em história | 10.1007/s11831-023-10032-z |
| 74 | borda §1.2 | 152 | 2025 | Edge deep learning in computer vision and medical diagnostics: a comprehensive survey | Artificial Intelligence Review | sim | S2+arXiv | edge DL com foco em aplicação (CV/médico) | 2605.06714 |
| 75 | borda §1.2 | 103 | 2023 | Knowledge Distillation on Graphs: A Survey | ACM Computing Surveys | sim | S2+arXiv | KD em grafos — §1.3: GNN fora do escopo de modelos | 2302.00219 |
| 76 | borda §1.2 | 103 | 2025 | Toward Edge General Intelligence With Agentic AI and Agentification: Concepts, Technologies, and Future Directions | IEEE Communications Surveys and Tutorials | sim | S2 | edge + agentes; provável redes | 2508.18725 |
| 77 | borda §1.2 | 80 | 2022 | Compute-Efficient Deep Learning: Algorithmic Trends and Opportunities | Journal of machine learning research | sim | S2 | compute-efficient = treino; §1.2 exclui treino puro | 2210.06640 |
| 78 | borda §1.2 | 74 | 2025 | Vision-Language Models for Edge Networks: A Comprehensive Survey | IEEE Internet of Things Journal | sim | S2+arXiv | VLM em edge networks | 2502.07855 |
| 79 | borda §1.2 | 69 | 2021 | A Survey on the Optimization of Neural Network Accelerators for Micro-AI On-Device Inference | IEEE Journal on Emerging and Selected Topics  | sim | S2 | aceleradores de hardware | 10.1109/jetcas.2021.3129415 |
| 80 | borda §1.2 | 69 | 2022 | AI on the edge: a comprehensive review | Artificial Intelligence Review | sim | S2 | edge AI amplo | 10.1007/s10462-022-10141-4 |
| 81 | borda §1.2 | 66 | 2023 | A survey of model compression strategies for object detection | Multimedia tools and applications | sim | S2 | compressão p/ detecção de objetos (CNN/aplicação) | 10.1007/s11042-023-17192-x |
| 82 | borda §1.2 | 49 | 2023 | Computation-efficient Deep Learning for Computer Vision: A Survey | Cybernetics and Intelligence | sim | arXiv | DL eficiente p/ visão | 2308.13998 |
| 83 | borda §1.2 | 47 | 2022 | Enabling All In-Edge Deep Learning: A Literature Review | IEEE Access | sim | arXiv | in-edge DL, treino+inferência | 2204.03326 |
| 84 | borda §1.2 | 41 | 2022 | Dimensionality Reduced Training by Pruning and Freezing Parts of a Deep Neural Network, a Survey | Artificial Intelligence Review | sim | arXiv | poda/congelamento p/ treino | 2205.08099 |
| 85 | borda §1.2 | 39 | 2025 | Cognitive Edge Computing: A Comprehensive Survey on Optimizing Large Models and AI Agents for Pervasive Deployment |  | — | arXiv | edge cognitivo: modelos grandes + agentes; sem venue, 39 cit | 2501.03265 |
| 86 | borda §1.2 | 35 | 2023 | Towards energy-efficient Deep Learning: An overview of energy-efficient approaches along the Deep Learning Lifecycle | arXiv.org | — | arXiv | energia ao longo do pipeline (treino+inferência) | 2303.01980 |
| 87 | borda §1.2 | 34 | 2024 | Knowledge Distillation in Federated Learning: a Survey on Long Lasting Challenges and New Solutions | International Journal of Intelligent Systems | sim | arXiv | KD em federado | 2406.10861 |
| 88 | borda §1.2 | 33 | 2023 | Model Compression Methods for YOLOv5: A Review | arXiv.org | — | arXiv | compressão de YOLOv5 (CNN/aplicação) | 2307.11904 |
| 89 | borda §1.2 | 32 | 2025 | A Survey on Efficient Vision-Language-Action Models | IEEE Transactions on Pattern Analysis and Mac | sim | arXiv | VLA eficientes (robótica) | 2510.24795 |
| 90 | borda §1.2 | 27 | 2023 | A Comprehensive Review and a Taxonomy of Edge Machine Learning: Requirements, Paradigms, and Techniques | Applied Informatics | sim | arXiv | edge ML amplo (paradigmas incl. federado) | 2302.08571 |
| 91 | borda §1.2 | 26 | 2024 | A survey on FPGA-based accelerator for ML models | arXiv.org | — | arXiv | aceleradores FPGA; arXiv, 26 | 2412.15666 |
| 92 | borda §1.2 | 26 | 2024 | Model Compression Techniques in Biometrics Applications: A Survey | Information Fusion | sim | arXiv | compressão p/ biometria; Information Fusion | 2401.10139 |
| 93 | borda §1.2 | 26 | 2023 | Data efficient deep learning for medical image analysis: A survey | arXiv.org | — | arXiv | eixo iii em imagem médica | 2310.06557 |
| 94 | borda §1.2 | 18 | 2025 | A Survey on Cache Methods in Diffusion Models: Toward Efficient Multi-Modal Generation | arXiv.org | — | arXiv | cache em difusão — §1.3: difusão fora, DiT é transformer | 2510.19755 |
| 95 | borda §1.2 | 18 | 2025 | Survey of Quantization Techniques for On-Device Vision-based Crack Detection | International Instrumentation and Measurement | sim | arXiv | quantização p/ aplicação (trincas) | 2502.02269 |
| 96 | borda §1.2 | 16 | 2024 | Deploying Foundation Model Powered Agent Services: A Survey | IEEE Communications Surveys and Tutorials | sim | arXiv | serving de agentes; COMST | 2412.13437 |
| 97 | borda §1.2 | 14 | 2023 | Efficient Transformer Knowledge Distillation: A Performance Review | Conference on Empirical Methods in Natural La | sim | arXiv | tipo: estudo empírico de KD, não survey; EMNLP 2023 | 2311.13657 |
| 98 | borda §1.2 | 11 | 2023 | A Survey of Serverless Machine Learning Model Inference | arXiv.org | — | arXiv | inferência serverless (infra) | 2311.13587 |
| 99 | borda §1.2 | 9 | 2026 | Embodied Foundation Models at the Edge: A Survey of Deployment Constraints and Mitigation Strategies | arXiv.org | — | arXiv | modelos embodied em edge | 2603.16952 |
| 100 | borda §1.2 | 6 | 2025 | Onboard Optimization and Learning: A Survey | IEEE Access | sim | arXiv | onboard (aeroespacial?) | 2505.08793 |
| 101 | borda §1.2 | 6 | 2023 | Relationship between Model Compression and Adversarial Robustness: A Review of Current Evidence | IEEE Symposium Series on Computational Intell | sim | arXiv | compressão × robustez adversarial | 2311.15782 |
| 102 | borda §1.2 | 0 | 2026 | Efficient Deep Learning for Biometrics: Overview, Challenges and Trends in Ear of Frugal AI | Swiss Conference on Data Science | sim | arXiv | DL eficiente p/ biometria (aplicação) | 2602.08809 |
| 103 | borda §1.2 | 0 | 2024 | Acceleration Algorithms in GNNs: A Survey | arXiv.org | — | arXiv | aceleração de GNN — §1.3 | 2405.04114 |
| 104 | fora da área | 3919 | 2020 | A Survey on Vision Transformer | IEEE Transactions on Pattern Analysis and Mac | sim | S2+arXiv | arquitetura ViT, sem eficiência; bateu por menção no resumo | 2012.12556 |
| 105 | fora da área | 473 | 2021 | A survey on adversarial attacks and defences | CAAI Transactions on Intelligence Technology | sim | S2 | adversarial | 10.1049/CIT2.12028 |
| 106 | fora da área | 211 | 2023 | Diffusion Models for Image Restoration and Enhancement: A Comprehensive Survey | International Journal of Computer Vision | sim | S2 | difusão p/ restauração | 2308.09388 |
| 107 | fora da área | 205 | 2023 | A brief review of hypernetworks in deep learning | Artificial Intelligence Review | sim | S2+arXiv | hypernetworks | 2306.06955 |
| 108 | fora da área | 182 | 2020 | A Survey on Contextual Embeddings | arXiv.org | — | S2+arXiv | embeddings contextuais; só uma seção de compressão | 2003.07278 |
| 109 | fora da área | 175 | 2021 | Boost Precision Agriculture with Unmanned Aerial Vehicle Remote Sensing and Edge Intelligence: A Survey | Remote Sensing | sim | S2 | agricultura | 10.3390/rs13214387 |
| 110 | fora da área | 175 | 2021 | Toward Resource-Efficient Federated Learning in Mobile Edge Computing | IEEE Network | sim | S2 | federado | 10.1109/MNET.011.2000295 |
| 111 | fora da área | 170 | 2022 | Research Progress on Memristor: From Synapses to Computing Systems | IEEE Transactions on Circuits and Systems Par | sim | S2 | memristor | 10.1109/tcsi.2022.3159153 |
| 112 | fora da área | 168 | 2022 | State of the art: a review of sentiment analysis based on sequential transfer learning | Artificial Intelligence Review | sim | S2 | sentimento | 10.1007/s10462-022-10183-8 |
| 113 | fora da área | 159 | 2020 | Database Meets Artificial Intelligence: A Survey | IEEE Transactions on Knowledge and Data Engin | sim | S2 | banco de dados | 10.1109/tkde.2020.2994641 |
| 114 | fora da área | 138 | 2025 | Federated Learning for Cloud and Edge Security: A Systematic Review of Challenges and AI Opportunities | Electronics | sim | S2 | federado/segurança | 10.3390/electronics14051019 |
| 115 | fora da área | 119 | 2022 | Neuromorphic computing hardware and neural architectures for robotics | Sci. Robotics | sim | S2 | neuromórfico | 10.1126/scirobotics.abl8419 |
| 116 | fora da área | 116 | 2021 | AI Meets Database: AI4DB and DB4AI | SIGMOD Conference | sim | S2 | banco de dados | 10.1145/3448016.3457542 |
| 117 | fora da área | 108 | 2022 | A Review of the State of the Art and Future Challenges of Deep Learning-Based Beamforming | IEEE Access | sim | S2 | beamforming | 10.1109/access.2022.3195299 |
| 118 | fora da área | 93 | 2025 | Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges |  | — | S2 | VLA/robótica | 2505.04769 |
| 119 | fora da área | 90 | 2024 | Demystifying Chains, Trees, and Graphs of Thoughts | IEEE Transactions on Pattern Analysis and Mac | sim | S2 | prompting (CoT/ToT/GoT) | 2401.14295 |
| 120 | fora da área | 87 | 2021 | A survey of deep learning approaches for WiFi-based indoor positioning | Journal of Information and Telecommunication | sim | S2 | WiFi | 10.1080/24751839.2021.1975425 |
| 121 | fora da área | 86 | 2024 | The Application of Deep Learning in the Whole Potato Production Chain: A Comprehensive Review | Agriculture | sim | S2 | batata | 10.3390/agriculture14081225 |
| 122 | fora da área | 81 | 2023 | A Survey on Deep-Learning-Based Real-Time SAR Ship Detection | IEEE Journal of Selected Topics in Applied Ea | sim | S2 | SAR | 10.1109/JSTARS.2023.3244616 |
| 123 | fora da área | 79 | 2020 | On Making Valid Inferences by Integrating Data from Surveys and Other Sources | Sankhya B | sim | S2 | estatística | 10.1007/s13571-020-00227-w |
| 124 | fora da área | 78 | 2020 | Deep Randomized Neural Networks | INNSBDDL | sim | S2 | redes randomizadas | 2002.12287 |
| 125 | fora da área | 78 | 2020 | Statistical data integration in survey sampling: a review | Japanese Journal of Statistics and Data Scien | sim | S2 | estatística | 2001.03259 |
| 126 | fora da área | 73 | 2024 | Transformer technology in molecular science | Wiley Interdisciplinary Reviews. Computationa | sim | S2 | química | 10.1002/wcms.1725 |
| 127 | fora da área | 72 | 2024 | Advances and Open Challenges in Federated Foundation Models | IEEE Communications Surveys and Tutorials | sim | S2 | federado | 2404.15381 |
| 128 | fora da área | 69 | 2020 | Compute-in-Memory with Emerging Nonvolatile-Memories: Challenges and Prospects | IEEE Custom Integrated Circuits Conference | sim | S2 | compute-in-memory: hardware sem modelo | 10.1109/CICC48029.2020.9075887 |
| 129 | fora da área | 67 | 2024 | Document Parsing Unveiled: Techniques, Challenges, and Prospects for Structured Information Extraction |  | — | S2 | parsing de documento | 2410.21169 |
| 130 | fora da área | 66 | 2020 | Convolutional Neural Network-Based Methods for Eye Gaze Estimation: A Survey | IEEE Access | sim | S2 | gaze | 10.1109/ACCESS.2020.3013540 |
| 131 | fora da área | 17 | 2025 | A Survey on Efficient Large Language Model Training: From Data-centric Perspectives | Annual Meeting of the Association for Computa | sim | arXiv | treino eficiente (dados) — §1.2 exclui treino puro | 2510.25817 |
| 132 | fora da área | 15 | 2024 | Decoding the Diversity: A Review of the Indic AI Research Landscape | arXiv.org | — | arXiv | Indic | 2406.09559 |
| 133 | fora da área | 14 | 2025 | From Replication to Redesign: Exploring Pairwise Comparisons for LLM-Based Peer Review | Neural Information Processing Systems | sim | arXiv | peer review por LLM | 2506.11343 |
| 134 | fora da área | 14 | 2025 | DeepSeek in Healthcare: A Survey of Capabilities, Risks, and Clinical Applications of Open-Source Large Language Models | arXiv.org | — | arXiv | saúde | 2506.01257 |
| 135 | fora da área | 13 | 2025 | Towards Adapting Federated & Quantum Machine Learning for Network Intrusion Detection: A Survey | arXiv.org | — | arXiv | IDS | 2509.21389 |
| 136 | fora da área | 13 | 2024 | ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models Performance & Efficiency on a Specific Domain | ENLSP | sim | arXiv | benchmark químico | 2412.00532 |
| 137 | fora da área | 7 | 2025 | How to Upscale Neural Networks with Scaling Law? A Survey and Practical Guidelines | Trans. Mach. Learn. Res. | sim | arXiv | leis de escala p/ crescer modelo | 2502.12051 |
| 138 | fora da área | 7 | 2022 | Graph Neural Networks Intersect Probabilistic Graphical Models: A Survey | arXiv.org | — | arXiv | GNN+PGM | 2206.06089 |
| 139 | fora da área | 4 | 2023 | Generalized Uncertainty of Deep Neural Networks: Taxonomy and Applications | arXiv.org | — | arXiv | incerteza — "confiança" não é eixo de §1.2 | 2302.01440 |
| 140 | fora da área | 2 | 2025 | INSIGHT: A Survey of In-Network Systems for Intelligent, High-Efficiency AI and Topology Optimization | arXiv.org | — | arXiv | in-network | 2505.24269 |
| 141 | fora da área | 1 | 2025 | A Survey of TinyML Applications in Beekeeping for Hive Monitoring and Management | arXiv.org | — | arXiv | apicultura | 2509.08822 |
| 142 | fora da área | 0 | 2026 | Trustworthy Machine Learning through the Lens of Combinatorial Optimization: Survey and Research Perspectives | arXiv.org | — | arXiv | ML confiável | 2607.07762 |
| 143 | fora da área | 0 | 2026 | Publishing FAIR and Machine-actionable Reviews in Materials Science: The Case for Symbolic Knowledge in Neuro-symbolic Artificial Intelligence | Journal of Vacuum Science &amp; Technology A | sim | arXiv | materiais | 2601.05051 |
| 144 | não é survey | 588 | 2023 | DeePMD-kit v2: A software package for deep potential models | Journal of Chemical Physics | sim | S2 | software de química | 2304.09409 |
| 145 | não é survey | 298 | 2024 | SparseDrive: End-to-End Autonomous Driving via Sparse Scene Representation | IEEE International Conference on Robotics and | sim | S2 | direção autônoma | 2405.19620 |
| 146 | não é survey | 269 | 2020 | Towards an effective and efficient deep learning model for COVID-19 patterns detection in X-ray images | Research on Biomedical Engineering | sim | S2 | COVID | 2004.05717 |
| 147 | não é survey | 241 | 2025 | Seedream 4.0: Toward Next-generation Multimodal Image Generation | arXiv.org | — | S2 | geração de imagem | 2509.20427 |
| 148 | não é survey | 197 | 2021 | Efficient Transformer for Remote Sensing Image Segmentation | Remote Sensing | sim | S2 | sensoriamento remoto | 10.3390/rs13183585 |
| 149 | não é survey | 119 | 2024 | User-LLM: Efficient LLM Contextualization with User Embeddings | The Web Conference | sim | S2 | paper primário | 2402.13598 |
| 150 | não é survey | 105 | 2020 | Xilinx Vitis Unified Software Platform | Symposium on Field Programmable Gate Arrays | sim | S2 | ferramenta FPGA, fora | 10.1145/3373087.3375887 |
| 151 | não é survey | 73 | 2021 | LightSeq: A High Performance Inference Library for Transformers | North American Chapter of the Association for | sim | S2 | LightSeq: paper de sistema — candidato a ferramenta (§3.1) | 10.18653/v1/2021.naacl-industry.15 |
| 152 | não é survey | 68 | 2021 | Bioacoustic classification of avian calls from raw sound waveforms with an open-source deep learning architecture | Scientific Reports | sim | S2 | bioacústica | 10.1038/s41598-021-95076-6 |
| 153 | não é survey | 61 | 2020 | VecQ: Minimal Loss DNN Model Compression With Vectorized Weight Quantization | IEEE transactions on computers | sim | S2 | VecQ: paper primário de quantização | 2005.08501 |
| 154 | não é survey | 61 | 2023 | Multi-target Knowledge Distillation via Student Self-reflection | International Journal of Computer Vision | sim | S2 | paper primário de KD | 10.1007/s11263-023-01792-z |
| 155 | não é survey | 3 | 2025 | Re4: Scientific Computing Agent with Rewriting, Resolution, Review and Revision | arXiv.org | — | arXiv | agente | 2508.20729 |
