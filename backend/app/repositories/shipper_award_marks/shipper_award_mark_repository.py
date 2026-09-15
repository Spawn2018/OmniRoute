from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipper_award_mark import ShipperAwardMark


class ShipperAwardMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._sess = session

    async def list_marks(self) -> list[ShipperAwardMark]:
        query = select(ShipperAwardMark).order_by(
            ShipperAwardMark.award_kind,
            ShipperAwardMark.id,
            ShipperAwardMark.mark_code,
        )
        return list((await self._sess.scalars(query)).all())

    async def add_mark(self, row: ShipperAwardMark) -> ShipperAwardMark:
        self._sess.add(row)
        await self._sess.flush()
        return row
