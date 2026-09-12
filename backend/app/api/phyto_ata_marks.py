from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.phyto_ata_mark import PhytoAtaMark
from app.services.phyto_ata_marks.phyto_ata_mark_service import (
    PhytoAtaMarkService,
)

router = APIRouter(prefix="/phyto-ata-marks", tags=["phyto-ata-marks"])

_PERM = "can_manage_phyto_ata_marks"


class PhytoAtaMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    permit_kind: str
    source_ref: str


class PhytoAtaMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    permit_kind: str
    source_ref: str


def _row(saved: PhytoAtaMark) -> PhytoAtaMarkResponse:
    return PhytoAtaMarkResponse.model_validate(saved)


@router.get("", response_model=list[PhytoAtaMarkResponse])
async def list_phyto_ata_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PhytoAtaMarkResponse]:
    packed = await PhytoAtaMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PhytoAtaMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_phyto_ata_mark(
    body: PhytoAtaMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PhytoAtaMarkResponse:
    saved = await PhytoAtaMarkService(session).persist_phyto_ata_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        permit_kind=body.permit_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
