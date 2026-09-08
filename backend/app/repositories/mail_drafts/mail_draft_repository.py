from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mail_draft import MailDraft


class MailDraftRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[MailDraft]:
        result = await self._session.scalars(
            select(MailDraft).order_by(MailDraft.created_at.desc()),
        )
        return list(result.all())

    async def get(self, draft_id: UUID) -> MailDraft | None:
        found = await self._session.get(MailDraft, draft_id)
        return found if isinstance(found, MailDraft) else None

    async def add(self, row: MailDraft) -> MailDraft:
        self._session.add(row)
        await self._session.flush()
        return row

    async def add_many(self, rows: list[MailDraft]) -> list[MailDraft]:
        for row in rows:
            self._session.add(row)
        await self._session.flush()
        return rows
