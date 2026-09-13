import pytest

from app.domain.counterfactual_run import parse_counterfactual_run_row
from app.domain.errors import InvalidCounterfactualRun


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "run_code": "fuel_spike",
        "baseline_label": "plan z wczoraj",
        "levers_label": "paliwo w gore",
        "result_label": "eta plus dwie godziny",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_counterfactual_run_row(
        body["run_code"],
        body["baseline_label"],
        body["levers_label"],
        body["result_label"],
        body["source_ref"],
    )


def test_parse_accepts_manual_row() -> None:
    draft = _ok()
    assert draft.run_code == "fuel_spike"
    assert draft.baseline_label == "plan z wczoraj"
    assert draft.result_label == "eta plus dwie godziny"


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidCounterfactualRun, match="kod"):
        _ok(run_code="X")


def test_parse_rejects_empty_baseline() -> None:
    with pytest.raises(InvalidCounterfactualRun, match="punkt"):
        _ok(baseline_label="  ")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidCounterfactualRun, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
