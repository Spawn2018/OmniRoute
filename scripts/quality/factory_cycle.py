#!/usr/bin/env python3
"""Jedno wejście taśmy: retrieve + podłoga + (close) bench/CI. Nie rusza HC."""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "docs" / "state" / "CURRENT.md"
KNOWLEDGE = ROOT / "docs" / "_knowledge"
CASES = ROOT / "docs" / "_bench" / "cases"
TOKEN = re.compile(r"[a-z0-9]{3,}")
QUALITY = Path(__file__).resolve().parent


def _run(script: str, *args: str) -> int:
    return subprocess.call([sys.executable, str(QUALITY / script), *args], cwd=ROOT)


def _tokens(text: str) -> set[str]:
    return set(TOKEN.findall(text.casefold()))


def _summarize(path: Path, limit: int = 4) -> str:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    body = [line for line in lines if not line.startswith("#")][:limit]
    rel = path.relative_to(ROOT).as_posix()
    return rel + "\n  " + "\n  ".join(body)


def retrieve(limit: int = 12) -> list[str]:
    current = CURRENT.read_text(encoding="utf-8") if CURRENT.is_file() else ""
    want = _tokens(current)
    cards = list(KNOWLEDGE.rglob("machine-*.md"))
    tools = KNOWLEDGE / "tools"
    if tools.is_dir():
        cards.extend(tools.glob("*.md"))
    scored: list[tuple[int, Path]] = []
    seen: set[Path] = set()
    for path in cards:
        if path in seen or path.name == "README.md":
            continue
        seen.add(path)
        score = 3 if path.name.startswith("machine-") else 0
        score += len(want & _tokens(path.name + " " + path.read_text(encoding="utf-8")[:800]))
        scored.append((score, path))
    scored.sort(key=lambda pair: (-pair[0], pair[1].as_posix()))
    picked = [path for _score, path in scored[:8]]
    benches = sorted(CASES.glob("*.md"), reverse=True) if CASES.is_dir() else []
    picked.extend(path for path in benches[:4] if path.name != "TEMPLATE.md")
    return [_summarize(path) for path in picked[:limit]]


def print_retrieve() -> None:
    print("factory_cycle retrieve (stosuj, nie dumpuj katalogu):", flush=True)
    items = retrieve()
    if not items:
        print("  (brak kart)", flush=True)
        return
    for item in items:
        print(f"- {item}", flush=True)


def start(phase: str) -> int:
    if phase != "noc":
        pre = subprocess.call(
            [sys.executable, str(QUALITY / "writer_preflight.py")],
            cwd=ROOT,
        )
        if pre != 0:
            return pre
    print_retrieve()
    if _run("repeat_learn.py") != 0:
        return 1
    if phase == "plaster" and _product_delta_missing():
        print(
            "factory_cycle: brak delty produktu w docs/deltas/open/ "
            "(pliki OS-* sie nie licza). Najpierw /plan-modul.",
            flush=True,
        )
        return 1
    return _run("quality_floor.py", "--check")


def _product_delta_missing() -> bool:
    path = QUALITY / "craft_oracles.py"
    spec = importlib.util.spec_from_file_location("craft_oracles_start", path)
    if spec is None or spec.loader is None:
        return True
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return not module.product_open_deltas(module.OPEN)


def close() -> int:
    if _run("craft_close.py", "--write") != 0:
        return 1
    if _run("repeat_learn.py", "--write") != 0:
        return 1
    if _run("quality_floor.py", "--write") != 0:
        return 1
    print_retrieve()
    print("factory_cycle close: OK (nie edytuj GROUNDING, nie dopisuj zasad do AGENTS)")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", choices=("plan", "plaster", "refactor", "noc"))
    parser.add_argument("--close", action="store_true")
    args = parser.parse_args()
    if args.close:
        return close()
    if args.start:
        return start(args.start)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
