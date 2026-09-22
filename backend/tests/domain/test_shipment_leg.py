from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidShipmentLeg
from app.domain.shipment_leg import (
    require_air_port_flag,
    require_air_waybill_kind,
    require_air_waybill_no,
    require_china_rail_country,
    require_distinct_ends,
    require_leg_kind,
    require_leg_location_id,
    require_leg_shipment_id,
    require_leg_source_ref,
    require_mawb_iata_check,
    require_ocean_seaport,
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
    assert require_leg_kind("ocean_lcl") == "ocean_lcl"
    assert require_leg_kind("air") == "air"


def test_require_leg_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidShipmentLeg, match="spoza zbioru"):
        require_leg_kind("air_parcel")


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


def test_require_ocean_seaport_rejects_inland() -> None:
    with pytest.raises(InvalidShipmentLeg, match="śródlądowy"):
        require_ocean_seaport(False)
    require_ocean_seaport(True)


def test_require_air_port_flag_rejects_sea_only() -> None:
    with pytest.raises(InvalidShipmentLeg, match="flagi airport"):
        require_air_port_flag(["port"])
    require_air_port_flag(["port", "airport"])


@given(st.sampled_from(["020-12345675", "HAWB-1", "awb9"]))
def test_air_waybill_keeps_carrier_token(raw: str) -> None:
    assert require_air_waybill_no(raw) == raw
    assert require_air_waybill_no(None) is None
    assert require_air_waybill_no("") is None


@given(st.sampled_from(["X", "HAWB 1", "a" * 33, "hawb_west"]))
def test_air_waybill_rejects_non_carrier_token(raw: str) -> None:
    with pytest.raises(InvalidShipmentLeg, match="numer"):
        require_air_waybill_no(raw)


@given(
    prefix=st.integers(min_value=0, max_value=999),
    serial=st.integers(min_value=0, max_value=9_999_999),
    hyphen=st.booleans(),
)
def test_mawb_iata_check_accepts_serial_modulo_seven(
    prefix: int,
    serial: int,
    hyphen: bool,
) -> None:
    body = f"{serial:07d}{serial % 7}"
    token = f"{prefix:03d}-{body}" if hyphen else f"{prefix:03d}{body}"
    assert require_mawb_iata_check(token) == token


@given(
    prefix=st.integers(min_value=0, max_value=999),
    serial=st.integers(min_value=0, max_value=9_999_999),
    hyphen=st.booleans(),
)
def test_mawb_iata_check_rejects_wrong_digit(
    prefix: int,
    serial: int,
    hyphen: bool,
) -> None:
    bad = (serial % 7 + 1) % 7
    body = f"{serial:07d}{bad}"
    token = f"{prefix:03d}-{body}" if hyphen else f"{prefix:03d}{body}"
    with pytest.raises(InvalidShipmentLeg, match="cyfra"):
        require_mawb_iata_check(token)


@given(st.sampled_from(["HAWB-1", "MAWB0001", "awb9", "020-1234567", ""]))
def test_mawb_iata_check_leaves_non_iata_token(raw: str) -> None:
    expected = None if raw == "" else raw
    assert require_mawb_iata_check(expected) == expected
    assert require_air_waybill_no("020-12345676") == "020-12345676"


def test_air_waybill_rejects_non_air_kind() -> None:
    with pytest.raises(InvalidShipmentLeg, match="list"):
        require_air_waybill_kind("road", "HAWB-1", None)
    require_air_waybill_kind("air", "HAWB-1", "020-12345675")
    require_air_waybill_kind("road", None, None)
