from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.general_average_mark import GeneralAverageMark


class GeneralAverageMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[GeneralAverageMark]:
        packed = await self._session.scalars(
            select(GeneralAverageMark).order_by(
                GeneralAverageMark.mark_code,
                GeneralAverageMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: GeneralAverageMark) -> GeneralAverageMark:
        self._session.add(row)
        await self._session.flush()
        return row
