import pytest

from app.domain.errors import InvalidRiskRegisterMark
from app.domain.risk_register_mark import parse_risk_register_mark_row


def test_parse_risk_register_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_risk_register_mark_row(
        "rr_open_01",
        "Open",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("rr_open_01", "open", "tenant:manual")


def test_parse_risk_register_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidRiskRegisterMark, match="rodzaj"):
        parse_risk_register_mark_row(
            "rr_open_01",
            "score_person",
            "tenant:manual",
        )
