from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text, update
from sqlalchemy.exc import DBAPIError

from app.core.database import bind_tenant
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_line_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    rate_a = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")
    rate_b = _buy_rate(organization_id=org_b.id, created_by=user_b.id, source_ref="tariff://b")

    await bind_tenant(session, org_a.id)
    session.add(rate_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(rate_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(RateLine))).all())
    assert {row.id for row in visible_a} == {rate_a.id}
    foreign_b = await session.scalar(select(RateLine).where(RateLine.id == rate_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(RateLine))).all())
    assert {row.id for row in visible_b} == {rate_b.id}
    foreign_a = await session.scalar(select(RateLine).where(RateLine.id == rate_a.id))
    assert foreign_a is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_line_amount_cannot_mutate_in_place(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    rate = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")

    await bind_tenant(session, org_a.id)
    session.add(rate)
    await session.flush()

    with pytest.raises(DBAPIError):
        await session.execute(
            update(RateLine).where(RateLine.id == rate.id).values(amount=Decimal("99.0000"))
        )
        await session.flush()

    await session.rollback()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    stored = await session.scalar(select(RateLine).where(RateLine.id == rate.id))
    assert stored is not None
    assert stored.amount == Decimal("10.0000")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_line_delete_is_rejected(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    rate = _buy_rate(organization_id=org_a.id, created_by=user_a.id, source_ref="tariff://a")

    await bind_tenant(session, org_a.id)
    session.add(rate)
    await session.flush()

    with pytest.raises(DBAPIError):
        await session.execute(text("DELETE FROM rate_line WHERE id = :id"), {"id": rate.id})
        await session.flush()
    await session.rollback()
