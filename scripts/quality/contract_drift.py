#!/usr/bin/env python3
"""C2: recipe / MCP / skrypt cytowany w kontrakcie, a nieistniejący w repo.

Skan tylko AGENTS, GROUNDING, alwaysApply rules i komend. Nie docs-debt
(historia „MCP Postgres”) i nie karty knowledge. Nigdy nie edytuje kontraktu.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_GLOBS = (
    "AGENTS.md",
    "GROUNDING.md",
    ".cursor/rules/*.mdc",
    ".cursor/commands/*.md",
)
RE_JUST = re.compile(r"`just ([a-z0-9][a-z0-9-]*)")
RE_MCP = re.compile(r"MCP ([A-Z][A-Za-z0-9_-]+)")
RE_SCRIPT = re.compile(r"`(scripts/[^`\s]+)`")
RE_RECIPE = re.compile(r"^([a-z0-9][a-z0-9-]*)(?:[ \t]+\S+)*:")


def just_recipes(justfile_text: str) -> frozenset[str]:
    names: set[str] = set()
    for line in justfile_text.splitlines():
        match = RE_RECIPE.match(line)
        if match is not None:
            names.add(match.group(1))
    return frozenset(names)


def mcp_server_names(mcp_json_text: str) -> frozenset[str]:
    payload = json.loads(mcp_json_text)
    servers = payload.get("mcpServers", {})
    if not isinstance(servers, dict):
        return frozenset()
    return frozenset(name.lower() for name in servers)


def load_recipes() -> frozenset[str]:
    path = ROOT / "justfile"
    if not path.is_file():
        return frozenset()
    return just_recipes(path.read_text(encoding="utf-8"))


def load_mcp_servers() -> frozenset[str]:
    path = ROOT / ".cursor" / "mcp.json"
    if not path.is_file():
        return frozenset()
    return mcp_server_names(path.read_text(encoding="utf-8"))


def contract_files() -> list[Path]:
    found: list[Path] = []
    for pattern in CONTRACT_GLOBS:
        found.extend(path for path in ROOT.glob(pattern) if path.is_file())
    return found


def drift_in_text(
    rel: str,
    text: str,
    recipes: frozenset[str],
    servers: frozenset[str],
) -> list[str]:
    errors: list[str] = []
    for match in RE_JUST.finditer(text):
        recipe = match.group(1)
        if recipes and recipe not in recipes:
            errors.append(f"{rel}: brak recipe `just {recipe}`")
    for match in RE_MCP.finditer(text):
        name = match.group(1)
        if name.lower() not in servers:
            errors.append(f"{rel}: brak serwera MCP `{name}` w mcp.json")
    for match in RE_SCRIPT.finditer(text):
        script = match.group(1)
        if not (ROOT / script).exists():
            errors.append(f"{rel}: brak `{script}`")
    return errors


def contract_drift_errors() -> list[str]:
    recipes = load_recipes()
    servers = load_mcp_servers()
    errors: list[str] = []
    for path in contract_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        errors.extend(drift_in_text(rel, text, recipes, servers))
    return errors
