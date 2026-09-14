from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ops_room_mark import OpsRoomMark


class OpsRoomMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[OpsRoomMark]:
        stmt = select(OpsRoomMark).order_by(
            OpsRoomMark.mark_code,
            OpsRoomMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: OpsRoomMark) -> OpsRoomMark:
        self._session.add(row)
        await self._session.flush()
        return row
