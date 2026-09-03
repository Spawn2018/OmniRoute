from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidShipmentLeg
from app.domain.shipment_leg import (
    require_china_rail_country,
    require_distinct_ends,
    require_leg_kind,
    require_leg_location_id,
    require_leg_shipment_id,
    require_leg_source_ref,
    require_rail_location_kind,
    require_rail_port_flag,
    require_road_leg_kind,
    require_road_location_kind,
)


def test_require_leg_source_ref_accepts_fixture() -> None:
    assert require_leg_source_ref(" fixture://shipment-leg/1 ") == "fixture://shipment-leg/1"
    assert require_leg_source_ref("tenant:manual") == "tenant:manual"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_leg_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidShipmentLeg):
        require_leg_source_ref(raw)


def test_require_leg_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_leg_shipment_id(token) == token
    assert require_leg_location_id(token, field="origin_location_id") == token


def test_require_leg_ids_reject_text() -> None:
    with pytest.raises(InvalidShipmentLeg, match="UUID"):
        require_leg_shipment_id("s")  # type: ignore[arg-type]
    with pytest.raises(InvalidShipmentLeg, match="UUID"):
        require_leg_location_id("o", field="origin_location_id")  # type: ignore[arg-type]


def test_require_distinct_ends_rejects_same_place() -> None:
    token = uuid4()
    with pytest.raises(InvalidShipmentLeg, match="różne"):
        require_distinct_ends(token, token)


def test_require_road_location_kind_rejects_port() -> None:
    with pytest.raises(InvalidShipmentLeg, match="UN/LOCODE"):
        require_road_location_kind("unlocode")
    assert require_road_location_kind("postal_zone") == "postal_zone"
    assert require_road_location_kind("address") == "address"


def test_require_road_leg_kind_is_road() -> None:
    assert require_road_leg_kind() == "road"
    assert require_leg_kind(None) == "road"
    assert require_leg_kind(" rail ") == "rail"
    assert require_leg_kind("china_rail") == "china_rail"


def test_require_leg_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidShipmentLeg, match="spoza zbioru"):
        require_leg_kind("ocean_lcl")


def test_require_rail_location_kind_rejects_zone() -> None:
    with pytest.raises(InvalidShipmentLeg, match="UN/LOCODE"):
        require_rail_location_kind("postal_zone")
    assert require_rail_location_kind("unlocode") == "unlocode"


def test_require_rail_port_flag_rejects_sea_only() -> None:
    with pytest.raises(InvalidShipmentLeg, match="flagi rail"):
        require_rail_port_flag(["port"])
    require_rail_port_flag(["port", "rail"])


def test_require_china_rail_country_rejects_other() -> None:
    with pytest.raises(InvalidShipmentLeg, match="Chinami"):
        require_china_rail_country("PL")
    require_china_rail_country("CN")
