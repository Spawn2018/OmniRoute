from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.stop import Stop
from app.services.geography.location_service import LocationService
from app.services.shipments.shipment_service import ShipmentService
from app.services.stops.stop_service import StopService

router = APIRouter(prefix="/stops", tags=["stops"])

_SHIP = "can_manage_shipments"


class StopCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    location_id: UUID
    stop_kind: str
    sequence_no: int
    time_zone: str
    status: str
    source_ref: str


class StopResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    location_id: UUID
    stop_kind: str
    sequence_no: int
    time_zone: str
    status: str
    source_ref: str
    superseded_by: UUID | None


def _as_response(row: Stop) -> StopResponse:
    return StopResponse.model_validate(row)


@router.get("", response_model=list[StopResponse])
async def list_stops(
    shipment_id: UUID = Query(...),
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[StopResponse]:
    await ShipmentService(session).get_shipment(shipment_id)
    rows = await StopService(session).list_for_shipment(shipment_id)
    return [_as_response(row) for row in rows]


@router.post("", response_model=StopResponse, status_code=status.HTTP_201_CREATED)
async def create_stop(
    body: StopCreate,
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> StopResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    place = await LocationService(session).get_location(body.location_id)
    row = await StopService(session).record_stop(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        location_id=place.id,
        stop_kind=body.stop_kind,
        sequence_no=body.sequence_no,
        time_zone=body.time_zone,
        status=body.status,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(row)
