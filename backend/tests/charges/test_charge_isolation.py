from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError

from app.core.database import bind_tenant
from app.models.charge import Charge


def _charge(*, organization_id, created_by, sell: str) -> Charge:
    return Charge(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        buy_amount=Decimal("10.0000"),
        buy_currency="EUR",
        sell_amount=Decimal(sell),
        sell_currency="EUR",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    charge_a = _charge(organization_id=org_a.id, created_by=user_a.id, sell="14.0000")
    charge_b = _charge(organization_id=org_b.id, created_by=user_b.id, sell="16.0000")

    await bind_tenant(session, org_a.id)
    session.add(charge_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(charge_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Charge))).all())
    assert {row.id for row in visible_a} == {charge_a.id}
    assert visible_a[0].source_ref is None
    foreign_b = await session.scalar(select(Charge).where(Charge.id == charge_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Charge))).all())
    assert {row.id for row in visible_b} == {charge_b.id}
    foreign_a = await session.scalar(select(Charge).where(Charge.id == charge_a.id))
    assert foreign_a is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_rejects_mixed_currency_at_database(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    row = Charge(
        id=uuid4(),
        organization_id=org_a.id,
        charge_code="THC",
        buy_amount=Decimal("10.0000"),
        buy_currency="EUR",
        sell_amount=Decimal("14.0000"),
        sell_currency="USD",
        created_by=user_a.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(row)
    with pytest.raises(DBAPIError):
        await session.flush()
