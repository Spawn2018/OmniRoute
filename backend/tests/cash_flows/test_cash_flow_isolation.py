from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.cash_flow import CashFlow
from tests.bank_payments.test_bank_payment_isolation import _account, _invoice, _payment
from tests.sales_invoices.test_sales_invoice_isolation import _booked


async def _flow(session, *, org, user, quotation_id, payment_id, suffix: str) -> CashFlow:
    row = CashFlow(
        id=uuid4(),
        organization_id=org.id,
        quotation_id=quotation_id,
        bank_payment_id=payment_id,
        source_ref=f"fixture://cash-flow/{suffix}",
        created_by=user.id,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cash_flow_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="qa")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="qa")
    acc_a = await _account(session, ship=ship_a, suffix="qa")
    pay_a = await _payment(
        session,
        org_id=org_a.id,
        user_id=user_a.id,
        invoice_id=inv_a.id,
        account_id=acc_a.id,
        suffix="qa",
    )
    row_a = await _flow(
        session,
        org=org_a,
        user=user_a,
        quotation_id=ship_a.quotation_id,
        payment_id=pay_a.id,
        suffix="a",
    )

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="qb")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="qb")
    acc_b = await _account(session, ship=ship_b, suffix="qb")
    pay_b = await _payment(
        session,
        org_id=org_b.id,
        user_id=user_b.id,
        invoice_id=inv_b.id,
        account_id=acc_b.id,
        suffix="qb",
    )
    row_b = await _flow(
        session,
        org=org_b,
        user=user_b,
        quotation_id=ship_b.quotation_id,
        payment_id=pay_b.id,
        suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CashFlow))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(CashFlow).where(CashFlow.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CashFlow))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cash_flow_rejects_foreign_payment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="xb")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="xb")
    acc_b = await _account(session, ship=ship_b, suffix="xb")
    pay_b = await _payment(
        session,
        org_id=org_b.id,
        user_id=user_b.id,
        invoice_id=inv_b.id,
        account_id=acc_b.id,
        suffix="xb",
    )

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="xa")
    session.add(
        CashFlow(
            id=uuid4(),
            organization_id=org_a.id,
            quotation_id=ship_a.quotation_id,
            bank_payment_id=pay_b.id,
            source_ref="fixture://cash-flow/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
