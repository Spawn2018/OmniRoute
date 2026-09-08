from base64 import b64decode
from binascii import Error as BinasciiError
from datetime import datetime
from typing import Any, Self
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.accept_extraction import AcceptExtractionToRates
from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.errors import UnparseableDocument
from app.models.channel_quote import ChannelQuote
from app.models.rate_line import RateLine
from app.services.extraction.extraction_service import ExtractionService

router = APIRouter(prefix="/extractions", tags=["extractions"])

# 4/3 znaków + padding z limitu 2 MB surowych bajtów (ExtractionService) — 422 przed decode (T0).
DOCUMENT_BASE64_MAX_LENGTH = 2_666_668


class CarrierQuoteExtract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    origin_port_id: UUID
    destination_port_id: UUID
    quote_date: str
    amount: str
    currency: str
    transit_days: int | None = None


class ExtractRequest(BaseModel):
    source_ref: str = Field(min_length=1, max_length=512)
    input_text: str | None = Field(default=None, min_length=1, max_length=50_000)
    document_base64: str | None = Field(
        default=None, min_length=1, max_length=DOCUMENT_BASE64_MAX_LENGTH
    )
    draft_kind: str | None = None
    quote: CarrierQuoteExtract | None = None

    @model_validator(mode="after")
    def require_one_source(self) -> Self:
        has_text = self.input_text is not None
        has_doc = self.document_base64 is not None
        if has_text == has_doc:
            raise ValueError("Podaj dokładnie jedno: input_text albo document_base64")
        return self


class ExtractionDraftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    status: str
    draft_kind: str = "rate_line"
    source_ref: str
    input_text: str
    payload: dict[str, Any]
    reviewed_by: UUID | None
    reviewed_at: datetime | None
    rate_line_ids: list[UUID] = Field(default_factory=list)
    channel_quote_ids: list[UUID] = Field(default_factory=list)


@router.get("", response_model=list[ExtractionDraftResponse])
async def list_extraction_drafts(
    status_filter: str | None = Query(default="pending", alias="status"),
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ExtractionDraftResponse]:
    service = ExtractionService(session)
    drafts = await service.list_drafts(status_filter)
    return [_draft_response(draft) for draft in drafts]


@router.post("", response_model=ExtractionDraftResponse, status_code=status.HTTP_201_CREATED)
async def create_extraction_draft(
    body: ExtractRequest,
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ExtractionDraftResponse:
    service = ExtractionService(session)
    if body.document_base64 is not None:
        try:
            raw_bytes = b64decode(body.document_base64, validate=True)
        except BinasciiError as exc:
            raise UnparseableDocument("document_base64 niepoprawne") from exc
        draft = await service.extract_from_document(
            organization_id=identity.organization_id,
            user_id=identity.user_id,
            source_ref=body.source_ref,
            raw_bytes=raw_bytes,
            draft_kind=body.draft_kind,
            quote_payload=None if body.quote is None else body.quote.model_dump(),
        )
    else:
        if body.input_text is None:
            raise UnparseableDocument("Brak input_text")
        draft = await service.extract_to_draft(
            organization_id=identity.organization_id,
            user_id=identity.user_id,
            source_ref=body.source_ref,
            input_text=body.input_text,
            draft_kind=body.draft_kind,
            quote_payload=None if body.quote is None else body.quote.model_dump(),
        )
    await session.commit()
    return _draft_response(draft)


@router.post("/{draft_id}/accept", response_model=ExtractionDraftResponse)
async def accept_extraction_draft(
    draft_id: UUID,
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ExtractionDraftResponse:
    outcome = await AcceptExtractionToRates(session).accept(
        draft_id=draft_id,
        user_id=identity.user_id,
    )
    await session.commit()
    return _draft_response(outcome.draft, outcome.rate_lines, outcome.channel_quotes)


@router.post("/{draft_id}/reject", response_model=ExtractionDraftResponse)
async def reject_extraction_draft(
    draft_id: UUID,
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ExtractionDraftResponse:
    service = ExtractionService(session)
    draft = await service.reject(draft_id=draft_id, user_id=identity.user_id)
    await session.commit()
    return _draft_response(draft)


def _draft_response(
    draft: object,
    rates: list[RateLine] | None = None,
    quotes: list[ChannelQuote] | None = None,
) -> ExtractionDraftResponse:
    body = ExtractionDraftResponse.model_validate(draft)
    updates: dict[str, list[UUID]] = {}
    if rates is not None:
        updates["rate_line_ids"] = [row.id for row in rates]
    if quotes is not None:
        updates["channel_quote_ids"] = [row.id for row in quotes]
    if updates == {}:
        return body
    return body.model_copy(update=updates)
