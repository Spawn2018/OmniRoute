from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.groupage_line import GroupageLine


class GroupageLineRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current(self) -> list[GroupageLine]:
        result = await self._session.scalars(
            select(GroupageLine)
            .where(GroupageLine.superseded_by.is_(None))
            .order_by(GroupageLine.line_code, GroupageLine.id),
        )
        return list(result.all())

    async def find_current_by_code(self, line_code: str) -> GroupageLine | None:
        result = await self._session.scalars(
            select(GroupageLine).where(
                GroupageLine.line_code == line_code,
                GroupageLine.superseded_by.is_(None),
            ),
        )
        found = list(result.all())
        return found[0] if found else None

    async def add_line(self, row: GroupageLine) -> GroupageLine:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(self, current: GroupageLine, successor_id: UUID) -> GroupageLine:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
