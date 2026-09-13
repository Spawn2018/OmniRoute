from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.nac_mark import NacMark


class NacMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[NacMark]:
        packed = await self._session.scalars(
            select(NacMark).order_by(
                NacMark.mark_code,
                NacMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: NacMark) -> NacMark:
        self._session.add(row)
        await self._session.flush()
        return row
