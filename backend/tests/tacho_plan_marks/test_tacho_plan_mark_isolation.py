from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.tacho_plan_mark import TachoPlanMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "tpm_plan_01",
    constraint_kind: str = "plan",
    source_ref: str = "tenant:manual",
) -> TachoPlanMark:
    return TachoPlanMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        constraint_kind=constraint_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tacho_plan_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="tpm_window_02",
        constraint_kind="window",
        source_ref="fixture://tacho-plan-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(TachoPlanMark))).all())
    assert {row.id for row in visible} == {row_a.id}
