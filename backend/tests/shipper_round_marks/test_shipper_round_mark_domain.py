import pytest

from app.domain.errors import InvalidShipperRoundMark
from app.domain.shipper_round_mark import parse_shipper_round_mark_row


def test_parse_shipper_round_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_shipper_round_mark_row(
        "srm_first_01",
        "First",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("srm_first_01", "first", "tenant:manual")


def test_parse_shipper_round_mark_row_rejects_award_kind() -> None:
    with pytest.raises(InvalidShipperRoundMark, match="rodzaj"):
        parse_shipper_round_mark_row("srm_first_01", "award", "tenant:manual")
