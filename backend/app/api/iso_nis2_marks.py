from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.iso_nis2_mark import IsoNis2Mark
from app.services.iso_nis2_marks.iso_nis2_mark_service import (
    IsoNis2MarkService,
)

router = APIRouter(prefix="/iso-nis2-marks", tags=["iso-nis2-marks"])

_PERM = "can_manage_iso_nis2_marks"


class IsoNis2MarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    ops_kind: str
    source_ref: str


class IsoNis2MarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    ops_kind: str
    source_ref: str


def _row(saved: IsoNis2Mark) -> IsoNis2MarkResponse:
    return IsoNis2MarkResponse.model_validate(saved)


@router.get("", response_model=list[IsoNis2MarkResponse])
async def list_iso_nis2_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[IsoNis2MarkResponse]:
    packed = await IsoNis2MarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=IsoNis2MarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_iso_nis2_mark(
    body: IsoNis2MarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> IsoNis2MarkResponse:
    saved = await IsoNis2MarkService(session).persist_iso_nis2_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        ops_kind=body.ops_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
