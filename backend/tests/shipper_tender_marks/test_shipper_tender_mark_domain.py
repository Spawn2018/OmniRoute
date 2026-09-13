import pytest

from app.domain.errors import InvalidShipperTenderMark
from app.domain.shipper_tender_mark import parse_shipper_tender_mark_row


def test_parse_shipper_tender_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_shipper_tender_mark_row(
        "stm_round_01",
        "Round",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("stm_round_01", "round", "tenant:manual")


def test_parse_shipper_tender_mark_row_rejects_award_kind() -> None:
    with pytest.raises(InvalidShipperTenderMark, match="rodzaj"):
        parse_shipper_tender_mark_row("stm_round_01", "award", "tenant:manual")
