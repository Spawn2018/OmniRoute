from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipper_tender_mark import ShipperTenderMark
from app.services.shipper_tender_marks.shipper_tender_mark_service import (
    ShipperTenderMarkService,
)

router = APIRouter(prefix="/shipper-tender-marks", tags=["shipper-tender-marks"])

_PERM = "can_manage_shipper_tender_marks"


class ShipperTenderMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    shipper_kind: str
    source_ref: str


class ShipperTenderMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    shipper_kind: str
    source_ref: str


def _row(saved: ShipperTenderMark) -> ShipperTenderMarkResponse:
    return ShipperTenderMarkResponse.model_validate(saved)


@router.get("", response_model=list[ShipperTenderMarkResponse])
async def list_shipper_tender_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipperTenderMarkResponse]:
    packed = await ShipperTenderMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ShipperTenderMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shipper_tender_mark(
    body: ShipperTenderMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipperTenderMarkResponse:
    saved = await ShipperTenderMarkService(session).persist_shipper_tender_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        shipper_kind=body.shipper_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
