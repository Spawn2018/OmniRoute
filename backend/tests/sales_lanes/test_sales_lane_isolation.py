from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.sales_lane import SalesLane


def _row(
    *,
    organization_id,
    created_by,
    lane_code: str = "sln_repeat_01",
    lane_kind: str = "repeat",
    origin_unlocode: str = "PLGDN",
    destination_unlocode: str = "DEHAM",
    source_ref: str = "tenant:manual",
) -> SalesLane:
    return SalesLane(
        id=uuid4(),
        organization_id=organization_id,
        lane_code=lane_code,
        lane_kind=lane_kind,
        origin_unlocode=origin_unlocode,
        destination_unlocode=destination_unlocode,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sales_lane_rls_isolates_tenants(session, two_tenants) -> None:
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
        lane_code="sln_spot_02",
        lane_kind="spot",
        origin_unlocode="PLWAW",
        destination_unlocode="NLRTM",
        source_ref="fixture://sales-lane/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(SalesLane))).all())
    assert {row.id for row in visible} == {row_a.id}
