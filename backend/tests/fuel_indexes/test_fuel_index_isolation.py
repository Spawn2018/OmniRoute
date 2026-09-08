from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.fuel_index import FuelIndex


def _row(*, organization_id, created_by, kind: str, day: date, value: str) -> FuelIndex:
    return FuelIndex(
        id=uuid4(),
        organization_id=organization_id,
        index_kind=kind,
        published_on=day,
        index_value=Decimal(value),
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fuel_index_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(
        organization_id=org_a.id,
        created_by=user_a.id,
        kind="fsc",
        day=date(2026, 3, 1),
        value="1.2500",
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        kind="baf",
        day=date(2026, 3, 2),
        value="1.1000",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(FuelIndex))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(FuelIndex).where(FuelIndex.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(FuelIndex))).all())
    assert {row.id for row in visible_b} == {row_b.id}
