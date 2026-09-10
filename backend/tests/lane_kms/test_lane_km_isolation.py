from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.lane_km import LaneKm


def _row(
    *,
    organization_id,
    created_by,
    km_code: str = "backhaul_a",
    loaded_km: Decimal = Decimal("120.0000"),
    empty_km: Decimal = Decimal("40.0000"),
    approach_km: Decimal = Decimal("15.0000"),
    source_ref: str = "tenant:manual",
) -> LaneKm:
    return LaneKm(
        id=uuid4(),
        organization_id=organization_id,
        km_code=km_code,
        loaded_km=loaded_km,
        empty_km=empty_km,
        approach_km=approach_km,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lane_km_rls_isolates_tenants(session, two_tenants) -> None:
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
        km_code="backhaul_b",
        source_ref="fixture://lane-km/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(LaneKm))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(LaneKm).where(LaneKm.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(LaneKm))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lane_km_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            km_code="backhaul_z",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lane_km_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            source_ref="fixture://lane-km/dup-code",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lane_km_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM lane_km WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_lane_km_organization_id" in joined
        or "uq_lane_km_org_id" in joined
        or "uq_lane_km_org_source_ref" in joined
        or "uq_lane_km_org_code" in joined
        or "Index Scan" in joined
    )
