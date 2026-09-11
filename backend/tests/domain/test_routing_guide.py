
import pytest

from app.domain.errors import InvalidRoutingGuide
from app.domain.routing_guide import parse_routing_guide_row


def test_parse_routing_guide_row_accepts_code_and_labels() -> None:
    code, lane, mode, origin = parse_routing_guide_row(
        " guide_pl_de ",
        " Gdańsk–Hamburg ",
        " road ",
        "fixture://routing-guide/a",
    )
    assert code == "guide_pl_de"
    assert lane == "Gdańsk–Hamburg"
    assert mode == "road"
    assert origin == "fixture://routing-guide/a"


def test_parse_routing_guide_row_accepts_blank_labels() -> None:
    code, lane, mode, origin = parse_routing_guide_row(
        "guide_01", "  ", None, "tenant:manual"
    )
    assert code == "guide_01"
    assert lane is None
    assert mode is None
    assert origin == "tenant:manual"


def test_parse_routing_guide_row_rejects_bad_code_and_origin() -> None:
    with pytest.raises(InvalidRoutingGuide, match="oznaczenie"):
        parse_routing_guide_row("X", None, None, "tenant:manual")
    with pytest.raises(InvalidRoutingGuide, match="obce"):
        parse_routing_guide_row("guide_01", None, None, "http://evil")
    with pytest.raises(InvalidRoutingGuide, match="korytarz"):
        parse_routing_guide_row("guide_01", 1, None, "tenant:manual")
    with pytest.raises(InvalidRoutingGuide, match="tryb"):
        parse_routing_guide_row("guide_01", None, "x" * 129, "tenant:manual")
