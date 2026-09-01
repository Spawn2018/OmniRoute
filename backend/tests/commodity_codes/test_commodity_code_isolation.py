from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.commodity_code import CommodityCode


@pytest.mark.integration
@pytest.mark.asyncio
async def test_commodity_code_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    code_a = CommodityCode(
        id=uuid4(),
        organization_id=org_a.id,
        code="0805",
        name="Citrus A",
        aliases=["080510"],
        source_ref="tenant:manual",
        created_by=user_a.id,
    )
    code_b = CommodityCode(
        id=uuid4(),
        organization_id=org_b.id,
        code="0805",
        name="Citrus B",
        aliases=["080520"],
        source_ref="tenant:manual",
        created_by=user_b.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(code_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(code_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CommodityCode))).all())
    assert {row.id for row in visible_a} == {code_a.id}
    foreign_b = await session.scalar(select(CommodityCode).where(CommodityCode.id == code_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CommodityCode))).all())
    assert {row.id for row in visible_b} == {code_b.id}
    foreign_a = await session.scalar(select(CommodityCode).where(CommodityCode.id == code_a.id))
    assert foreign_a is None
