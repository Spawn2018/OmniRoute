#!/usr/bin/env python3
"""CURRENT.md → README / ARCHITECTURE / PLAN. GitHub nie aktualizuje się sam.

Agent bywa omijał README. Gate --check pada przy rozjeździe, żeby origin
nie kłamał „następny = Charge 0.25” przy plasterze 3.0.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "docs" / "state" / "CURRENT.md"
README = ROOT / "README.md"
ARCHITECTURE = ROOT / "docs" / "ARCHITECTURE.md"
PLAN = ROOT / "docs" / "PLAN-REALIZACJA.md"
PROGRAM = ROOT / "docs" / "state" / "PROGRAM-12M.md"
AGENTS = ROOT / "AGENTS.md"

STATUS_START = "<!-- os-status:start -->"
STATUS_END = "<!-- os-status:end -->"
TREE_START = "<!-- os-tree:start -->"
TREE_END = "<!-- os-tree:end -->"
START_START = "<!-- os-start:start -->"
START_END = "<!-- os-start:end -->"

_FIELD = re.compile(r"^\*\*(Ostatni plaster|Etap|Następny):\*\*\s*(.+)$")


class OsStatus:
    last_plaster: str
    etap: str
    next_step: str

    def __init__(self, last_plaster: str, etap: str, next_step: str) -> None:
        self.last_plaster = last_plaster
        self.etap = etap
        self.next_step = next_step

    @property
    def command(self) -> str:
        # Etap Plan = wydmuszka; Refaktor = slot /refaktor; inaczej /plaster.
        etap = self.etap.casefold()
        if "plan" in etap:
            return "/plan-modul"
        if "refaktor" in etap:
            return "/refaktor"
        return "/plaster"


def parse_current(text: str) -> OsStatus:
    found: dict[str, str] = {}
    for line in text.splitlines():
        match = _FIELD.match(line.strip())
        if match is None:
            continue
        found[match.group(1)] = match.group(2).strip()
    missing = [name for name in ("Ostatni plaster", "Etap", "Następny") if name not in found]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"CURRENT.md bez pól: {joined}")
    return OsStatus(found["Ostatni plaster"], found["Etap"], found["Następny"])


def package_dirs(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    names = [
        path.name
        for path in root.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and path.name != "__pycache__"
    ]
    return sorted(names)


def _mid(start: str, end: str, inner: str) -> str:
    return f"{start}\n{inner.rstrip()}\n{end}"


def replace_marked(text: str, start: str, end: str, inner: str, label: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text) is None:
        raise ValueError(f"{label}: brak {start}")
    return pattern.sub(_mid(start, end, inner), text, count=1)


def render_readme(status: OsStatus) -> str:
    return (
        f"- **Ostatni plaster:** {status.last_plaster}\n"
        f"- **Etap:** {status.etap}\n"
        f"- **Następny:** {status.next_step}\n"
        f"- **Komenda teraz:** `{status.command}` "
        f"(z `docs/state/CURRENT.md`; Plan → `/plan-modul`, Refaktor → `/refaktor`, inaczej `/plaster`)\n"
        f"- **Jedyny plan:** `docs/PLAN-REALIZACJA.md` · `docs/state/CURRENT.md`"
    )


def _one_sentence(piece: str) -> str:
    return piece[:-1] if piece.endswith(".") else piece


def render_architecture_status(status: OsStatus) -> str:
    return (
        f"**Status:** {_one_sentence(status.last_plaster)}. "
        f"**Etap:** {_one_sentence(status.etap)}. "
        f"**Następny:** {status.next_step} "
        f"Plan: [PLAN-REALIZACJA.md](PLAN-REALIZACJA.md)."
    )


def render_tree() -> str:
    features = " · ".join(package_dirs(ROOT / "frontend" / "src" / "features"))
    services = " · ".join(package_dirs(ROOT / "backend" / "app" / "services"))
    return (
        "```\n"
        "frontend/                 React 19 + Compiler, Vite, TanStack, shadcn, PostHog\n"
        f"  src/features/           {features}\n"
        "  src/components/ui/      shadcn\n"
        "  src/components/data-table/  DataTableShell (Golden Standard)\n"
        "backend/app/\n"
        "  api/             routery, DTO, require_permission — bez logiki\n"
        f"  services/        {services}\n"
        "  repositories/    dostęp SQL\n"
        "  models/          SQLAlchemy\n"
        "  domain/          typy, wyjątki, Money\n"
        "  ai_transforms/   ekstrakcja → JSON (stateless, HITL)\n"
        "  workflows/       Temporal (wizja — nie działający system)\n"
        "  integrations/    OpenFGA, docling, langfuse (trace przy extract; no-op bez kluczy)\n"
        "authz/             model.fga (źródło prawdy AuthZ)\n"
        "```"
    )


def render_plan_status(status: OsStatus) -> str:
    return f"**Następny (zablokowany):** {status.next_step}"


def render_plan_start(status: OsStatus) -> str:
    if status.command == "/plan-modul":
        other = "/plaster"
    elif status.command == "/refaktor":
        other = "/plaster"
    else:
        other = "/plan-modul"
    return (
        f"**Teraz:** `{status.command}` (Etap z CURRENT.md).\n\n"
        "```\n"
        f"{status.command}\n"
        "```\n\n"
        "Kontekst: `@docs/state/CURRENT.md` `@docs/PLAN-REALIZACJA.md` `@GROUNDING.md`\n\n"
        f"Druga komenda (`{other}`) tylko gdy CURRENT zmieni Etap."
    )


def render_program(status: OsStatus) -> str:
    return f"**Stan (z CURRENT.md):** {status.last_plaster} **Następny:** {status.next_step}"


def apply_all(status: OsStatus) -> dict[Path, str]:
    readme = replace_marked(README.read_text(encoding="utf-8"), STATUS_START, STATUS_END, render_readme(status), "README.md")
    arch = ARCHITECTURE.read_text(encoding="utf-8")
    arch = replace_marked(arch, STATUS_START, STATUS_END, render_architecture_status(status), "ARCHITECTURE status")
    arch = replace_marked(arch, TREE_START, TREE_END, render_tree(), "ARCHITECTURE tree")
    plan = PLAN.read_text(encoding="utf-8")
    plan = replace_marked(plan, STATUS_START, STATUS_END, render_plan_status(status), "PLAN status")
    plan = replace_marked(plan, START_START, START_END, render_plan_start(status), "PLAN start")
    program = replace_marked(
        PROGRAM.read_text(encoding="utf-8"),
        STATUS_START,
        STATUS_END,
        render_program(status),
        "PROGRAM-12M.md",
    )
    return {
        README: readme,
        ARCHITECTURE: arch,
        PLAN: plan,
        PROGRAM: program,
    }


def agents_kanon_ok(text: str) -> bool:
    return "Plan realizacji (jedyny)" in text and "docs/PLAN-REALIZACJA.md" in text


def run(*, check: bool) -> int:
    status = parse_current(CURRENT.read_text(encoding="utf-8"))
    if not agents_kanon_ok(AGENTS.read_text(encoding="utf-8")):
        print("AGENTS.md: brak kanonu Plan realizacji (jedyny) → docs/PLAN-REALIZACJA.md")
        return 1
    rendered = apply_all(status)
    drifted: list[str] = []
    for path, new_text in rendered.items():
        old = path.read_text(encoding="utf-8")
        if old == new_text:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if check:
            drifted.append(rel)
            continue
        path.write_text(new_text, encoding="utf-8", newline="\n")
    if check and drifted:
        print("OS status rozjechany z CURRENT.md. Uruchom: just docs")
        for rel in drifted:
            print(f"  {rel}")
        return 1
    print("sync_os_status: OK")
    return 0


def main() -> int:
    check = "--check" in sys.argv[1:]
    try:
        return run(check=check)
    except ValueError as exc:
        print(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
