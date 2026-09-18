from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    ROOT / "codex" / "three-tier-system",
    ROOT / "zcode" / "three-tier-system",
]
REQUIRED = [
    ROOT / "README.md",
    ROOT / "LICENSE",
    SKILLS[0] / "SKILL.md",
    SKILLS[0] / "agents" / "openai.yaml",
    SKILLS[1] / "SKILL.md",
    SKILLS[1] / "profiles" / "employee.md",
    SKILLS[1] / "tools" / "sync-employee-profile.ps1",
]
REMOVED_GATE_PATHS = [
    SKILLS[1] / "references" / "supervision.md",
    SKILLS[1] / "references" / "mechanics.md",
    SKILLS[1] / "tools" / "README.md",
    SKILLS[1] / "tools" / "gate.py",
    SKILLS[1] / "tools" / "fleet.py",
    SKILLS[1] / "tools" / "cruise-gate.ps1",
    SKILLS[1] / "tools" / "cruise-fleet.ps1",
    SKILLS[1] / "tools" / "run_tests.py",
]
FORBIDDEN_PARTS = {"__pycache__", ".pytest_cache"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}
PRIVATE_MARKERS = (
    "C:" + "\\Users\\",
    "C:/" + "Users/",
    "279" + "61",
    "茉莉" + "知识库",
    "afc793e1-" + "734f-4d05-874f-788ac0a54184",
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")


def check_skill(skill: Path, errors: list[str]) -> None:
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"missing YAML frontmatter: {skill / 'SKILL.md'}")
        return
    frontmatter = match.group(1)
    if not re.search(r"(?m)^name:\s*three-tier-system\s*$", frontmatter):
        errors.append(f"unexpected skill name: {skill / 'SKILL.md'}")
    if not re.search(r"(?m)^description:\s*\S", frontmatter):
        errors.append(f"missing description: {skill / 'SKILL.md'}")


def check_markdown_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(text):
        target = match.group(1)
        if re.match(r"^(?:https?|mailto):", target):
            continue
        if not (path.parent / target).exists():
            errors.append(f"broken link: {path.relative_to(ROOT)} -> {target}")


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
    for path in REMOVED_GATE_PATHS:
        if path.exists():
            errors.append(f"removed cruise-gate file returned: {path.relative_to(ROOT)}")

    for skill in SKILLS:
        if (skill / "SKILL.md").is_file():
            check_skill(skill, errors)

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if any(part in FORBIDDEN_PARTS for part in path.parts):
            errors.append(f"generated directory in release: {path.relative_to(ROOT)}")
            continue
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"generated file in release: {path.relative_to(ROOT)}")
        if not path.is_file():
            continue
        if path.suffix.lower() == ".md":
            check_markdown_links(path, errors)
        if path.suffix.lower() in {".md", ".yaml", ".yml", ".py", ".ps1", ".json"}:
            text = path.read_text(encoding="utf-8")
            for marker in PRIVATE_MARKERS:
                if marker in text:
                    errors.append(
                        f"private marker {marker!r}: {path.relative_to(ROOT)}"
                    )

    if errors:
        print("Release validation failed:")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1
    print("Release validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
