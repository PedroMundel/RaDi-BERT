"""Google Forms version of the blind reading, for Pedro and friends: worked examples first, then the 50 items.

Writes a Google Apps Script (criar_formulario.gs) that builds the form, one page per item, from
leitura-50-gabarito.csv, keeping only what the reader may see (label, premise, hypothesis, rationale); source and
votes stay in the key. The worked examples are the ones in Wiegreffe et al. (2022)'s SNLI annotation template
(github.com/allenai/few_shot_explanations, mechanicalTurk_templates/snli/explanation_quality_absolute_snli.html),
translated.

To create the form: script.google.com > New project > paste criar_formulario.gs > Run `criarFormulario` > allow
access. The log prints the link to edit and the link to answer.
The `pt` version swaps the English sentences for traducao-pt.json (for readers without English); its answers are a
separate condition in the analysis, since translation changes what is judged.
Usage: python -m radibert.forms # -> criar_formulario.gs
       python -m radibert.forms pt # -> criar_formulario_pt.gs
"""
import json
import sys

import pandas as pd

from radibert.paths import LOTE_35B

KEY = LOTE_35B / "leitura-50-gabarito.csv"
TRANSLATION = LOTE_35B / "traducao-pt.json"
LABELS = {"entailment": "implicação", "neutral": "neutro", "contradiction": "contradição"}

TITLE = "Avaliação de justificativas de inferência textual"
DESCRIPTION = (
    "Obrigado por ajudar! São 50 itens, uns 40 minutos no total.\n\n"
    "Cada item tem duas frases em inglês, uma PREMISSA (uma cena, sempre tomada como verdade) e uma HIPÓTESE, "
    "o RÓTULO que diz como elas se relacionam e uma JUSTIFICATIVA que explica esse rótulo. "
    "Sua tarefa é julgar a justificativa, não o rótulo.\n\n"
    "Os três rótulos:\n"
    "• implicação: a hipótese decorre da premissa.\n"
    "• contradição: a hipótese não pode ser verdade se a premissa for.\n"
    "• neutro: a hipótese é possível, mas a premissa não garante nem nega.\n\n"
    "Importante: você pode discordar do rótulo, mas finja que ele está certo ao julgar a justificativa. "
    "Algumas frases vêm em minúscula por erro; ignore isso.\n\n"
    "A rubrica é a de Wiegreffe et al. (2022), NAACL. Os exemplos da próxima página são os das instruções originais "
    "deles, traduzidos."
)
QUESTIONS = [
    ("Traz informação nova?", "Fatos, informação ou raciocínio que não estão na premissa nem na hipótese.",
     ["Sim", "Não"]),
    ("A informação é relevante para justificar o rótulo dado?", "", ["Sim", "Não"]),
    ("Quanta informação ela traz para justificar o rótulo?", "", ["Pouca", "Suficiente", "Demais"]),
    ("No geral, você aceitaria essa justificativa?", "", ["Sim", "Não"]),
]
EXAMPLES = [
    ("Exemplo principal (todas as respostas)",
     "Premissa: A person on a horse jumps over a broken down airplane.\n"
     "Hipótese: A person is at a diner, ordering an omelette.\n"
     "Rótulo: contradição\n"
     "Justificativa: one cannot be on a jumping horse while at a diner ordering food.\n\n"
     "• Informação nova? Sim: diz que estar num cavalo saltando torna impossível estar, ao mesmo tempo, num "
     "restaurante.\n"
     "• Relevante para o rótulo? Sim: sustenta a contradição.\n"
     "• Quantidade? Suficiente: explica a relação sem nada a mais ou fora do assunto."),
    ("Mais exemplos (mesmo par, outras justificativas)",
     "Premissa: A person on a horse jumps over a broken down airplane.\n"
     "Hipótese: A person is training his horse for a competition.\n"
     "Rótulo: neutro\n\n"
     "Informação nova?\n"
     "• \"A person is training over a broken down airplane.\" → Não: só repete partes da premissa e da hipótese.\n"
     "• \"people ride horses for many reasons, including to train them, but also for fun and for transportation.\" "
     "→ Sim: traz o fato de que se monta a cavalo por vários motivos, com exemplos.\n\n"
     "Relevante para o rótulo?\n"
     "• A mesma frase dos vários motivos → Sim: explica o neutro.\n"
     "• \"a person jumping on a horse is training the horse.\" → Não: explica a implicação, que não é o rótulo "
     "dado.\n\n"
     "Quantidade?\n"
     "• \"the person is not necessarily training his horse.\" → Pouca: falta dizer por que saltar a cavalo pode "
     "ser outra coisa além de treinar.\n"
     "• A frase dos vários motivos → Suficiente.\n"
     "• A frase dos vários motivos seguida de um parágrafo sobre cavalos na colonização do Oeste americano → "
     "Demais: frases desnecessárias, informação sobrando."),
]


APPS_SCRIPT = """// Gerado por montar_google_forms.py: cria o formulario da leitura cega na sua conta Google.
// Como usar: script.google.com > Novo projeto > colar este arquivo > Executar criarFormulario > permitir acesso.
const DADOS = __DADOS__;

function criarFormulario() {
  const form = FormApp.create(DADOS.title);
  form.setDescription(DADOS.description).setProgressBar(true).setCollectEmail(false);
  form.addTextItem().setTitle('Seu nome ou apelido').setRequired(true);
  form.addPageBreakItem().setTitle('Exemplos').setHelpText('Leia antes de começar.');
  DADOS.examples.forEach(e => form.addSectionHeaderItem().setTitle(e[0]).setHelpText(e[1]));
  DADOS.items.forEach(it => {
    form.addPageBreakItem().setTitle(it.title).setHelpText(it.text);
    DADOS.questions.forEach(q => {
      form.addMultipleChoiceItem().setTitle(q[0]).setHelpText(q[1]).setChoiceValues(q[2]).setRequired(true);
    });
    form.addTextItem().setTitle('Motivo (opcional)');
  });
  Logger.log('Editar: ' + form.getEditUrl());
  Logger.log('Responder (mande este aos amigos): ' + form.getPublishedUrl());
}
"""


EXAMPLES_PT = [
    ("Exemplo principal (todas as respostas)",
     "Premissa: Uma pessoa a cavalo salta por cima de um avião abandonado.\n"
     "Hipótese: Uma pessoa está numa lanchonete, pedindo uma omelete.\n"
     "Rótulo: contradição\n"
     "Justificativa: não dá para estar num cavalo saltando enquanto se está numa lanchonete pedindo comida.\n\n"
     "• Informação nova? Sim: diz que estar num cavalo saltando torna impossível estar, ao mesmo tempo, numa "
     "lanchonete.\n"
     "• Relevante para o rótulo? Sim: sustenta a contradição.\n"
     "• Quantidade? Suficiente: explica a relação sem nada a mais ou fora do assunto."),
    ("Mais exemplos (mesmo par, outras justificativas)",
     "Premissa: Uma pessoa a cavalo salta por cima de um avião abandonado.\n"
     "Hipótese: Uma pessoa está treinando o cavalo para uma competição.\n"
     "Rótulo: neutro\n\n"
     "Informação nova?\n"
     "• \"Uma pessoa está treinando por cima de um avião abandonado.\" → Não: só repete partes da premissa e da "
     "hipótese.\n"
     "• \"as pessoas andam a cavalo por muitos motivos, inclusive para treiná-los, mas também por diversão e como "
     "meio de transporte.\" → Sim: traz o fato de que se monta a cavalo por vários motivos, com exemplos.\n\n"
     "Relevante para o rótulo?\n"
     "• A mesma frase dos vários motivos → Sim: explica o neutro.\n"
     "• \"uma pessoa saltando a cavalo está treinando o cavalo.\" → Não: explica a implicação, que não é o rótulo "
     "dado.\n\n"
     "Quantidade?\n"
     "• \"a pessoa não está necessariamente treinando o cavalo.\" → Pouca: falta dizer por que saltar a cavalo pode "
     "ser outra coisa além de treinar.\n"
     "• A frase dos vários motivos → Suficiente.\n"
     "• A frase dos vários motivos seguida de um parágrafo sobre cavalos na colonização do Oeste americano → "
     "Demais: frases desnecessárias, informação sobrando."),
]
PT_NOTE = ("\n\nVersão em português: as frases foram traduzidas do inglês, mantendo os erros e as frases estranhas do "
           "original de propósito.")


def data(pt: bool) -> dict:
    key = pd.read_csv(KEY)
    if pt:
        tr = json.loads(TRANSLATION.read_text(encoding="utf-8"))
        key[["premissa", "hipotese", "justificativa"]] = [
            [tr[str(n)]["premissa"], tr[str(n)]["hipotese"], tr[str(n)]["justificativa"]] for n in key["n"]]
    items = [{"title": f"Item {r.n} de {len(key)}",
              "text": f"Premissa: {r.premissa}\nHipótese: {r.hipotese}\nRótulo: {LABELS[r.gold_label]}\n\n"
                      f"Justificativa: {r.justificativa}"} for r in key.itertuples()]
    description = DESCRIPTION.replace("duas frases em inglês", "duas frases") + PT_NOTE if pt else DESCRIPTION
    return {"title": TITLE + (" (em português)" if pt else ""), "description": description,
            "examples": EXAMPLES_PT if pt else EXAMPLES, "questions": QUESTIONS, "items": items}


if __name__ == "__main__":
    pt = sys.argv[1:] == ["pt"]
    out = LOTE_35B / ("criar_formulario_pt.gs" if pt else "criar_formulario.gs")
    d = data(pt)
    out.write_text(APPS_SCRIPT.replace("__DADOS__", json.dumps(d, ensure_ascii=False, indent=1)), encoding="utf-8")
    print(f"{len(d['items'])} itens -> {out}")
