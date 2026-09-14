from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rfid_mark import RfidMark


class RfidMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RfidMark]:
        stmt = select(RfidMark).order_by(RfidMark.mark_code, RfidMark.id)
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: RfidMark) -> RfidMark:
        self._session.add(row)
        await self._session.flush()
        return row
