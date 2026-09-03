from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fx_difference import FxDifference


class FxDifferenceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[FxDifference]:
        result = await self._session.scalars(
            select(FxDifference).order_by(FxDifference.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: FxDifference) -> FxDifference:
        self._session.add(row)
        await self._session.flush()
        return row
