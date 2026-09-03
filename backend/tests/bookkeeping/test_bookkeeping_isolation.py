from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.bookkeeping import Bookkeeping
from tests.bank_payments.test_bank_payment_isolation import _invoice
from tests.charges.test_charge_isolation import _charge
from tests.sales_invoices.test_sales_invoice_isolation import _booked


async def _entry(session, *, org, user, charge_id, invoice_id, suffix: str) -> Bookkeeping:
    row = Bookkeeping(
        id=uuid4(),
        organization_id=org.id,
        charge_id=charge_id,
        sales_invoice_id=invoice_id,
        source_ref=f"fixture://bookkeeping/{suffix}",
        created_by=user.id,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_bookkeeping_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="ba")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="ba")
    charge_a = _charge(organization_id=org_a.id, created_by=user_a.id, sell="14.0000")
    session.add(charge_a)
    await session.flush()
    row_a = await _entry(
        session,
        org=org_a,
        user=user_a,
        charge_id=charge_a.id,
        invoice_id=inv_a.id,
        suffix="a",
    )

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="bb")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="bb")
    charge_b = _charge(organization_id=org_b.id, created_by=user_b.id, sell="16.0000")
    session.add(charge_b)
    await session.flush()
    row_b = await _entry(
        session,
        org=org_b,
        user=user_b,
        charge_id=charge_b.id,
        invoice_id=inv_b.id,
        suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Bookkeeping))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(Bookkeeping).where(Bookkeeping.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Bookkeeping))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_bookkeeping_rejects_foreign_charge(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    charge_b = _charge(organization_id=org_b.id, created_by=user_b.id, sell="18.0000")
    session.add(charge_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="bx")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="bx")
    session.add(
        Bookkeeping(
            id=uuid4(),
            organization_id=org_a.id,
            charge_id=charge_b.id,
            sales_invoice_id=inv_a.id,
            source_ref="fixture://bookkeeping/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
