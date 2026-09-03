from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.money_cost import MoneyCost


class MoneyCostRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[MoneyCost]:
        result = await self._session.scalars(
            select(MoneyCost).order_by(MoneyCost.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: MoneyCost) -> MoneyCost:
        self._session.add(row)
        await self._session.flush()
        return row
