from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain.errors import InvalidPlanSnapshot
from app.services.plan_snapshots.plan_snapshot_service import PlanSnapshotService

_HITL = "2026-09-10T12:00:00+02:00"


async def _persist(desk: PlanSnapshotService) -> None:
    await desk.persist_snapshot(
        organization_id=uuid4(),
        user_id=uuid4(),
        snapshot_code="plan_v1",
        shipment_id=str(uuid4()),
        trip_id=str(uuid4()),
        resource_id=str(uuid4()),
        author_label="Anna",
        recorded_at=_HITL,
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_persist_maps_fk_integrity() -> None:
    desk = PlanSnapshotService(AsyncMock())
    orig = Exception(
        'violates foreign key constraint "fk_plan_snapshot_shipment"'
    )
    desk._rows.add = AsyncMock(side_effect=IntegrityError("INSERT", {}, orig))
    with pytest.raises(InvalidPlanSnapshot, match="trójka"):
        await _persist(desk)


@pytest.mark.asyncio
async def test_persist_reraises_other_integrity() -> None:
    desk = PlanSnapshotService(AsyncMock())
    orig = Exception('duplicate key value violates unique constraint "uq_plan_snapshot_org_code"')
    desk._rows.add = AsyncMock(side_effect=IntegrityError("INSERT", {}, orig))
    with pytest.raises(IntegrityError):
        await _persist(desk)
