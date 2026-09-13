from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from app.ai_transforms.extraction.input_guard import ExtractionInputGuard
from app.ai_transforms.extraction.protocol import DocumentExtractor
from app.ai_transforms.extraction.provider import default_extractor
from app.domain.errors import DraftNotPending, ResourceNotFound, UnparseableDocument
from app.domain.extraction_draft import (
    extraction_carrier_quote_kind,
    extraction_tender_rfp_kind,
    require_carrier_quote_payload,
    require_extraction_draft_kind,
    require_rate_candidates_editable,
    require_tender_rfp_payload,
)
from app.integrations.docling.parser import DocumentParser
from app.integrations.docling.provider import default_parser
from app.integrations.langfuse.tracer import LangfuseTracer, build_langfuse_tracer
from app.models.extraction_draft import ExtractionDraft
from app.repositories.extraction.extraction_draft_repository import ExtractionDraftRepository

_MAX_DOCUMENT_BYTES = 2_000_000


class ExtractionService:
    """HITL: ekstrakcja → draft; accept tylko status — rate_line pisze warstwa API (1.3)."""

    def __init__(
        self,
        session: AsyncSession,
        extractor: DocumentExtractor | None = None,
        guard: ExtractionInputGuard | None = None,
        parser: DocumentParser | None = None,
        tracer: LangfuseTracer | None = None,
    ) -> None:
        self._drafts = ExtractionDraftRepository(session)
        self._session = session
        self._extractor = extractor or default_extractor()
        self._guard = guard or ExtractionInputGuard()
        self._parser = parser or default_parser()
        self._tracer = tracer or build_langfuse_tracer()

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
        draft_kind: object = None,
        quote_payload: object = None,
        rfp_payload: object = None,
    ) -> ExtractionDraft:
        kind = require_extraction_draft_kind(draft_kind)
        self._guard.scan(input_text)
        if kind == extraction_carrier_quote_kind():
            dumped = _quote_payload(source_ref, quote_payload)
        elif kind == extraction_tender_rfp_kind():
            dumped = _rfp_payload(source_ref, rfp_payload)
        else:
            dumped = self._rate_payload(
                source_ref,
                input_text,
                parser_name,
                parser_challenger,
                ab_delta_chars,
            )
        stored_ref = dumped.get("source_ref")
        draft = ExtractionDraft(
            id=uuid4(),
            organization_id=organization_id,
            status="pending",
            draft_kind=kind,
            source_ref=stored_ref if type(stored_ref) is str else source_ref,
            input_text=input_text,
            payload=dumped,
            created_by=user_id,
        )
        return await self._drafts.add(draft)

    def _rate_payload(
        self,
        source_ref: str,
        input_text: str,
        parser_name: str,
        parser_challenger: str | None,
        ab_delta_chars: int | None,
    ) -> dict[str, object]:
        trace = self._tracer.start_trace("extract")
        payload = self._extractor.extract(source_ref=source_ref, input_text=input_text)
        payload = payload.model_copy(
            update={
                "parser_name": parser_name,
                "parser_challenger": parser_challenger,
                "ab_delta_chars": ab_delta_chars,
            },
        )
        trace.update(
            source_ref=payload.source_ref,
            parser_name=parser_name,
            candidate_count=len(payload.candidates),
            unparsed_count=len(payload.unparsed_regions),
        )
        self._tracer.finish(trace)
        return payload.model_dump()

    async def extract_from_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        raw_bytes: bytes,
        draft_kind: object = None,
        quote_payload: object = None,
        rfp_payload: object = None,
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
            draft_kind=draft_kind,
            quote_payload=quote_payload,
            rfp_payload=rfp_payload,
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

    async def patch_candidates(
        self,
        *,
        draft_id: UUID,
        candidates: list[dict[str, object]],
    ) -> ExtractionDraft:
        draft = await self._require_pending(draft_id)
        require_rate_candidates_editable(draft.draft_kind)
        payload = dict(draft.payload)
        payload["candidates"] = candidates
        draft.payload = payload
        flag_modified(draft, "payload")
        await self._session.flush()
        return draft

    async def _require_pending(self, draft_id: UUID) -> ExtractionDraft:
        draft = await self._drafts.get_by_id(draft_id)
        if draft is None:
            raise ResourceNotFound("Szkic ekstrakcji nie istnieje")
        if draft.status != "pending":
            raise DraftNotPending("Szkic nie jest w statusie pending")
        return draft


def _quote_payload(source_ref: str, raw: object) -> dict[str, object]:
    stored = require_carrier_quote_payload(raw)
    return {
        "source_ref": source_ref,
        "unparsed_regions": [],
        "candidates": [],
        "party_id": str(stored.party_id),
        "origin_port_id": str(stored.origin_port_id),
        "destination_port_id": str(stored.destination_port_id),
        "quote_date": stored.quote_date,
        "amount": stored.amount,
        "currency": stored.currency,
        "transit_days": stored.transit_days,
    }


def _rfp_payload(source_ref: str, raw: object) -> dict[str, object]:
    stored = require_tender_rfp_payload(raw)
    return {
        "source_ref": source_ref,
        "unparsed_regions": [],
        "candidates": [],
        "tender_id": str(stored.tender_id),
        "intake_code": stored.intake_code,
    }
