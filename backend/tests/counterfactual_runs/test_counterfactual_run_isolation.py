from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.counterfactual_run import CounterfactualRun
from app.models.plan_snapshot import PlanSnapshot
from app.models.what_if_replay import WhatIfReplay
from tests.plan_snapshots.test_plan_snapshot_isolation import _triple


async def _snapshot(session, *, organization_id, created_by, suffix: str):
    ship, trip, res = await _triple(
        session, organization_id=organization_id, created_by=created_by, suffix=suffix
    )
    row = PlanSnapshot(
        id=uuid4(),
        organization_id=organization_id,
        snapshot_code=f"plan_{suffix}"[:32],
        shipment_id=ship,
        trip_id=trip,
        resource_id=res,
        author_label="Anna",
        recorded_at=datetime(2026, 9, 10, 12, 0, tzinfo=UTC),
        source_ref=f"fixture://plan-snapshot/{suffix}",
        created_by=created_by,
    )
    session.add(row)
    await session.flush()
    return row.id


def _row(
    *,
    organization_id,
    created_by,
    plan_snapshot_id,
    source_ref: str = "fixture://counterfactual-run/",
    run_code: str = "fuel_spike",
) -> CounterfactualRun:
    return CounterfactualRun(
        id=uuid4(),
        organization_id=organization_id,
        run_code=run_code,
        plan_snapshot_id=plan_snapshot_id,
        baseline_label="plan z wczoraj",
        levers_label="paliwo w gore",
        result_label="eta plus dwie godziny",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_counterfactual_run_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    snap_a = await _snapshot(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="cfa"
    )
    row_a = _row(
        organization_id=org_a.id, created_by=user_a.id, plan_snapshot_id=snap_a
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    snap_b = await _snapshot(
        session, organization_id=org_b.id, created_by=user_b.id, suffix="cfb"
    )
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        plan_snapshot_id=snap_b,
        run_code="port_close",
        source_ref="fixture://counterfactual-run/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(CounterfactualRun))).all())
    assert {row.id for row in visible} == {row_a.id}
    replays = list((await session.scalars(select(WhatIfReplay))).all())
    assert {row.run_id for row in replays} == {row_a.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_counterfactual_run_rejects_foreign_snapshot(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    await bind_tenant(session, org_b.id)
    snap_b = await _snapshot(
        session, organization_id=org_b.id, created_by=user_b.id, suffix="steal"
    )
    await bind_tenant(session, org_a.id)
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            plan_snapshot_id=snap_b,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_counterfactual_run_restricts_snapshot_delete(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    snap_id = await _snapshot(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="hold"
    )
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            plan_snapshot_id=snap_id,
        )
    )
    await session.flush()
    snapshot = await session.get(PlanSnapshot, snap_id)
    assert snapshot is not None
    await session.delete(snapshot)
    with pytest.raises(IntegrityError):
        await session.flush()
