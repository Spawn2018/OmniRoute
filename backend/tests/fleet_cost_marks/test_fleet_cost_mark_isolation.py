from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.fleet_cost_mark import FleetCostMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "tco_01",
    cost_kind: str = "tco",
    source_ref: str = "tenant:manual",
) -> FleetCostMark:
    return FleetCostMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        cost_kind=cost_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fleet_cost_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        cost_kind="lease",
        source_ref="fixture://fleet-cost-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(FleetCostMark))).all())
    assert {row.id for row in visible} == {row_a.id}
