from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_transforms.extraction.input_guard import ExtractionInputGuard
from app.ai_transforms.extraction.protocol import DocumentExtractor
from app.ai_transforms.extraction.provider import default_extractor
from app.domain.errors import DraftNotPending, ResourceNotFound, UnparseableDocument
from app.integrations.docling.parser import DocumentParser
from app.integrations.docling.provider import default_parser
from app.models.extraction_draft import ExtractionDraft
from app.repositories.extraction.extraction_draft_repository import ExtractionDraftRepository

_MAX_DOCUMENT_BYTES = 2_000_000


class ExtractionService:
    """HITL: ekstrakcja → draft; accept nie tworzy rate_line (HC-04)."""

    def __init__(
        self,
        session: AsyncSession,
        extractor: DocumentExtractor | None = None,
        guard: ExtractionInputGuard | None = None,
        parser: DocumentParser | None = None,
    ) -> None:
        self._drafts = ExtractionDraftRepository(session)
        self._session = session
        self._extractor = extractor or default_extractor()
        self._guard = guard or ExtractionInputGuard()
        self._parser = parser or default_parser()

    async def list_drafts(self, status: str | None = "pending") -> list[ExtractionDraft]:
        return await self._drafts.list_by_status(status)

    async def extract_to_draft(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        input_text: str,
        parser_name: str = "plain",
        parser_challenger: str | None = None,
        ab_delta_chars: int | None = None,
    ) -> ExtractionDraft:
        self._guard.scan(input_text)
        payload = self._extractor.extract(source_ref=source_ref, input_text=input_text)
        payload = payload.model_copy(
            update={
                "parser_name": parser_name,
                "parser_challenger": parser_challenger,
                "ab_delta_chars": ab_delta_chars,
            },
        )
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

    async def extract_from_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        raw_bytes: bytes,
    ) -> ExtractionDraft:
        if len(raw_bytes) > _MAX_DOCUMENT_BYTES:
            raise UnparseableDocument("Dokument przekracza 2 MB")
        parsed = self._parser.parse(source_ref=source_ref, raw_bytes=raw_bytes)
        return await self.extract_to_draft(
            organization_id=organization_id,
            user_id=user_id,
            source_ref=source_ref,
            input_text=parsed.text,
            parser_name=parsed.parser_name,
            parser_challenger=parsed.parser_challenger,
            ab_delta_chars=parsed.ab_delta_chars,
        )

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
