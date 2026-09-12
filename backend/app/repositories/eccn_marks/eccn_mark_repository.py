from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.eccn_mark import EccnMark


class EccnMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[EccnMark]:
        packed = await self._session.scalars(
            select(EccnMark).order_by(
                EccnMark.mark_code,
                EccnMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: EccnMark) -> EccnMark:
        self._session.add(row)
        await self._session.flush()
        return row
