"""Guardrail do RaDi-BERT: hook PreToolUse do Claude Code (só biblioteca padrão).

Recusa, antes de a ferramenta rodar:
- GIT: commit ou push no `main`, push para o `main`, push forçado, `--no-verify`, mudar o `core.hooksPath`,
  desinstalar o pre-commit. Trabalho vai por branch `tipo/descricao` e PR.
- PROTEGIDO: escrever em `.env*`, em `.claude/hooks/` ou em `.claude/settings.json` (o agente não desliga a própria
  guarda).

Contrato: recebe o payload JSON na entrada padrão; para barrar imprime a decisão `deny` com o motivo, para deixar
passar imprime `{}`. Falha fechada: payload ilegível, sem `tool_name`, comando que não dá para ler ou erro interno
barram (erro fora da análise sai com exit 2, que o Claude Code também trata como bloqueio).

Limite: é leitura da string do comando, não sandbox. Variável de shell, script que escreve por dentro ou alias
contornam. Serve contra o erro distraído (adaptado do guardrail do ULTIMATUM).
"""
import json
import re
import shlex
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTECTED_BRANCH = "main"
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
FILE_WRITERS = {"tee", "cp", "mv", "set-content", "add-content", "out-file", "new-item"}
REDIRECT = re.compile(r"^\d?>>?(.*)$")


class Unreadable(Exception):
    pass


def is_protected(path: str) -> bool:
    rel = Path(path).as_posix().removeprefix("./")
    name = rel.rsplit("/", 1)[-1]
    return name.startswith(".env") and name != ".env.example" or rel.startswith(".claude/hooks/") or \
        rel == ".claude/settings.json" or rel.endswith("/.claude/settings.json") or "/.claude/hooks/" in rel


def split_commands(command: str) -> list[str]:
    """Split on `;`, `&&`, `||`, `|`, `&` and newlines that sit outside quotes."""
    parts, current, single, double = [], [], False, False
    for i, c in enumerate(command):
        if c == "'" and not double:
            single = not single
        elif c == '"' and not single:
            double = not double
        elif not single and not double and c in ";|&\n" and not (c == "&" and command[i - 1 : i] in {">", "<"}):
            parts.append("".join(current))
            current = []
            continue
        current.append(c)
    if single or double:
        raise Unreadable("aspas sem par")
    parts.append("".join(current))
    return [p.strip() for p in parts if p.strip()]


def tokens(segment: str, powershell: bool) -> list[str]:
    try:
        if powershell:
            return [t.strip("\"'") for t in shlex.split(segment, posix=False)]
        return shlex.split(segment, posix=True)
    except ValueError as exc:
        raise Unreadable(str(exc)) from exc


def program(token: str) -> str:
    return re.split(r"[\\/]", token)[-1].lower().removesuffix(".exe")


def git_reason(args: list[str], branch: str | None) -> str | None:
    i = 0
    while i < len(args) and args[i].startswith("-"):
        if args[i] == "-c" and i + 1 < len(args) and args[i + 1].lower().startswith("core.hookspath"):
            return "GIT: mudar o core.hooksPath desliga os ganchos do pre-commit."
        i += 2 if args[i] in {"-C", "-c", "--git-dir", "--work-tree"} else 1
    if i >= len(args):
        return None
    sub, rest = args[i], args[i + 1 :]
    if sub == "config" and any(t.lower() == "core.hookspath" for t in rest):
        return "GIT: mudar o core.hooksPath desliga os ganchos do pre-commit."
    if sub not in {"commit", "push"}:
        return None
    short = "".join(t[1:] for t in rest if re.match(r"^-[a-zA-Z]+$", t))
    if "--no-verify" in rest or (sub == "commit" and "n" in short):
        return "GIT: `--no-verify` pula os ganchos do pre-commit."
    if sub == "push":
        refspecs = [t for t in rest if not t.startswith("-")][1:]
        if any(t.startswith("--force") for t in rest) or "f" in short or any(r.startswith("+") for r in refspecs):
            return "GIT: push forçado reescreve histórico publicado."
        if any(r.split(":")[-1].removeprefix("refs/heads/") == PROTECTED_BRANCH for r in refspecs):
            return "GIT: nada vai direto para o main; abra um PR."
    if branch == PROTECTED_BRANCH:
        return "GIT: commit e push no main, não; crie um branch tipo/descricao e abra um PR."
    return None


def segment_reason(toks: list[str], branch: str | None) -> str | None:
    if not toks:
        return None
    name, args = program(toks[0]), toks[1:]
    targets = [m.group(1) or (args[i + 1] if i + 1 < len(args) else "")
               for i, t in enumerate(args) if (m := REDIRECT.match(t))]
    edits = name in FILE_WRITERS or (name == "sed" and any(re.match(r"^(-[a-zA-Z]*i|--in-place)", t) for t in args))
    if edits:
        targets += [t for t in args if not t.startswith("-")]
    if any(is_protected(t) for t in targets if t):
        return "PROTEGIDO: .env, .claude/hooks/ e .claude/settings.json não se escrevem pelo agente."
    if name == "git":
        return git_reason(args, branch)
    if "pre-commit" in [program(t) for t in toks] and "uninstall" in args:
        return "GIT: desinstalar o pre-commit desliga os ganchos."
    return None


def current_branch(cwd: str) -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd or None,
                             capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() or None


def avaliar(payload: object, ramo: Callable[[str], str | None] = current_branch) -> str | None:
    """Reason to block the call, or None to let it through."""
    if not isinstance(payload, dict) or not isinstance(payload.get("tool_name"), str):
        return "payload sem `tool_name`; barrado por precaução (falha fechada)."
    tool, entry = payload["tool_name"], payload.get("tool_input")
    if not isinstance(entry, dict):
        return "payload sem `tool_input`; barrado por precaução (falha fechada)."
    if tool in FILE_TOOLS:
        path = str(entry.get("file_path") or entry.get("notebook_path") or "")
        try:
            path = Path(path).resolve().relative_to(ROOT).as_posix() if Path(path).is_absolute() else path
        except ValueError:
            pass
        return "PROTEGIDO: .env, .claude/hooks/ e .claude/settings.json não se escrevem pelo agente." \
            if is_protected(path) else None
    if tool in {"Bash", "PowerShell"}:
        branch = ramo(str(payload.get("cwd") or ROOT))
        try:
            for segment in split_commands(str(entry.get("command") or "")):
                if reason := segment_reason(tokens(segment, tool == "PowerShell"), branch):
                    return reason
        except Unreadable as exc:
            return f"comando que o guardrail não consegue ler ({exc}); reescreva sem a construção ambígua."
    return None


def respond(reason: str | None) -> None:
    if reason is None:
        print("{}")
        return
    text = f"Bloqueado pelo guardrail do projeto: {reason}"
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": text}, "systemMessage": text},
                     ensure_ascii=False))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        payload = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace") or "null")
    except ValueError:
        respond("payload ilegível; barrado por precaução (falha fechada).")
        return
    try:
        respond(avaliar(payload))
    except Exception as exc:  # internal error must not open the gate
        respond(f"erro interno do guardrail ({type(exc).__name__}: {exc}); barrado por precaução.")


if __name__ == "__main__":
    try:
        main()
    except BaseException as exc:  # even a broken stdout blocks: exit 2 is a block in Claude Code
        sys.stderr.write(f"guardrail do projeto: falha ({type(exc).__name__}); barrado por precaução.\n")
        sys.exit(2)
