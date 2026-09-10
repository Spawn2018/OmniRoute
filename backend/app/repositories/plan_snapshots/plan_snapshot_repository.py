from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan_snapshot import PlanSnapshot


class PlanSnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[PlanSnapshot]:
        packed = await self._session.scalars(
            select(PlanSnapshot).order_by(
                PlanSnapshot.recorded_at.desc(),
                PlanSnapshot.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: PlanSnapshot) -> PlanSnapshot:
        self._session.add(row)
        await self._session.flush()
        return row
