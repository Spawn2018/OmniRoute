from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.iso_nis2_mark import IsoNis2Mark


class IsoNis2MarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[IsoNis2Mark]:
        packed = await self._session.scalars(
            select(IsoNis2Mark).order_by(
                IsoNis2Mark.mark_code,
                IsoNis2Mark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: IsoNis2Mark) -> IsoNis2Mark:
        self._session.add(row)
        await self._session.flush()
        return row
