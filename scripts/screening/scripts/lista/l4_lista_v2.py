"""Lista rápida, etapa 4 (27/09): lista v2 = regras da etapa 3 + ajustes declarados da revisão do Claude.
Cada item diz de onde veio: 'regra' (saiu da etapa 3 como estava) ou 'ajuste: <motivo>'. Votos lidos das candidatas.
Grava lista-v2.csv."""
import csv, os, re
OUT = os.path.join(r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial", "Screening", "fase1", "lista-rapida")
C = list(csv.DictReader(open(os.path.join(OUT, "candidatas-marcadas.csv"), encoding="utf-8-sig")))
J = list(csv.DictReader(open(os.path.join(OUT, "juri.csv"), encoding="utf-8-sig")))
def acha(rx):
    cs = [c for c in C if re.search(rx, c["title"], re.I)]
    return max(cs, key=lambda c: int(c["votos"])) if cs else None
L = [  # (bloco, divisão, regex do título, origem)
    ("A mapas", "hardware", r"^Efficient Processing of Deep Neural Networks: A Tutorial", "ajuste: a regra não achou divisão pelo título; é o survey mais votado de hardware (14 + 25 da reserva)"),
    ("A mapas", "compressão (geral)", r"^Model Compression and Hardware Acceleration for Neural Networks", "regra"),
    ("A mapas", "destilação", r"^Knowledge Distillation: A Survey", "regra"),
    ("A mapas", "quantização", r"^A Survey of Quantization Methods for Efficient", "regra"),
    ("A mapas", "poda e esparsidade", r"^Pruning and Quantization for Deep Neural Network Acceleration: A Survey", "ajuste: a regra pôs 'Sparse Expert Models' (é MoE) como mapa de poda"),
    ("A mapas", "computação condicional", r"^A Review of Sparse Expert Models", "ajuste: movido de poda para computação condicional; substitui o survey de early exiting (mesmos 4 votos, MoE pesa mais na era LLM)"),
    ("A mapas", "atenção e sequência eficientes", r"^Efficient Transformers: A Survey", "regra"),
    ("A mapas", "arquitetura eficiente e NAS", r"^A Comprehensive Survey of Neural Architecture Search", "regra"),
    ("A mapas", "ajuste eficiente (PEFT)", r"^Parameter-Efficient Fine-Tuning for Large Models", "regra"),
    ("A mapas", "inferência e serving", r"^Towards Efficient Generative Large Language Model Serving", "regra"),
    ("A mapas", "compressão de LLM", r"^A Survey on Model Compression for Large Language Models", "regra (mapa da era LLM)"),
    ("A mapas", "inferência e serving", r"^LLM Inference Unveiled", "regra (mapa da era LLM; traz o modelo roofline, útil para 'como pensar')"),
    ("B fundadores", "destilação", r"^Model compression$", "ajuste: Buciluă 2006 (20 votos) perdeu a vaga para a cota de época; é a origem da destilação"),
    ("B fundadores", "destilação", r"^Distilling the Knowledge in a Neural Network", "regra"),
    ("B fundadores", "destilação", r"^DistilBERT", "regra"),
    ("B fundadores", "quantização", r"^XNOR-Net", "ajuste: excluído pela regra por ter 'ImageNet' no título (22 votos)"),
    ("B fundadores", "quantização", r"^GPTQ", "ajuste: substitui HAWQ; GPTQ tem mais votos (15 × 13) e é base da quantização de LLM"),
    ("B fundadores", "quantização", r"^SmoothQuant", "regra"),
    ("B fundadores", "poda e esparsidade", r"^Optimal Brain Damage", "regra"),
    ("B fundadores", "poda e esparsidade", r"^Deep Compression", "ajuste: movido de quantização para poda (o título começa por pruning; é o pipeline clássico)"),
    ("B fundadores", "poda e esparsidade", r"^The Lottery Ticket Hypothesis", "regra"),
    ("B fundadores", "poda e esparsidade", r"^SparseGPT", "regra"),
    ("B fundadores", "fatoração de baixo posto", r"^Exploiting Linear Structure Within Convolutional", "regra"),
    ("B fundadores", "fatoração de baixo posto", r"^Low-rank matrix factorization for Deep Neural Network training", "ajuste: segundo fundador exigido pelo critério de sucesso (10 votos; o mais votado depois de Denton)"),
    ("B fundadores", "ajuste eficiente (PEFT)", r"^LoRA: Low-Rank Adaptation", "ajuste: a regra pôs LoRA em baixo posto; é o fundador do PEFT"),
    ("B fundadores", "ajuste eficiente (PEFT)", r"^QLoRA", "ajuste: a regra pôs em PEFT um paper de FPGA ('exp-LORA-tion' casou com LoRA)"),
    ("B fundadores", "computação condicional", r"^Outrageously Large Neural Networks", "ajuste: origem do MoE moderno (7 votos); substitui o paper de Bengio 2013, citado pelo estimador straight-through da quantização, não por computação condicional"),
    ("B fundadores", "computação condicional", r"^Switch Transformers: Scaling to Trillion", "regra (vaga de MoE da era LLM; 12 votos, igual ao GLaM, e mais citado)"),
    ("B fundadores", "computação condicional", r"^DeeBERT", "ajuste: early exit, a outra metade da divisão"),
    ("B fundadores", "atenção e sequência eficientes", r"^Reformer", "regra"),
    ("B fundadores", "atenção e sequência eficientes", r"^Mamba", "regra"),
    ("B fundadores", "inferência e serving", r"^Fast Transformer Decoding: One Write-Head", "regra (multi-query attention: reduz o KV cache; é arquitetura de decoder)"),
    ("B fundadores", "inferência e serving", r"^FlashAttention: Fast", "regra"),
    ("B fundadores", "inferência e serving", r"^Fast Inference from Transformers via Speculative", "ajuste: substitui FlashAttention-2 (redundante com FlashAttention; critério de acréscimo)"),
    ("B fundadores", "arquitetura eficiente e NAS", r"^MobileNets: Efficient", "regra"),
    ("B fundadores", "arquitetura eficiente e NAS", r"^FBNet: Hardware-Aware", "ajuste: substitui MobileNetV2 (redundante com MobileNets); NAS ciente de hardware, 16 votos"),
    ("B fundadores", "arquitetura eficiente e NAS", r"^MobileBERT", "ajuste: encoder compacto (12 votos); liga a divisão às arquiteturas de linguagem"),
    ("B fundadores", "hardware", r"^DianNao: a small-footprint", "ajuste: origem da família DianNao (6 + 13 = 19 votos, empate prático com DaDianNao, 20)"),
    ("B fundadores", "hardware", r"^Eyeriss: An Energy-Efficient Reconfigurable", "regra"),
    ("B fundadores", "hardware", r"^EIE: Efficient Inference Engine", "regra"),
    ("B fundadores", "hardware", r"^In-datacenter performance analysis of a tensor processing unit", "ajuste: TPU (5 + 27 = 32 votos) não casou com a regra por falta de palavra-chave; substitui Eyeriss v2 (redundante)"),
    ("B fundadores", "hardware", r"^FlightLLM", "regra (hardware para LLM, 2024)"),
    ("B fundadores", "edge e on-device", r"^Quantization and Training of Neural Networks for Efficient Integer-Arithmetic", "ajuste: inferência inteira em dispositivo (14 + 10 votos); substitui um paper de 4 votos"),
    ("C conceitos", "", r"^Attention is All you Need", "regra"),
    ("C conceitos", "", r"^BERT: Pre-training", "regra (encoder)"),
    ("C conceitos", "", r"^Exploring the Limits of Transfer Learning", "regra (encoder-decoder, T5)"),
    ("C conceitos", "", r"^Language Models are Few-Shot", "regra (decoder, GPT-3)"),
    ("C conceitos", "", r"^LLaMA: Open and Efficient", "regra (decoder aberto)"),
    ("C conceitos", "", r"^Long Short-Term Memory", "regra (base pré-transformer, §1.3)"),
    ("C conceitos", "", r"^A Survey of Large Language Models", "regra (mapa conceitual de LLM)"),
    ("D sistemas", "", r"^PyTorch: An Imperative", "regra"),
    ("D sistemas", "", r"^TVM: An Automated", "regra"),
    ("D sistemas", "inferência e serving", r"^Efficient Memory Management for Large Language Model Serving", "regra (vLLM)"),
    ("D sistemas", "edge e on-device", r"^TensorFlow Lite Micro", "regra"),
    ("D sistemas", "hardware", r"^FINN: A Framework", "regra"),
]
rows = []
for bloco, div, rx, origem in L:
    c = acha(rx)
    if not c:
        print("NÃO ACHADO:", rx); continue
    rows.append({"bloco": bloco, "divisao": div, "ano": c["year"], "titulo": re.sub(r"\s+", " ", c["title"]),
                 "votos_juri": int(c["votos"]) - int(c["votos_hw"]), "votos_reserva_hw": c["votos_hw"],
                 "origem": origem, "s2": c["s2"], "arxiv": c["arxiv"], "citacoes_s2": c["cit"], "venue": c["venue"]})
# mapa recente (2025-26), do próprio júri: ainda não teve tempo de ser citado
r = next(r for r in J if r["title"].startswith("Empowering Edge Intelligence"))
rows.insert(12, {"bloco": "A mapas", "divisao": "edge e on-device", "ano": r["year"], "titulo": r["title"], "votos_juri": "(jurado; 2025)",
                 "votos_reserva_hw": "", "origem": "regra do plano: mapa de 2025-26; jurado do gabarito mais citado de 2025-26 (265 citações)",
                 "s2": r["chave"], "arxiv": "", "citacoes_s2": r["cit"], "venue": ""})
with open(os.path.join(OUT, "lista-v2.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r["bloco"] for r in rows), "| ajustes:", sum(r["origem"].startswith("ajuste") for r in rows))
