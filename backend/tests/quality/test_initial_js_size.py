from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "check_initial_js_size.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_initial_js_size", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = ModuleType("check_initial_js_size")
    spec.loader.exec_module(module)
    return module


def test_just_perf_is_not_echo_stub() -> None:
    justfile = (_ROOT / "justfile").read_text(encoding="utf-8")
    assert "check_initial_js_size.py" in justfile
    assert '@echo "perf: stub, nie DoD (k6 / budżety p95)"' not in justfile


def test_parses_module_and_preload_scripts() -> None:
    check = _load()
    html = (
        '<script type="module" src="/assets/index-aaaa.js"></script>'
        '<link rel="modulepreload" href="/assets/index-aaaa.js">'
        '<link rel="modulepreload" href="/assets/vendor-bbbb.js">'
    )
    assert check.script_paths(html) == ["/assets/index-aaaa.js", "/assets/vendor-bbbb.js"]


def test_oversize_initial_js_fails(tmp_path: Path) -> None:
    check = _load()
    assets = tmp_path / "assets"
    assets.mkdir()
    payload = os.urandom(check.LIMIT_BYTES + 2048)
    (assets / "index-over.js").write_bytes(payload)
    (tmp_path / "index.html").write_text(
        '<script type="module" src="/assets/index-over.js"></script>',
        encoding="utf-8",
    )
    assert check.main(["check", str(tmp_path)]) == 1
    assert check.initial_js_gzip_bytes(tmp_path) >= check.LIMIT_BYTES


def test_undersize_initial_js_passes(tmp_path: Path) -> None:
    check = _load()
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "index-ok.js").write_bytes(b"export const x = 1;\n")
    (tmp_path / "index.html").write_text(
        '<script type="module" src="/assets/index-ok.js"></script>',
        encoding="utf-8",
    )
    assert check.main(["check", str(tmp_path)]) == 0
    assert check.initial_js_gzip_bytes(tmp_path) < check.LIMIT_BYTES
