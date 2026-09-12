from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.demand_snapshot_mark import DemandSnapshotMark


def _ordered_catalog() -> Select[tuple[DemandSnapshotMark]]:
    return select(DemandSnapshotMark).order_by(
        DemandSnapshotMark.created_at.desc(),
        DemandSnapshotMark.mark_code.asc(),
    )


class DemandSnapshotMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def list_marks(self) -> list[DemandSnapshotMark]:
        result = await self._db.scalars(_ordered_catalog())
        rows: Sequence[DemandSnapshotMark] = result.all()
        return list(rows)

    async def add_mark(self, entity: DemandSnapshotMark) -> DemandSnapshotMark:
        self._db.add(entity)
        await self._db.flush()
        return entity
