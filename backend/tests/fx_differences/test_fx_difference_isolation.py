from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.fx_difference import FxDifference
from tests.nbp_rates.test_nbp_rate_isolation import _rate
from tests.sales_invoices.test_sales_invoice_isolation import _booked


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


async def _noted(session, *, org, user, quotation_id, rate_id, suffix: str) -> FxDifference:
    row = FxDifference(
        id=uuid4(),
        organization_id=org.id,
        quotation_id=quotation_id,
        nbp_rate_id=rate_id,
        source_ref=f"fixture://fx-difference/{suffix}",
        created_by=user.id,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fx_difference_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="fa")
    rate_a = await _rate_row(
        session, org=org_a, user=user_a, currency="EUR", day=date(2026, 9, 1), mid="4.2500",
    )
    row_a = await _noted(
        session,
        org=org_a,
        user=user_a,
        quotation_id=ship_a.quotation_id,
        rate_id=rate_a.id,
        suffix="a",
    )

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="fb")
    rate_b = await _rate_row(
        session, org=org_b, user=user_b, currency="USD", day=date(2026, 9, 2), mid="3.8000",
    )
    row_b = await _noted(
        session,
        org=org_b,
        user=user_b,
        quotation_id=ship_b.quotation_id,
        rate_id=rate_b.id,
        suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(FxDifference))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(FxDifference).where(FxDifference.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(FxDifference))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fx_difference_rejects_foreign_rate(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    rate_b = await _rate_row(
        session, org=org_b, user=user_b, currency="GBP", day=date(2026, 9, 3), mid="5.1000",
    )

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="fx")
    session.add(
        FxDifference(
            id=uuid4(),
            organization_id=org_a.id,
            quotation_id=ship_a.quotation_id,
            nbp_rate_id=rate_b.id,
            source_ref="fixture://fx-difference/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
