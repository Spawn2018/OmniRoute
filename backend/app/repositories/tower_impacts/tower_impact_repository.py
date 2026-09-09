from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tower_impact import TowerImpact


class TowerImpactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_marks(self) -> list[TowerImpact]:
        packed = await self._session.scalars(
            select(TowerImpact).order_by(
                TowerImpact.created_at.desc(),
                TowerImpact.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: TowerImpact) -> TowerImpact:
        self._session.add(row)
        await self._session.flush()
        return row
