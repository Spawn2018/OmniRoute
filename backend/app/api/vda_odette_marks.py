from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.vda_odette_mark import VdaOdetteMark
from app.services.vda_odette_marks.vda_odette_mark_service import (
    VdaOdetteMarkService,
)

router = APIRouter(prefix="/vda-odette-marks", tags=["vda-odette-marks"])

_PERM = "can_manage_vda_odette_marks"


class VdaOdetteMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    edi_kind: str
    source_ref: str


class VdaOdetteMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    edi_kind: str
    source_ref: str


def _row(saved: VdaOdetteMark) -> VdaOdetteMarkResponse:
    return VdaOdetteMarkResponse.model_validate(saved)


@router.get("", response_model=list[VdaOdetteMarkResponse])
async def list_vda_odette_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[VdaOdetteMarkResponse]:
    packed = await VdaOdetteMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=VdaOdetteMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_vda_odette_mark(
    body: VdaOdetteMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> VdaOdetteMarkResponse:
    saved = await VdaOdetteMarkService(session).persist_vda_odette_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        edi_kind=body.edi_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
