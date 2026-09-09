from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tower_impact import TowerImpact


class TowerImpactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_marks(self) -> list[TowerImpact]:
        stmt = select(TowerImpact).order_by(TowerImpact.id.desc())
        executed = await self._session.execute(stmt)
        return list(executed.scalars())

    async def add(self, row: TowerImpact) -> TowerImpact:
        self._session.add(row)
        await self._session.flush()
        return row
