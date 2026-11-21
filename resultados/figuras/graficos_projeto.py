"""Figures of the whole project, from Semana 3 (citation tree) to 18/11, each drawn only from numbers read from a
file on disk. Writes one PNG per figure next to this file and INDICE.md, which names the source of each one.

    uv run --frozen --with matplotlib python resultados/figuras/graficos_projeto.py [--so 07 13]
Labels are in Portuguese: the figures go into Pedro's gate documents. Trains nothing.
"""
import argparse
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
RES = ROOT / "resultados"
SCREENING = ROOT / "docs" / "screening" / "fase1"
SMALL = RES / "rte-pequenos"
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"  # categorical slots, fixed order
INDEX: list[dict] = []


# --- helpers ------------------------------------------------------------------------------------------------------

def comma(value: float, digits: int = 1, sign: bool = False) -> str:
    return f"{value:{'+' if sign else ''}.{digits}f}".replace(".", ",")


def thousands(value: float) -> str:
    return f"{int(value):,}".replace(",", ".")


def canvas(width: float, height: float, title: str, subtitle: str, panels: int = 1, sharey: bool = False,
           key: list[tuple[str, str]] | None = None):
    """A figure whose title and subtitle sit on the figure, so long tick labels never push them out. `key` is a
    colour legend (label, colour) drawn in a row under the subtitle, clear of the marks."""
    fig, axes = plt.subplots(1, panels, figsize=(width, height), facecolor=SURFACE, sharey=sharey)
    top = 1 - (1.3 if key else 0.95) / height
    fig.text(0.02, 1 - 0.36 / height, title, color=INK, fontsize=13, fontweight="bold", va="center")
    fig.text(0.02, 1 - 0.68 / height, subtitle, color=MUTED, fontsize=9, va="center")
    if key:
        handles = [plt.Line2D([], [], marker="o", linewidth=0, markersize=7, color=color, label=label)
                   for label, color in key]
        fig.legend(handles=handles, frameon=False, fontsize=9, labelcolor=INK, ncol=len(key), loc="center left",
                   bbox_to_anchor=(0.012, 1 - 1.0 / height), handletextpad=0.3, columnspacing=1.6)
    fig.subplots_adjust(top=top)
    return fig, axes, top


def style(ax, grid: str = "y"):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, length=0, labelsize=9)
    ax.grid(axis=grid, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def save(fig, top: float, name: str, title: str, source: str, how: str):
    fig.tight_layout(rect=(0, 0, 1, top))
    fig.savefig(HERE / f"{name}.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)
    INDEX.append({"file": f"{name}.png", "title": title, "source": source, "how": how})


def interval(values) -> tuple[float, float]:
    """Mean and half of the 95% t interval."""
    values = pd.Series(values).dropna()
    return values.mean(), stats.t.ppf(0.975, len(values) - 1) * values.std() / len(values) ** 0.5


def paired(frame: pd.DataFrame, value: str, arm: str, base: str, arm_column: str = "arm") -> pd.Series:
    """arm minus base, seed by seed, on the seeds both have."""
    wide = frame[frame[arm_column].isin([arm, base])].pivot(index="seed", columns=arm_column, values=value)
    return (wide[arm] - wide[base]).dropna()


def hbars(ax, labels: list[str], values: list[float], color: str = BLUE, fmt=thousands):
    positions = range(len(labels))[::-1]
    ax.barh(list(positions), values, color=color, height=0.62)
    for position, value in zip(positions, values):
        ax.annotate(fmt(value), (value, position), xytext=(5, 0), textcoords="offset points", va="center",
                    fontsize=9, color=INK)
    ax.set_yticks(list(positions), labels, fontsize=10, color=INK)
    style(ax, "x")
    ax.set_xlim(0, max(values) * 1.16)


def dots(ax, groups: list[tuple[str, pd.Series, str]], digits: int = 1):
    """One row per group: every value small and pale, the mean large, the mean's number above it."""
    for position, (_, values, color) in zip(range(len(groups))[::-1], groups):
        ax.scatter(values, [position] * len(values), s=34, color=color, alpha=0.4, linewidths=0)
        ax.scatter([values.mean()], [position], s=130, color=color, edgecolors=SURFACE, linewidths=2, zorder=3)
        ax.annotate(comma(values.mean(), digits), (values.mean(), position), xytext=(0, 11),
                    textcoords="offset points", ha="center", fontsize=9, color=INK)
    ax.set_yticks(range(len(groups))[::-1], [label for label, _, _ in groups], fontsize=10, color=INK)
    ax.set_ylim(-0.6, len(groups) - 0.25)
    style(ax, "x")


def forest(ax, rows: list[tuple[str, pd.Series, str]], digits: int = 1, scale: float = 1.0):
    """One row per comparison: the paired difference's mean with its 95% interval, and a line at zero."""
    for position, (_, diff, color) in zip(range(len(rows))[::-1], rows):
        mean, half = interval(diff * scale)
        ax.errorbar([mean], [position], xerr=[half], color=color, elinewidth=1.6, capsize=3, marker="o",
                    markersize=7, linewidth=0)
        ax.annotate(f"{comma(mean, digits, sign=True)}  (n={len(diff)})", (mean + half, position), xytext=(7, 0),
                    textcoords="offset points", va="center", fontsize=8.5, color=INK)
    ax.axvline(0, color=MUTED, linewidth=1)
    ax.set_yticks(range(len(rows))[::-1], [label for label, _, _ in rows], fontsize=9.5, color=INK)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    style(ax, "x")
    low, high = ax.get_xlim()
    ax.set_xlim(low, high + 0.22 * (high - low))


def legend(ax, entries: list[tuple[str, str]], loc: str = "lower right"):
    handles = [plt.Line2D([], [], marker="o", linewidth=0, markersize=7, color=color, label=label)
               for label, color in entries]
    ax.legend(handles=handles, frameon=False, fontsize=9, loc=loc, labelcolor=INK)


def results(folder: str) -> pd.DataFrame:
    return pd.read_csv(RES / folder / "pc" / "resultados.csv", dtype={"warmup": str})


# --- screening (Semanas 3 a 5) ------------------------------------------------------------------------------------

def fig_01_funil():
    forest_csv = SCREENING / "2026-09-22-floresta-obras.csv"
    works = pd.read_csv(forest_csv, encoding="utf-8-sig", low_memory=False,
                        usecols=["camada_A", "para_camada_C", "camada_C_F1"]).fillna("")
    fig, (left, right), top = canvas(11.5, 4.3, "Do levantamento à árvore de citação",
                                     "Obras em cada etapa da limpeza em camadas (22 e 23/09).", panels=2)
    hbars(left, ["Floresta (todas as buscas)", "Mantidas na camada A (área)", "Seguem para a camada C"],
          [len(works), (works["camada_A"] == "mantida").sum(), (works["para_camada_C"] == "sim").sum()])
    left.set_title("Funil", loc="left", fontsize=10, color=MUTED)
    fate = works.loc[works["camada_C_F1"] != "", "camada_C_F1"].value_counts()
    hbars(right, list(fate.index), list(fate.values), ORANGE)
    right.set_title("Destino das 14.901 na árvore de citação (F1)", loc="left", fontsize=10, color=MUTED)
    save(fig, top, "01-screening-funil", "Do levantamento à árvore de citação",
         "docs/screening/fase1/2026-09-22-floresta-obras.csv (colunas camada_A, para_camada_C, camada_C_F1)",
         "Cada barra é uma contagem de obras. À esquerda, quantas sobram a cada camada; à direita, o que a "
         "árvore de citação fez com as que chegaram à camada C.")


def fig_02_f2():
    verdicts = pd.read_csv(SCREENING / "F2" / "vereditos.csv", encoding="utf-8-sig")["veredito"].value_counts()
    fig, ax, top = canvas(8.5, 3.4, "F2: o que os agentes disseram das 962 obras lidas",
                          "Triagem por agentes de 26 e 27/09; veredito por obra.")
    hbars(ax, list(verdicts.index), list(verdicts.values))
    save(fig, top, "02-screening-f2-vereditos", "F2: vereditos das 962 obras lidas",
         "docs/screening/fase1/F2/vereditos.csv (coluna veredito)",
         "Contagem de obras por veredito. 'Relevante' são 55 de 962.")


def fig_03_classificador():
    data = json.loads((SCREENING / "C1-diagnostico" / "resultados.json").read_text(encoding="utf-8"))["E1_P1"]
    methods = sorted(data, key=lambda name: -data[name]["rec@25%"])
    fig, ax, top = canvas(8.5, 3.6, "Classificador da triagem: bate o acaso, mas não chega ao contrato",
                          "Parcela das obras relevantes achadas ao ler os 25% do topo da lista (27/09).")
    hbars(ax, methods, [100 * data[m]["rec@25%"] for m in methods], fmt=lambda v: comma(v, 1) + "%")
    ax.axvline(25, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.annotate("acaso: 25%", (25, len(methods) - 0.55), xytext=(4, 0), textcoords="offset points", fontsize=8.5,
                color=MUTED)
    save(fig, top, "03-screening-classificador", "Classificador da triagem: recuperação nos 25% do topo",
         "docs/screening/fase1/C1-diagnostico/resultados.json (chave E1_P1, campo rec@25%)",
         "Cada barra é um jeito de ordenar a lista. A linha tracejada é o que se acha lendo 25% ao acaso.")


def fig_04_lista():
    works = pd.read_csv(SCREENING / "lista-rapida" / "lista-v2.csv")
    blocks = sorted(works["bloco"].unique())
    colors = dict(zip(blocks, (BLUE, ORANGE, AQUA, YELLOW)))
    fig, ax, top = canvas(9.5, 3.6, "As 56 obras da lista v2, por bloco e ano",
                          "Lista rápida de 27/09, tirada do júri de surveys.")
    rng = np.random.default_rng(0)
    for position, block in zip(range(len(blocks))[::-1], blocks):
        years = works.loc[works["bloco"] == block, "ano"]
        ax.scatter(years, position + rng.uniform(-0.22, 0.22, len(years)), s=46, color=colors[block], alpha=0.75,
                   linewidths=0)
    ax.set_yticks(range(len(blocks))[::-1], [f"{b} ({(works['bloco'] == b).sum()})" for b in blocks], fontsize=10,
                  color=INK)
    style(ax, "x")
    ax.set_xlabel("Ano de publicação", color=MUTED, fontsize=9)
    save(fig, top, "04-screening-lista-v2", "As 56 obras da lista v2, por bloco e ano",
         "docs/screening/fase1/lista-rapida/lista-v2.csv (colunas bloco, ano)",
         "Cada ponto é uma obra, na linha do seu bloco e na posição do seu ano; o número entre parênteses é o "
         "total do bloco. A posição vertical dentro da linha é só para os pontos não se cobrirem.")


# --- geração das justificativas (outubro) -------------------------------------------------------------------------

def words(texts: pd.Series) -> pd.Series:
    return texts.fillna("").str.split().str.len()


def fig_05_piloto():
    folder = RES / "piloto-qwen"
    variants = [("A", "resultados.csv"), ("B", "resultados-B.csv"), ("D", "resultados-D.csv"),
                ("E", "resultados-E.csv"), ("E2", "resultados-E2.csv"), ("E3", "resultados-E3.csv"),
                ("E4", "resultados-E4.csv"), ("F", "resultados-F.csv"), ("FR", "resultados-FR.csv"),
                ("FRG", "resultados-FRG.csv"), ("E, modelo 35B", "resultados-E-35B.csv"),
                ("F, modelo 35B", "resultados-F-35B.csv"), ("FRG, modelo 35B", "resultados-FRG-35B.csv")]
    human = words(pd.read_csv(folder / "resultados.csv")["Explanation_1"])
    groups = [("Humano (e-SNLI)", human, MUTED)]
    groups += [(f"Variante {name}", words(pd.read_csv(folder / file)["qwen"]), ORANGE if "35B" in name else BLUE)
               for name, file in variants]
    fig, ax, top = canvas(9.5, 6.4, "Piloto do prompt: quantas palavras tem a justificativa",
                          "45 pares do dev do e-SNLI, os mesmos em todas as variantes (20 a 26/10).")
    dots(ax, groups)
    ax.set_xlabel("Palavras por justificativa", color=MUTED, fontsize=9)
    legend(ax, [("Qwen 9B", BLUE), ("Qwen 35B", ORANGE), ("justificativa humana", MUTED)])
    save(fig, top, "05-geracao-piloto-comprimento", "Piloto do prompt: comprimento da justificativa por variante",
         "resultados/piloto-qwen/resultados*.csv (coluna qwen; Explanation_1 para a humana)",
         "Cada ponto pequeno é uma justificativa, o grande é a média da variante. Conta palavras separadas por "
         "espaço.")


def fig_06_lote():
    batch = RES / "lote-35B"
    pattern = re.compile(r"^(\d\d):(\d\d):(\d\d) (\d+) pares no total")
    points = [(int(h) * 3600 + int(m) * 60 + int(s), int(n)) for h, m, s, n in
              (match.groups() for match in map(pattern.match, (batch / "run" / "train.log").read_text(
                  encoding="utf-8", errors="replace").splitlines()) if match)]
    seconds = np.array([p[0] for p in points]) - points[0][0]
    fig, (left, right), top = canvas(11, 3.9, "O lote de 16.000 justificativas (Qwen 35B, variante F)",
                                     "Madrugada de 27/10 na RTX 5060; eco marcado em 28/10.", panels=2)
    left.plot(seconds / 3600, [p[1] for p in points], color=BLUE, linewidth=2)
    style(left)
    left.set_xlabel("Horas desde o início", color=MUTED, fontsize=9)
    left.set_ylabel("Pares gerados", color=MUTED, fontsize=9)
    left.set_title("Progresso", loc="left", fontsize=10, color=MUTED)
    marks = pd.read_csv(batch / "marcas.csv").merge(
        pd.read_csv(batch / "racionalizacoes-F-35B.csv", usecols=["pairID", "gold_label"], nrows=16_000), on="pairID")
    echo = 100 * marks.groupby("gold_label")["eco"].mean().sort_values(ascending=False)
    hbars(right, list(echo.index), list(echo.values), ORANGE, fmt=lambda v: comma(v, 1) + "%")
    right.set_title("Justificativas marcadas como eco, por rótulo", loc="left", fontsize=10, color=MUTED)
    save(fig, top, "06-geracao-lote-35B", "O lote de 16.000 justificativas",
         "resultados/lote-35B/run/train.log (linhas 'N pares no total'), marcas.csv (coluna eco) e "
         "racionalizacoes-F-35B.csv (gold_label)",
         "À esquerda, pares gerados ao longo das horas. À direita, a parcela das justificativas de cada rótulo "
         "que a regra de eco marcou. No arquivo só há marcas em entailment; não foi conferido na regra se isso é "
         "por desenho.")


# --- replicação do Agrawal e controles (novembro) -----------------------------------------------------------------

def fig_07_decoder():
    rte, esnli4, esnli16 = results("rte-treino"), results("esnli-treino"), results("esnli-treino-16k")
    grids = [("RTE, BERT base, aquecimento proporcional", rte[rte["warmup"] == "prop"], "bert_decoder", "bert"),
             ("RTE, BERT base, aquecimento da Tabela 4", rte[rte["warmup"] == "500"], "bert_decoder", "bert"),
             ("RTE, BERT MS-MARCO (nboost)", results("rte-msmarco"), "bert_decoder", "bert"),
             ("RTE, BERT MS-MARCO (Capreolus)", results("rte-capreolus"), "bert_decoder", "bert"),
             ("RTE, T5 v1.1 como encoder", results("rte-t5enc"), "t5enc_decoder", "t5enc"),
             ("RTE, BERT small", results("rte-small"), "bert_decoder", "bert"),
             ("RTE, BERT tiny", results("rte-tiny"), "bert_decoder", "bert"),
             ("e-SNLI, 4.000 pares", esnli4, "bert_decoder", "bert"),
             ("e-SNLI, 16.000 pares", esnli16, "bert_decoder", "bert")]
    rows = [(label, paired(frame, "roc_auc", arm, base), BLUE) for label, frame, arm, base in grids]
    calendars = [("RTE, BERT base, proporcional", pd.concat([rte[rte["warmup"] == "prop"], results("rte-calendario")])),
                 ("e-SNLI, 4.000 pares", pd.concat([esnli4, results("esnli-treino-calendario")])),
                 ("e-SNLI, 16.000 pares", pd.concat([esnli16, results("esnli-treino-16k-calendario")]))]
    rows += [(f"{label}  [contra o calendário]", paired(frame, "roc_auc", "bert_decoder", "bert_calendar"), ORANGE)
             for label, frame in calendars]
    fig, ax, top = canvas(10.5, 6.5, "O decoder auxiliar não deu ganho em nenhuma condição",
                          "ROC-AUC do braço com decoder menos o braço sem, pareado por semente; barras: intervalo "
                          "de 95%.",
                          key=[("contra o BERT sem decoder", BLUE),
                               ("contra o BERT sem decoder com o mesmo calendário", ORANGE)])
    forest(ax, rows, digits=3)
    ax.set_xlabel("Diferença de ROC-AUC (positivo = o decoder ajuda)", color=MUTED, fontsize=9)
    save(fig, top, "07-decoder-todas-as-grades", "Decoder menos sem decoder, em todas as grades",
         "resultados/{rte-treino,rte-msmarco,rte-capreolus,rte-t5enc,rte-small,rte-tiny,esnli-treino,"
         "esnli-treino-16k,rte-calendario,esnli-treino-calendario,esnli-treino-16k-calendario}/pc/resultados.csv "
         "(coluna roc_auc)",
         "Cada linha é uma condição de treino. O ponto é a diferença média entre sementes e a barra o intervalo de "
         "95%; à direita da linha vertical o decoder ajuda. n é o número de sementes pareadas. No RTE o T5 como "
         "encoder tem causa própria (desequilíbrio de gradiente).")


def fig_08_baseline():
    conditions = pd.read_csv(RES / "rte-msmarco" / "condicoes-baseline.csv")
    nboost, capreolus = results("rte-msmarco"), results("rte-capreolus")
    groups = [("nboost, ajuste completo", nboost.loc[nboost["arm"] == "bert", "roc_auc"], BLUE),
              ("Capreolus, ajuste completo", capreolus.loc[capreolus["arm"] == "bert", "roc_auc"], BLUE),
              ("nboost, uma época (aquec. proporcional)",
               conditions.loc[conditions["condition"] == "one_epoch_prop", "roc_auc"], BLUE),
              ("nboost, uma época (aquec. da Tabela 4)",
               conditions.loc[conditions["condition"] == "one_epoch_500", "roc_auc"], BLUE),
              ("nboost, encoder congelado", conditions.loc[conditions["condition"] == "frozen", "roc_auc"], BLUE)]
    fig, ax, top = canvas(10, 4.3, "Nenhuma condição tentada dá o baseline do artigo no RTE",
                          "ROC-AUC no dev do RTE de um BERT base MS-MARCO sem decoder, 5 sementes por condição.")
    dots(ax, groups, digits=3)
    for value, text in ((0.4754, "artigo: BERT (0,4754)"), (0.5873, "artigo: + Reasoning (0,5873)")):
        ax.axvline(value, color=ORANGE, linewidth=1.2, linestyle=(0, (3, 3)))
        ax.annotate(text, (value, len(groups) - 0.35), xytext=(4, 0), textcoords="offset points", fontsize=8.5,
                    color=INK)
    ax.set_xlabel("ROC-AUC", color=MUTED, fontsize=9)
    ax.set_xlim(0.44, 0.80)
    save(fig, top, "08-baseline-do-artigo", "Condições do baseline MS-MARCO no RTE",
         "resultados/rte-msmarco/condicoes-baseline.csv, resultados/rte-msmarco/pc/resultados.csv e "
         "resultados/rte-capreolus/pc/resultados.csv (braço bert); linhas tracejadas: Tabela 2 de Agrawal, Ahemad & "
         "Sembium (2025), conferida no PDF",
         "Cada ponto pequeno é uma semente e o grande a média. As linhas tracejadas são os dois números que o "
         "artigo relata para o RTE.")


def fig_09_perda_grupos():
    names = {"C": ("copiada do par", BLUE), "N": ("nova, fora do par", ORANGE), "S": ("expressão de rótulo", AQUA),
             "F": ("gramatical", YELLOW)}
    fig, axes, top = canvas(11, 4.2, "Com 16.000 pares o decoder aprende mais, em todos os tipos de palavra",
                            "Perda do decoder por token na sonda, média de 5 sementes; e-SNLI, BERT base.",
                            panels=2, sharey=True)
    for ax, (folder, label) in zip(axes, (("esnli-treino", "4.000 pares (1.000 passos)"),
                                          ("esnli-treino-16k", "16.000 pares (4.000 passos)"))):
        steps = pd.read_csv(RES / folder / "pc" / "gradientes.csv").groupby("step")[[f"l_{g}" for g in names]].mean()
        for group, (text, color) in names.items():
            ax.plot(steps.index, steps[f"l_{group}"], color=color, linewidth=2, label=text)
            ax.annotate(comma(steps[f"l_{group}"].iloc[-1], 2), (steps.index[-1], steps[f"l_{group}"].iloc[-1]),
                        xytext=(5, 0), textcoords="offset points", fontsize=8.5, va="center", color=INK)
        style(ax)
        ax.set_title(label, loc="left", fontsize=10, color=MUTED)
        ax.set_xlabel("Passo de treino", color=MUTED, fontsize=9)
        ax.set_xlim(0, steps.index[-1] * 1.12)
    axes[0].set_ylabel("Perda (nats por token)", color=MUTED, fontsize=9)
    axes[1].legend(frameon=False, fontsize=9, labelcolor=INK, loc="upper right")
    save(fig, top, "09-decoder-perda-por-tipo-de-palavra", "Perda do decoder por tipo de palavra, 4 mil e 16 mil pares",
         "resultados/esnli-treino/pc/gradientes.csv e resultados/esnli-treino-16k/pc/gradientes.csv (colunas l_C, "
         "l_N, l_S, l_F)",
         "Cada linha é a perda do decoder num tipo de palavra-alvo ao longo do treino; menor é melhor. O número no "
         "fim de cada linha é o valor no último passo. As sondas das duas grades são 63 pares sorteados do treino de "
         "cada uma, não os mesmos pares.")


def fig_10_embaralhada():
    grids = pd.concat([results("esnli-treino-16k"), results("esnli-treino-16k-calendario"),
                       results("esnli-treino-16k-embaralhado")])
    names = [("bert_calendar", "Sem decoder, mesmo calendário", BLUE), ("bert", "Sem decoder, treino comum", YELLOW),
             ("bert_decoder", "Com decoder, justificativa do par", ORANGE),
             ("bert_decoder_shuffled", "Com decoder, justificativa de outro par", AQUA)]
    fig, ax, top = canvas(10, 3.8, "A justificativa certa custa pouco; a de outro par custa muito",
                          "Acurácia no dev ao fim do treino; e-SNLI, 16.000 pares, BERT base, 5 sementes.")
    dots(ax, [(label, 100 * grids.loc[grids["arm"] == arm, "accuracy"], color) for arm, label, color in names])
    ax.set_xlabel("Acurácia no dev (%)", color=MUTED, fontsize=9)
    save(fig, top, "10-justificativa-embaralhada", "Acurácia final dos quatro braços nos 16 mil pares",
         "resultados/{esnli-treino-16k,esnli-treino-16k-calendario,esnli-treino-16k-embaralhado}/pc/resultados.csv "
         "(coluna accuracy)",
         "Cada ponto pequeno é uma semente e o grande a média do braço.")


def fig_11_curva():
    curve = RES / "esnli-treino-16k-curva"
    pc = pd.read_csv(curve / "pc" / "curva.csv")
    rows = pd.concat([pc[pc["seed"] <= 3], pd.read_csv(curve / "amigo" / "curva.csv")])
    rows = rows.assign(since=rows["step"] - 1200, accuracy=100 * rows["dev_accuracy"])
    wide = rows.pivot(index="since", columns=["arm", "seed"], values="accuracy")
    fig, ax, top = canvas(9.5, 4.6, "O decoder adianta o começo e termina atrás",
                          "Acurácia no dev depois que a classificação começa; e-SNLI, 16.000 pares, 5 sementes.")
    for arm, label, color in (("bert_calendar", "Sem decoder, mesmo calendário", BLUE),
                              ("bert_decoder", "Com decoder, justificativa do par", ORANGE)):
        for seed in wide[arm]:
            ax.plot(wide.index, wide[arm][seed], color=color, linewidth=0.8, alpha=0.35)
        mean = wide[arm].mean(axis=1)
        ax.plot(wide.index, mean, color=color, linewidth=2, marker="o", markersize=5, label=label)
        ax.annotate(comma(mean.iloc[0]), (wide.index[0], mean.iloc[0]), xytext=(-7, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=9, color=INK)
        ax.annotate(comma(mean.iloc[-1]), (wide.index[-1], mean.iloc[-1]),
                    xytext=(7, 5 if arm == "bert_calendar" else -5), textcoords="offset points", va="center",
                    fontsize=9, color=INK)
    style(ax)
    ax.set_xscale("log")
    ticks = [t for t in wide.index if t != 2300]
    ax.set_xticks(ticks, [thousands(t) for t in ticks], fontsize=8)
    ax.minorticks_off()
    ax.set_xlabel("Passos de classificação já dados (escala logarítmica)", color=MUTED, fontsize=9)
    ax.set_ylabel("Acurácia no dev (%)", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=9, loc="lower right", labelcolor=INK)
    save(fig, top, "11-curva-de-arranque", "Curva de arranque: com decoder contra sem decoder",
         "resultados/esnli-treino-16k-curva/pc/curva.csv (sementes 1 a 3) e amigo/curva.csv (sementes 4 e 5)",
         "Linha grossa: média de 5 sementes; linhas finas: cada semente. O eixo horizontal conta os passos desde "
         "o passo 1.200, em escala logarítmica. A versão com o painel da diferença está em "
         "resultados/esnli-treino-16k/figs/curva-de-arranque.png.")


# --- marcas de atenção e destaque (10 a 16/11) --------------------------------------------------------------------

def fig_12_marcas():
    arms = [("marks_none", "Sem marcas", MUTED), ("marks_random", "Marca sorteada", YELLOW),
            ("marks_real", "Marca das palavras do LLM", BLUE)]
    panels = [("BERT base, dev do RTE (5 sementes)", results("rte-marcas"), "roc_auc"),
              ("BERT small, dev do RTE (15 sementes)", results("rte-marcas-small"), "roc_auc"),
              ("BERT small, fora da distribuição (15 sementes)", results("rte-marcas-small-fora"), "fora_roc_auc")]
    fig, axes, top = canvas(13, 3.5, "Marcas na atenção do [CLS]: a marca real não passa do modelo sem marcas",
                            "ROC-AUC por braço; RTE, 10/11. A marca sorteada derruba a nota no BERT base.",
                            panels=3)
    for index, (ax, (label, frame, column)) in enumerate(zip(axes, panels)):
        dots(ax, [(name, frame.loc[frame["arm"] == arm, column], color) for arm, name, color in arms], digits=3)
        ax.set_title(label, loc="left", fontsize=9.5, color=MUTED)
        ax.set_xlabel("ROC-AUC", color=MUTED, fontsize=9)
        if index:
            ax.set_yticklabels([])
    save(fig, top, "12-marcas-nota", "Marcas de atenção: ROC-AUC por braço",
         "resultados/rte-marcas/pc/resultados.csv, rte-marcas-small/pc/resultados.csv (roc_auc) e "
         "rte-marcas-small-fora/pc/resultados.csv (fora_roc_auc)",
         "Três painéis, um por condição. Em cada um, ponto pequeno é uma semente e ponto grande a média do braço. "
         "Os eixos horizontais não são os mesmos entre os painéis.")


def fig_13_atencao():
    mass = pd.read_csv(SMALL / "atencao.csv")
    held = mass[mass["split"] == "held"].groupby(["arm", "layer"])[["mass_real", "uniform"]].mean()
    arms = [("untrained", "BERT small sem treino no RTE", MUTED), ("marks_none", "Treinado sem marcas", YELLOW),
            ("marks_random", "Treinado com marca sorteada", AQUA), ("marks_real", "Treinado com a marca real", BLUE)]
    fig, ax, top = canvas(9, 4.2, "A marca real muda a atenção da última camada, e só dela",
                          "Parcela da atenção do [CLS] nas palavras marcadas, em pares nunca treinados; BERT small.")
    for arm, label, color in arms:
        ax.plot(held.loc[arm].index, 100 * held.loc[arm, "mass_real"], color=color, linewidth=2, marker="o",
                markersize=6, label=label)
    # end labels, pushed apart where three lines end within a few points of each other
    ends = sorted((100 * held.loc[arm, "mass_real"].iloc[-1], arm) for arm, _, _ in arms)
    placed = []
    for value, _ in ends:
        placed.append(max(value, placed[-1] + 3.2) if placed else value)
    for (value, _), y in zip(ends, placed):
        ax.annotate(comma(value) + "%", (4, value), xytext=(4.12, y), textcoords="data", va="center", fontsize=8.5,
                    color=INK)
    ax.axhline(100 * held["uniform"].mean(), color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.annotate("atenção igual em todos os tokens", (4.45, 100 * held["uniform"].mean()), xytext=(0, -11),
                textcoords="offset points", fontsize=8.5, color=MUTED, ha="right")
    style(ax)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xlim(0.8, 4.5)
    ax.set_xlabel("Camada do BERT small", color=MUTED, fontsize=9)
    ax.set_ylabel("Atenção nas palavras marcadas (%)", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=9, loc="upper left", labelcolor=INK)
    save(fig, top, "13-marcas-atencao-por-camada", "Atenção do [CLS] nas palavras marcadas, por camada",
         "resultados/rte-pequenos/atencao.csv (split held, coluna mass_real; linha tracejada: coluna uniform)",
         "Cada linha é um modelo; o eixo vertical é quanto da atenção do [CLS] cai nas palavras que a justificativa "
         "copia. A marca foi cobrada na camada 4.")


def fig_14_destaque():
    scores = pd.read_csv(SMALL / "destaque-2000-cabeca.csv")
    names = [("token_head", "Cabeça por token treinada nas marcas", ORANGE),
             ("marks_real", "Atenção do modelo com a marca real", BLUE),
             ("rule_content_both", "Regra: palavra de conteúdo nas duas frases", MUTED),
             ("untrained", "Atenção do BERT small sem treino", MUTED),
             ("rule_content_hypothesis", "Regra: palavra de conteúdo da hipótese", MUTED),
             ("rule_content", "Regra: palavra de conteúdo", MUTED),
             ("marks_none", "Atenção do modelo sem marcas", MUTED),
             ("marks_random", "Atenção do modelo com marca sorteada", MUTED),
             ("rule_random", "Sorteio", MUTED)]
    fig, ax, top = canvas(9.8, 5, "Destaque: a atenção treinada aponta as palavras que o LLM copia",
                          "Precisão média (AP) em 470 pares nunca treinados; BERT small, 2.000 pares de treino.")
    dots(ax, [(label, scores.loc[scores["method"] == method, "ap"], color) for method, label, color in names],
         digits=3)
    ax.set_xlabel("Precisão média (AP)", color=MUTED, fontsize=9)
    save(fig, top, "14-destaque", "Destaque: quem aponta melhor as palavras copiadas pelo LLM",
         "resultados/rte-pequenos/destaque-2000-cabeca.csv (coluna ap)",
         "Cada linha é um jeito de dar nota às palavras do par; quanto mais à direita, melhor ele ordena as "
         "palavras que a justificativa copia. As regras e o modelo sem treino têm um valor só.")


def fig_15_camadas():
    layers = pd.read_csv(SMALL / "camadas-esnli-4000.csv")
    base = layers[layers["kind"] == "none"].set_index("seed")["dev_accuracy"]
    real = layers[layers["kind"] == "real"]
    order = ["1", "2", "3", "4", "1+2", "1+3", "1+4", "2+3", "2+4", "3+4", "1+2+3+4"]
    rows = [(f"camada {combo}", (real[real["layers"] == combo].set_index("seed")["dev_accuracy"] - base).dropna(),
             BLUE) for combo in order if (real["layers"] == combo).any()]
    fig, ax, top = canvas(9, 5.4, "Cobrar a marca em outras camadas também não ajuda",
                          "Acurácia no dev com a marca real em cada combinação de camadas menos sem marcas; "
                          "e-SNLI, BERT small.")
    forest(ax, rows, digits=2, scale=100)
    ax.set_xlabel("Diferença de acurácia (pontos)", color=MUTED, fontsize=9)
    save(fig, top, "15-marcas-por-camada", "Marca real cobrada em cada combinação de camadas",
         "resultados/rte-pequenos/camadas-esnli-4000.csv (kind real menos kind none, coluna dev_accuracy)",
         "Cada linha é uma combinação de camadas onde a marca foi cobrada; o ponto é a diferença para o modelo sem "
         "marcas, pareada por semente, com o intervalo de 95%.")


def fig_16_intervencao():
    runs = pd.read_csv(SMALL / "intervencao-2000.csv", dtype={"layers": str})
    block = runs[(runs["arm"] == "marks_none") & (runs["operation"] == "block") & (runs["rows"] == "cls")
                 & runs["layers"].isin(["1", "2", "3", "4"])]
    flips = 100 * block.groupby(["set", "layers"])["flip"].mean().unstack("layers")
    names = [("real", "palavras que a justificativa copia", BLUE), ("content_a", "palavras de conteúdo (regra a)", ORANGE),
             ("content_b", "palavras de conteúdo (regra b)", AQUA), ("random", "palavras sorteadas", MUTED)]
    fig, ax, top = canvas(9, 4.2, "A decisão depende da atenção do [CLS] nas camadas 3 e 4",
                          "Tapar a atenção do [CLS] numa camada, sem treinar: decisões que mudam; BERT small, RTE.")
    for key, label, color in names:
        ax.plot([1, 2, 3, 4], flips.loc[key, ["1", "2", "3", "4"]], color=color, linewidth=2, marker="o",
                markersize=6, label=label)
    style(ax)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xlabel("Camada em que a atenção foi tapada", color=MUTED, fontsize=9)
    ax.set_ylabel("Decisões que mudam (%)", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=9, loc="upper left", labelcolor=INK, title="Conjunto de palavras tapado",
              title_fontsize=9)
    save(fig, top, "16-intervencao-por-camada", "Tapar a atenção do [CLS] por camada",
         "resultados/rte-pequenos/intervencao-2000.csv (arm marks_none, operation block, rows cls, coluna flip)",
         "Cada linha é um conjunto de palavras cuja atenção foi tapada na linha do [CLS]; o eixo vertical é a "
         "parcela dos 470 pares em que a decisão do modelo muda. Média das sementes.")


# --- destilação (16 a 18/11) --------------------------------------------------------------------------------------

def fig_17_destilacao():
    answers = pd.read_csv(SMALL / "respostas-esnli-4000.csv")
    names = [("out_t1", "Respostas do professor (temperatura 1)"), ("out_t2", "Respostas (temperatura 2)"),
             ("out_t4", "Respostas (temperatura 4)"), ("big_t1", "Professor com mais dados (temperatura 1)"),
             ("big_t2", "Professor com mais dados (temperatura 2)"), ("smooth", "Controle: rótulo suavizado"),
             ("swapped", "Controle: respostas de outro par")]
    rows = [(label, paired(answers, "choice_accuracy", arm, "none"), ORANGE if arm in ("smooth", "swapped") else BLUE)
            for arm, label in names]
    fig, ax, top = canvas(10, 4.9, "Imitar as respostas do professor é o que dá ganho",
                          "Acurácia no conjunto de escolha menos o aluno sem professor; BERT small aluno, BERT base "
                          "professor, e-SNLI.", key=[("destilação das respostas", BLUE), ("controles", ORANGE)])
    forest(ax, rows, digits=2, scale=100)
    ax.set_xlabel("Diferença de acurácia (pontos)", color=MUTED, fontsize=9)
    save(fig, top, "17-destilacao-respostas", "Destilação das respostas do professor",
         "resultados/rte-pequenos/respostas-esnli-4000.csv (coluna choice_accuracy, cada braço menos none)",
         "Cada linha é um jeito de usar o professor; o ponto é o ganho sobre o aluno sem professor, pareado por "
         "semente, com intervalo de 95%. Os controles mostram se o ganho vem do que o professor diz de cada par.")


def fig_18_atencao_destilada():
    runs = pd.read_csv(SMALL / "destilacao-esnli-fora-4000.csv")
    names = [("outputs", "Respostas do professor"), ("att_last", "Atenção do professor, última camada"),
             ("att_all", "Atenção do professor, todas as camadas")]
    rows = [(label, paired(runs, "dev_accuracy", arm, "none"), BLUE) for arm, label in names]
    fig, ax, top = canvas(9.5, 3.2, "Destilar a atenção do professor não ajuda; as respostas, sim",
                          "Acurácia no dev menos o aluno sem professor; professor que não viu os pares do aluno.")
    forest(ax, rows, digits=2, scale=100)
    ax.set_xlabel("Diferença de acurácia (pontos)", color=MUTED, fontsize=9)
    save(fig, top, "18-destilacao-atencao", "Destilar a atenção contra destilar as respostas",
         "resultados/rte-pequenos/destilacao-esnli-fora-4000.csv (coluna dev_accuracy, cada braço menos none)",
         "Cada linha é o que o aluno imita do professor; ganho sobre o aluno sem professor, pareado por semente.")


def fig_19_juntar():
    runs = pd.read_csv(SMALL / "juntar-esnli-4000.csv")
    names = [("sequence", "Sequência (interior, depois respostas)"),
             ("sequence_clean", "Sequência, atenção antes do dropout"),
             ("sequence_untrained", "Controle: sequência com professor sem tarefa"),
             ("sum", "Soma simples (atenção + respostas)"), ("mini_joint", "Pacote MiniLM junto"),
             ("tiny_joint", "Pacote TinyBERT junto"), ("mini_content", "MiniLM sem a atenção"),
             ("tiny_content", "TinyBERT sem a atenção"), ("none", "Aluno sem professor")]
    rows = [(label, paired(runs, "choice_accuracy", arm, "answers"),
             ORANGE if arm in ("sequence_untrained", "none") else BLUE) for arm, label in names]
    fig, ax, top = canvas(10.5, 5.5, "Juntar o interior do professor com as respostas: só a sequência passa",
                          "Acurácia no conjunto de escolha menos 'só as respostas do professor'; BERT small, e-SNLI.",
                          key=[("jeitos de juntar", BLUE), ("controles", ORANGE)])
    forest(ax, rows, digits=2, scale=100)
    ax.set_xlabel("Diferença de acurácia para 'só as respostas' (pontos)", color=MUTED, fontsize=9)
    save(fig, top, "19-destilacao-juntar", "Juntar o interior do professor com as respostas",
         "resultados/rte-pequenos/juntar-esnli-4000.csv (coluna choice_accuracy, cada braço menos answers)",
         "Cada linha é um braço comparado com o aluno que só imita as respostas; à direita da linha vertical o "
         "braço é melhor. n é o número de sementes pareadas (a sequência tem 15, os demais 5).")


# --- palavras novas e cabeça de grupos (17 e 18/11) ---------------------------------------------------------------

def fig_20_palavras_novas():
    table = pd.read_csv(SMALL / "palavras-novas-esnli-4000.csv").set_index("words")
    names = [("rationale", "Justificativa inteira"), ("S", "Só as expressões de rótulo"), ("F", "Só as gramaticais"),
             ("N", "Só as palavras novas"), ("pair+N", "Par + palavras novas"), ("C", "Só as copiadas do par"),
             ("pair", "Só as palavras do par"), ("majority class", "Chutar o rótulo mais comum")]
    fig, ax, top = canvas(9, 4.4, "As palavras novas da justificativa dizem muito sobre o rótulo",
                          "Acurácia de uma regressão logística que vê só aquele conjunto de palavras; e-SNLI, 17/11.")
    hbars(ax, [label for _, label in names], [100 * table.loc[key, "accuracy"] for key, _ in names],
          fmt=lambda v: comma(v, 1) + "%")
    save(fig, top, "20-palavras-novas-e-rotulo", "Quanto cada conjunto de palavras diz sobre o rótulo",
         "resultados/rte-pequenos/palavras-novas-esnli-4000.csv (coluna accuracy)",
         "Cada barra é a acurácia de prever o rótulo vendo só aquele conjunto de palavras. O acaso é a última barra.")


def fig_21_grupos_cls():
    cut = pd.read_csv(SMALL / "recorte-acuracias.csv")
    names = [("head_cut", "none", "Sete grupos"), ("head_all", "none", "29 grupos"),
             ("head_cut_swapped", "none", "Controle: sete grupos trocados"),
             ("head_all_swapped", "none", "Controle: 29 grupos trocados"),
             ("head_cut_answers", "answers", "Sete grupos + respostas do professor"),
             ("head_all_answers", "answers", "29 grupos + respostas do professor"),
             ("head_cut_swapped_answers", "answers", "Controle: sete trocados + respostas"),
             ("head_all_swapped_answers", "answers", "Controle: 29 trocados + respostas")]
    rows = [(label, paired(cut, "cut", arm, base), ORANGE if "swapped" in arm else BLUE) for arm, base, label in names]
    fig, ax, top = canvas(10.5, 5.2, "Cabeça de grupos no [CLS]: nenhum braço passa do critério de 0,64 ponto",
                          "Acurácia no recorte de 1.249 pares menos a referência do braço; BERT small, e-SNLI, "
                          "17 e 18/11.",
                          key=[("grupos certos", BLUE), ("controle com grupos de outro par", ORANGE)])
    forest(ax, rows, digits=2)
    ax.set_xlim(-0.8, 1.15)
    for value in (-0.64, 0.64):
        ax.axvline(value, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.annotate("critério: 0,64", (0.64, len(rows) - 0.45), xytext=(4, 0), textcoords="offset points", fontsize=8.5,
                color=MUTED)
    ax.set_xlabel("Diferença de acurácia no recorte (pontos)", color=MUTED, fontsize=9)
    save(fig, top, "21-cabeca-de-grupos", "Cabeça de grupos no [CLS], no recorte",
         "resultados/rte-pequenos/recorte-acuracias.csv (coluna cut; braços sem professor menos none, com "
         "professor menos answers)",
         "Cada linha é um braço menos a sua referência, pareado por semente; as linhas tracejadas são o critério "
         "de 0,64 ponto escrito antes. n é o número de sementes (15 nos dois primeiros braços de sete grupos).")


def fig_22_dificeis():
    hits = pd.read_csv(SMALL / "grupos-cls-acertos-esnli-4000.csv", dtype={"hits": str})
    bands = [("Fáceis (13 a 15 acertam)", 13, 15), ("Médios (3 a 12)", 3, 12), ("Difíceis (0 a 2)", 0, 2)]
    rows = []
    for split, label, color in (("choice", "conjunto de escolha", BLUE), ("dev", "dev", ORANGE)):
        table = {arm: np.array([[c == "1" for c in row.hits] for row in rows_.sort_values("seed").itertuples()])
                 for arm, rows_ in hits[hits["split"] == split].groupby("arm")}
        difficulty = table["answers"].sum(axis=0)
        for name, low, high in bands:
            mask = (difficulty >= low) & (difficulty <= high)
            diff = 100 * (table["head_cut"][:, mask].mean(axis=1) - table["none"][:, mask].mean(axis=1))
            rows.append((f"{name}, {label}", pd.Series(diff), color))
    rows = [rows[i] for i in (2, 5, 1, 4, 0, 3)]  # each band's two sets side by side, hard first
    fig, ax, top = canvas(10, 4.5, "O ganho nos pares difíceis não se repete no dev",
                          "Sete grupos menos o aluno sem nada, por dificuldade do par; BERT small, e-SNLI, 15 "
                          "sementes.",
                          key=[("conjunto de escolha (olhar exploratório)", BLUE),
                               ("dev (critério escrito antes)", ORANGE)])
    forest(ax, rows, digits=2)
    ax.set_xlabel("Diferença de acurácia (pontos)", color=MUTED, fontsize=9)
    save(fig, top, "22-pares-dificeis", "Pares difíceis: conjunto de escolha contra o dev",
         "resultados/rte-pequenos/grupos-cls-acertos-esnli-4000.csv (acertos par a par; mesma conta de "
         "medir_dificeis.py)",
         "Dificuldade de um par = quantos dos 15 alunos do braço 'respostas' o acertam naquele conjunto. Cada "
         "linha é a diferença do braço de sete grupos para o aluno sem nada, pareada por semente.")


ARGUMENT_GROUP = 22  # the one group of argument words (leitura-grade.md, "HDBSCAN groups"); the other 28 are topics
TARGET_GROUPS = [21, 2, 3, 14, 20, 16, 4]  # Pedro's seven target groups of 17/11 (medir_grupos_cls.CUT_GROUPS)


def fig_23_grupos_composicao():
    groups = pd.read_csv(SMALL / "grupos-palavras-novas.csv")
    groups = pd.concat([groups[groups["group"] != -1].sort_values("pairs_with_it", ascending=False),
                        groups[groups["group"] == -1]])
    labels = [("share_entailment", "entailment", BLUE), ("share_neutral", "neutral", ORANGE),
              ("share_contradiction", "contradiction", AQUA)]
    fig, ax, top = canvas(12.5, 11.5, "Os 29 grupos de palavras novas: quase todos são um assunto",
                          "Grupos do HDBSCAN sobre as palavras novas das justificativas (e-SNLI, 4.000 pares, 17/11); "
                          "barra: como os pares do grupo se dividem entre os rótulos.",
                          key=[(name, color) for _, name, color in labels])
    positions = np.arange(len(groups))[::-1]
    left = np.zeros(len(groups))
    for column, _, color in labels:
        ax.barh(positions, 100 * groups[column], left=left, color=color, height=0.68, edgecolor=SURFACE, linewidth=2)
        left += 100 * groups[column].to_numpy()
    names = []
    for row in groups.itertuples():
        tag = ("sem grupo" if row.group == -1 else f"grupo {row.group}")
        tag += "  [argumentar]" if row.group == ARGUMENT_GROUP else "  [alvo]" if row.group in TARGET_GROUPS else ""
        names.append(f"{tag}:  {', '.join(row.top_words.split()[:5])}")
    ax.set_yticks(positions, names, fontsize=9, color=INK)
    for position, row in zip(positions, groups.itertuples()):
        ax.annotate(f"{thousands(row.words)} palavras, {thousands(row.pairs_with_it)} pares", (100, position),
                    xytext=(6, 0), textcoords="offset points", va="center", fontsize=8.5, color=MUTED)
    style(ax, "x")
    ax.set_xlim(0, 128)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_ylim(-0.7, len(groups) - 0.3)
    ax.set_xlabel("Pares do grupo por rótulo (%)", color=MUTED, fontsize=9)
    save(fig, top, "23-grupos-hdbscan-composicao", "Os grupos de palavras novas, um a um",
         "resultados/rte-pequenos/grupos-palavras-novas.csv (colunas words, pairs_with_it, share_*, top_words)",
         "Cada linha é um grupo, com as cinco palavras mais frequentes dele; a barra mostra a parcela dos pares "
         "com palavra do grupo em cada rótulo, e à direita vão o número de palavras e de pares. [alvo] marca os "
         "sete grupos escolhidos pelo Pedro em 17/11; [argumentar] é o único grupo de palavras de argumentar. Um "
         "par pode ter palavra de vários grupos.")


def fig_24_grupos_mapa():
    words = pd.read_csv(SMALL / "grupos-palavras-novas-mapa.csv")
    top_words = pd.read_csv(SMALL / "grupos-palavras-novas.csv").set_index("group")["top_words"]
    palette = [BLUE, ORANGE, AQUA, YELLOW, "#e87ba4", "#008300", "#6250d6", "#e34948"]
    highlighted = dict(zip([ARGUMENT_GROUP, *TARGET_GROUPS], palette))
    fig, ax, top = canvas(12, 9.5, "Mapa das palavras novas das justificativas e dos grupos do HDBSCAN",
                          "2.323 palavras; cada ponto é uma palavra, o tamanho cresce com o número de pares em que "
                          "ela aparece. Em cor: o grupo de argumentar e os sete grupos-alvo.")
    outside = words[words["group"] == -1]
    ax.scatter(outside["x"], outside["y"], s=6, color="#d9d8d3", linewidths=0)
    for group, rows in words[words["group"] != -1].groupby("group"):
        color = highlighted.get(group, "#9a998f")
        ax.scatter(rows["x"], rows["y"], s=10 + 6 * np.sqrt(rows["pairs"]), color=color, linewidths=0,
                   alpha=0.9 if group in highlighted else 0.55)
        name = ", ".join(top_words[group].split()[:3 if group in highlighted else 2])
        text = f"{group}: {name}" + ("  [argumentar]" if group == ARGUMENT_GROUP else "")
        nudge = {16: (30, -16), 18: (-45, 9)}.get(group, (0, 9))  # two neighbours whose labels ran into each other
        ax.annotate(text, (rows["x"].median(), rows["y"].median()), xytext=nudge, textcoords="offset points",
                    ha="center", fontsize=8.5 if group in highlighted else 7.5,
                    color=INK if group in highlighted else MUTED,
                    fontweight="bold" if group in highlighted else "normal",
                    bbox={"boxstyle": "round,pad=0.15", "facecolor": SURFACE, "edgecolor": "none", "alpha": 0.75})
    style(ax, "both")
    ax.grid(visible=False)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    save(fig, top, "24-grupos-hdbscan-mapa", "Mapa das palavras novas e dos grupos",
         "resultados/rte-pequenos/grupos-palavras-novas-mapa.csv (posições, de mapa_grupos_palavras.py) e "
         "grupos-palavras-novas-palavras.csv (o grupo de cada palavra, salvo em 17/11)",
         "Cada ponto é uma palavra nova. O grupo de cada palavra é o que o HDBSCAN deu em 17/11, sobre uma "
         "projeção de 10 dimensões; a posição no mapa vem de uma segunda projeção, de 2 dimensões, feita só para "
         "o desenho, então a distância no mapa não é a que o agrupamento viu. Cinza claro: palavras sem grupo "
         "(1.069). Os eixos não têm unidade.")


# --- figuras que faltavam para o artigo (18/11) -------------------------------------------------------------------

def box(ax, x: float, y: float, width: float, height: float, text: str, edge: str = MUTED, fill: str = SURFACE,
        dashed: bool = False, size: float = 9.5):
    ax.add_patch(matplotlib.patches.FancyBboxPatch(
        (x, y), width, height, boxstyle="round,pad=0.02,rounding_size=0.12", facecolor=fill, edgecolor=edge,
        linewidth=1.6, linestyle=(0, (4, 3)) if dashed else "solid"))
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=size, color=INK)


def arrow(ax, start: tuple[float, float], end: tuple[float, float], color: str = MUTED):
    ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "-|>", "color": color, "linewidth": 1.5,
                                                      "shrinkA": 2, "shrinkB": 2})


def fig_25_metodo():
    fig, ax, top = canvas(11.5, 5.6, "O método testado: um decoder auxiliar que gera a justificativa do LLM",
                          "Desenho de Agrawal, Ahemad & Sembium (2025), como foi implementado aqui. O decoder só existe "
                          "no treino.")
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    box(ax, 0.2, 2.35, 2.0, 0.9, "Premissa + hipótese")
    box(ax, 3.0, 2.0, 2.3, 1.6, "Encoder\n(BERT)", edge=BLUE, fill="#e7f0fb", size=11)
    box(ax, 6.2, 3.55, 2.5, 1.0, "Cabeça de classificação\n(lê o [CLS])", edge=BLUE, fill="#e7f0fb")
    box(ax, 9.4, 3.65, 1.9, 0.8, "Rótulo\n(perda L_cls)")
    box(ax, 6.2, 1.0, 2.5, 1.1, "Decoder auxiliar (T5)\n(lê os estados de\ntodos os tokens)", edge=ORANGE,
        fill="#fdeee7", dashed=True)
    box(ax, 9.4, 1.05, 1.9, 1.0, "Justificativa\ndo LLM\n(perda L_aux)")
    box(ax, 0.2, 0.25, 3.2, 0.9, "LLM professor (Qwen 35B) escreve\na justificativa de cada par, antes do treino",
        size=8.5)
    arrow(ax, (2.2, 2.8), (3.0, 2.8))
    arrow(ax, (5.3, 3.1), (6.2, 4.0), BLUE)
    arrow(ax, (8.7, 4.05), (9.4, 4.05), BLUE)
    arrow(ax, (5.3, 2.5), (6.2, 1.6), ORANGE)
    arrow(ax, (8.7, 1.55), (9.4, 1.55), ORANGE)
    ax.plot([3.4, 10.35], [0.6, 0.6], color=MUTED, linewidth=1.5)  # one elbow: along the bottom, then up
    arrow(ax, (10.35, 0.58), (10.35, 1.05))
    ax.text(5.75, 2.82, "No fim do treino: L_cls + 0,1 x L_aux", fontsize=9.5, color=INK, va="center")
    ax.text(6.2, 2.38, "Tracejado: descartado na inferência (fica só o que está em azul).", fontsize=8.5,
            color=MUTED, va="center")
    save(fig, top, "25-artigo-metodo", "Diagrama do método",
         "Sem dado: esquema do modelo de src/radibert/rte_modelo.py (RationaleBert) e do peso AUX_WEIGHT = 0,1 de "
         "src/radibert/rte_treino.py",
         "Azul: o que classifica e fica na inferência. Laranja tracejado: o decoder auxiliar, que gera a "
         "justificativa a partir dos estados do encoder e é descartado depois do treino.")


def fig_26_bracos():
    plan = results("esnli-treino-16k").iloc[-1]
    total, phase_a, phase_b = int(plan["total"]), int(plan["phase_a"]), int(plan["phase_b"])
    light = "#f3d98a"
    arms = [("Sem decoder, treino comum", [(1, total)], [], []),
            ("Sem decoder, mesmo calendário", [(phase_b + 1, total)], [], []),
            ("Com decoder, justificativa do par", [(phase_b + 1, total)], [(1, total)], [(-phase_a, 0)]),
            ("Com decoder, justificativa de outro par", [(phase_b + 1, total)], [(1, total)], [(-phase_a, 0)])]
    fig, ax, top = canvas(11.5, 4.6, "Os quatro braços: o que treina o encoder em cada trecho",
                          "e-SNLI, 16.000 pares. O braço de calendário isola o efeito de esperar; o de outro par isola "
                          "o conteúdo da justificativa.",
                          key=[("classificação (L_cls)", BLUE), ("gerar a justificativa (L_aux)", ORANGE),
                               ("gerar a justificativa com o encoder congelado (fase A)", light)])
    for position, (_, classify, generate, frozen) in zip(range(len(arms))[::-1], arms):
        for lane, spans, color in ((0.18, classify, BLUE), (-0.18, generate, ORANGE), (-0.18, frozen, light)):
            ax.broken_barh([(start, end - start + 1) for start, end in spans], (position + lane - 0.14, 0.28),
                           facecolors=color, edgecolor=SURFACE, linewidth=2)
    ax.set_yticks(range(len(arms))[::-1], [name for name, *_ in arms], fontsize=10, color=INK)
    ax.axvline(phase_b + 0.5, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.annotate(f"passo {thousands(phase_b)}: começa a classificação nos três braços de baixo",
                (phase_b, len(arms) - 0.3), xytext=(6, 0), textcoords="offset points", fontsize=8.5, color=MUTED,
                va="center")
    style(ax, "x")
    ax.set_xlim(-phase_a - 60, total + 60)
    ax.set_ylim(-0.6, len(arms) - 0.1)
    ax.set_xlabel(f"Passo de treino (os {phase_a} passos antes do zero são a fase A)", color=MUTED, fontsize=9)
    save(fig, top, "26-artigo-bracos", "Os quatro braços e o calendário de cada um",
         "resultados/esnli-treino-16k/pc/resultados.csv (colunas total, phase_a, phase_b) e as fases de "
         "src/radibert/rte_treino.py (training_loss, run_phase_a, braço bert_calendar)",
         "Cada braço tem duas faixas: em cima, os passos em que a classificação treina; embaixo, os passos em que "
         "gerar a justificativa treina. Nos dois braços com decoder o peso da geração é 0,1 depois do passo 1.200.")


GRADIENT_GRIDS = [("RTE (2.470 pares)", "rte-treino", "prop"), ("e-SNLI, 4.000 pares", "esnli-treino", None),
                  ("e-SNLI, 16.000 pares", "esnli-treino-16k", None),
                  ("e-SNLI, 16.000, justificativa de outro par", "esnli-treino-16k-embaralhado", None)]


def gradient_rows(folder: str, warmup: str | None) -> pd.DataFrame:
    rows = pd.read_csv(RES / folder / "pc" / "gradientes.csv", dtype={"warmup": str})
    return rows[rows["warmup"] == warmup] if warmup else rows


def fig_27_cosseno():
    fig, axes, top = canvas(14, 3.9, "O gradiente do decoder e o da classificação quase não se alinham",
                            "Cosseno entre o gradiente de gerar a justificativa e o de classificar, nos pesos do "
                            "encoder, ao longo do treino; BERT base, 5 sementes.", panels=4, sharey=True)
    for ax, (label, folder, warmup) in zip(axes, GRADIENT_GRIDS):
        rows = gradient_rows(folder, warmup)
        wide = rows.pivot(index="step", columns="seed", values="cos_c_a")
        for seed in wide:
            ax.plot(wide.index, wide[seed], color=BLUE, linewidth=0.7, alpha=0.35)
        ax.plot(wide.index, wide.mean(axis=1), color=BLUE, linewidth=2)
        ax.axhline(0, color=MUTED, linewidth=1)
        ax.axvline(rows.loc[rows["phase"] == "B", "step"].max(), color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
        style(ax)
        ax.set_title(label, loc="left", fontsize=9.5, color=MUTED)
        ax.set_xlabel("Passo de treino", color=MUTED, fontsize=9)
    axes[0].set_ylim(-0.35, 0.35)
    axes[0].set_ylabel("Cosseno (1 = mesma direção)", color=MUTED, fontsize=9)
    save(fig, top, "27-artigo-cosseno-dos-gradientes", "Cosseno entre o gradiente do decoder e o da classificação",
         "resultados/{rte-treino,esnli-treino,esnli-treino-16k,esnli-treino-16k-embaralhado}/pc/gradientes.csv "
         "(coluna cos_c_a; no RTE, só o aquecimento proporcional)",
         "Linha grossa: média das 5 sementes; linhas finas: cada semente. Zero quer dizer que gerar a "
         "justificativa empurra o encoder numa direção que nem ajuda nem atrapalha a classificação. A linha "
         "tracejada é o fim da fase em que só o decoder treina o encoder. Com 16.000 pares a média sobe a cerca de "
         "0,15 logo depois que a classificação começa e volta a zero. O eixo vai de -0,35 a 0,35: picos de sementes "
         "isoladas saem do quadro (no RTE uma chega a -0,73), sobretudo antes da linha tracejada, quando o "
         "gradiente de classificação é medido num modelo que ainda não classifica.")


def fig_28_empurrao():
    names = [("C", "copiada do par", BLUE), ("N", "nova, fora do par", ORANGE), ("S", "expressão de rótulo", AQUA),
             ("F", "gramatical", YELLOW)]
    fig, ax, top = canvas(11, 5.4, "De que palavras vem o empurrão do decoder no encoder",
                          "Fase de classificação, média das 5 sementes. Em cada condição: a parcela dos tokens da "
                          "justificativa e a parcela do gradiente.",
                          key=[(label, color) for _, label, color in names])
    labels, position = [], 0.0
    positions = []
    for grid, folder, warmup in GRADIENT_GRIDS:
        rows = gradient_rows(folder, warmup)
        rows = rows[rows["phase"] == "C"]
        for kind, prefix in (("tokens", "frac_tokens_"), ("empurrão", "share_")):
            shares = [100 * rows[f"{prefix}{group}"].mean() for group, _, _ in names]
            left = 0.0
            for share, (_, _, color) in zip(shares, names):
                ax.barh(position, share, left=left, color=color, height=0.62, edgecolor=SURFACE, linewidth=2)
                if share >= 6:
                    ax.text(left + share / 2, position, comma(share, 0), ha="center", va="center", fontsize=8.5,
                            color=INK)
                left += share
            labels.append(f"{grid}: {kind}")
            positions.append(position)
            position -= 0.75
        position -= 0.45
    ax.set_yticks(positions, labels, fontsize=9.5, color=INK)
    style(ax, "x")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Parcela (%)", color=MUTED, fontsize=9)
    save(fig, top, "28-artigo-empurrao-por-tipo-de-palavra", "De que palavras vem o empurrão do decoder",
         "resultados/{rte-treino,esnli-treino,esnli-treino-16k,esnli-treino-16k-embaralhado}/pc/gradientes.csv "
         "(colunas frac_tokens_* e share_*, fase C; no RTE, só o aquecimento proporcional)",
         "Para cada condição, a barra de cima é quanto de cada tipo de palavra há no alvo do decoder, e a de baixo "
         "é quanto do gradiente do decoder no encoder vem de cada tipo (medido na sonda). No braço de outro par "
         "quase nada do alvo está no par, então 'copiada' some e as palavras passam a contar como 'nova'.")


def fig_29_curva_tres_bracos():
    curve = RES / "esnli-treino-16k-curva"
    pc = pd.read_csv(curve / "pc" / "curva.csv")
    rows = pd.concat([pc[pc["seed"] <= 3], pd.read_csv(curve / "amigo" / "curva.csv")])
    arms = [("bert_calendar", "Sem decoder, mesmo calendário", BLUE),
            ("bert_decoder", "Com decoder, justificativa do par", ORANGE),
            ("bert_decoder_shuffled", "Com decoder, justificativa de outro par", AQUA)]
    seeds = {arm: sorted(rows.loc[rows["arm"] == arm, "seed"].unique()) for arm, _, _ in arms}
    if not seeds["bert_decoder_shuffled"]:
        raise SystemExit("figura 29: o braço embaralhado ainda não tem curva em curva.csv")
    rows = rows.assign(since=rows["step"] - 1200, accuracy=100 * rows["dev_accuracy"])
    wide = rows.pivot(index="since", columns=["arm", "seed"], values="accuracy")
    counts = ", ".join(f"{len(seeds[arm])}" for arm, _, _ in arms)
    fig, ax, top = canvas(9.8, 4.9, "Curva de arranque dos três braços com o mesmo calendário",
                          f"Acurácia no dev depois que a classificação começa; e-SNLI, 16.000 pares. Sementes por "
                          f"braço, na ordem da legenda: {counts}.")
    for arm, label, color in arms:
        for seed in wide[arm]:
            ax.plot(wide.index, wide[arm][seed], color=color, linewidth=0.8, alpha=0.3)
        mean = wide[arm].mean(axis=1)
        ax.plot(wide.index, mean, color=color, linewidth=2, marker="o", markersize=5, label=label)
        ax.annotate(comma(mean.iloc[0]), (wide.index[0], mean.iloc[0]), xytext=(-7, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=9, color=INK)
    style(ax)
    ax.set_xscale("log")
    ticks = [t for t in wide.index if t != 2300]
    ax.set_xticks(ticks, [thousands(t) for t in ticks], fontsize=8)
    ax.minorticks_off()
    ax.set_xlabel("Passos de classificação já dados (escala logarítmica)", color=MUTED, fontsize=9)
    ax.set_ylabel("Acurácia no dev (%)", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=9, loc="lower right", labelcolor=INK)
    save(fig, top, "29-artigo-curva-tres-bracos", "Curva de arranque: calendário, decoder e decoder embaralhado",
         "resultados/esnli-treino-16k-curva/pc/curva.csv (sementes 1 a 3) e amigo/curva.csv (sementes 4 e 5)",
         "Linha grossa: média das sementes disponíveis de cada braço; linhas finas: cada semente. O número à "
         "esquerda é a acurácia no primeiro passo medido (25 passos de classificação).")


def write_tables():
    """Markdown tables for the article: the 16,000-pair results, their paired differences, every grid's decoder
    effect, and three pairs with their own rationale and the swapped one."""
    grids = pd.concat([results("esnli-treino-16k"), results("esnli-treino-16k-calendario"),
                       results("esnli-treino-16k-embaralhado")])
    names = {"bert": "Sem decoder, treino comum", "bert_calendar": "Sem decoder, mesmo calendário",
             "bert_decoder": "Com decoder, justificativa do par",
             "bert_decoder_shuffled": "Com decoder, justificativa de outro par"}
    lines = ["# Tabelas para o artigo (geradas por `graficos_projeto.py` em 18/11/2026)", "",
             "Todas saem dos mesmos arquivos das figuras; nenhuma traz número digitado à mão.", "",
             "## 1. e-SNLI, 16.000 pares: os quatro braços", "",
             "Como ler: média e desvio padrão entre 5 sementes, no dev do e-SNLI (9.842 pares).", "",
             "| Braço | ROC-AUC | Acurácia (%) | Sementes |", "|---|---|---|---|"]
    for arm, label in names.items():
        rows = grids[grids["arm"] == arm]
        lines.append(f"| {label} | {comma(rows['roc_auc'].mean(), 3)} ± {comma(rows['roc_auc'].std(), 3)} | "
                     f"{comma(100 * rows['accuracy'].mean())} ± {comma(100 * rows['accuracy'].std())} | {len(rows)} |")
    lines += ["", "## 2. e-SNLI, 16.000 pares: diferenças pareadas", "",
              "Como ler: primeiro braço menos o segundo, semente a semente; entre parênteses o intervalo de 95%; "
              "acurácia em pontos percentuais.", "", "| Comparação | ROC-AUC | Acurácia (pontos) |", "|---|---|---|"]
    for arm, base in (("bert_calendar", "bert"), ("bert_decoder", "bert_calendar"),
                      ("bert_decoder_shuffled", "bert_calendar"), ("bert_decoder", "bert_decoder_shuffled")):
        cells = []
        for column, scale, digits in (("roc_auc", 1, 3), ("accuracy", 100, 1)):
            mean, half = interval(paired(grids, column, arm, base) * scale)
            cells.append(f"{comma(mean, digits, sign=True)} ({comma(mean - half, digits, sign=True)} a "
                         f"{comma(mean + half, digits, sign=True)})")
        lines.append(f"| {names[arm]} menos {names[base].lower()} | {cells[0]} | {cells[1]} |")
    rte, esnli4 = results("rte-treino"), results("esnli-treino")
    conditions = [("RTE, BERT base, aquecimento proporcional", rte[rte["warmup"] == "prop"], "bert_decoder", "bert"),
                  ("RTE, BERT base, aquecimento da Tabela 4", rte[rte["warmup"] == "500"], "bert_decoder", "bert"),
                  ("RTE, BERT MS-MARCO (nboost)", results("rte-msmarco"), "bert_decoder", "bert"),
                  ("RTE, BERT MS-MARCO (Capreolus)", results("rte-capreolus"), "bert_decoder", "bert"),
                  ("RTE, T5 v1.1 como encoder", results("rte-t5enc"), "t5enc_decoder", "t5enc"),
                  ("RTE, BERT small", results("rte-small"), "bert_decoder", "bert"),
                  ("RTE, BERT tiny", results("rte-tiny"), "bert_decoder", "bert"),
                  ("e-SNLI, 4.000 pares", esnli4, "bert_decoder", "bert"),
                  ("e-SNLI, 16.000 pares", results("esnli-treino-16k"), "bert_decoder", "bert")]
    lines += ["", "## 3. Decoder menos sem decoder, em todas as condições", "",
              "Como ler: diferença pareada de ROC-AUC com o intervalo de 95%; a coluna do meio é o ROC-AUC do braço "
              "sem decoder.", "", "| Condição | Sem decoder | Decoder menos sem decoder | Sementes |", "|---|---|---|---|"]
    for label, frame, arm, base in conditions:
        diff = paired(frame, "roc_auc", arm, base)
        mean, half = interval(diff)
        lines.append(f"| {label} | {comma(frame.loc[frame['arm'] == base, 'roc_auc'].mean(), 3)} | "
                     f"{comma(mean, 3, sign=True)} ({comma(mean - half, 3, sign=True)} a "
                     f"{comma(mean + half, 3, sign=True)}) | {len(diff)} |")
    from radibert import esnli_dados, rte_dados  # only here: the swapped rationales are recomputed, not stored

    pairs = esnli_dados.batch_pairs()
    swapped = rte_dados.shuffle_within_label(pairs, 0)
    lines += ["", "## 4. Três pares com a justificativa do par e a trocada", "",
              "Como ler: o primeiro par de cada rótulo no lote de 16.000; a justificativa trocada é a que o braço "
              "'de outro par' recebe (outro par do mesmo rótulo, troca fixa com semente 0).", "",
              "| Rótulo | Premissa | Hipótese | Justificativa do par (Qwen 35B) | Justificativa trocada |",
              "|---|---|---|---|---|"]
    for y, label in esnli_dados.LABELS.items():
        index = pairs.index[pairs["y"] == y][0]
        row = pairs.loc[index]
        lines.append(f"| {label} | {row['sentence1']} | {row['sentence2']} | {row['rationale']} | "
                     f"{swapped.loc[index, 'rationale']} |")
    (HERE / "tabelas-artigo.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


FIGURES = {name.split("_")[1]: function for name, function in list(globals().items()) if name.startswith("fig_")}
SECTIONS = [("Screening (Semanas 3 a 5)", "01", "04"), ("Geração das justificativas (outubro)", "05", "06"),
            ("Replicação do Agrawal e controles (9 a 18/11)", "07", "11"),
            ("Marcas de atenção e destaque (10 a 16/11)", "12", "16"), ("Destilação (16 a 18/11)", "17", "19"),
            ("Palavras novas e cabeça de grupos (17 e 18/11)", "20", "24"),
            ("Figuras que faltavam para o artigo (18/11)", "25", "29")]
WAITS_FOR_DATA = {"29"}  # drawn only when asked with --so: its run may not have finished


def write_index():
    lines = ["# Figuras do projeto, da Semana 3 a 18/11", "",
             "Geradas por `graficos_projeto.py` em 18/11/2026, a pedido do Pedro. Cada figura sai só de números "
             "lidos de arquivo; a coluna da fonte diz qual. Títulos que afirmam uma conclusão são leitura do Claude "
             "sobre os números da figura.", ""]
    for title, first, last in SECTIONS:
        lines += [f"## {title}", "", "| Figura | Fonte dos números | Como ler |", "|---|---|---|"]
        lines += [f"| `{entry['file']}`: {entry['title']} | {entry['source']} | {entry['how']} |"
                  for entry in INDEX if first <= entry["file"][:2] <= last]
        lines.append("")
    (HERE / "INDICE.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--so", nargs="+", choices=sorted(FIGURES), help="only these figure numbers (no index)")
    args = parser.parse_args()
    curve_ready = (RES / "esnli-treino-16k-curva" / "pc" / "curva.csv").read_text(encoding="utf-8").count(
        "bert_decoder_shuffled") > 0
    for number in args.so or sorted(FIGURES):
        if number in WAITS_FOR_DATA and not args.so and not curve_ready:
            print(f"pulada {number}: a curva do braço embaralhado ainda não existe", flush=True)
            continue
        FIGURES[number]()
        print("ok", INDEX[-1]["file"], flush=True)
    if not args.so:
        write_index()
        write_tables()


if __name__ == "__main__":
    main()
