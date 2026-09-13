from decimal import Decimal

import pytest

from app.domain.benefit_ledger import parse_benefit_ledger_row
from app.domain.errors import InvalidBenefitLedger


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "benefit_code": "dock_save",
        "method_label": "porownanie z wczorajszym charge",
        "hours_saved": "2.5",
        "saved_amount": "150",
        "saved_currency": "EUR",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_benefit_ledger_row(
        body["benefit_code"],
        body["method_label"],
        body["hours_saved"],
        body["saved_amount"],
        body["saved_currency"],
        body["source_ref"],
    )


def test_parse_accepts_manual_row() -> None:
    draft = _ok()
    assert draft.benefit_code == "dock_save"
    assert draft.method_label == "porownanie z wczorajszym charge"
    assert draft.hours_saved == Decimal("2.5000")
    assert draft.saved_amount == Decimal("150.0000")
    assert draft.saved_currency == "EUR"


def test_parse_rejects_float_hours() -> None:
    with pytest.raises(InvalidBenefitLedger, match="float"):
        _ok(hours_saved=1.5)


def test_parse_rejects_float_amount() -> None:
    with pytest.raises(InvalidBenefitLedger, match="float"):
        _ok(saved_amount=1.5)


def test_parse_rejects_empty_method() -> None:
    with pytest.raises(InvalidBenefitLedger, match="metoda"):
        _ok(method_label="  ")


def test_parse_rejects_bad_currency() -> None:
    with pytest.raises(InvalidBenefitLedger, match="waluta"):
        _ok(saved_currency="eur")


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidBenefitLedger, match="kod"):
        _ok(benefit_code="X")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidBenefitLedger, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
