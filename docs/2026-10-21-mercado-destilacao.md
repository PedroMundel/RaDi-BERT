# Quem contrata quem sabe destilação (21/10/2026)

Pergunta do Pedro: "Quais empresas estão procurando profissionais com conhecimento sobre destilação?"

**Procedência: nível 3.** Tudo saiu de trechos de resultado de busca de 21/10/2026. As páginas de carreira
(NVIDIA, Intel) são montadas por JavaScript e não abriram, então **nenhuma vaga foi conferida na página original**.
Data, status (aberta ou fechada) e salário podem estar errados. Agregadores (Indeed, ZipRecruiter, Glassdoor) dão
contagens que não servem como número.

## 1. O achado

Destilação **quase nunca aparece sozinha** num anúncio. Ela vem num pacote com quantização, poda e otimização de
inferência, com títulos como "model compression", "inference optimization" e "model optimization". É o nome que o
mercado dá à especialização que o Pedro nomeou em 15/09 ("eficiência de modelos para implantação").

## 2. Exterior: quem aparece

| Tipo de empresa | Exemplos (via busca) | Como destilação aparece |
|---|---|---|
| Fabricante de chip ou hardware | NVIDIA (Deep Learning Engineer, LLM and VLM Model Compression; Senior ML Engineer, Quantized Inference), Intel (equipe do Neural Compressor), Qualcomm (Staff ML Engineer, Model Optimization & Quantization, com AIMET), Apple (Senior ML Engineer para ambientes com poucos recursos) | ao lado de poda, NAS e quantização; na NVIDIA, "quantization-aware distillation" |
| Borda: carro e robô | General Motors (Staff AI/ML Software Engineer, Model Distillation & Fine-Tuning, borda automotiva), XPENG (LLM Quantization & Deployment), Dyna Robotics (inferência de baixa latência para robô) | **a única com destilação no título é a da GM** |
| Ferramenta aberta de compressão | Red Hat (LLM Compressor) | quantização como foco |
| Startup de compressão | Multiverse Computing (Espanha, Deep Learning Engineer, Model Compression) | contrato temporário até jun/2026, provavelmente fechado |
| Laboratório de fronteira | OpenAI (ML engineer) | destilação como **diferencial**, não como requisito |

## 3. Brasil

**Nenhum anúncio brasileiro encontrado cita destilação.** O mais próximo:

- XP Inc. (vaga de MLOps em São Paulo, publicada 18/10/2026, híbrida): "quantização e otimização de inferência de
  LLMs" aparece como **diferencial**.
- Robert Half (São Paulo, remota, 23/09/2026): implantação, inferência e uso de GPU (H200), com foco em latência e
  throughput.
- O resto pede a pilha de sempre (scikit-learn, PyTorch, MLOps, RAG, fine-tuning).

A busca não achou vagas de Nubank, iFood, Mercado Livre nem CloudWalk com esses termos. Isso **não** prova que elas
não contratam: só que os agregadores não mostraram.

## 4. O que isso permite (leitura do Claude, a confirmar pelo Pedro)

- No exterior a habilidade é pedida, mas **dentro do pacote de compressão e inferência**, e sobretudo por quem vende
  hardware ou roda modelo na borda.
- No Brasil a palavra que aparece é **"otimização de inferência" e "quantização"**, ligada ao **custo de GPU**, e
  não "destilação".
- Inferência, não verificada em vaga: o caso de uso local mais provável do tema v3 é trocar uma chamada de LLM por
  um classificador encoder pequeno, para cortar custo e latência. Destilação aqui é o meio, não o nome da vaga.
- Para a régua do empregador: o termo que "grita" num currículo é "compressão e otimização de inferência
  (destilação, quantização)", não "destilação" sozinho.

## 4.1 Objeção do Pedro (21/10): "essas vagas são para mobile e edge; não vou usar destilação"

- **A própria lista não confirma "quase tudo é edge"**, numa amostra pequena:
  - servidor: NVIDIA (compressão de LLM e VLM), Red Hat (LLM Compressor, para servir no vLLM), OpenAI, XP Inc.;
  - edge: Qualcomm, Apple, GM, XPENG, Dyna;
  - a Intel atende os dois.
- **Edge não exclui destilação.** A única vaga com destilação no título (GM) é justamente para a borda.
- **O que se sustenta:** nos dois lados, destilação aparece como diferencial e a quantização domina, porque
  quantizar não exige retreinar. Destilar exige professor, dados e um treino inteiro.
- **Onde destilação seria o trabalho do dia (hipótese, não verificada em vaga):** equipes que trocam chamada de LLM
  por modelo pequeno no servidor, para cortar custo. O Agrawal 2025 (COLING Industry Track, Amazon; lido pelo Pedro)
  é uma instância: classificação de e-commerce, não edge. Essas vagas costumam ter títulos genéricos (Applied
  Scientist, ML Engineer de NLP), e a busca por palavra-chave não as acha. É um viés do método desta busca.

## 5. Limites e próximo passo possível

- A amostra é pequena e enviesada para os EUA: a busca é US-only.
- Uma contagem de verdade seria: no LinkedIn e na Gupy, filtrar Brasil + remoto internacional e contar anúncios por
  termo ("distillation", "quantization", "inference optimization", "model compression"), numa data fixa. Isso pode ser
  feito à mão pelo Pedro ou pelo navegador, se ele pedir.

## Fontes (resultados de busca, 21/10/2026)

- NVIDIA, LLM and VLM Model Compression: https://jobs.nvidia.com/careers/job/893394093790
- NVIDIA, Quantized Inference: https://jobs.nvidia.com/careers/job/893393661052
- Intel, AI Frameworks Software Engineer, Model Compression: https://intel.wd1.myworkdayjobs.com/en-US/External/job/AI-Frameworks-Software-Engineer---Model-Compression_JR0286404
- GM, Model Distillation & Fine-Tuning (via agregador): https://zapply.jobs/jobs/5d95ddd1-9da3-48a2-9a03-c30f354f4fb5/
- Qualcomm, Model Optimization & Quantization: https://www.theladders.com/job/staff-machine-learning-engineer-model-optimization-quantization-qualcomm-santa-clara-ca_88277759
- XPENG, LLM Quantization & Deployment: https://haystackapp.io/jobs/b310d792-ce6b-4fed-abe0-a577b47a21fd
- Multiverse Computing, Model Compression: https://jobs.forgepointcap.com/companies/multiverse-computing/jobs/62443226-deep-learning-engineer-model-compression-fixed-term-contract-technical-madrid-zaragoza-barcelona
- Brasil, MLOps com quantização (XP Inc., via agregador): https://zapply.jobs/jobs/7708a135-fdd4-4842-a54b-07719833a52c/
- Brasil, vagas de engenheiro(a) de IA, Robert Half: https://www.roberthalf.com/br/pt/vagas/sao-paulo/engenheiroa-de-inteligencia-artificial
