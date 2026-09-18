from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.postal_epo_mark import PostalEpoMark
from app.services.postal_epo_marks.postal_epo_mark_service import PostalEpoMarkService

router = APIRouter(prefix="/postal-epo-marks", tags=["postal-epo-marks"])
_PERM = "can_manage_postal_epo_marks"


class PostalEpoMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mark_code: str
    epo_kind: str
    source_ref: str


class PostalEpoMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: UUID
    mark_code: str
    epo_kind: str
    source_ref: str


def _row(saved: PostalEpoMark) -> PostalEpoMarkResponse:
    return PostalEpoMarkResponse.model_validate(saved)


@router.get("", response_model=list[PostalEpoMarkResponse])
async def list_postal_epo_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PostalEpoMarkResponse]:
    return [_row(item) for item in await PostalEpoMarkService(session).list_marks()]


@router.post("", response_model=PostalEpoMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_postal_epo_mark(
    body: PostalEpoMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PostalEpoMarkResponse:
    saved = await PostalEpoMarkService(session).persist_postal_epo_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        epo_kind=body.epo_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
