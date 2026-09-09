from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.lane_pattern import LanePattern


def _pattern(
    *,
    organization_id,
    created_by,
    origin: str = "PLGDY",
    dest: str = "DEHAM",
) -> LanePattern:
    return LanePattern(
        id=uuid4(),
        organization_id=organization_id,
        origin_unlocode=origin,
        destination_unlocode=dest,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lane_pattern_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _pattern(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _pattern(
        organization_id=org_b.id,
        created_by=user_b.id,
        origin="NLRTM",
        dest="GBFXT",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(LanePattern))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert (
        await session.scalar(select(LanePattern).where(LanePattern.id == row_b.id))
        is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(LanePattern))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lane_pattern_rejects_duplicate_pair(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_pattern(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_pattern(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lane_pattern_list_uses_org_origin_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM lane_pattern "
            "WHERE organization_id = :org_id AND origin_unlocode = :origin"
        ),
        {"org_id": org_a.id, "origin": "PLGDY"},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_lane_pattern_org_origin" in joined
        or "uq_lane_pattern_org_pair" in joined
    )
