"""OS-4: slop z no-slop.mdc pada w craft_style, nie w autorecenzji."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "craft_style.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("craft_style", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_echo_comment_is_reported() -> None:
    style = _load()
    source = "# get_user\n\ndef get_user() -> None:\n    return\n"
    errors = style.py_file_errors("backend/app/demo.py", source)
    assert any("get_user" in err and "komentarz" in err for err in errors)


def test_justified_comment_is_silent() -> None:
    style = _load()
    source = (
        "# NBP D-1 roboczy — wymóg ustawy o VAT art. 31a\n"
        "def nbp_table_a() -> None:\n    return\n"
    )
    assert style.py_file_errors("backend/app/nbp.py", source) == []


def test_except_exception_is_reported() -> None:
    style = _load()
    source = "try:\n    x = 1\nexcept Exception:\n    pass\n"
    errors = style.py_file_errors("backend/app/demo.py", source)
    assert any("except Exception" in err for err in errors)


def test_float_call_is_reported() -> None:
    style = _load()
    source = "amount = float(1)\n"
    errors = style.py_file_errors("backend/app/charges/x.py", source)
    assert any("float()" in err for err in errors)


def test_todo_is_reported() -> None:
    style = _load()
    source = "x = 1  # TODO potem\n"
    errors = style.py_file_errors("backend/app/demo.py", source)
    assert any("TODO" in err for err in errors)


def test_param_only_docstring_is_reported() -> None:
    style = _load()
    source = 'def f(x: int) -> int:\n    """Args:\n        x: n."""\n    return x\n'
    errors = style.py_file_errors("backend/app/demo.py", source)
    assert any("docstring" in err for err in errors)


def test_banned_utils_module_is_reported() -> None:
    style = _load()
    errors = style.py_file_errors("backend/app/services/foo/utils.py", "x = 1\n")
    assert any("utils" in err for err in errors)


def test_shadcn_utils_ts_is_silent_on_name() -> None:
    style = _load()
    assert style.banned_module_error("frontend/src/lib/utils.ts") == []


def test_as_any_is_reported() -> None:
    style = _load()
    errors = style.ts_file_errors("frontend/src/lib/x.ts", "const x = y as any;\n")
    assert any("any" in err for err in errors)


def test_http_exception_in_service_is_reported() -> None:
    style = _load()
    rel = "backend/app/services/charges/charge_service.py"
    source = "raise HTTPException(status_code=400)\n"
    errors = style.py_file_errors(rel, source)
    assert any("HTTPException" in err for err in errors)


def test_factory_class_is_reported() -> None:
    style = _load()
    source = "class ChargeFactory:\n    pass\n"
    errors = style.py_file_errors("backend/app/demo.py", source)
    assert any("ChargeFactory" in err for err in errors)


def test_live_product_has_no_style_errors() -> None:
    assert _load().scan_errors() == []
