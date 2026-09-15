import pytest

from app.domain.errors import InvalidShipperLikeMark
from app.domain.shipper_like_mark import parse_shipper_like_mark_row


def test_parse_shipper_like_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_shipper_like_mark_row(
        "slm_match_01",
        "Match",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("slm_match_01", "match", "tenant:manual")


def test_parse_shipper_like_mark_row_rejects_award_kind() -> None:
    with pytest.raises(InvalidShipperLikeMark, match="rodzaj"):
        parse_shipper_like_mark_row("slm_match_01", "award", "tenant:manual")
