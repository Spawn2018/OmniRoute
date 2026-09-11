import pytest

from app.domain.errors import InvalidOtifMark
from app.domain.otif_mark import parse_otif_mark_row


def test_parse_otif_mark_row_accepts_code_and_scope() -> None:
    code, scope, origin = parse_otif_mark_row(
        " otif_pickup_pl ",
        " Pickup ",
        "fixture://otif-mark/a",
    )
    assert code == "otif_pickup_pl"
    assert scope == "pickup"
    assert origin == "fixture://otif-mark/a"


def test_parse_otif_mark_row_accepts_manual_origin() -> None:
    code, scope, origin = parse_otif_mark_row("otif_sku_01", "sku", "tenant:manual")
    assert code == "otif_sku_01"
    assert scope == "sku"
    assert origin == "tenant:manual"


def test_parse_otif_mark_row_rejects_bad_code_scope_and_origin() -> None:
    with pytest.raises(InvalidOtifMark, match="oznaczenie"):
        parse_otif_mark_row("X", "pickup", "tenant:manual")
    with pytest.raises(InvalidOtifMark, match="zakres"):
        parse_otif_mark_row("otif_01", "lane", "tenant:manual")
    with pytest.raises(InvalidOtifMark, match="obce"):
        parse_otif_mark_row("otif_01", "delivery", "http://evil")
