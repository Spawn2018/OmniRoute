from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pallet_pool_mark import PalletPoolMark


class PalletPoolMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PalletPoolMark]:
        packed = await self._session.scalars(
            select(PalletPoolMark).order_by(
                PalletPoolMark.mark_code,
                PalletPoolMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: PalletPoolMark) -> PalletPoolMark:
        self._session.add(row)
        await self._session.flush()
        return row
