from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cash_flow import CashFlow


class CashFlowRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CashFlow]:
        result = await self._session.scalars(
            select(CashFlow).order_by(CashFlow.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: CashFlow) -> CashFlow:
        self._session.add(row)
        await self._session.flush()
        return row
