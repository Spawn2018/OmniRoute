from decimal import Decimal
from uuid import UUID

import pytest

from app.domain.errors import InvalidSuggestionLedger
from app.domain.suggestion_ledger import parse_suggestion_ledger_row

_ENTITY = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "target_bc": "shipment",
        "entity_id": _ENTITY,
        "suggestion_kind": "eta",
        "interval_low": "30",
        "interval_high": "90",
        "model_version": "hist_eta",
        "prompt_version": "prompt_v1",
        "reaction": "accept",
        "changed_to": "none",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_suggestion_ledger_row(
        body["target_bc"],
        body["entity_id"],
        body["suggestion_kind"],
        body["interval_low"],
        body["interval_high"],
        body["model_version"],
        body["prompt_version"],
        body["reaction"],
        body["changed_to"],
        body["source_ref"],
    )


def test_parse_accepts_manual_row() -> None:
    draft = _ok()
    assert draft.suggestion_kind == "eta"
    assert draft.interval_low == Decimal("30.0000")
    assert draft.entity_id == UUID(_ENTITY)
    assert draft.changed_to == "none"


def test_parse_rejects_float_interval() -> None:
    with pytest.raises(InvalidSuggestionLedger, match="float"):
        _ok(interval_low=1.5)


def test_parse_rejects_inverted_interval() -> None:
    with pytest.raises(InvalidSuggestionLedger, match="przedział"):
        _ok(interval_low="90", interval_high="30")


def test_parse_rejects_modify_none() -> None:
    with pytest.raises(InvalidSuggestionLedger, match="zmiana"):
        _ok(reaction="modify", changed_to="none")


def test_parse_accepts_open_kind() -> None:
    draft = _ok(suggestion_kind="tender_twin")
    assert draft.suggestion_kind == "tender_twin"


def test_parse_rejects_bad_kind() -> None:
    with pytest.raises(InvalidSuggestionLedger, match="rodzaj"):
        _ok(suggestion_kind="1x")
