from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.money_cost import MoneyCost
from tests.bank_payments.test_bank_payment_isolation import _account, _invoice, _payment
from tests.nbp_rates.test_nbp_rate_isolation import _rate
from tests.sales_invoices.test_sales_invoice_isolation import _booked


async def _paid(session, *, org, user, suffix: str):
    ship = await _booked(session, organization_id=org.id, user_id=user.id, suffix=suffix)
    invoice = await _invoice(session, ship=ship, user_id=user.id, suffix=suffix)
    account = await _account(session, ship=ship, suffix=suffix)
    return await _payment(
        session,
        org_id=org.id,
        user_id=user.id,
        invoice_id=invoice.id,
        account_id=account.id,
        suffix=suffix,
    )


async def _noted(session, *, org, user, payment_id, rate_id, suffix: str) -> MoneyCost:
    row = MoneyCost(
        id=uuid4(),
        organization_id=org.id,
        bank_payment_id=payment_id,
        nbp_rate_id=rate_id,
        source_ref=f"fixture://money-cost/{suffix}",
        created_by=user.id,
    )
    session.add(row)
    await session.flush()
    return row


async def _rate_row(session, *, org, user, currency: str, day: date, mid: str):
    row = _rate(
        organization_id=org.id,
        user_id=user.id,
        currency=currency,
        rate_date=day,
        mid=mid,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_money_cost_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    pay_a = await _paid(session, org=org_a, user=user_a, suffix="ca")
    rate_a = await _rate_row(
        session, org=org_a, user=user_a, currency="EUR", day=date(2026, 9, 1), mid="4.2500",
    )
    row_a = await _noted(
        session, org=org_a, user=user_a, payment_id=pay_a.id, rate_id=rate_a.id, suffix="a",
    )

    await bind_tenant(session, org_b.id)
    pay_b = await _paid(session, org=org_b, user=user_b, suffix="cb")
    rate_b = await _rate_row(
        session, org=org_b, user=user_b, currency="USD", day=date(2026, 9, 2), mid="3.8000",
    )
    row_b = await _noted(
        session, org=org_b, user=user_b, payment_id=pay_b.id, rate_id=rate_b.id, suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(MoneyCost))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(MoneyCost).where(MoneyCost.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(MoneyCost))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_money_cost_rejects_foreign_rate(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    rate_b = await _rate_row(
        session, org=org_b, user=user_b, currency="GBP", day=date(2026, 9, 3), mid="5.1000",
    )

    await bind_tenant(session, org_a.id)
    pay_a = await _paid(session, org=org_a, user=user_a, suffix="xa")
    session.add(
        MoneyCost(
            id=uuid4(),
            organization_id=org_a.id,
            bank_payment_id=pay_a.id,
            nbp_rate_id=rate_b.id,
            source_ref="fixture://money-cost/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
