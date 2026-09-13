from decimal import Decimal
from uuid import UUID

import pytest

from app.domain.errors import InvalidOutcomeLedger
from app.domain.outcome_ledger import parse_outcome_ledger_row

_ENTITY = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
_SUGGESTION = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "target_bc": "shipment",
        "entity_id": _ENTITY,
        "suggestion_id": _SUGGESTION,
        "outcome_kind": "eta",
        "actual_value": "45",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_outcome_ledger_row(
        body["target_bc"],
        body["entity_id"],
        body["suggestion_id"],
        body["outcome_kind"],
        body["actual_value"],
        body["source_ref"],
    )


def test_parse_accepts_manual_row() -> None:
    draft = _ok()
    assert draft.outcome_kind == "eta"
    assert draft.actual_value == Decimal("45.0000")
    assert draft.entity_id == UUID(_ENTITY)
    assert draft.suggestion_id == UUID(_SUGGESTION)


def test_parse_rejects_float_actual() -> None:
    with pytest.raises(InvalidOutcomeLedger, match="float"):
        _ok(actual_value=1.5)


def test_parse_rejects_bad_kind() -> None:
    with pytest.raises(InvalidOutcomeLedger, match="rodzaj"):
        _ok(outcome_kind="person_score")


def test_parse_rejects_bad_suggestion() -> None:
    with pytest.raises(InvalidOutcomeLedger, match="podpowiedź"):
        _ok(suggestion_id="not-a-uuid")
