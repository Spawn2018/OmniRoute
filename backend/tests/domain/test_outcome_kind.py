import pytest

from app.domain.errors import InvalidOutcomeKind
from app.domain.outcome_kind import parse_outcome_kind_row


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "kind_code": "tender",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_outcome_kind_row(body["kind_code"], body["source_ref"])


def test_parse_accepts_open_kind_outside_ledger_set() -> None:
    draft = _ok()
    assert draft.kind_code == "tender"


def test_parse_accepts_legacy_eta() -> None:
    draft = _ok(kind_code="eta")
    assert draft.kind_code == "eta"


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidOutcomeKind, match="kod"):
        _ok(kind_code="X")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidOutcomeKind, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
