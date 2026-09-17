from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.postal_dispatch_mark import PostalDispatchMark
from app.services.postal_dispatch_marks.postal_dispatch_mark_service import (
    PostalDispatchMarkService,
)

router = APIRouter(prefix="/postal-dispatch-marks", tags=["postal-dispatch-marks"])

_PERM = "can_manage_postal_dispatch_marks"


class PostalDispatchMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    dispatch_kind: str
    source_ref: str


class PostalDispatchMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    dispatch_kind: str
    source_ref: str


def _row(saved: PostalDispatchMark) -> PostalDispatchMarkResponse:
    return PostalDispatchMarkResponse.model_validate(saved)


@router.get("", response_model=list[PostalDispatchMarkResponse])
async def list_postal_dispatch_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PostalDispatchMarkResponse]:
    packed = await PostalDispatchMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PostalDispatchMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_postal_dispatch_mark(
    body: PostalDispatchMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PostalDispatchMarkResponse:
    saved = await PostalDispatchMarkService(session).persist_postal_dispatch_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        dispatch_kind=body.dispatch_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
