import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidResource
from app.domain.resource import (
    require_adr_certified,
    require_capacity_kg,
    require_capacity_ldm,
    require_capacity_m3,
    require_display_name,
    require_inventory_no,
    require_phone,
    require_reefer,
    require_registration_no,
    require_resource_kind,
    require_resource_source_ref,
    require_tail_lift,
)


def test_resource_allowlists() -> None:
    assert require_resource_kind("trailer") == "trailer"
    assert require_display_name(" MAN TGX ") == "MAN TGX"
    assert require_registration_no(" WX 1234 ") == "WX 1234"
    assert require_registration_no("") is None
    assert require_registration_no(None) is None
    assert require_inventory_no(" INV-1 ") == "INV-1"
    assert require_inventory_no("") is None
    assert require_inventory_no(None) is None
    assert require_adr_certified(True) is True
    assert require_adr_certified(None) is None
    assert require_reefer(True) is True
    assert require_reefer(None) is None
    assert require_tail_lift(True) is True
    assert require_tail_lift(None) is None
    assert require_phone(" +48 ") == "+48"
    assert require_phone("") is None
    assert require_phone(None) is None
    assert require_resource_source_ref("fixture://resource/man") == "fixture://resource/man"
    assert require_capacity_kg("24000") is not None
    assert require_capacity_ldm("13.6") is not None
    assert require_capacity_m3("90") is not None
    assert require_capacity_kg(None) is None
    assert require_capacity_ldm(None) is None
    assert require_capacity_m3(None) is None


def test_resource_rejects_truck_kind_and_foreign_ref() -> None:
    with pytest.raises(InvalidResource, match="rodzaj"):
        require_resource_kind("truck")
    with pytest.raises(InvalidResource, match="nazwa"):
        require_display_name("  ")
    with pytest.raises(InvalidResource, match="obce"):
        require_resource_source_ref("https://evil.example/resource")
    with pytest.raises(InvalidResource, match="pojemność"):
        require_capacity_kg(0.5)
    with pytest.raises(InvalidResource, match="pojemność"):
        require_capacity_kg(0)
    with pytest.raises(InvalidResource, match="ldm"):
        require_capacity_ldm(0.5)
    with pytest.raises(InvalidResource, match="m3"):
        require_capacity_m3(0.5)
    with pytest.raises(InvalidResource, match="inwentarzowy"):
        require_inventory_no("x" * 33)
    with pytest.raises(InvalidResource, match="adr"):
        require_adr_certified("tak")
    with pytest.raises(InvalidResource, match="reefer"):
        require_reefer("tak")
    with pytest.raises(InvalidResource, match="winda"):
        require_tail_lift("tak")
    with pytest.raises(InvalidResource, match="telefon"):
        require_phone("1" * 65)


@given(st.sampled_from(["truck", "car", "fleet"]))
def test_resource_kind_is_not_loose_vehicle_word(raw: str) -> None:
    with pytest.raises(InvalidResource, match="rodzaj"):
        require_resource_kind(raw)
