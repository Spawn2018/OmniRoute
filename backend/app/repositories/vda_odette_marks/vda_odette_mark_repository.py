from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vda_odette_mark import VdaOdetteMark


class VdaOdetteMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[VdaOdetteMark]:
        packed = await self._session.scalars(
            select(VdaOdetteMark).order_by(
                VdaOdetteMark.mark_code,
                VdaOdetteMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: VdaOdetteMark) -> VdaOdetteMark:
        self._session.add(row)
        await self._session.flush()
        return row
