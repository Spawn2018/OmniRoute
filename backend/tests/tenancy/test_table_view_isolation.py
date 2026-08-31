from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.table_view import TableView


@pytest.mark.integration
@pytest.mark.asyncio
async def test_table_view_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    view_a = TableView(
        id=uuid4(),
        organization_id=org_a.id,
        user_id=user_a.id,
        table_key="tenancy.users",
        name="Domyślny",
        config={"density": "compact"},
        created_by=user_a.id,
    )
    view_b = TableView(
        id=uuid4(),
        organization_id=org_b.id,
        user_id=user_b.id,
        table_key="tenancy.users",
        name="Domyślny",
        config={"density": "comfortable"},
        created_by=user_b.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(view_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(view_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(TableView))).all())
    assert {row.id for row in visible_a} == {view_a.id}
    assert await session.get(TableView, view_b.id) is None

    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(TableView))).all())
    assert {row.id for row in visible_b} == {view_b.id}
    assert await session.get(TableView, view_a.id) is None
