from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.style_cascade_mark import StyleCascadeMark
from app.services.style_cascade_marks.style_cascade_mark_service import (
    StyleCascadeMarkService,
)

router = APIRouter(
    prefix="/style-cascade-marks",
    tags=["style-cascade-marks"],
)

_PERM = "can_manage_style_cascade_marks"


class StyleCascadeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    cascade_kind: str
    source_ref: str


class StyleCascadeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    cascade_kind: str
    source_ref: str


def _row(saved: StyleCascadeMark) -> StyleCascadeMarkResponse:
    return StyleCascadeMarkResponse.model_validate(saved)


@router.get("", response_model=list[StyleCascadeMarkResponse])
async def list_style_cascade_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[StyleCascadeMarkResponse]:
    packed = await StyleCascadeMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=StyleCascadeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_style_cascade_mark(
    body: StyleCascadeMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> StyleCascadeMarkResponse:
    saved = await StyleCascadeMarkService(session).persist_style_cascade_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        cascade_kind=body.cascade_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
