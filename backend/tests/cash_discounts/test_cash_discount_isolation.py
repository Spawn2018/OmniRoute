from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.cash_discount import CashDiscount
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


def _discount(
    *,
    organization_id,
    created_by,
    sales_invoice_id,
    discount_kind: str = "skonto",
) -> CashDiscount:
    return CashDiscount(
        id=uuid4(),
        organization_id=organization_id,
        sales_invoice_id=sales_invoice_id,
        discount_kind=discount_kind,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cash_discount_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="da")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="da")
    row_a = _discount(
        organization_id=org_a.id,
        created_by=user_a.id,
        sales_invoice_id=inv_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="db")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="db")
    row_b = _discount(
        organization_id=org_b.id,
        created_by=user_b.id,
        sales_invoice_id=inv_b.id,
        discount_kind="reserve",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CashDiscount))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(CashDiscount).where(CashDiscount.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CashDiscount))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cash_discount_rejects_foreign_invoice(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="xb")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="xb")

    await bind_tenant(session, org_a.id)
    session.add(
        _discount(
            organization_id=org_a.id,
            created_by=user_a.id,
            sales_invoice_id=inv_b.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cash_discount_rejects_duplicate_kind(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="dup")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="dup")
    session.add(
        _discount(
            organization_id=org_a.id,
            created_by=user_a.id,
            sales_invoice_id=inv_a.id,
        ),
    )
    await session.flush()
    session.add(
        _discount(
            organization_id=org_a.id,
            created_by=user_a.id,
            sales_invoice_id=inv_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cash_discount_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM cash_discount WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_cash_discount_organization_id" in joined
        or "uq_cash_discount_org_invoice_kind" in joined
    )
