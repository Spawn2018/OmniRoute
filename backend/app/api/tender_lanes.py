from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_lane import TenderLane
from app.services.tender_lanes.tender_lane_service import TenderLaneService
from app.services.tender_lots.tender_lot_service import TenderLotService

router = APIRouter(prefix="/tender-lanes", tags=["tender-lanes"])

_PERM = "can_manage_tender_lanes"


class TenderLaneCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_lot_id: UUID
    origin_unlocode: str
    destination_unlocode: str
    source_ref: str


class TenderLaneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_lot_id: UUID
    origin_unlocode: str
    destination_unlocode: str
    source_ref: str


def _as_row(row: TenderLane) -> TenderLaneResponse:
    return TenderLaneResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_lot_id=row.tender_lot_id,
        origin_unlocode=row.origin_unlocode,
        destination_unlocode=row.destination_unlocode,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderLaneResponse])
async def list_tender_lanes(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderLaneResponse]:
    rows = await TenderLaneService(session).list_marks()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderLaneResponse, status_code=status.HTTP_201_CREATED)
async def create_tender_lane(
    body: TenderLaneCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderLaneResponse:
    lot = await TenderLotService(session).get_lot(body.tender_lot_id)
    row = await TenderLaneService(session).record_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_lot_id=lot.id,
        origin_unlocode=body.origin_unlocode,
        destination_unlocode=body.destination_unlocode,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
