"""Project paths, resolved from the package location so every module runs from any working directory."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ESNLI = ROOT / "dados" / "esnli"
ESNLI_DEV = ESNLI / "esnli_dev.csv"
WIEGREFFE = ROOT / "dados" / "wiegreffe2022"

RESULTADOS = ROOT / "resultados"
PILOTO_PROFESSORES = RESULTADOS / "piloto-professores"
PILOTO_QWEN = RESULTADOS / "piloto-qwen"
COPIA = RESULTADOS / "s6-copia-esnli"
LOTE_35B = RESULTADOS / "lote-35B"
