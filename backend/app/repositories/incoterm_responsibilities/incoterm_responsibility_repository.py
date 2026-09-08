from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incoterm_responsibility import IncotermResponsibility


class IncotermResponsibilityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current_for_pair(
        self,
        incoterm: str,
        trade_side: str,
    ) -> list[IncotermResponsibility]:
        result = await self._session.scalars(
            select(IncotermResponsibility)
            .where(
                IncotermResponsibility.incoterm == incoterm,
                IncotermResponsibility.trade_side == trade_side,
                IncotermResponsibility.superseded_by.is_(None),
            )
            .order_by(IncotermResponsibility.created_at.desc(), IncotermResponsibility.id),
        )
        return list(result.all())

    async def list_current(self) -> list[IncotermResponsibility]:
        result = await self._session.scalars(
            select(IncotermResponsibility)
            .where(IncotermResponsibility.superseded_by.is_(None))
            .order_by(
                IncotermResponsibility.incoterm,
                IncotermResponsibility.trade_side,
                IncotermResponsibility.id,
            ),
        )
        return list(result.all())

    async def find_current(
        self,
        incoterm: str,
        trade_side: str,
    ) -> IncotermResponsibility | None:
        found = (await self.list_current_for_pair(incoterm, trade_side))
        return found[0] if found else None

    async def add(self, row: IncotermResponsibility) -> IncotermResponsibility:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(
        self,
        current: IncotermResponsibility,
        successor_id: UUID,
    ) -> IncotermResponsibility:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
