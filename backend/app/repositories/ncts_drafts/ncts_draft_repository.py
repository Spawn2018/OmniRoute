from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ncts_draft import NctsDraft


class NctsDraftRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_drafts(self) -> list[NctsDraft]:
        packed = await self._session.scalars(
            select(NctsDraft).order_by(NctsDraft.draft_code, NctsDraft.id),
        )
        return list(packed.all())

    async def add_draft(self, row: NctsDraft) -> NctsDraft:
        self._session.add(row)
        await self._session.flush()
        return row
