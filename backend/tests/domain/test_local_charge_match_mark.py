import pytest

from app.domain.errors import InvalidLocalChargeMatchMark
from app.domain.local_charge_match_mark import parse_local_charge_match_mark_row


def test_parse_local_charge_match_mark_row_accepts_match() -> None:
    code, kind, origin = parse_local_charge_match_mark_row(
        "var_match_01",
        "match",
        "fixture://local-charge-match/a",
    )
    assert code == "var_match_01"
    assert kind == "match"
    assert origin == "fixture://local-charge-match/a"


def test_parse_local_charge_match_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidLocalChargeMatchMark, match="dopasowanie"):
        parse_local_charge_match_mark_row(
            "var_match_01",
            "live",
            "tenant:manual",
        )


def test_parse_local_charge_match_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidLocalChargeMatchMark, match="obce"):
        parse_local_charge_match_mark_row(
            "var_match_01",
            "match",
            "http://evil",
        )
