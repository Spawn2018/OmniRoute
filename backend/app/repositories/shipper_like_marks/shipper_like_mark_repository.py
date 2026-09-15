from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipper_like_mark import ShipperLikeMark


class ShipperLikeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ShipperLikeMark]:
        packed = await self._session.scalars(
            select(ShipperLikeMark).order_by(
                ShipperLikeMark.mark_code,
                ShipperLikeMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: ShipperLikeMark) -> ShipperLikeMark:
        self._session.add(row)
        await self._session.flush()
        return row
