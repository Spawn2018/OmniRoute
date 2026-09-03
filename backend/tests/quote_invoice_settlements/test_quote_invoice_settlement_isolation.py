from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.quote_invoice_settlement import QuoteInvoiceSettlement
from app.models.sales_invoice import SalesInvoice
from tests.sales_invoices.test_sales_invoice_isolation import _booked


async def _invoice(session, *, ship, user_id, suffix: str) -> SalesInvoice:
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_settlement_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sa")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="sa")
    row_a = QuoteInvoiceSettlement(
        id=uuid4(),
        organization_id=org_a.id,
        quotation_id=ship_a.quotation_id,
        sales_invoice_id=inv_a.id,
        source_ref="fixture://quote-invoice-settlement/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sb")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="sb")
    row_b = QuoteInvoiceSettlement(
        id=uuid4(),
        organization_id=org_b.id,
        quotation_id=ship_b.quotation_id,
        sales_invoice_id=inv_b.id,
        source_ref="fixture://quote-invoice-settlement/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(QuoteInvoiceSettlement))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    foreign_b = await session.scalar(
        select(QuoteInvoiceSettlement).where(QuoteInvoiceSettlement.id == row_b.id),
    )
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(QuoteInvoiceSettlement))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_settlement_rejects_foreign_invoice(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="xb")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="xb")

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="xa")
    stolen = QuoteInvoiceSettlement(
        id=uuid4(),
        organization_id=org_a.id,
        quotation_id=ship_a.quotation_id,
        sales_invoice_id=inv_b.id,
        source_ref="fixture://quote-invoice-settlement/stolen",
        created_by=user_a.id,
    )
    session.add(stolen)
    with pytest.raises(IntegrityError):
        await session.flush()
