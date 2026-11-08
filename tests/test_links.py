"""Every relative link in a tracked .md file must point to a file or folder that exists."""
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(<?([^)>\s#]+)(?:#[^)\s>]*)?>?\)")


def looks_like_path(target: str) -> bool:
    """Formulas such as `p(y|x)](y)` match the link syntax; only targets with a folder or an extension are paths."""
    return "/" in target or bool(Path(target).suffix)


def broken_links(md_file: Path) -> list[str]:
    targets = LINK.findall(md_file.read_text(encoding="utf-8"))
    relative = [t for t in targets if not re.match(r"^[a-z]+:", t) and not t.startswith("/") and looks_like_path(t)]
    return [t for t in relative if not (md_file.parent / unquote(t)).exists()]


def tracked_md_files() -> list[Path]:
    names = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True, check=True)
    return [ROOT / n for n in names.stdout.splitlines()]


def test_detects_a_broken_link(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text("[ok](doc.md) [morto](pasta/nao-existe.md) formula p(y|x)](y)", encoding="utf-8")
    assert broken_links(doc) == ["pasta/nao-existe.md"]


def test_tracked_markdown_has_no_broken_relative_link():
    broken = {str(f.relative_to(ROOT)): b for f in tracked_md_files() if (b := broken_links(f))}
    assert broken == {}
