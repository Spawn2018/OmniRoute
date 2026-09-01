from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.quotation import Quotation
from app.models.rate_line import RateLine


def _buy_rate(*, organization_id, created_by, source_ref: str) -> RateLine:
    return RateLine(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


def _quote(*, organization_id, created_by, rate_line_id, source_ref: str) -> Quotation:
    return Quotation(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        rate_line_id=rate_line_id,
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quotation_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    session.add(rate_a)
    await session.flush()
    quote_a = _quote(
        organization_id=org_a.id,
        created_by=user_a.id,
        rate_line_id=rate_a.id,
        source_ref="tariff://a",
    )
    session.add(quote_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")
    session.add(rate_b)
    await session.flush()
    quote_b = _quote(
        organization_id=org_b.id,
        created_by=user_b.id,
        rate_line_id=rate_b.id,
        source_ref="tariff://b",
    )
    session.add(quote_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Quotation))).all())
    assert {row.id for row in visible_a} == {quote_a.id}
    foreign_b = await session.scalar(select(Quotation).where(Quotation.id == quote_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Quotation))).all())
    assert {row.id for row in visible_b} == {quote_b.id}
    foreign_a = await session.scalar(select(Quotation).where(Quotation.id == quote_a.id))
    assert foreign_a is None
