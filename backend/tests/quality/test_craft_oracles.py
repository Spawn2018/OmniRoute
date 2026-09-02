"""OS-3: test z kodem, how-to albo leftover, delta zanim produkt."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT = _ROOT / "scripts" / "quality" / "craft_oracles.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("craft_oracles", _SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_new_api_without_tests_is_reported() -> None:
    oracles = _load()
    added = frozenset({"backend/app/api/rfqs.py"})
    changed = added
    errors = oracles.missing_tests(added, changed)
    assert any("rfqs.py" in err for err in errors)


def test_new_api_with_tests_is_silent() -> None:
    oracles = _load()
    added = frozenset({"backend/app/api/rfqs.py"})
    changed = frozenset({"backend/app/api/rfqs.py", "backend/tests/rfqs/test_rfq.py"})
    assert oracles.missing_tests(added, changed) == []


def test_init_py_is_not_a_service() -> None:
    oracles = _load()
    added = frozenset({"backend/app/services/rfqs/__init__.py"})
    assert oracles.missing_tests(added, added) == []


def test_catalog_page_needs_howto_or_debt() -> None:
    oracles = _load()
    added = frozenset({"frontend/src/features/rfqs/catalog-page.tsx"})
    errors = oracles.missing_operator_docs(added, added, {})
    assert errors
    with_debt = added | frozenset({"docs/ops/docs-debt.md"})
    assert oracles.missing_operator_docs(added, with_debt, {}) == []


def test_post_api_needs_operator_docs() -> None:
    oracles = _load()
    rel = "backend/app/api/rfqs.py"
    added = frozenset({rel})
    sources = {rel: "@router.post('/rfqs')\n"}
    assert oracles.missing_operator_docs(added, added, sources)
    with_howto = added | frozenset({"docs/operator/rfq.md"})
    assert oracles.missing_operator_docs(added, with_howto, sources) == []


def test_product_code_without_delta_is_reported() -> None:
    oracles = _load()
    changed = frozenset({"backend/app/services/rfqs/rfq_service.py"})
    errors = oracles.missing_product_delta(changed, [], frozenset())
    assert errors
    archived = frozenset({"docs/deltas/archived/67.0-rfq.md"})
    assert oracles.missing_product_delta(changed, [], archived) == []


def test_factory_scripts_are_not_product() -> None:
    oracles = _load()
    changed = frozenset({"scripts/quality/craft_oracles.py"})
    assert oracles.missing_product_delta(changed, [], frozenset()) == []


def test_os_open_deltas_do_not_count_as_product() -> None:
    oracles = _load()
    opens = oracles.product_open_deltas(_ROOT / "docs" / "deltas" / "open")
    assert all(not path.name.upper().startswith("OS-") for path in opens)
