import pytest

from app.domain.errors import InvalidLocalChargeWarningMark
from app.domain.local_charge_warning_mark import parse_local_charge_warning_mark_row


def test_parse_local_charge_warning_mark_row_accepts_warn() -> None:
    code, kind, origin = parse_local_charge_warning_mark_row(
        "warn_thc_01",
        "warn",
        "fixture://local-charge-warning/a",
    )
    assert code == "warn_thc_01"
    assert kind == "warn"
    assert origin == "fixture://local-charge-warning/a"


def test_parse_local_charge_warning_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidLocalChargeWarningMark, match="ostrzezenie"):
        parse_local_charge_warning_mark_row(
            "warn_thc_01",
            "live",
            "tenant:manual",
        )


def test_parse_local_charge_warning_mark_row_rejects_foreign_source() -> None:
    with pytest.raises(InvalidLocalChargeWarningMark, match="obce"):
        parse_local_charge_warning_mark_row(
            "warn_thc_01",
            "hold",
            "http://evil",
        )
