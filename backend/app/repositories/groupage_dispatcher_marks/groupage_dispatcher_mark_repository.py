from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.groupage_dispatcher_mark import GroupageDispatcherMark


class GroupageDispatcherMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[GroupageDispatcherMark]:
        packed = await self._session.scalars(
            select(GroupageDispatcherMark).order_by(
                GroupageDispatcherMark.mark_code,
                GroupageDispatcherMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: GroupageDispatcherMark) -> GroupageDispatcherMark:
        self._session.add(row)
        await self._session.flush()
        return row
