from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.stop_group import StopGroup
from tests.sales_invoices.test_sales_invoice_isolation import _booked


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_group_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sga")
    row_a = StopGroup(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        group_code="GRP-A",
        source_ref="fixture://stop-group/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sgb")
    row_b = StopGroup(
        id=uuid4(),
        organization_id=org_b.id,
        shipment_id=ship_b.id,
        group_code="GRP-B",
        source_ref="fixture://stop-group/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(StopGroup))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(StopGroup).where(StopGroup.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(StopGroup))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_group_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sgx")

    await bind_tenant(session, org_a.id)
    session.add(
        StopGroup(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            group_code="STOLEN",
            source_ref="fixture://stop-group/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_group_allows_n_rows_on_one_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sgn")
    session.add(
        StopGroup(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship.id,
            group_code="G1",
            source_ref="fixture://stop-group/n1",
            created_by=user_a.id,
        )
    )
    session.add(
        StopGroup(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship.id,
            group_code="G2",
            source_ref="fixture://stop-group/n2",
            created_by=user_a.id,
        )
    )
    await session.flush()
    rows = list((await session.scalars(select(StopGroup))).all())
    assert {row.group_code for row in rows} == {"G1", "G2"}
