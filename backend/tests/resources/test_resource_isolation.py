from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.core.database import bind_tenant
from app.models.resource import Resource


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resource_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = Resource(
        id=uuid4(),
        organization_id=org_a.id,
        resource_kind="vehicle",
        display_name="MAN A",
        registration_no="WA 1",
        source_ref="fixture://resource/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = Resource(
        id=uuid4(),
        organization_id=org_b.id,
        resource_kind="driver",
        display_name="Kowalski",
        registration_no=None,
        source_ref="fixture://resource/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Resource))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(Resource).where(Resource.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Resource))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resource_list_uses_org_kind_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM resource "
            "WHERE organization_id = :org_id AND resource_kind = 'vehicle' "
            "AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_resource_org_kind" in joined
