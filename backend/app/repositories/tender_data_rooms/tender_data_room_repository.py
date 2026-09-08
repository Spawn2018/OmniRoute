from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_data_room import TenderDataRoom


class TenderDataRoomRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[TenderDataRoom]:
        result = await self._session.scalars(
            select(TenderDataRoom).order_by(TenderDataRoom.created_at.desc(), TenderDataRoom.id),
        )
        return list(result.all())

    async def add(self, row: TenderDataRoom) -> TenderDataRoom:
        self._session.add(row)
        await self._session.flush()
        return row
