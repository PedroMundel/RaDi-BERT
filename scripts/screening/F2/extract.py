#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de frases para agente 2 (screening F2).
Copia exata do título e abstract conforme roteiro.
"""

import json
import sys

# Ler arquivos
with open("a1/lote01-entrada.json", "r", encoding="utf-8") as f:
    obras = json.load(f)

with open("a1/lote01-saida.json", "r", encoding="utf-8") as f:
    decisoes = json.load(f)

# Mapear decisões
decisoes_map = {d["id"]: d["decisao"] for d in decisoes}

# Saída
saida = []

# Processar cada obra
for obra in obras:
    obra_id = obra["id"]
    decisao = decisoes_map.get(obra_id)

    # Pular se é claramente fora
    if decisao == "claramente fora":
        continue

    registro = {
        "id": obra_id,
        "acesso": obra["acesso"],
        "frases": []
    }

    # Se é sem acesso, frases vazias
    if decisao == "sem acesso" or obra["acesso"] == "sem acesso":
        saida.append(registro)
        continue

    # Se passa, extrair frases
    titulo = obra.get("title", "")
    abstract = obra.get("abstract", "")
    texto_completo = titulo + " " + abstract

    # Extração manual por obra (usar dados do abstract/título)
    frases = []

    # Estrutura: campo nome_padrao -> buscar trecho exato no título/abstract
    # Aqui vai a lógica específica por obra

    # F0001 - Diffusion Model Quantization
    if obra_id == "F0001":
        frases = [
            {"item": "tipo", "texto": "This survey offers a thorough review of the latest advancements in diffusion model quantization"},
            {"item": "objeto", "texto": "model quantization has emerged as a pivotal technique for both compression and acceleration"},
            {"item": "modelos", "texto": "U-Net architectures and Diffusion Transformers (DiT)"},
            {"item": "tecnica", "texto": "quantization errors, elucidating these impacts through both visual analysis and trajectory examination"},
            {"item": "pratica", "texto": "The list of related papers, corresponding codes, pre-trained models and comparison results are publicly available at the survey project homepage https://github.com/TaylorJocelyn/Diffusion-Model-Quantization."},
        ]

    # F0002 - Speech Recognition
    elif obra_id == "F0002":
        frases = [
            {"item": "tipo", "texto": "In this paper, we review various end-to-end automatic speech recognition algorithms and their optimization techniques for on-device applications"},
            {"item": "objeto", "texto": "we review such end-to-end speech recognition models"},
            {"item": "modelos", "texto": "speech recognition systems based on Connectionist Temporal Classification (CTC), Recurrent Neural Network Transducer (RNN-T), Attention-based Encoder-Decoder models (AED), Monotonic Chunk-wise Attention (MoChA), transformer-based speech recognition systems"},
            {"item": "tecnica", "texto": "These fully neural network-based systems require much smaller memory footprints compared to conventional algorithms"},
        ]

    # F0003 - LLM Inference Optimizations
    elif obra_id == "F0003":
        frases = [
            {"item": "tipo", "texto": "This literature review focuses on various techniques for reducing resource requirements and compressing large language models"},
            {"item": "objeto", "texto": "focusing on various techniques for reducing resource requirements and compressing large language models"},
            {"item": "tecnica", "texto": "quantization, pruning, knowledge distillation, and architectural optimizations"},
        ]

    # F0008 - Trends of Modern Processors for AI
    elif obra_id == "F0008":
        frases = [
            {"item": "tipo", "texto": "the technological challenges and trends in the latest AI accelerators are reviewed"},
            {"item": "objeto", "texto": "the technological challenges and trends in the latest AI accelerators"},
            {"item": "tecnica", "texto": "low-power hardware accelerators are essential for feasible implementation"},
        ]

    # F0009 - Federated Learning and IoT Security
    elif obra_id == "F0009":
        frases = [
            {"item": "tipo", "texto": "In this era of ubiquitous connectivity and smart systems, combining Federated Learning (FL) and the Internet of Things (IoT) symbolizes a revolutionary trend in edge-based intelligence"},
            {"item": "objeto", "texto": "FL offers an exclusive decentralized feature for machine learning wherein the data resides on IoT devices"},
            {"item": "tecnica", "texto": "Several security mechanisms have evolved with different approaches"},
        ]

    # F0010 - QoS in IoT Healthcare
    elif obra_id == "F0010":
        frases = [
            {"item": "tipo", "texto": "Our focus is on the individual devices present at different levels of the smart healthcare infrastructure and the QoS requirements of the healthcare system as a whole"},
            {"item": "objeto", "texto": "Quick responses among healthcare organizations are important in general, but in an emergency, significant latency at different stakeholders might result in disastrous situations"},
            {"item": "tecnica", "texto": "edge computing and artificial intelligence (AI) can deal with such problems"},
        ]

    # F0011 - Smart City Automation LoRa
    elif obra_id == "F0011":
        frases = [
            {"item": "tipo", "texto": "The control of street lights in the city can be controlled as a whole in one place with the help of and also it is assisted by artificial intelligence for its automation"},
            {"item": "objeto", "texto": "To guarantee the cleanliness and quality of the air and reduce pollution, smart cities have installed air quality monitoring systems"},
            {"item": "pratica", "texto": "The technology measures the quality of the air and tests for purity"},
        ]

    # F0013 - Structural Health Monitoring with IoT
    elif obra_id == "F0013":
        frases = [
            {"item": "tipo", "texto": "Structural Health Monitoring (SHM) is increasingly embraced thanks to advancements in the Internet of Things (IoT) and Artificial Intelligence (AI) being combined and infused"},
            {"item": "objeto", "texto": "remote and continuous monitoring solution is still required"},
            {"item": "pratica", "texto": "Through case studies, the practical applications of SHM are illustrated, emphasizing its effectiveness in real-world scenarios"},
        ]

    # F0016 - Deep Tensor Decomposition
    elif obra_id == "F0016":
        frases = [
            {"item": "tipo", "texto": "In this survey, we provide a comprehensive review of deep TD models"},
            {"item": "objeto", "texto": "a new paradigm, deep tensor decomposition (deep TD) has recently emerged inspired by the success of deep learning"},
            {"item": "modelos", "texto": "deep neural networks (DNNs)"},
            {"item": "tecnica", "texto": "Deep TD techniques can be mainly divided into two categories: linear and nonlinear deep TD"},
        ]

    # F0018 - CultureSynth
    elif obra_id == "F0018":
        frases = [
            {"item": "tipo", "texto": "we introduce CultureSynth, a novel framework comprising (1) a comprehensive hierarchical multilingual cultural taxonomy"},
            {"item": "objeto", "texto": "Cultural competence, defined as the ability to understand and adapt to multicultural contexts, is increasingly vital for large language models (LLMs)"},
            {"item": "modelos", "texto": "large language models (LLMs)"},
            {"item": "pratica", "texto": "The CultureSynth-7 synthetic benchmark contains 19,360 entries and 4,149 manually verified entries across 7 languages"},
        ]

    # F0019 - Knowledge Distillation in Federated Learning
    elif obra_id == "F0019":
        frases = [
            {"item": "tipo", "texto": "In this paper, we investigate the works that KD applies to FEL"},
            {"item": "objeto", "texto": "Knowledge Distillation (KD) has been leveraged as an important technique to tackle the above challenges in FEL"},
            {"item": "tecnica", "texto": "Knowledge Distillation (KD)"},
        ]

    # F0020 - ECG Classification
    elif obra_id == "F0020":
        frases = [
            {"item": "tipo", "texto": "This review systematically analyzes ECG classification research published between 2017 and 2024"},
            {"item": "objeto", "texto": "The classification of electrocardiogram (ECG) signals is essential for early arrhythmia detection"},
            {"item": "tecnica", "texto": "hardware constraints crucial for deployment in pacemakers, Holter monitors, and wearable ECG patches"},
        ]

    # F0021 - Pruning in Model Compression
    elif obra_id == "F0021":
        frases = [
            {"item": "tipo", "texto": "This paper provides a comprehensive overview of pruning as a model compression strategy"},
            {"item": "objeto", "texto": "Model compression techniques aim to reduce model size and computational cost without significantly compromising accuracy"},
            {"item": "tecnica", "texto": "pruning has emerged as one of the most effective methods"},
        ]

    # F0022 - Deepfake Audio Detection
    elif obra_id == "F0022":
        frases = [
            {"item": "tipo", "texto": "This survey presents a comprehensive overview of deepfake audio generation and detection techniques"},
            {"item": "objeto", "texto": "Deepfake audio generation systems are creating extremely realistic human voices"},
            {"item": "modelos", "texto": "CNN-based and transformer-based"},
            {"item": "pratica", "texto": "commonly used datasets and evaluation metrics like accuracy, AUROC and EER"},
        ]

    # F0023 - Evolution of NLP
    elif obra_id == "F0023":
        frases = [
            {"item": "tipo", "texto": "An overview of the significant turning points and patterns that have influenced the development of NLP is given in this study"},
            {"item": "objeto", "texto": "Natural Language Processing (NLP) has evolved dramatically, moving from early rule based systems to the current era dominated by advanced deep learning models"},
            {"item": "modelos", "texto": "Transformer and other models"},
        ]

    # F0024 - Customer Review Analysis
    elif obra_id == "F0024":
        frases = [
            {"item": "tipo", "texto": "optimized recommendation system is developed for analyzing customer reviews"},
            {"item": "objeto", "texto": "Customer reviews and ratings are more helpful to the new customer to purchase the product"},
            {"item": "modelos", "texto": "batch normalized capsule networks (NCN)"},
        ]

    # F0025 - Face Mask Detection Lightweight
    elif obra_id == "F0025":
        frases = [
            {"item": "tipo", "texto": "This review presents an architecture-centered synthesis of face mask detection systems"},
            {"item": "objeto", "texto": "Automated face mask detection remains an important component of hygiene compliance, occupational safety, and public health monitoring"},
            {"item": "modelos", "texto": "MobileNet family, and hybrid frameworks"},
            {"item": "tecnica", "texto": "model compression, and the extension of mask detection toward broader Personal Protective Equipment (PPE) compliance monitoring"},
        ]

    # F0026 - Cervical Cancer Detection
    elif obra_id == "F0026":
        frases = [
            {"item": "tipo", "texto": "This study presents a comprehensive survey of methods and architectures for automatic cervical cancer detection"},
            {"item": "objeto", "texto": "deep learning (DL) techniques have emerged as powerful tools for automating cervical cancer detection and segmentation from medical images"},
            {"item": "modelos", "texto": "convolutional neural networks (CNNs), segmentation models such as U-Net and nnU-Net"},
            {"item": "pratica", "texto": "deep learning models achieve high classification accuracy (above 95%) and segmentation performance (Dice scores up to 0.90)"},
        ]

    # F0028 - UAV 3D Machine Vision
    elif obra_id == "F0028":
        frases = [
            {"item": "objeto", "texto": "the application of UAV in urban planning and construction is mainly manifested in urban planning survey, urban illegal building supervision and environmental monitoring"},
            {"item": "tecnica", "texto": "embedded technology can be managed by multiple users, you can run multiple processes program"},
        ]

    # F0029 - Face Recognition Lightweight
    elif obra_id == "F0029":
        frases = [
            {"item": "tipo", "texto": "This paper first introduces the recognition methods of face recognition"},
            {"item": "objeto", "texto": "reducing the computing and storage overhead of deep neural networks is a very important and challenging problem in the field of face recognition"},
            {"item": "modelos", "texto": "lightweight neural networks"},
        ]

    # F0030 - Agentic AI Review
    elif obra_id == "F0030":
        frases = [
            {"item": "tipo", "texto": "a comprehensive review can provide researchers and practitioners with valuable insights into the current state and future research scopes of agentic AI"},
            {"item": "objeto", "texto": "Agentic AI is gaining new insights and advancements in the field of Artificial Intelligence"},
        ]

    # F0031 - Lightweight Object Detection
    elif obra_id == "F0031":
        frases = [
            {"item": "tipo", "texto": "This paper reviews research from 2020 to 2025 on lightweight object detection"},
            {"item": "objeto", "texto": "object detection becomes vital in sectors such as agriculture, industry, and healthcare"},
            {"item": "modelos", "texto": "efficient architecture and model compression techniques"},
        ]

    # F0032 - Vision Transformers and Skin Lesion
    elif obra_id == "F0032":
        frases = [
            {"item": "tipo", "texto": "This survey examines contemporary research trends in skin lesion analysis"},
            {"item": "objeto", "texto": "Early identification of malignant and pre-malignant skin lesions plays a decisive role in improving patient survival and treatment effectiveness"},
            {"item": "modelos", "texto": "Vision Transformers, few-shot learning paradigms, and efficiency-oriented system designs"},
        ]

    # F0033 - WSN Distributed State Estimation
    elif obra_id == "F0033":
        frases = [
            {"item": "tipo", "texto": "This paper provides a survey of the trending resource-efficient and secure techniques currently used with distributed estimation algorithms"},
            {"item": "objeto", "texto": "resource-efficient distributed state estimation"},
            {"item": "tecnica", "texto": "protocol-based scheduling, static event-triggered scheduling, dynamic event-triggered scheduling and stochastic event-triggered scheduling"},
        ]

    # F0036 - Lane and Obstacle Detection Automotive
    elif obra_id == "F0036":
        frases = [
            {"item": "tipo", "texto": "This paper reviews recent advances AI-driven lane and obstacle detection methods"},
            {"item": "objeto", "texto": "Autonomous driving and Advanced Driver Assistance Systems (ADAS) rely heavily on accurate lane detection, vehicle recognition, and obstacle avoidance"},
            {"item": "modelos", "texto": "convolutional neural networks (CNNs), attention-based architectures, and YOLO-based frameworks"},
            {"item": "tecnica", "texto": "deploying computationally intensive models on automotive-grade processors remains a key challenge"},
        ]

    # F0038 - Human Pose Estimation Lightweight
    elif obra_id == "F0038":
        frases = [
            {"item": "tipo", "texto": "This paper provides a comprehensive review of lightweight human pose estimation methods"},
            {"item": "objeto", "texto": "The integration of human pose estimation in mobile and embedded systems has been limited by computational constraints"},
        ]

    # F0039 - On-Device Recommender Systems
    elif obra_id == "F0039":
        frases = [
            {"item": "tipo", "texto": "To bridge this gap, we aim to provide a comprehensive survey of DeviceRSs"},
            {"item": "objeto", "texto": "there has been a shift of focus from CloudRSs to on-device recommender systems (DeviceRSs)"},
            {"item": "tecnica", "texto": "deployment and inference of DeviceRSs, exploring how large recommendation models can be compressed"},
        ]

    # F0040 - Air Quality Prediction with Quantization
    elif obra_id == "F0040":
        frases = [
            {"item": "tipo", "texto": "This review synthesizes recent developments in air quality prediction using embedded Machine Learning (ML) and Deep Learning (DL) models with emphasis on 8 bit quantization"},
            {"item": "objeto", "texto": "Air pollution is a major global environmental and health concern, necessitating accurate and timely forecasting of pollutant levels"},
            {"item": "modelos", "texto": "CNN BiGRU model"},
            {"item": "tecnica", "texto": "multi task learning frameworks, spatial temporal modeling over multiple pollutants, and transformer based approaches"},
        ]

    # Atribuir frases ao registro se não estiverem vazias
    registro["frases"] = frases
    saida.append(registro)

# Escrever saída
with open("a2/lote01-saida.json", "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)

print(f"Saída gerada: {len(saida)} registros")
print(json.dumps(saida[:2], ensure_ascii=False, indent=2))
