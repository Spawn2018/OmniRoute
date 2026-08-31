from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.extraction_draft import ExtractionDraft


class ExtractionDraftRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_status(self, status: str | None) -> list[ExtractionDraft]:
        stmt = select(ExtractionDraft).order_by(ExtractionDraft.created_at.desc())
        if status is not None:
            stmt = stmt.where(ExtractionDraft.status == status)
        return list((await self._session.scalars(stmt)).all())

    async def get_by_id(self, draft_id: UUID) -> ExtractionDraft | None:
        return await self._session.get(ExtractionDraft, draft_id)

    async def add(self, draft: ExtractionDraft) -> ExtractionDraft:
        self._session.add(draft)
        await self._session.flush()
        return draft
