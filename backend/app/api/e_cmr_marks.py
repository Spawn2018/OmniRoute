from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.e_cmr_mark import ECmrMark
from app.services.e_cmr_marks.e_cmr_mark_service import (
    ECmrMarkService,
)

router = APIRouter(prefix="/e-cmr-marks", tags=["e-cmr-marks"])

_PERM = "can_manage_e_cmr_marks"


class ECmrMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    cmr_kind: str
    source_ref: str


class ECmrMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    cmr_kind: str
    source_ref: str


def _row(saved: ECmrMark) -> ECmrMarkResponse:
    return ECmrMarkResponse.model_validate(saved)


@router.get("", response_model=list[ECmrMarkResponse])
async def list_e_cmr_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ECmrMarkResponse]:
    packed = await ECmrMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ECmrMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_e_cmr_mark(
    body: ECmrMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ECmrMarkResponse:
    saved = await ECmrMarkService(session).persist_e_cmr_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        cmr_kind=body.cmr_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
