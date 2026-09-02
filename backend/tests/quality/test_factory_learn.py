"""Podłoga jakości nie spada; C4 zlicza czerwone runy."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path
from types import ModuleType

_ROOT = Path(__file__).resolve().parents[3]
_FLOOR = _ROOT / "scripts" / "quality" / "quality_floor.py"
_REPEAT = _ROOT / "scripts" / "quality" / "repeat_learn.py"
_CYCLE = _ROOT / "scripts" / "quality" / "factory_cycle.py"


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_floor_snapshot_has_isolation_and_hc() -> None:
    floor = _load(_FLOOR, "quality_floor")
    snap = floor.snapshot()
    assert snap["isolation_tests"] >= 20
    assert snap["grounding_hc"] == 8
    assert snap["bench_cases"] >= 1
    assert snap["promptfoo_fixtures"] >= 2
    assert snap["long_functions"] <= 5
    assert snap["long_function_overflow"] <= 54


def test_floor_regression_is_reported() -> None:
    floor = _load(_FLOOR, "quality_floor")
    errors = floor.regressions(
        {"isolation_tests": 1, "bench_cases": 0, "promptfoo_fixtures": 1, "grounding_hc": 7},
        {"isolation_tests": 23, "bench_cases": 1, "promptfoo_fixtures": 2, "grounding_hc": 8},
    )
    assert any("isolation_tests" in err for err in errors)
    assert any("grounding_hc" in err for err in errors)


def test_floor_ceiling_regression_is_reported() -> None:
    floor = _load(_FLOOR, "quality_floor")
    errors = floor.regressions(
        {"long_functions": 6, "long_function_overflow": 60},
        {"long_functions": 5, "long_function_overflow": 54},
    )
    assert any("long_functions" in err for err in errors)
    assert any("long_function_overflow" in err for err in errors)


def test_repeat_threshold() -> None:
    learn = _load(_REPEAT, "repeat_learn")
    counter = learn.load_failed_runs(
        [
            {"conclusion": "failure", "name": "gate"},
            {"conclusion": "failure", "name": "gate"},
            {"conclusion": "failure", "name": "gate"},
            {"conclusion": "success", "name": "gate"},
            {"conclusion": "failure", "name": "meta"},
        ]
    )
    assert counter == Counter({"gate": 3, "meta": 1})
    assert learn.repeats(counter) == [("gate", 3)]


def test_factory_retrieve_includes_machine_or_bench() -> None:
    cycle = _load(_CYCLE, "factory_cycle")
    items = cycle.retrieve()
    blob = "\n".join(items)
    assert "machine-" in blob or "66.0" in blob
