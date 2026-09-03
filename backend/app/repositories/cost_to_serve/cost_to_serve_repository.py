from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cost_to_serve import CostToServe


class CostToServeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CostToServe]:
        result = await self._session.scalars(
            select(CostToServe).order_by(CostToServe.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: CostToServe) -> CostToServe:
        self._session.add(row)
        await self._session.flush()
        return row
