---
name: termogate
description: Draft the weekly "Termo de Aceite de Entrega" for the Residência gate from the project's current state. Use when the user asks for the termo, the entrega text, or says a gate is coming and the form needs filling.
---

# termogate

Produces `termo-de-entrega-Semana-<N>.md` at project root: the text Pedro pastes into the
program's form, plus the table of documents to link. **It is a draft** — Pedro rewrites it in his
own voice before submitting; the skill's job is to get the facts, the structure, and the tone close
enough that his rewrite is short.

## What the form asks

Two fields, verbatim from the form:

1. **"O que fiz nessa <N-ésima> Semana:"** — the deliverables.
2. **"Planejamento: [descrever o que pretende fazer para realizar a próxima ENTREGA]"**.

Header fields (date of the gate, matrícula) stay as `[preencher]`.

## Procedure

1. **Find N.** `ls termo-de-entrega-Semana-*.md`; N = highest + 1.
2. **Gather what was delivered since the last gate**, in this order of authority:
   - `CLAUDE.md` top block (current activity, "Entregas" paragraph) and the `entrega/` folder
     (`.docx` with mtime after the previous gate = the deliverables).
   - Latest files in `docs/handoffs/` — `## Status` and `## Decisions` since the previous termo.
   - The previous termo's `## Planejamento` — every item there must be either delivered, in the
     new Planejamento, or dropped **silently** (see Tone, rule 6).
   - **The previous termo as Pedro DELIVERED it**: `entrega/termos-entregues/Termo Semana <N-1>.docx`. It, not
     the `.md` draft at root, is the source for the Resumo and for the Planejamento check: his version differs
     from the draft every week (items cut, Planejamento rewritten).
3. **For each deliverable, read the delivered document itself** (the md in `entrega/` or root), not
   the handoff's summary of it — the termo describes the document, and counts (decisions, terms,
   groups, findings) must match the delivered version, not the working version.
4. **Write the draft** with the structure and tone below.
5. **Run the checks.** Then hand over with the list of open choices (things only Pedro can decide:
   whether to mention a pivot, whether a claimed reading happened).

## Structure

```
# Termo de Aceite de Entrega — Semana <N>

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

---

**Resumo das Semanas 1 a <N-1>:**

<one short dissertative paragraph (not a list), one sentence per previous week, only for context —
required by the professor (Pedro, 07/10/2026). Copy the DELIVERED previous paragraph verbatim and add
one or two sentences for week N-1. Even when he asks for "mais detalhe" (S8: another professor last
week), he kept only two of the five sentences drafted: what he did and the main finding.>

**O que fiz nessa <N-ésima> Semana:**

<one block per deliverable — see Tone>

**Planejamento:**

<1–3 items; the "X para:" header is optional (he dropped it in S3 and S8)>

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| <name as written in the termo> | `<path to .docx>` or a link (he links Google Forms too, S8) |
```

## Tone — distilled from Pedro's rewrite of the Semana 2 draft (19/09/2026) and from the delivered S3–S8 (compared 29/10/2026)

0. **The termo's job (Pedro, 01/10/2026):** show what he **did and learned** without explaining it in depth;
   every item has the shape **"fiz isso aqui por esse motivo"**. Depth lives in the linked .docx, never in the
   termo. One or two lines per item; if an item needs a paragraph, the paragraph belongs in the document.

1. **Lists over prose.** An enumeration of more than three things becomes a bullet list, one
   line each, ending in `;`. Never an inline enumeration in a paragraph.
2. **His role explicit, in first person, at every step that is his.** "editados por mim", "revisão
   feita por mim", "Fixei apenas o que consigo defender hoje". The professor evaluates the process
   — the text must show who decided.
3. **LLM use declared where the LLM did the work, inside that item.** "34 meus, 8 sugeridos por LLMs";
   "levantada com LLM"; "Pedi que agentes de LLM lessem as 56 obras". Never inflate it. **No closing
   catch-all item** ("O código e as rodadas foram feitos com apoio de LLM..."): he deleted it in S6, S7 and S8.
   If an LLM part is not attached to any item, list it as an open choice instead of a body line.
4. **Reason for each design decision, in plain words, tied to his own limitation.** "porque hoje
   não tenho conhecimento extensivo sobre a área ... eu poderia ficar preso lá na frente por
   escolhas feitas sem ter a base ainda". The reason is the deliverable; the artifact is evidence.
5. **Cut internal process mechanics.** Number of review findings, acceptance/rejection criteria,
   version numbers, "rev-N" — out. Keep what the professor can see in the linked document.
6. **Never narrate pivots or the previous plan's failure.** Items from the last Planejamento that
   were dropped are dropped without comment (project rule: "Narrar a troca de temas nos documentos
   de entrega" is rejected). No "Observação" section explaining what did not happen. **Exception he
   uses himself:** a concrete obstacle stated as the cause of what he did instead, in one item ("Meu
   computador deu um problema de hardware, não consegui testar mais nada [...]. Para não perder tempo,
   montei uma avaliação humana", S8; "Não estava conseguindo filtrar muito bem [...] Pedi que agentes
   de LLM lessem", S4). Use his words when the session has them.
7. **Fewer parentheticals, shorter sentences.** One qualifier per sentence at most. "(ainda)" is
   the acceptable size of a caveat.
8. **Citations always carry the year.** `Autor, ano` or `Autor et al. (ano)`; years taken from the
   project's own notes (`docs/metodo-de-construcao-do-metodo.md`, `docs/artigos/`), never from
   memory.
9. **Planejamento is short and chained by purpose**: "Finalizar X para: [item]; [item]." Three
   items, four at most. No dates, no hour budgets, no reading lists by title. **Next week only**
   (Pedro, 21/10/2026: "você se passou no planejamento, e sempre faz isso"): the immediate next
   steps, never the project's end goal (e.g. "treinar o encoder e comparar humano × LLM" is the
   final phase, not next week's plan).
10. **Document names in the termo = link anchors.** Write the deliverable's name exactly as the
    `.docx` is titled (no accents, as in `entrega/`), in bold, at the end of its block.

11. **Lead with the finding, not the method's rigor (Pedro, 14/10/2026).** The item says what was
    **discovered** and what it **makes possible**. How carefully it was done (blind, his own criteria, key
    revealed at the end, sample size) stays out of the termo: it lives in the linked document and comes out
    in the arguição if asked. Bad: "Avaliação manual às cegas de 20 trios, com critérios meus e chave
    revelada no fim". Good: "Encontrei inconsistências nas racionalizações humanas do e-SNLI, e as de LLM,
    geradas a baixo custo, podem dar mais robustez e permitem comparar treino com justificativa humana ×
    de LLM".

12. **Short: 4–6 items, one action sentence + one finding or reason each.** His bodies run ~200–300 words;
    every draft ran ~2× that and he cut it down. If the item needs a table, the table goes to the linked
    document and the item keeps only the action (S8: "Medi quantos pares o gerador produz mandando vários
    pedidos ao mesmo tempo." — numbers and model choice moved out).
13. **Numbers only when the number IS the finding.** Kept or added by him: "cerca de 8,5% do e-SNLI",
    "16 mil pares", "cerca de 8%", "em média, 76% das palavras vêm do par", "~99%". Cut by him: costs
    (US$ 0,64, US$ 19), speeds (0,28 / 1,66 s/par), durations (5h20), lengths (22 palavras), sample and
    count details (962 obras, 96%, 17 de 56), model specs, configs and file names.
14. **No item about process hygiene or safeguards.** Cut every time: calibrating agents before use, asking
    the LLM for a source per claim, checking terms of use, keeping a model "como reserva", splitting the
    reference into halves, which second database filled a gap. They belong to the document or the arguição.
15. **No external rule as the reason.** He swapped "a política de uso da Anthropic não permite..." for
    "por praticidade" (S7) and dropped it from the S8 Resumo. Give the practical reason, or none.
16. **Leave room for his own sentence.** What he adds is personal and specific: where he found a source
    ("lendo uma thread no Reddit", S5), what was hard ("Não estava conseguindo filtrar", S4), his own reading
    of a risk ("O risco real é as duas perdas puxarem o encoder para lados opostos", S7). Never invent these;
    when the session has his words for a motive or an insight, use them verbatim.

## Evidence: draft -> delivered (29/10/2026)

Delivered versions in `entrega/termos-entregues/`. What changed, per week:

| Semana | He cut | He added or changed |
|---|---|---|
| 3 | the `edge` string move, "termos do professor", screening in rounds, train/test split of the reference, OpenAlex | kept the layered cleaning with its numbers; Planejamento without "para:" |
| 4 | agent calibration, the 962-work sample, "framework nos dois sentidos" | "Não estava conseguindo filtrar..." as the reason for the LLM reading cards |
| 5 | the Fang (2025) survey item, "pedi fonte para cada afirmação", the four readings as sub-bullets | readings merged into one item with the conclusion; "lendo uma thread no Reddit"; Planejamento = 1 item |
| 6 | costs (US$ 0,64 / US$ 19), terms-of-use check, LLM catch-all item, 3rd Planejamento item | copy numbers (76%, ~99%) into the inconsistency item; "custo muito baixo" |
| 7 | Anthropic policy reason, "Parti de rascunhos gerados por LLM", decoder item, 35B-as-reserve item, LLM catch-all item | "por praticidade"; "as justificativas anteriores agora servem apenas para comparação"; his own risk sentence |
| 8 | speeds and model choice, lote details, "ainda não há resultado", LLM catch-all item, 3 of 5 Resumo sentences | the hardware problem as the reason for the human evaluation; Forms linked; one merged design item in Planejamento |

## Checks before handing over

- Every number in the text (decisions, terms, groups) matches the **delivered** document.
- Every list's count matches its introducing sentence ("nove decisões" → nine bullets).
- Every citation has a year; parentheses balance.
- Zero mentions of pivots, suspended plans, or "o gate anterior".
- Every `.docx` in the link table exists and has mtime after the previous gate.
- The draft claims no reading Pedro has not done (see memory `procedencia-de-leitura`).
- Grep the text for the previous termo's Planejamento items: each is delivered, re-planned, or
  silently gone — never "was not done because".

## What this skill does not do

- Does not generate the `.docx` — the termo is pasted into the form.
- Does not decide whether a pivot is mentioned or a reading is claimed: list those as open choices.
- Does not edit the delivered documents; if a count mismatch is found, report it.
