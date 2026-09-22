from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.clone_carry_mark import CloneCarryMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "carry_on_clone_01",
    carry_kind: str = "carry",
    source_ref: str = "tenant:manual",
) -> CloneCarryMark:
    return CloneCarryMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        carry_kind=carry_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_clone_carry_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="carry_skip_b",
        carry_kind="skip",
        source_ref="fixture://clone-carry/b",
    )
    session.add(row_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(CloneCarryMark))).all())
    assert {row.mark_code for row in visible} == {"carry_on_clone_01"}
