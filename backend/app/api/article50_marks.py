from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.article50_mark import Article50Mark
from app.services.article50_marks.article50_mark_service import (
    Article50MarkService,
)

router = APIRouter(
    prefix="/article50-marks",
    tags=["article50-marks"],
)

_PERM = "can_manage_article50_marks"


class Article50MarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    label_kind: str
    source_ref: str


class Article50MarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    label_kind: str
    source_ref: str


def _row(saved: Article50Mark) -> Article50MarkResponse:
    return Article50MarkResponse.model_validate(saved)


@router.get("", response_model=list[Article50MarkResponse])
async def list_article50_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[Article50MarkResponse]:
    packed = await Article50MarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=Article50MarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_article50_mark(
    body: Article50MarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> Article50MarkResponse:
    saved = await Article50MarkService(session).persist_article50_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        label_kind=body.label_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
