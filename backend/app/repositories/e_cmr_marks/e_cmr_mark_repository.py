from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.e_cmr_mark import ECmrMark


class ECmrMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ECmrMark]:
        packed = await self._session.scalars(
            select(ECmrMark).order_by(
                ECmrMark.mark_code,
                ECmrMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: ECmrMark) -> ECmrMark:
        self._session.add(row)
        await self._session.flush()
        return row
