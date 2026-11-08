"""The commit-msg hook must refuse Claude authorship lines and accept Claude as a subject of the text."""
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "scripts" / "hooks" / "sem_trailer_claude.py"

REFUSED = [
    "feat: x\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n",
    "feat: x\n\nco-authored-by: claude <noreply@anthropic.com>\n",
    "feat: x\n\nCo-authored-by: Someone <noreply@anthropic.com>\n",
    "docs: y\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n",
    "docs: y\n\nGenerated with Claude Code\n",
]
ACCEPTED = [
    "chore: estrutura inicial do repositório\n",
    "docs: Claude como gerador fica arquivado (Usage Policy)\n",
    "feat: x\n\nCo-Authored-By: Maria <maria@example.com>\n",
    "feat: x\n\n# Co-Authored-By: Claude <noreply@anthropic.com>\n",  # git strips comment lines
]


def run_hook(message: str, tmp_path: Path) -> int:
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text(message, encoding="utf-8")
    return subprocess.run([sys.executable, str(HOOK), str(msg_file)], capture_output=True).returncode


@pytest.mark.parametrize("message", REFUSED)
def test_refuses_claude_attribution(message, tmp_path):
    assert run_hook(message, tmp_path) == 1


@pytest.mark.parametrize("message", ACCEPTED)
def test_accepts_message_without_claude_attribution(message, tmp_path):
    assert run_hook(message, tmp_path) == 0
