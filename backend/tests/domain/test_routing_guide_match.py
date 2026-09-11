import pytest

from app.domain.errors import InvalidRoutingGuideMatch
from app.domain.routing_guide_match import parse_routing_guide_match_row


def test_parse_match_accepts() -> None:
    code, kind, origin = parse_routing_guide_match_row(
        " match_lane_01 ",
        " Lane_Label ",
        "fixture://routing-guide-match/a",
    )
    assert code == "match_lane_01"
    assert kind == "lane_label"
    assert origin == "fixture://routing-guide-match/a"


def test_parse_match_rejects() -> None:
    with pytest.raises(InvalidRoutingGuideMatch, match="oznaczenie"):
        parse_routing_guide_match_row("X", "lane_label", "tenant:manual")
    with pytest.raises(InvalidRoutingGuideMatch, match="rodzaj"):
        parse_routing_guide_match_row("match_01", "gps", "tenant:manual")
    with pytest.raises(InvalidRoutingGuideMatch, match="obce"):
        parse_routing_guide_match_row("match_01", "mode_label", "http://evil")
