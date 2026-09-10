from datetime import datetime
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
    eta_physical: str
    eta_legal: str
    stop_group_code: str | None = None
    notes_for_driver: str | None = None
    weight_kg: str | None = None
    quantity: int | str | float | bool | None = None
    packaging_code: str | None = None
    seal_in: str | None = None
    seal_out: str | None = None
    appointment_ref: str | None = None
    waiting_free_minutes: int | str | float | bool | None = None
    waiting_started_at: str | None = None
    pod_quality: str | None = None


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
    eta_physical: datetime
    eta_legal: datetime
    stop_group_code: str | None
    notes_for_driver: str | None
    weight_kg: str | None
    quantity: int | None
    packaging_code: str | None
    seal_in: str | None
    seal_out: str | None
    appointment_ref: str | None
    waiting_free_minutes: int | None
    waiting_started_at: datetime | None
    pod_quality: str | None
    superseded_by: UUID | None


def _as_response(row: Stop) -> StopResponse:
    dumped = {name: getattr(row, name) for name in StopResponse.model_fields}
    dumped["weight_kg"] = None if row.weight_kg is None else format(row.weight_kg, "f")
    return StopResponse.model_validate(dumped)


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
        eta_physical=body.eta_physical,
        eta_legal=body.eta_legal,
        stop_group_code=body.stop_group_code,
        notes_for_driver=body.notes_for_driver,
        weight_kg=body.weight_kg,
        quantity=body.quantity,
        packaging_code=body.packaging_code,
        seal_in=body.seal_in,
        seal_out=body.seal_out,
        appointment_ref=body.appointment_ref,
        waiting_free_minutes=body.waiting_free_minutes,
        waiting_started_at=body.waiting_started_at,
        pod_quality=body.pod_quality,
    )
    await session.commit()
    return _as_response(row)
