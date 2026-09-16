from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip_bill_mark import TripBillMark


class TripBillMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[TripBillMark]:
        stmt = select(TripBillMark).order_by(
            TripBillMark.mark_code,
            TripBillMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: TripBillMark) -> TripBillMark:
        self._session.add(row)
        await self._session.flush()
        return row
