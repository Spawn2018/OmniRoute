from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_transforms.extraction.protocol import DocumentExtractor
from app.ai_transforms.extraction.provider import default_extractor
from app.domain.errors import DraftNotPending, ResourceNotFound
from app.models.extraction_draft import ExtractionDraft
from app.repositories.extraction.extraction_draft_repository import ExtractionDraftRepository


class ExtractionService:
    """HITL: ekstrakcja → draft; accept nie tworzy rate_line (HC-04)."""

    def __init__(
        self,
        session: AsyncSession,
        extractor: DocumentExtractor | None = None,
    ) -> None:
        self._drafts = ExtractionDraftRepository(session)
        self._session = session
        self._extractor = extractor or default_extractor()

    async def list_drafts(self, status: str | None = "pending") -> list[ExtractionDraft]:
        return await self._drafts.list_by_status(status)

    async def extract_to_draft(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        input_text: str,
    ) -> ExtractionDraft:
        payload = self._extractor.extract(source_ref=source_ref, input_text=input_text)
        draft = ExtractionDraft(
            id=uuid4(),
            organization_id=organization_id,
            status="pending",
            source_ref=payload.source_ref,
            input_text=input_text,
            payload=payload.model_dump(),
            created_by=user_id,
        )
        return await self._drafts.add(draft)

    async def accept(self, *, draft_id: UUID, user_id: UUID) -> ExtractionDraft:
        draft = await self._require_pending(draft_id)
        draft.status = "accepted"
        draft.reviewed_by = user_id
        draft.reviewed_at = datetime.now(UTC)
        await self._session.flush()
        return draft

    async def reject(self, *, draft_id: UUID, user_id: UUID) -> ExtractionDraft:
        draft = await self._require_pending(draft_id)
        draft.status = "rejected"
        draft.reviewed_by = user_id
        draft.reviewed_at = datetime.now(UTC)
        await self._session.flush()
        return draft

    async def _require_pending(self, draft_id: UUID) -> ExtractionDraft:
        draft = await self._drafts.get_by_id(draft_id)
        if draft is None:
            raise ResourceNotFound("Szkic ekstrakcji nie istnieje")
        if draft.status != "pending":
            raise DraftNotPending("Szkic nie jest w statusie pending")
        return draft
