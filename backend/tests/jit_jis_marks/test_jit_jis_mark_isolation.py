from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.jit_jis_mark import JitJisMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "jj_jit_01",
    flow_kind: str = "jit",
    source_ref: str = "fixture://jit-jis-mark/",
) -> JitJisMark:
    return JitJisMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        flow_kind=flow_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_jit_jis_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="shared_01",
        flow_kind="kanban",
        source_ref="fixture://jit-jis-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(JitJisMark))).all())
    assert {row.id for row in visible} == {row_a.id}
