import pytest

from app.domain.errors import InvalidLocalChargeBindMark
from app.domain.local_charge_bind_mark import parse_local_charge_bind_mark_row


def test_parse_local_charge_bind_mark_row_accepts_charge() -> None:
    code, kind, origin = parse_local_charge_bind_mark_row(
        "bind_charge_01",
        "charge",
        "fixture://local-charge-bind/a",
    )
    assert code == "bind_charge_01"
    assert kind == "charge"
    assert origin == "fixture://local-charge-bind/a"


def test_parse_local_charge_bind_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidLocalChargeBindMark, match="wiązanie"):
        parse_local_charge_bind_mark_row(
            "bind_charge_01",
            "live",
            "tenant:manual",
        )


def test_parse_local_charge_bind_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidLocalChargeBindMark, match="obce"):
        parse_local_charge_bind_mark_row(
            "bind_charge_01",
            "charge",
            "http://evil",
        )
