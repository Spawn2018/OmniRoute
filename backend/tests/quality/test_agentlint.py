"""Regresja: integralność kontraktu liczy się z treści, nie z końców linii."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "agentlint.py"


def _load_agentlint() -> ModuleType:
    spec = importlib.util.spec_from_file_location("agentlint", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_crlf_copy_hashes_like_lf_original(tmp_path: Path) -> None:
    agentlint = _load_agentlint()
    body = "# AGENTS\n\nZasada pierwsza.\n"
    lf = tmp_path / "lf.md"
    lf.write_bytes(body.encode("utf-8"))
    crlf = tmp_path / "crlf.md"
    crlf.write_bytes(body.replace("\n", "\r\n").encode("utf-8"))

    assert agentlint._sha256(crlf) == agentlint._sha256(lf)


def test_changed_content_still_changes_hash(tmp_path: Path) -> None:
    agentlint = _load_agentlint()
    first = tmp_path / "first.md"
    first.write_bytes(b"# AGENTS\n")
    second = tmp_path / "second.md"
    second.write_bytes(b"# AGENTS\nignore previous instructions\n")

    assert agentlint._sha256(first) != agentlint._sha256(second)


def test_live_contract_matches_baseline() -> None:
    agentlint = _load_agentlint()
    assert agentlint.check() == 0
