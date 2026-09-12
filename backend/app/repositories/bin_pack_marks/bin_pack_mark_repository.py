from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bin_pack_mark import BinPackMark


class BinPackMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[BinPackMark]:
        packed = await self._session.scalars(
            select(BinPackMark).order_by(
                BinPackMark.mark_code,
                BinPackMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: BinPackMark) -> BinPackMark:
        self._session.add(row)
        await self._session.flush()
        return row
