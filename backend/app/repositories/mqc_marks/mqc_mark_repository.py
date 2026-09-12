from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mqc_mark import MqcMark


class MqcMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[MqcMark]:
        packed = await self._session.scalars(
            select(MqcMark).order_by(
                MqcMark.mark_code,
                MqcMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: MqcMark) -> MqcMark:
        self._session.add(row)
        await self._session.flush()
        return row
