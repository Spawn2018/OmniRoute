from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidPlanSnapshot
from app.domain.plan_snapshot import (
    require_author_label,
    require_recorded_at,
    require_resource_id,
    require_shipment_id,
    require_snapshot_code,
    require_snapshot_source_ref,
    require_trip_id,
)
from app.models.plan_snapshot import PlanSnapshot
from app.repositories.plan_snapshots.plan_snapshot_repository import PlanSnapshotRepository


class PlanSnapshotService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PlanSnapshotRepository(session)

    async def list_rows(self) -> list[PlanSnapshot]:
        return await self._rows.fetch_rows()

    async def persist_snapshot(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        snapshot_code: object,
        shipment_id: object,
        trip_id: object,
        resource_id: object,
        author_label: object,
        recorded_at: object,
        source_ref: object,
    ) -> PlanSnapshot:
        row = PlanSnapshot(
            id=uuid4(),
            organization_id=organization_id,
            snapshot_code=require_snapshot_code(snapshot_code),
            shipment_id=require_shipment_id(shipment_id),
            trip_id=require_trip_id(trip_id),
            resource_id=require_resource_id(resource_id),
            author_label=require_author_label(author_label),
            recorded_at=require_recorded_at(recorded_at),
            source_ref=require_snapshot_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as exc:
            detail = str(getattr(exc, "orig", exc))
            if "fk_plan_snapshot_" in detail:
                raise InvalidPlanSnapshot("trójka musi istnieć w tym tenancie") from exc
            raise
