"""The agent hook blocks what the project forbids and lets ordinary work through (matrix per rule)."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "guardrails.py"


def load_hook():
    spec = importlib.util.spec_from_file_location("guardrails", HOOK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bash(command: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": "."}


def write(path: str) -> dict:
    return {"tool_name": "Write", "tool_input": {"file_path": path, "content": "x"}}


BLOCKED = [
    (bash("git commit -m 'feat: x'"), "main"),
    (bash("cd pasta && git commit -am 'feat: x'"), "main"),
    (bash("git push"), "main"),
    (bash("git push origin main"), "feat/x"),
    (bash("git push origin HEAD:refs/heads/main"), "feat/x"),
    (bash("git push --force"), "feat/x"),
    (bash("git push -f origin feat/x"), "feat/x"),
    (bash("git push origin +feat/x"), "feat/x"),
    (bash("git commit --no-verify -m 'feat: x'"), "feat/x"),
    (bash("git commit -nm 'feat: x'"), "feat/x"),
    (bash("git -c core.hooksPath=/dev/null commit -m 'feat: x'"), "feat/x"),
    (bash("git config core.hooksPath outro"), "feat/x"),
    (bash("uv run pre-commit uninstall"), "feat/x"),
    (bash("echo SEGREDO=1 > .env"), "feat/x"),
    (bash("sed -i 's/x/y/' .claude/hooks/guardrails.py"), "feat/x"),
    ({"tool_name": "PowerShell", "tool_input": {"command": "git push --force"}}, "feat/x"),
    (write(".env"), "feat/x"),
    (write("config/.env.local"), "feat/x"),
    ({"tool_name": "Edit", "tool_input": {"file_path": ".claude/hooks/guardrails.py"}}, "feat/x"),
    (write(".claude/settings.json"), "feat/x"),
    ({"tool_input": {"command": "ls"}}, "feat/x"),
]
ALLOWED = [
    (bash("git commit -m 'feat: x'"), "feat/x"),
    (bash("git push -u origin feat/x"), "feat/x"),
    (bash("git status"), "main"),
    (bash("git checkout -b feat/x"), "main"),
    (bash("git pull --ff-only"), "main"),
    (bash("git log --oneline main"), "feat/x"),
    (bash("echo 'git push origin main'"), "feat/x"),
    (bash("uv run pre-commit install --hook-type commit-msg"), "feat/x"),
    (bash("cat .env.example"), "feat/x"),
    (write("src/radibert/novo.py"), "main"),
    ({"tool_name": "Read", "tool_input": {"file_path": ".claude/hooks/guardrails.py"}}, "feat/x"),
]


@pytest.mark.parametrize(("payload", "branch"), BLOCKED)
def test_blocks(payload, branch):
    assert load_hook().avaliar(payload, ramo=lambda cwd: branch) is not None


@pytest.mark.parametrize(("payload", "branch"), ALLOWED)
def test_allows(payload, branch):
    assert load_hook().avaliar(payload, ramo=lambda cwd: branch) is None


def run_script(stdin: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(HOOK)], input=stdin.encode(), capture_output=True)


def test_script_denies_with_json_decision():
    out = run_script(json.dumps(write(".env")))
    assert json.loads(out.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_script_allows_with_empty_json():
    out = run_script(json.dumps(write("src/radibert/novo.py")))
    assert json.loads(out.stdout) == {}


def test_script_denies_unreadable_payload():
    out = run_script("isto não é json")
    assert json.loads(out.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"
