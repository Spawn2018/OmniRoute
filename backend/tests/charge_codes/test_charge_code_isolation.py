from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.charge_code import ChargeCode


@pytest.mark.integration
@pytest.mark.asyncio
async def test_charge_code_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    code_a = ChargeCode(
        id=uuid4(),
        organization_id=org_a.id,
        code="BAF",
        name="Bunker A",
        aliases=["BUNKER"],
        source_ref="fixture://charge-code/test",
        created_by=user_a.id,
    )
    code_b = ChargeCode(
        id=uuid4(),
        organization_id=org_b.id,
        code="BAF",
        name="Bunker B",
        aliases=["FUEL"],
        source_ref="fixture://charge-code/test",
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
    visible_a = list((await session.scalars(select(ChargeCode))).all())
    assert {row.id for row in visible_a} == {code_a.id}
    foreign_b = await session.scalar(select(ChargeCode).where(ChargeCode.id == code_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ChargeCode))).all())
    assert {row.id for row in visible_b} == {code_b.id}
    foreign_a = await session.scalar(select(ChargeCode).where(ChargeCode.id == code_a.id))
    assert foreign_a is None
