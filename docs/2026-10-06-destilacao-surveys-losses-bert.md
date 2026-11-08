# Surveys de destilação, losses e treino de BERT: o que existe (06/10/2026)

**O que motivou:** as necessidades que a leitura do DistilBERT levantou (`docs/leituras/fichas/distilbert-sanh-2019.md`).

**Procedência:** título, autores, datas, venue e abstract conferidos na API do arXiv e por busca na web em 06/10.
**Nenhuma obra foi lida inteira, nem pelo Claude nem pelo Pedro.** Tudo aqui é nível 3: serve para escolher o que
ler, não para citar.

**Como interpretei o pedido 1** (confirme): "KD" = surveys de destilação de conhecimento em geral; "destilação" =
surveys de destilação **de LLM**, a frente em que o tema v3 está.

---

## 1a. Surveys de KD em geral

**Achado:** só existe **um** survey geral e recente. Os outros recentes são de nicho (federada, difusão, grafos,
sensoriamento remoto, tradução).

| Obra | Data | Por que olhar |
|---|---|---|
| **A Comprehensive Survey on Knowledge Distillation** (Mansourian et al.; arXiv:2503.12067) | mar/2025, rev. out/2025, **TMLR** | Organiza a KD por fonte, esquema, algoritmo e modalidade, com seções sobre transformers, modelos fundacionais e LLM. É o substituto atual do Gou 2020. 102 páginas: por consulta. |
| **Feature Alignment and Representation Transfer in Knowledge Distillation for LLMs** (Yang et al.; arXiv:2504.13825) | abr/2025, sem venue | Trata da destilação por **estado oculto e atenção**, a família da cosine loss do DistilBERT. Serve ao pedido 4. |
| **KD4MT: A Survey of Knowledge Distillation for Machine Translation** (arXiv:2602.15845) | jan/2026 | O mais recente, mas é só de tradução automática. Entra apenas se você quiser ver KD em geração de sequência; para um encoder classificador, pode pular. |

## 1b. Surveys de destilação de LLM

| Obra | Data | Por que olhar |
|---|---|---|
| **Knowledge Distillation and Dataset Distillation of LLMs: Emerging Trends, Challenges, and Future Directions** (Fang et al.; arXiv:2504.14772) | abr/2025, rev. jan/2026 | O abstract cita **"rationale-based training"** entre os métodos centrais. É o mais próximo do DSbS entre os surveys. |
| **A Survey on Knowledge Distillation of Large Language Models** (Xu et al.; arXiv:2402.13116) | fev/2024, rev. out/2024 | O mais citado da frente. Organiza por algoritmo, habilidade e verticalização. |
| **Survey on Knowledge Distillation for LLMs: Methods, Evaluation, and Application** (Yang et al.; arXiv:2407.01885) | jul/2024 | Divide a área em caixa-branca (acesso aos logits do professor) e caixa-preta (só o texto que ele gera). **Essa divisão decide quais losses você consegue usar** (ver §3). |

**O mais novo de todos, com ressalva:** *A Survey of On-Policy Distillation for LLMs* (Song & Zheng; arXiv:2604.00626,
rev. jun/2026). Na destilação on-policy, o **aluno gera texto** e o professor corrige. **Um encoder não gera texto**,
então essa linha não se aplica ao aluno do tema v3, a não ser pela cabeça decodificadora auxiliar (H2). Vale saber
que existe, mas não entra entre os 3.

## 2. Existe survey de destilação de racionalização (estilo DSbS)?

**Não encontrei nenhum dedicado.** Busquei no arXiv (título e abstract) e na web em 06/10. O que existe:

- **Fang et al. 2025** (acima): seção de *rationale-based training* dentro de um survey de KD de LLM.
- **Efficient Reasoning Models: A Survey** (Feng et al.; arXiv:2504.10903; **TMLR 2025**): o ramo *smaller* trata de
  destilar raciocínio para modelos pequenos. Aqui o raciocínio é CoT gerado, então o foco é aluno decoder.
- Dois **estudos primários** que funcionam como mapa dos fatores, e um deles mexe direto no tema v3:
  - ⚠️ **Investigating Mysteries of CoT-Augmented Distillation** (Wadhwa et al.; arXiv:2406.14511; **EMNLP 2024**).
    Pelo abstract: (1) a racionalização colocada **depois** do rótulo funciona melhor, então o aluno não precisa
    raciocinar no teste; (2) **embaralhar os tokens da racionalização não tira o ganho**; (3) poucos tokens-chave
    bastam. **É exatamente o controle que o tema v3 marcava como lacuna** ("Agrawal não rodou racionalização
    embaralhada"). Eles rodaram, com aluno decoder. Não derruba o tema (novidade não é critério), mas o tema precisa
    ler e citar isso, e a pergunta muda para "**isso vale para encoder?**".
  - **Unveiling the Key Factors for Distilling Chain-of-Thought Reasoning** (Chen et al.; arXiv:2502.18001; **ACL
    2025 Findings**): granularidade, formato e professor. Achado do abstract: professor mais forte nem sempre dá
    aluno melhor.

## 3. Losses: o que dá para montar a partir de obras recentes

O que você tirou do DistilBERT foi "a loss de destilação é a maior parte do ganho, e eu vou destilar racionalização,
não conhecimento". As famílias de loss são três. Qual delas cabe depende de **o professor ser caixa-branca ou
caixa-preta** (1b, Yang 2024) e de **o aluno ser encoder**.

| Família | O que alinha | Obras recentes (conferidas) | Cabe num aluno encoder? |
|---|---|---|---|
| **Resposta / logit** (a L_ce do DistilBERT) | distribuição de saída do professor × aluno | **Logit Standardization in KD** (Sun et al.; arXiv:2403.01427; CVPR 2024): temperatura por amostra no lugar de uma temperatura única. **Rethinking KL Divergence in KD for LLMs** (Wu et al.; arXiv:2404.02657; COLING 2025): KL direta × reversa. **DistiLLM** (Ko et al.; arXiv:2402.03898; ICML 2024): KL "enviesada", para aluno gerador. | Sim, **se** o professor der probabilidades sobre os mesmos rótulos. O Logit Standardization é de classificação, então encaixa direto. O DistiLLM é de aluno gerador. |
| **Representação** (a cosine loss do DistilBERT) | estado oculto e atenção | Yang et al. 2025 (survey de feature alignment, §1a). LRKD (arXiv:2601.21611, já no projeto) faz regressão ao embedding da racionalização: é o H1. | Sim. É a família mais natural para encoder. |
| **Tarefa auxiliar com a racionalização** | o aluno aprende a racionalização como segunda tarefa | DSbS, DHRD e Agrawal 2025 (**você já leu os três**). Wadhwa 2024 (racionalização depois do rótulo; controle embaralhado). | Só com uma cabeça que gere texto (a decodificadora auxiliar do H2) ou com regressão a embedding (H1). |

**Próximo passo, que é seu:** o pedido 3 (ler os surveys e tirar 5 obras) vai dizer quais losses têm evidência.
O §3 é só o terreno.

## 4. Best practices para treinar BERT (recentes)

Antes de tudo, uma pergunta que decide qual obra serve: **você vai pré-treinar um encoder ou ajustar um já
pré-treinado?** Com uma RTX 5060 de 8 GB, o realista é ajustar.

| Obra | Data | Por que olhar |
|---|---|---|
| **Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder...** (ModernBERT; Warner et al.; arXiv:2412.13663) | dez/2024 | A receita moderna de encoder: arquitetura, dados e treino. **Também é candidato a aluno** do tema v3. Já estava nas lacunas de 05/10. |
| **NeoBERT: A Next-Generation BERT** (Le Breton et al.; arXiv:2502.19587) | fev/2025, rev. jun/2025, submetido à TMLR | Integra avanços de arquitetura, dados e pré-treino, e o abstract promete as escolhas com ablação. Sem venue confirmado. |
| **Seq vs Seq: An Open Suite of Paired Encoders and Decoders** (Ettin; Weller et al.; arXiv:2507.11412) | jul/2025, **ICLR 2026** | Encoder e decoder treinados com **a mesma receita e os mesmos dados**, de 17M a 1B. Serve ao pedido 5 **e** ao seu objetivo de 15/09 (comparar arquiteturas com controle). |

Mais antigos, só se for pré-treinar com orçamento: *Cramming* (Geiping & Goldstein; arXiv:2212.14034; dez/2022;
uma GPU, um dia) e *How to Train BERT with an Academic Budget* (Izsak et al.; arXiv:2104.07705; 2021).

---

**A pergunta do fim da sua ficha** (remover cabeças de atenção ainda interessa hoje?) fica aberta. Dá para responder
depois, olhando se os surveys de 2025–26 tratam poda de cabeças.
