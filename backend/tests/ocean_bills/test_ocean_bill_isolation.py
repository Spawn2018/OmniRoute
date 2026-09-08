from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.ocean_bill import OceanBill
from tests.sales_invoices.test_sales_invoice_isolation import _booked


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ocean_bill_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="oa")
    row_a = OceanBill(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        bill_no="HLCUSHA1234567",
        bill_kind="hbl",
        source_ref="fixture://ocean-bill/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="ob")
    row_b = OceanBill(
        id=uuid4(),
        organization_id=org_b.id,
        shipment_id=ship_b.id,
        bill_no="MSCU-AB12",
        bill_kind="mbl",
        source_ref="fixture://ocean-bill/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(OceanBill))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(OceanBill).where(OceanBill.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(OceanBill))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ocean_bill_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="ox")

    await bind_tenant(session, org_a.id)
    session.add(
        OceanBill(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            bill_no="STOLEN1",
            bill_kind="hbl",
            source_ref="fixture://ocean-bill/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
