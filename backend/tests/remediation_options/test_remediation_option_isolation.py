from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.remediation_option import RemediationOption


def _row(
    *,
    organization_id,
    created_by,
    option_code: str = "rebook_lane_01",
    source_ref: str = "tenant:manual",
) -> RemediationOption:
    return RemediationOption(
        id=uuid4(),
        organization_id=organization_id,
        option_code=option_code,
        option_kind="rebook",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_remediation_option_rls_isolates_tenants(session, two_tenants) -> None:
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
        option_code="wait_dock_02",
        source_ref="fixture://remediation-option/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(RemediationOption))).all())
    assert {row.id for row in visible} == {row_a.id}
