from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission, require_tenant_session
from app.services.extraction.extraction_service import ExtractionService

router = APIRouter(prefix="/extractions", tags=["extractions"])


class ExtractRequest(BaseModel):
    source_ref: str = Field(min_length=1, max_length=512)
    input_text: str = Field(min_length=1, max_length=50_000)


class ExtractionDraftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    status: str
    source_ref: str
    input_text: str
    payload: dict[str, Any]
    reviewed_by: UUID | None
    reviewed_at: datetime | None


@router.get("", response_model=list[ExtractionDraftResponse])
async def list_extraction_drafts(
    status_filter: str | None = Query(default="pending", alias="status"),
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ExtractionDraftResponse]:
    service = ExtractionService(session)
    drafts = await service.list_drafts(status_filter)
    return [ExtractionDraftResponse.model_validate(draft) for draft in drafts]


@router.post("", response_model=ExtractionDraftResponse, status_code=status.HTTP_201_CREATED)
async def create_extraction_draft(
    body: ExtractRequest,
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    x_organization_id: UUID = Header(..., alias="X-Organization-Id"),
    x_user_id: UUID = Header(..., alias="X-User-Id"),
) -> ExtractionDraftResponse:
    service = ExtractionService(session)
    draft = await service.extract_to_draft(
        organization_id=x_organization_id,
        user_id=x_user_id,
        source_ref=body.source_ref,
        input_text=body.input_text,
    )
    await session.commit()
    return ExtractionDraftResponse.model_validate(draft)


@router.post("/{draft_id}/accept", response_model=ExtractionDraftResponse)
async def accept_extraction_draft(
    draft_id: UUID,
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    x_user_id: UUID = Header(..., alias="X-User-Id"),
) -> ExtractionDraftResponse:
    service = ExtractionService(session)
    draft = await service.accept(draft_id=draft_id, user_id=x_user_id)
    await session.commit()
    return ExtractionDraftResponse.model_validate(draft)


@router.post("/{draft_id}/reject", response_model=ExtractionDraftResponse)
async def reject_extraction_draft(
    draft_id: UUID,
    _authz: None = Depends(require_permission("can_review_extractions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    x_user_id: UUID = Header(..., alias="X-User-Id"),
) -> ExtractionDraftResponse:
    service = ExtractionService(session)
    draft = await service.reject(draft_id=draft_id, user_id=x_user_id)
    await session.commit()
    return ExtractionDraftResponse.model_validate(draft)
