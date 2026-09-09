from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.war_room_mark import WarRoomMark


class WarRoomMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def fetch_incidents(self) -> list[WarRoomMark]:
        stmt = select(WarRoomMark).order_by(WarRoomMark.incident_kind, WarRoomMark.id)
        executed = await self._db.execute(stmt)
        return list(executed.scalars())

    async def add(self, row: WarRoomMark) -> WarRoomMark:
        self._db.add(row)
        await self._db.flush()
        return row
