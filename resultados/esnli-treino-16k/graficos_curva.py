"""Figures of the 16,000-pair e-SNLI results of 18/11: the learning curve (decoder arm against the calendar arm)
and the final accuracy of the four arms. Reads the CSVs already copied from the machines; trains nothing.

    uv run --frozen --with matplotlib python resultados/esnli-treino-16k/graficos_curva.py
Writes figs/curva-de-arranque.png and figs/acuracia-final-quatro-bracos.png next to this file. Labels are in
Portuguese: the figures go into Pedro's gate documents.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

HERE = Path(__file__).parent
CURVE = HERE.with_name("esnli-treino-16k-curva")
FIGS = HERE / "figs"
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
# one colour per arm, the same in both figures (categorical slots in fixed order; validated for colour blindness)
ARMS = {"bert_calendar": ("Sem decoder, mesmo calendário", "#2a78d6"),
        "bert_decoder": ("Com decoder, justificativa do par", "#eb6834"),
        "bert_decoder_shuffled": ("Com decoder, justificativa de outro par", "#1baf7a"),
        "bert": ("Sem decoder, treino comum", "#eda100")}
CLASSIFICATION_STARTS = 1200  # the last step of phase B: both arms take their first classification step at 1,201
PC_SEEDS = 3  # seeds 1-3 ran on Pedro's PC, 4-5 on the friend's machine; each seed has both arms on one machine


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, length=0, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def curve_rows() -> pd.DataFrame:
    pc = pd.read_csv(CURVE / "pc" / "curva.csv")
    friend = pd.read_csv(CURVE / "amigo" / "curva.csv")
    rows = pd.concat([pc[pc["seed"] <= PC_SEEDS], friend])
    return rows.assign(since=rows["step"] - CLASSIFICATION_STARTS, accuracy=100 * rows["dev_accuracy"])


def half_interval(values: pd.Series) -> float:
    return stats.t.ppf(0.975, len(values) - 1) * values.std() / len(values) ** 0.5


def curve_figure(rows: pd.DataFrame):
    by_arm = rows.pivot(index="since", columns=["arm", "seed"], values="accuracy")
    ticks = list(by_arm.index)
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(9, 7.6), sharex=True, height_ratios=(3, 2), facecolor=SURFACE)
    for arm in ("bert_calendar", "bert_decoder"):
        label, color = ARMS[arm]
        for seed in by_arm[arm]:
            top.plot(ticks, by_arm[arm][seed], color=color, linewidth=0.8, alpha=0.35)
        mean = by_arm[arm].mean(axis=1)
        top.plot(ticks, mean, color=color, linewidth=2, marker="o", markersize=5, label=label)
        top.annotate(f"{mean.iloc[0]:.1f}".replace(".", ","), (ticks[0], mean.iloc[0]), xytext=(-8, 0),
                     textcoords="offset points", ha="right", va="center", fontsize=9, color=INK)
        nudge = 5 if arm == "bert_calendar" else -5  # the two end labels are less than a point apart
        top.annotate(f"{mean.iloc[-1]:.1f}".replace(".", ","), (ticks[-1], mean.iloc[-1]), xytext=(8, nudge),
                     textcoords="offset points", ha="left", va="center", fontsize=9, color=INK)
    style(top)
    top.set_xscale("log")
    top.set_ylabel("Acurácia no dev (%)", color=MUTED, fontsize=10)
    top.legend(frameon=False, fontsize=10, loc="lower right", labelcolor=INK)
    top.set_title("O decoder adianta o começo e termina atrás", loc="left", color=INK, fontsize=13, pad=26,
                  fontweight="bold")
    top.text(0, 1.04, "e-SNLI, 16.000 pares de treino, BERT base. Linha grossa: média de 5 sementes; linhas finas: "
             "cada semente.", transform=top.transAxes, color=MUTED, fontsize=9)

    gain = by_arm["bert_decoder"] - by_arm["bert_calendar"]  # paired by seed
    mean, half = gain.mean(axis=1), gain.apply(half_interval, axis=1)
    bottom.axhline(0, color=MUTED, linewidth=1)
    bottom.errorbar(ticks, mean, yerr=half, color=INK, linewidth=0, elinewidth=1.4, capsize=3, marker="o",
                    markersize=5)
    for x, y, offset in ((ticks[0], mean.iloc[0], (8, 4)), (ticks[1], mean.iloc[1], (8, 4)),
                         (ticks[-1], mean.iloc[-1], (-4, 16))):
        bottom.annotate(f"{y:+.2f}".replace(".", ","), (x, y), xytext=offset, textcoords="offset points", fontsize=9,
                        color=INK, ha="left" if offset[0] > 0 else "center")
    style(bottom)
    bottom.set_ylabel("Com decoder menos sem decoder\n(pontos de acurácia)", color=MUTED, fontsize=10)
    bottom.set_xlabel("Passos de classificação já dados (escala logarítmica; a classificação começa depois de 1.200 "
                      "passos nos dois braços)", color=MUTED, fontsize=9)
    crowded = {2300}  # its label would run into 2,800's on the log scale; the point stays
    bottom.set_xticks(ticks, ["" if t in crowded else f"{t:,}".replace(",", ".") for t in ticks], fontsize=8)
    bottom.minorticks_off()
    bottom.text(0, 1.04, "Diferença pareada por semente; barras: intervalo de 95%.", transform=bottom.transAxes,
                color=MUTED, fontsize=9)
    fig.tight_layout()
    fig.savefig(FIGS / "curva-de-arranque.png", dpi=160, facecolor=SURFACE)
    plt.close(fig)


def final_figure():
    rows = pd.concat([pd.read_csv(HERE.with_name(name) / "pc" / "resultados.csv") for name in
                      ("esnli-treino-16k", "esnli-treino-16k-calendario", "esnli-treino-16k-embaralhado")])
    rows = rows.assign(accuracy=100 * rows["accuracy"])
    order = ["bert_calendar", "bert", "bert_decoder", "bert_decoder_shuffled"]
    fig, ax = plt.subplots(figsize=(9, 3.6), facecolor=SURFACE)
    for position, arm in enumerate(reversed(order)):
        label, color = ARMS[arm]
        values = rows.loc[rows["arm"] == arm, "accuracy"]
        ax.scatter(values, [position] * len(values), s=42, color=color, alpha=0.45, linewidths=0)
        ax.scatter([values.mean()], [position], s=150, color=color, edgecolors=SURFACE, linewidths=2, zorder=3)
        ax.annotate(f"{values.mean():.1f}".replace(".", ","), (values.mean(), position), xytext=(0, 13),
                    textcoords="offset points", ha="center", fontsize=10, color=INK)
    style(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_yticks(range(len(order)), [ARMS[arm][0] for arm in reversed(order)], fontsize=10, color=INK)
    ax.set_ylim(-0.6, len(order) - 0.3)
    ax.set_xlabel("Acurácia no dev ao fim do treino (%)", color=MUTED, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.86))  # the title sits on the figure: the long arm names push the axes right
    fig.text(0.02, 0.94, "A justificativa certa custa pouco; a de outro par custa muito", color=INK, fontsize=13,
             fontweight="bold")
    fig.text(0.02, 0.88, "e-SNLI, 16.000 pares, BERT base. Ponto grande: média de 5 sementes; pontos pequenos: cada "
             "semente.", color=MUTED, fontsize=9)
    fig.savefig(FIGS / "acuracia-final-quatro-bracos.png", dpi=160, facecolor=SURFACE)
    plt.close(fig)


def main():
    FIGS.mkdir(exist_ok=True)
    curve_figure(curve_rows())
    final_figure()
    print("figuras em", FIGS)


if __name__ == "__main__":
    main()
