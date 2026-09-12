"""HTTP katalog zakresu RAG — HITL, bez pgvector i wyceny."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.rag_sop_mark import RagSopMark
from app.services.rag_sop_marks.rag_sop_mark_service import RagSopMarkService

router = APIRouter(prefix="/rag-sop-marks", tags=["rag-sop"])

_PERM = "can_manage_rag_sop_marks"


class RagSopMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    scope_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class RagSopMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    scope_kind: str
    source_ref: str


def _to_dto(row: RagSopMark) -> RagSopMarkResponse:
    return RagSopMarkResponse.model_validate(row)


@router.get("", response_model=list[RagSopMarkResponse])
async def list_rag_sop_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RagSopMarkResponse]:
    catalog = RagSopMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=RagSopMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_rag_sop_mark(
    body: RagSopMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RagSopMarkResponse:
    catalog = RagSopMarkService(session)
    saved = await catalog.persist_rag_sop_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        scope_kind=body.scope_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "rag-sop-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
