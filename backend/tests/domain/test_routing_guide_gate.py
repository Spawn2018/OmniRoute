import pytest

from app.domain.errors import RoutingGuideOffGuide
from app.domain.routing_guide_gate import assert_asn_on_routing_guide


def test_gate_allows_without_guide_when_no_block() -> None:
    assert_asn_on_routing_guide(
        guide_code=None,
        enforcement_kinds={"record_only"},
        known_guide_codes={"lane_pl_de"},
    )
    assert_asn_on_routing_guide(
        guide_code=None,
        enforcement_kinds=set(),
        known_guide_codes=set(),
    )


def test_gate_requires_known_guide_when_block_409() -> None:
    assert_asn_on_routing_guide(
        guide_code="lane_pl_de",
        enforcement_kinds={"block_409"},
        known_guide_codes={"lane_pl_de"},
    )
    with pytest.raises(RoutingGuideOffGuide, match="brak guide_code"):
        assert_asn_on_routing_guide(
            guide_code=None,
            enforcement_kinds={"block_409"},
            known_guide_codes={"lane_pl_de"},
        )
    with pytest.raises(RoutingGuideOffGuide, match="katalogiem"):
        assert_asn_on_routing_guide(
            guide_code="other_lane",
            enforcement_kinds={"record_only", "block_409"},
            known_guide_codes={"lane_pl_de"},
        )
