# Pergunta à Anthropic sobre o decoder auxiliar (rascunho, 09/11/2026)

**Nada foi enviado.** Rascunho para o Pedro mandar ou não, como resposta no mesmo fio do suporte (e-mail de 19/10,
resposta de 05/11). Contexto e cláusulas em `docs/2026-10-19-geracao-dataset-prompt-e-licenca.md` §2.1.

**Por que perguntar:** a resposta de 05/11 disse que o caso "parece permitido", mas listou "Using Outputs as training
targets for models" como proibido e não falou do decoder. No desenho, o decoder auxiliar usa as saídas exatamente como
alvo de treino, e é jogado fora antes da entrega. A pergunta pede um sim ou não sobre esse ponto, por escrito.

**O que muda com a resposta:**
- **Sim por escrito:** o Claude volta a ser opção de professor (no RTE, no e-SNLI ou como terceiro professor para
  comparar com o Qwen).
- **Não, ou outra resposta ambígua:** nada muda; o Qwen segue como professor.

---

Subject: Follow-up: written yes/no on Outputs as training targets for a discarded auxiliary decoder

Hello,

Thank you for your reply of November 5. Before I use Claude for this project, I need a written yes or no on one
specific point that the reply did not cover.

My setup, for an undergraduate research project (not published as a model, no weights or dataset released):

1. Claude writes a one-sentence explanation for each training pair of a natural language inference dataset
   (e-SNLI or GLUE RTE), given the pair and its correct label.
2. I train a BERT-base classifier (about 110M parameters) on the labels. During training only, a small auxiliary
   decoder attached to the classifier learns to reproduce Claude's explanation, as a token-level training target.
3. After training, the auxiliary decoder is deleted. The only model kept is the classifier, which outputs a label
   and cannot generate text.

Your help article "Can I use my Outputs to train an AI model?" allows specialized classifiers, but lists "Using
Outputs as training targets for models" among the prohibited uses. Step 2 uses Outputs as training targets for the
auxiliary decoder, even though that decoder is discarded and the delivered model is a classifier.

Question: is step 2 permitted under the Usage Policy and the Commercial Terms, yes or no? If yes, may I treat your
reply as the prior written authorization the Usage Policy requires?

Thank you,
Pedro Mundel
