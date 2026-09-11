from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collaboration_mark import CollaborationMark


class CollaborationMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CollaborationMark]:
        packed = await self._session.scalars(
            select(CollaborationMark).order_by(
                CollaborationMark.mark_code, CollaborationMark.id
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CollaborationMark) -> CollaborationMark:
        self._session.add(row)
        await self._session.flush()
        return row
