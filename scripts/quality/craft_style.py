#!/usr/bin/env python3
"""OS-4: zapach slopu z no-slop.mdc. Nie robi z agenta człowieka. Nie rusza HC."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAX_FN_LINES = 40
BANNED_STEMS = frozenset(
    {"utils", "helper", "helpers", "manager", "handlers", "misc", "common"}
)
SHADCN_CN = "frontend/src/lib/utils.ts"
TODO = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")
EXCEPT = re.compile(r"except (Exception|BaseException)\b")
BARE_EXCEPT = re.compile(r"except\s*:")
FLOAT_CALL = re.compile(r"\bfloat\s*\(")
HTTP_RAISE = re.compile(r"raise HTTPException\b")
BANNER = re.compile(r"^#\s*[-=*#]{4,}")
TS_BANNER = re.compile(r"^//\s*[-=*#]{4,}")
COMMENTED = re.compile(r"^#\s*(?:async\s+)?(?:def |class |import |from \w+ import)")
AS_ANY = re.compile(r"\bas any\b")
COLON_ANY = re.compile(r":\s*any\b")
EMOJI = re.compile("[\U0001f300-\U0001faff\U00002700-\U000027bf\U00002600-\U000026ff]")
DEF_LINE = re.compile(r"(?:async )?def (\w+)\s*\(")
SLOP_DOC = ("Args:", "Arguments:", "Parameters:", "Returns:", "Raises:", ":param")
SLOP_CLASS = ("Factory", "Manager", "Helper", "Utils", "Handler")


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _note(rel: str, lineno: int, msg: str) -> str:
    return f"{rel}:{lineno}: {msg}"


def py_sources() -> list[Path]:
    app = ROOT / "backend" / "app"
    # main_cors = lokalny sales-mock ASGI, nie produkt (może wrócić z BOM)
    return sorted(
        path
        for path in app.rglob("*.py")
        if "__pycache__" not in path.parts and path.stem != "main_cors"
    )


def ts_sources() -> list[Path]:
    src = ROOT / "frontend" / "src"
    if not src.is_dir():
        return []
    return sorted(
        path
        for path in src.rglob("*")
        if path.suffix in {".ts", ".tsx"} and not path.name.endswith(".gen.ts")
    )


def banned_module_error(rel: str) -> list[str]:
    if rel == SHADCN_CN:
        return []
    stem = Path(rel).stem.casefold()
    if stem not in BANNED_STEMS:
        return []
    return [f"{rel}: zakazana nazwa modułu {stem} (no-slop)"]


def py_line_errors(rel: str, source: str) -> list[str]:
    errors: list[str] = []
    for lineno, raw in enumerate(source.splitlines(), start=1):
        line = raw.strip()
        if TODO.search(line):
            errors.append(_note(rel, lineno, "TODO/FIXME/HACK w kodzie produktu"))
        if EXCEPT.search(line) or BARE_EXCEPT.search(line):
            errors.append(_note(rel, lineno, "except Exception — wyjątek domenowy"))
        if FLOAT_CALL.search(line):
            errors.append(_note(rel, lineno, "float() — kwoty i miary to Decimal"))
        if BANNER.search(line):
            errors.append(_note(rel, lineno, "baner komentarzowy"))
        if COMMENTED.search(line):
            errors.append(_note(rel, lineno, "zakomentowany kod"))
        if EMOJI.search(line):
            errors.append(_note(rel, lineno, "emoji w kodzie"))
        if HTTP_RAISE.search(line) and "/services/" in rel:
            errors.append(_note(rel, lineno, "HTTPException w serwisie — mapuj w API"))
    return errors


def echo_comment_errors(rel: str, source: str) -> list[str]:
    errors: list[str] = []
    lines = source.splitlines()
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("#") and not stripped.startswith("#!"):
            comment = stripped.lstrip("#").strip()
            nxt = index + 1
            while nxt < len(lines) and not lines[nxt].strip():
                nxt += 1
            match = DEF_LINE.match(lines[nxt].strip()) if nxt < len(lines) else None
            if match is not None:
                name = match.group(1)
                slug = re.sub(r"[^a-z0-9]+", "", comment.casefold())
                if slug and slug in {name.casefold(), name.replace("_", "").casefold()}:
                    errors.append(_note(rel, index + 1, f"komentarz powtarza nazwę {name}"))
        index += 1
    return errors


def docstring_errors(rel: str, tree: ast.AST) -> list[str]:
    errors: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        doc = ast.get_docstring(node, clean=True)
        if not doc:
            continue
        first = doc.splitlines()[0].strip()
        if first.startswith(SLOP_DOC):
            errors.append(_note(rel, node.lineno, "docstring Args/Returns bez uzasadnienia"))
    return errors


def banned_class_errors(rel: str, tree: ast.AST) -> list[str]:
    errors: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        if not node.name.endswith(SLOP_CLASS):
            continue
        errors.append(_note(rel, node.lineno, f"klasa {node.name} — nazwa warstwy slopu"))
    return errors


def py_file_errors(rel: str, source: str) -> list[str]:
    errors = banned_module_error(rel)
    errors.extend(py_line_errors(rel, source))
    errors.extend(echo_comment_errors(rel, source))
    try:
        tree = ast.parse(source)
    except SyntaxError as err:
        where = err.lineno or 1
        errors.append(_note(rel, where, f"składnia {err.msg}"))
        return errors
    errors.extend(docstring_errors(rel, tree))
    errors.extend(banned_class_errors(rel, tree))
    return errors


def ts_file_errors(rel: str, source: str) -> list[str]:
    errors = banned_module_error(rel)
    for lineno, raw in enumerate(source.splitlines(), start=1):
        line = raw.strip()
        if TODO.search(line):
            errors.append(_note(rel, lineno, "TODO/FIXME/HACK w kodzie produktu"))
        if AS_ANY.search(line) or COLON_ANY.search(line):
            errors.append(_note(rel, lineno, "any — typ na granicy danych, nie w UI"))
        if TS_BANNER.search(line):
            errors.append(_note(rel, lineno, "baner komentarzowy"))
        if EMOJI.search(line):
            errors.append(_note(rel, lineno, "emoji w kodzie"))
    return errors


def _fn_overflow(node: ast.AST) -> int:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return 0
    if node.end_lineno is None:
        return 0
    extra = (node.end_lineno - node.lineno + 1) - MAX_FN_LINES
    if extra > 0:
        return extra
    return 0


def long_function_stats(paths: list[Path] | None = None) -> tuple[int, int]:
    count = 0
    overflow = 0
    for path in paths if paths is not None else py_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            extra = _fn_overflow(node)
            if extra == 0:
                continue
            count += 1
            overflow += extra
    return count, overflow


def scan_errors() -> list[str]:
    errors: list[str] = []
    for path in py_sources():
        errors.extend(py_file_errors(rel_posix(path), path.read_text(encoding="utf-8")))
    for path in ts_sources():
        errors.extend(ts_file_errors(rel_posix(path), path.read_text(encoding="utf-8")))
    return errors


def main() -> int:
    errors = scan_errors()
    if errors:
        print("craft_style: slop (nie 'jak człowiek' — mechanika no-slop)")
        for err in errors:
            print(f"  {err}")
        return 1
    count, overflow = long_function_stats()
    print(f"craft_style: OK (funkcje>40: {count}, nadmiar linii: {overflow})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
