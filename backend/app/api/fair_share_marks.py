from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.fair_share_mark import FairShareMark
from app.services.fair_share_marks.fair_share_mark_service import (
    FairShareMarkService,
)

router = APIRouter(prefix="/fair-share-marks", tags=["fair-share-marks"])

_PERM = "can_manage_fair_share_marks"


class FairShareMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    share_kind: str
    source_ref: str


class FairShareMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    share_kind: str
    source_ref: str


def _row(saved: FairShareMark) -> FairShareMarkResponse:
    return FairShareMarkResponse.model_validate(saved)


@router.get("", response_model=list[FairShareMarkResponse])
async def list_fair_share_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FairShareMarkResponse]:
    packed = await FairShareMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=FairShareMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_fair_share_mark(
    body: FairShareMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FairShareMarkResponse:
    saved = await FairShareMarkService(session).persist_fair_share_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        share_kind=body.share_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
