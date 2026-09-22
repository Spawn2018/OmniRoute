from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.pallet_synchro_mark import PalletSynchroMark
from app.services.pallet_synchro_marks.pallet_synchro_mark_service import (
    PalletSynchroMarkService,
)

router = APIRouter(prefix="/pallet-synchro-marks", tags=["pallet-synchro-marks"])

_PERM = "can_manage_pallet_synchro_marks"


class PalletSynchroMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    synchro_kind: str
    source_ref: str


class PalletSynchroMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    synchro_kind: str
    source_ref: str


def _as_response(row: PalletSynchroMark) -> PalletSynchroMarkResponse:
    return PalletSynchroMarkResponse.model_validate(row)


@router.get("", response_model=list[PalletSynchroMarkResponse])
async def list_pallet_synchro_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PalletSynchroMarkResponse]:
    rows = await PalletSynchroMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=PalletSynchroMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_pallet_synchro_mark(
    body: PalletSynchroMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PalletSynchroMarkResponse:
    saved = await PalletSynchroMarkService(session).persist_pallet_synchro_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        synchro_kind=body.synchro_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
