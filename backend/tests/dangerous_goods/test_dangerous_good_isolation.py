from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.dangerous_good import DangerousGood


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dangerous_good_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    good_a = DangerousGood(
        id=uuid4(),
        organization_id=org_a.id,
        un_number="1203",
        imdg_class="3",
        adr_tunnel_code="D",
        segregation_group="none",
        packing_group="II",
        marine_pollutant=False,
        name="Petrol A",
        aliases=["UN1203"],
        source_ref="imdg:1203",
        created_by=user_a.id,
    )
    good_b = DangerousGood(
        id=uuid4(),
        organization_id=org_b.id,
        un_number="1203",
        imdg_class="3",
        adr_tunnel_code="D",
        segregation_group="none",
        packing_group="II",
        marine_pollutant=False,
        name="Petrol B",
        aliases=["UN1203"],
        source_ref="imdg:1203",
        created_by=user_b.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(good_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(good_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(DangerousGood))).all())
    assert {row.id for row in visible_a} == {good_a.id}
    foreign_b = await session.scalar(select(DangerousGood).where(DangerousGood.id == good_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(DangerousGood))).all())
    assert {row.id for row in visible_b} == {good_b.id}
    foreign_a = await session.scalar(select(DangerousGood).where(DangerousGood.id == good_a.id))
    assert foreign_a is None
