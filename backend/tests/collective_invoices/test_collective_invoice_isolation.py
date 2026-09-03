from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.collective_invoice import CollectiveInvoice
from app.models.sales_invoice import SalesInvoice
from app.models.shipment import Shipment
from tests.sales_invoices.test_sales_invoice_isolation import _booked, _buy_rate, _quote


async def _invoice_on(session, *, ship: Shipment, user_id, suffix: str) -> SalesInvoice:
    row = SalesInvoice(
        id=uuid4(),
        organization_id=ship.organization_id,
        shipment_id=ship.id,
        invoice_kind="issued",
        invoice_ref=f"FV/{suffix}",
        source_ref=f"fixture://sales-invoice/{suffix}",
        created_by=user_id,
    )
    session.add(row)
    await session.flush()
    return row


async def _extra_ship(session, *, ship: Shipment, user_id, suffix: str) -> Shipment:
    rate = _buy_rate(
        organization_id=ship.organization_id,
        created_by=user_id,
        source_ref=f"tariff://collective-{suffix}",
    )
    session.add(rate)
    await session.flush()
    quote = _quote(
        organization_id=ship.organization_id,
        created_by=user_id,
        rate_line_id=rate.id,
        source_ref=f"tariff://collective-{suffix}",
    )
    session.add(quote)
    await session.flush()
    extra = Shipment(
        id=uuid4(),
        organization_id=ship.organization_id,
        quotation_id=quote.id,
        party_id=ship.party_id,
        source_ref=f"fixture://shipment/collective-{suffix}",
        status="draft",
        created_by=user_id,
    )
    session.add(extra)
    await session.flush()
    return extra


async def _member(session, *, org, user, invoice_id, shipment_id, suffix: str) -> CollectiveInvoice:
    row = CollectiveInvoice(
        id=uuid4(),
        organization_id=org.id,
        sales_invoice_id=invoice_id,
        shipment_id=shipment_id,
        source_ref=f"fixture://collective-invoice/{suffix}",
        created_by=user.id,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_collective_invoice_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="ca")
    extra_a = await _extra_ship(session, ship=ship_a, user_id=user_a.id, suffix="ca")
    inv_a = await _invoice_on(session, ship=ship_a, user_id=user_a.id, suffix="ca")
    row_a = await _member(
        session,
        org=org_a,
        user=user_a,
        invoice_id=inv_a.id,
        shipment_id=extra_a.id,
        suffix="a",
    )

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="cb")
    extra_b = await _extra_ship(session, ship=ship_b, user_id=user_b.id, suffix="cb")
    inv_b = await _invoice_on(session, ship=ship_b, user_id=user_b.id, suffix="cb")
    row_b = await _member(
        session,
        org=org_b,
        user=user_b,
        invoice_id=inv_b.id,
        shipment_id=extra_b.id,
        suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CollectiveInvoice))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(CollectiveInvoice).where(CollectiveInvoice.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CollectiveInvoice))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_collective_invoice_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="cx")

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="cy")
    inv_a = await _invoice_on(session, ship=ship_a, user_id=user_a.id, suffix="cy")
    session.add(
        CollectiveInvoice(
            id=uuid4(),
            organization_id=org_a.id,
            sales_invoice_id=inv_a.id,
            shipment_id=ship_b.id,
            source_ref="fixture://collective-invoice/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
