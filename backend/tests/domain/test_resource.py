import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidResource
from app.domain.resource import (
    require_capacity_kg,
    require_capacity_ldm,
    require_display_name,
    require_registration_no,
    require_resource_kind,
    require_resource_source_ref,
)


def test_resource_allowlists() -> None:
    assert require_resource_kind("trailer") == "trailer"
    assert require_display_name(" MAN TGX ") == "MAN TGX"
    assert require_registration_no(" WX 1234 ") == "WX 1234"
    assert require_registration_no("") is None
    assert require_registration_no(None) is None
    assert require_resource_source_ref("fixture://resource/man") == "fixture://resource/man"
    assert require_capacity_kg("24000") is not None
    assert require_capacity_ldm("13.6") is not None
    assert require_capacity_kg(None) is None
    assert require_capacity_ldm(None) is None


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


@given(st.sampled_from(["truck", "car", "fleet"]))
def test_resource_kind_is_not_loose_vehicle_word(raw: str) -> None:
    with pytest.raises(InvalidResource, match="rodzaj"):
        require_resource_kind(raw)
