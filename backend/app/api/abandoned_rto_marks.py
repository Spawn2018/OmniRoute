from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.abandoned_rto_mark import AbandonedRtoMark
from app.services.abandoned_rto_marks.abandoned_rto_mark_service import (
    AbandonedRtoMarkService,
)

router = APIRouter(prefix="/abandoned-rto-marks", tags=["abandoned-rto-marks"])

_PERM = "can_manage_abandoned_rto_marks"


class AbandonedRtoMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    fate_kind: str
    source_ref: str


class AbandonedRtoMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    fate_kind: str
    source_ref: str


def _row(saved: AbandonedRtoMark) -> AbandonedRtoMarkResponse:
    return AbandonedRtoMarkResponse.model_validate(saved)


@router.get("", response_model=list[AbandonedRtoMarkResponse])
async def list_abandoned_rto_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AbandonedRtoMarkResponse]:
    packed = await AbandonedRtoMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=AbandonedRtoMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_abandoned_rto_mark(
    body: AbandonedRtoMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AbandonedRtoMarkResponse:
    saved = await AbandonedRtoMarkService(session).persist_abandoned_rto_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        fate_kind=body.fate_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
