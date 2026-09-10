"""NOC-LIVE: /noc na main; pas pomocniczy tylko poza ROOT."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "writer_preflight.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("writer_preflight", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_status(path: Path, status: str) -> None:
    path.write_text(f"status: {status}\n", encoding="utf-8")


def test_plain_ok_when_noc_absent(tmp_path: Path, monkeypatch: object) -> None:
    pre = _load()
    monkeypatch.setattr(pre, "NOC", tmp_path / "NOC-LIVE.md")
    monkeypatch.setattr("sys.argv", ["writer_preflight.py"])
    assert pre.main() == 0


def test_plain_stops_when_noc_idle(tmp_path: Path, monkeypatch: object) -> None:
    pre = _load()
    noc = tmp_path / "NOC-LIVE.md"
    _write_status(noc, "idle")
    monkeypatch.setattr(pre, "NOC", noc)
    monkeypatch.setattr("sys.argv", ["writer_preflight.py"])
    assert pre.main() == 1


def test_allow_noc_ok_when_idle(tmp_path: Path, monkeypatch: object) -> None:
    pre = _load()
    noc = tmp_path / "NOC-LIVE.md"
    _write_status(noc, "idle")
    monkeypatch.setattr(pre, "NOC", noc)
    monkeypatch.setattr("sys.argv", ["writer_preflight.py", "--allow-noc"])
    assert pre.main() == 0


def test_flags_together_fail(monkeypatch: object) -> None:
    pre = _load()
    monkeypatch.setattr(
        "sys.argv",
        ["writer_preflight.py", "--allow-noc", "--allow-noc-helper"],
    )
    assert pre.main() == 1


def test_side_lane_fails_when_noc_stopped(
    tmp_path: Path, monkeypatch: object
) -> None:
    pre = _load()
    monkeypatch.setattr(pre, "NOC", tmp_path / "missing.md")
    monkeypatch.setattr("sys.argv", ["writer_preflight.py", "--allow-noc-helper"])
    assert pre.main() == 1


def test_side_lane_fails_on_main_tree(
    tmp_path: Path, monkeypatch: object
) -> None:
    pre = _load()
    noc = tmp_path / "NOC-LIVE.md"
    _write_status(noc, "idle")
    monkeypatch.setattr(pre, "NOC", noc)
    monkeypatch.chdir(pre.ROOT)
    monkeypatch.setattr("sys.argv", ["writer_preflight.py", "--allow-noc-helper"])
    assert pre.main() == 1


def test_side_lane_ok_outside_root(tmp_path: Path, monkeypatch: object) -> None:
    pre = _load()
    noc = tmp_path / "NOC-LIVE.md"
    _write_status(noc, "idle")
    monkeypatch.setattr(pre, "NOC", noc)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["writer_preflight.py", "--allow-noc-helper"])
    assert pre.main() == 0
