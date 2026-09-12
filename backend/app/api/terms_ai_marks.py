"""HTTP katalog Terms AI — HITL, bez live mapa/GPS."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.terms_ai_mark import TermsAiMark
from app.services.terms_ai_marks.terms_ai_mark_service import TermsAiMarkService

router = APIRouter(prefix="/terms-ai-marks", tags=["funnel"])

_PERM = "can_manage_terms_ai_marks"

class TermsAiMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    terms_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)

class TermsAiMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    terms_kind: str
    source_ref: str

def _to_dto(row: TermsAiMark) -> TermsAiMarkResponse:
    return TermsAiMarkResponse.model_validate(row)

@router.get("", response_model=list[TermsAiMarkResponse])
async def list_terms_ai_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TermsAiMarkResponse]:
    catalog = TermsAiMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]

@router.post("", response_model=TermsAiMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_terms_ai_mark(
    body: TermsAiMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TermsAiMarkResponse:
    catalog = TermsAiMarkService(session)
    saved = await catalog.persist_terms_ai_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        terms_kind=body.terms_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "terms-ai-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
