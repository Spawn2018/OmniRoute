from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.abandoned_rto_mark import AbandonedRtoMark


class AbandonedRtoMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[AbandonedRtoMark]:
        packed = await self._session.scalars(
            select(AbandonedRtoMark).order_by(
                AbandonedRtoMark.mark_code,
                AbandonedRtoMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: AbandonedRtoMark) -> AbandonedRtoMark:
        self._session.add(row)
        await self._session.flush()
        return row
