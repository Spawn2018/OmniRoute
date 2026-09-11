from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.make_or_buy_mark import MakeOrBuyMark


class MakeOrBuyMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[MakeOrBuyMark]:
        packed = await self._session.scalars(
            select(MakeOrBuyMark).order_by(
                MakeOrBuyMark.mark_code,
                MakeOrBuyMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: MakeOrBuyMark) -> MakeOrBuyMark:
        self._session.add(row)
        await self._session.flush()
        return row
