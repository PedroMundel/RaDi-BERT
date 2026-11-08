"""commit-msg hook: refuse any authorship line crediting Claude (Pedro, 08/11/2026: never co-commit with Claude).

Only attribution is refused. Claude as the subject of the text ("Claude como gerador fica arquivado") passes.
Usage (by pre-commit): python scripts/hooks/sem_trailer_claude.py <commit message file>
"""
import re
import sys
from pathlib import Path

ATTRIBUTION = [
    re.compile(r"^co-authored-by:.*(claude|anthropic)", re.IGNORECASE),
    re.compile(r"generated with \[?claude code", re.IGNORECASE),
]


def claude_attribution_lines(message: str) -> list[str]:
    """Lines of the message (git comment lines excluded) that credit Claude as an author."""
    lines = [line.strip() for line in message.splitlines() if not line.lstrip().startswith("#")]
    return [line for line in lines if any(p.search(line) for p in ATTRIBUTION)]


def main() -> int:
    message = Path(sys.argv[1]).read_text(encoding="utf-8")
    found = claude_attribution_lines(message)
    if not found:
        return 0
    print("Commit recusado: linha de autoria do Claude na mensagem (regra do Pedro, 08/11/2026).", file=sys.stderr)
    for line in found:
        print(f"  {line}", file=sys.stderr)
    print("Tire a linha e faça o commit de novo.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
