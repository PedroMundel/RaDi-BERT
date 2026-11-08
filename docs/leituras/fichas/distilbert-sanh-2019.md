# DistilBERT (Sanh et al. 2019) — extração do Pedro

**Procedência:** nível 1. Lido e extraído pelo Pedro em 06/10/2026. Texto copiado sem edição do arquivo dele
(`DistillBert (1).docx`).

---

Prior: distillation for building task-specific models
DistillBERT: Distill during pre-train to prove that reducing the model size whilst retaining its language understanding capabilities and increasing its speed is possible. Smaller, Faster, Lighter, Cheaper

Extracted points:

**Introdução (s.1)**
- Environmental cost of Exponentially scaling these models' computational requirements (Schwartz, 2019) and the growing computational and memory requirements to operate this models on-device in real time may hamper the wide adoption of these models in this type of regime (Sanh, 2020);
- Triple Loss? The ablation studies show it is important for best performances;

**Par. 2:**
- Distillation Loss Lce = Σi ti * log(si) where ti (resp. si) is a probability estimated by the teacher (resp. the student).
- (Hinton, 2015) softmax temperature, where the temperature controls the smoothness of the output distribution
- Final objective: linear combination of the distill loss with the supervised training loss (masked language modeling loss (Devlin, 2018). Cosine embedding loss to align the directions of the student and teacher hidden state vectors.
- What I got from par. 2: I'll need to study different types of losses for a better performance on our task, specially since we'll distill the rationale and not the knowledge

**Par. 3:**
- Bert with token-type embedding and the pooler removed, layers reduced by a factor of 2.
- Variations on the last dimension of the tensor (Hidden size dimension) have a smaller impact on the computational efficiency than variations on the other factors like num of layers.
- I will need to find the right initialization for the sub-net to converge. Because of the common dimensionality, they've initialized the student from the teacher by taking one layer out of the two (?). I'll have to keep this in mind whilst looking for models to use in my study.
- I'll have to search for the most recent "best practices for training BERT models"

**Par. 4:**
- They used GLUE to assess the language understanding and generalization capabilities, I'll need a similar way to assess my model's understanding and generalization capabilities.

**4.1:**
- I found their On device computation interesting, if i have time, i'll explore what they did afterwards.

**4.2:**
- MLM loss has little impact. Distillation loss accounts for a large portion of the performance.

**Par. 5:**
- They found it interesting to leverage the teacher's knowledge with initialization and additional losses to pre-train with additional distillation signals, leading to substantial gains.
- They say it's possible to remove some heads in the self-attention at test time without degrading the performance (Michel, 2019). Some layers can even be reduced to one head (Gupta, 2015).
- About this assumptions, do I also find them interesting? What about time? Does time also found this approaches interesting or better approaches have emergiram?

## Necessidades que a leitura levantou (Pedro, 06/10)

1. As 3 surveys mais recentes sobre destilação e 3 sobre KD.
2. Saber se existe survey recente sobre Rationale Distillation (DSbS).
3. Ler as surveys e determinar 5 obras importantes.
4. Arquitetar as losses: estudar quais dá para implementar com base em obras recentes, porque o DistilBERT afirma
   que as losses de destilação causam grande parte do ganho.
5. Uma obra recente de best practices para treinar modelos BERT.

**Material levantado para 1, 2, 4 e 5:** `docs/2026-10-06-destilacao-surveys-losses-bert.md`.
