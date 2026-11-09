# Pergunta aos autores do Agrawal 2025 (rascunho, 09/11/2026)

**Nada foi enviado.** Rascunho para o Pedro mandar ou não. Endereços tirados da primeira página do PDF
(`docs/artigos/2025.coling-industry.12-agrawal.pdf`): sanjagr@amazon.com, ahemf@amazon.com, viveksem@amazon.com.

**Por que perguntar:** o cronograma do aquecimento está em três frases do §4.4, sem as quantidades exatas, e o paper
não publicou código. Enquanto não houver resposta, o treino segue a leitura literal (D3 em
`docs/2026-11-09-treino-agrawal-rte-explicado.md`). Se responderem, roda-se também a leitura deles e comparam-se os
resultados. As perguntas 2–4 tiram outras dúvidas da replicação no RTE, que o paper também não responde.

---

Subject: Question on the decoder warmup schedule in "Rationale-Guided Distillation" (COLING 2025 Industry)

Dear Dr. Agrawal, Dr. Ahemad and Dr. Sembium,

I am an undergraduate student at the Federal University of Goiás (Brazil), replicating your COLING 2025 Industry
paper on the GLUE RTE task, as part of a research residency. The paper is very clear on the architecture and the
loss. I have a few questions on details I could not find in the text, and I would be grateful for any answer, even
a short one.

1. Decoder warmup (Section 4.4). How should I read these three quantities?
   a. "train only the decoder on 50% of the data": one pass over half of the training pairs, or half of the epochs?
   b. "a linear warmup phase for the encoder": the encoder learning rate rising linearly from 0, or gradual
      unfreezing of the layers?
   c. "over the first 30% of training": 30% of all training steps, or 30% of the steps after the decoder-only phase?
2. Hyperparameters on GLUE. Were the Table 4 values (batch 32, learning rate 5e-5, 8 epochs, 500 warmup steps) also
   used for RTE? With 2,490 training pairs, 500 warmup steps are about 80% of 8 epochs.
3. Evaluation on GLUE. Were the RTE numbers in Tables 2 and 7 measured on the GLUE validation split? And how many
   random seeds are behind each mean and 95% confidence interval?
4. Rationales. Are the Mixtral rationales for the GLUE tasks available anywhere?

Thank you for your time and for a very readable paper.

Best regards,
Pedro Mundel
Federal University of Goiás (UFG), Brazil
mundel@discente.ufg.br
