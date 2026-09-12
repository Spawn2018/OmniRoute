"""HTTP katalog reefer — HITL, bez live filing."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.posting_mark import PostingMark
from app.services.posting_marks.posting_mark_service import PostingMarkService

router = APIRouter(prefix="/posting-marks", tags=["empty-depot"])

_PERM = "can_manage_posting_marks"


class PostingMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    posting_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class PostingMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    posting_kind: str
    source_ref: str


def _to_dto(row: PostingMark) -> PostingMarkResponse:
    return PostingMarkResponse.model_validate(row)


@router.get("", response_model=list[PostingMarkResponse])
async def list_posting_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PostingMarkResponse]:
    catalog = PostingMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=PostingMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_posting_mark(
    body: PostingMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PostingMarkResponse:
    catalog = PostingMarkService(session)
    saved = await catalog.persist_posting_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        posting_kind=body.posting_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "posting-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
