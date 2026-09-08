import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidShipmentStakeholder
from app.domain.shipment_stakeholder import (
    require_stakeholder_role,
    require_stakeholder_source_ref,
)


def test_allowlisted_role_and_manual_source() -> None:
    assert require_stakeholder_role(" shipper ") == "shipper"
    assert require_stakeholder_source_ref("tenant:manual") == "tenant:manual"


def test_reject_exp1_role_and_foreign_source() -> None:
    with pytest.raises(InvalidShipmentStakeholder, match="rola"):
        require_stakeholder_role("sold_to")
    with pytest.raises(InvalidShipmentStakeholder, match="obce"):
        require_stakeholder_source_ref("icc://incoterms-2020")


@given(st.sampled_from(["notify", "bill_to", "ship_to", "customer"]))
def test_reject_party_catalog_roles_as_stakeholder(raw: str) -> None:
    with pytest.raises(InvalidShipmentStakeholder, match="rola"):
        require_stakeholder_role(raw)
