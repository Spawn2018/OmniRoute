from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.groupage_dispatcher_mark import GroupageDispatcherMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "gdp_line_01",
    dispatcher_kind: str = "line",
    source_ref: str = "tenant:manual",
) -> GroupageDispatcherMark:
    return GroupageDispatcherMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        dispatcher_kind=dispatcher_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_groupage_dispatcher_mark_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        mark_code="gdp_hub_02",
        dispatcher_kind="hub",
        source_ref="fixture://groupage-dispatcher-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(GroupageDispatcherMark))).all())
    assert {row.id for row in visible} == {row_a.id}
