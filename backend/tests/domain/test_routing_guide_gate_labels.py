import pytest

from app.domain.errors import RoutingGuideOffGuide
from app.domain.routing_guide_gate import (
    assert_asn_labels_on_routing_guide,
    assert_asn_on_routing_guide,
)


def test_guide_code_gate_unchanged() -> None:
    assert_asn_on_routing_guide(
        guide_code="lane_a",
        enforcement_kinds={"block_409"},
        known_guide_codes={"lane_a"},
    )
    with pytest.raises(RoutingGuideOffGuide, match="brak guide_code"):
        assert_asn_on_routing_guide(
            guide_code=None,
            enforcement_kinds={"block_409"},
            known_guide_codes={"lane_a"},
        )


def test_lane_label_match_requires_plant() -> None:
    assert_asn_labels_on_routing_guide(
        guide_code="lane_a",
        enforcement_kinds={"block_409"},
        match_kinds={"lane_label"},
        plant_label=" PL-DE ",
        carrier_label=None,
        guide_lane_by_code={"lane_a": "pl-de"},
        guide_mode_by_code={"lane_a": None},
    )
    with pytest.raises(RoutingGuideOffGuide, match="plant_label"):
        assert_asn_labels_on_routing_guide(
            guide_code="lane_a",
            enforcement_kinds={"block_409"},
            match_kinds={"lane_label"},
            plant_label="other",
            carrier_label=None,
            guide_lane_by_code={"lane_a": "pl-de"},
            guide_mode_by_code={"lane_a": None},
        )


def test_mode_label_match_requires_carrier() -> None:
    with pytest.raises(RoutingGuideOffGuide, match="carrier_label"):
        assert_asn_labels_on_routing_guide(
            guide_code="lane_a",
            enforcement_kinds={"block_409"},
            match_kinds={"mode_label"},
            plant_label=None,
            carrier_label=None,
            guide_lane_by_code={"lane_a": None},
            guide_mode_by_code={"lane_a": "road"},
        )


def test_labels_ignored_without_block_409() -> None:
    assert_asn_labels_on_routing_guide(
        guide_code="lane_a",
        enforcement_kinds={"record_only"},
        match_kinds={"lane_label", "mode_label"},
        plant_label=None,
        carrier_label=None,
        guide_lane_by_code={"lane_a": "x"},
        guide_mode_by_code={"lane_a": "y"},
    )
