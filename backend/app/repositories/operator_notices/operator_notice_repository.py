from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operator_notice import OperatorNotice


class OperatorNoticeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[OperatorNotice]:
        result = await self._session.scalars(
            select(OperatorNotice).order_by(OperatorNotice.created_at.desc()),
        )
        return list(result.all())

    async def get(self, notice_id: UUID) -> OperatorNotice | None:
        found = await self._session.get(OperatorNotice, notice_id)
        return found if isinstance(found, OperatorNotice) else None

    async def add(self, row: OperatorNotice) -> OperatorNotice:
        self._session.add(row)
        await self._session.flush()
        return row

    async def save(self, row: OperatorNotice) -> OperatorNotice:
        await self._session.flush()
        return row
