from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.shipment_stakeholder import ShipmentStakeholder
from tests.sales_invoices.test_sales_invoice_isolation import _booked

_MANUAL = "tenant:manual"


def _party(*, organization_id, legal_name: str, created_by):
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["agent"],
        source_ref=_MANUAL,
        is_active=True,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_stakeholder_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sa")
    party_a = _party(organization_id=org_a.id, legal_name="Agent A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    row_a = ShipmentStakeholder(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        party_id=party_a.id,
        role="shipper",
        source_ref="fixture://shipment-stakeholder/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sb")
    party_b = _party(organization_id=org_b.id, legal_name="Agent B", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    row_b = ShipmentStakeholder(
        id=uuid4(),
        organization_id=org_b.id,
        shipment_id=ship_b.id,
        party_id=party_b.id,
        role="consignee",
        source_ref="fixture://shipment-stakeholder/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ShipmentStakeholder))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(ShipmentStakeholder).where(ShipmentStakeholder.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ShipmentStakeholder))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_stakeholder_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sx")
    await bind_tenant(session, org_a.id)
    party_a = _party(organization_id=org_a.id, legal_name="Agent A", created_by=user_a.id)
    session.add(party_a)
    await session.flush()
    session.add(
        ShipmentStakeholder(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            party_id=party_a.id,
            role="shipper",
            source_ref="fixture://shipment-stakeholder/stolen-ship",
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_stakeholder_rejects_foreign_party(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Agent X", created_by=user_b.id)
    session.add(party_b)
    await session.flush()
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sy")
    session.add(
        ShipmentStakeholder(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            party_id=party_b.id,
            role="consignee",
            source_ref="fixture://shipment-stakeholder/stolen-party",
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()
