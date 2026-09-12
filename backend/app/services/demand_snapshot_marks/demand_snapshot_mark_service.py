from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.demand_snapshot_mark import parse_demand_snapshot_mark_row
from app.models.demand_snapshot_mark import DemandSnapshotMark
from app.repositories.demand_snapshot_marks.demand_snapshot_mark_repository import (
    DemandSnapshotMarkRepository,
)


class DemandSnapshotMarkService:
    """HITL zapis powodu decline — bez auto-award i bez auto-forecast."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = DemandSnapshotMarkRepository(session)

    async def list_marks(self) -> list[DemandSnapshotMark]:
        return await self._repo.list_marks()

    async def persist_demand_snapshot_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        snapshot_kind: object,
        source_ref: object,
    ) -> DemandSnapshotMark:
        code, kind, pointer = parse_demand_snapshot_mark_row(
            mark_code,
            snapshot_kind,
            source_ref,
        )
        entity = DemandSnapshotMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            snapshot_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._repo.add_mark(entity)
