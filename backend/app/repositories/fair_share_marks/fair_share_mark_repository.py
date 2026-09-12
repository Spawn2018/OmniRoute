from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fair_share_mark import FairShareMark


class FairShareMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FairShareMark]:
        packed = await self._session.scalars(
            select(FairShareMark).order_by(
                FairShareMark.mark_code,
                FairShareMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FairShareMark) -> FairShareMark:
        self._session.add(row)
        await self._session.flush()
        return row
