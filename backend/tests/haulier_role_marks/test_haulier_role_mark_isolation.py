from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.haulier_role_mark import HaulierRoleMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "hrm_booked_main",
    role_kind: str = "booked",
    source_ref: str = "fixture://haulier-role-mark/",
) -> HaulierRoleMark:
    return HaulierRoleMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        role_kind=role_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_haulier_role_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="hrm_actual_sub",
        role_kind="actual",
        source_ref="fixture://haulier-role-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(HaulierRoleMark))).all())
    assert {row.id for row in visible} == {row_a.id}
