from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ferry_booking_mark import FerryBookingMark


class FerryBookingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FerryBookingMark]:
        packed = await self._session.scalars(
            select(FerryBookingMark).order_by(
                FerryBookingMark.mark_code,
                FerryBookingMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FerryBookingMark) -> FerryBookingMark:
        self._session.add(row)
        await self._session.flush()
        return row
