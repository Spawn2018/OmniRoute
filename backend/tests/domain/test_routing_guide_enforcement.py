import pytest

from app.domain.errors import InvalidRoutingGuideEnforcement
from app.domain.routing_guide_enforcement import parse_routing_guide_enforcement_row


def test_parse_enforcement_accepts() -> None:
    code, kind, origin = parse_routing_guide_enforcement_row(
        " mode_block_01 ",
        " Block_409 ",
        "fixture://routing-guide-enforcement/a",
    )
    assert code == "mode_block_01"
    assert kind == "block_409"
    assert origin == "fixture://routing-guide-enforcement/a"


def test_parse_enforcement_rejects() -> None:
    with pytest.raises(InvalidRoutingGuideEnforcement, match="oznaczenie"):
        parse_routing_guide_enforcement_row("X", "record_only", "tenant:manual")
    with pytest.raises(InvalidRoutingGuideEnforcement, match="rodzaj"):
        parse_routing_guide_enforcement_row("mode_01", "soft_warn", "tenant:manual")
    with pytest.raises(InvalidRoutingGuideEnforcement, match="obce"):
        parse_routing_guide_enforcement_row("mode_01", "record_only", "http://evil")
