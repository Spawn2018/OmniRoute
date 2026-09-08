from datetime import date, time
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.dock_appointment import require_stop_on_shipment, require_warehouse_location_kind
from app.models.dock_appointment import DockAppointment
from app.services.dock_appointments.dock_appointment_service import DockAppointmentService
from app.services.geography.location_service import LocationService
from app.services.shipments.shipment_service import ShipmentService
from app.services.stops.stop_service import StopService

router = APIRouter(prefix="/dock-appointments", tags=["dock-appointments"])

_PERM = "can_manage_dock_appointments"


class DockAppointmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    stop_id: UUID
    appointment_code: str
    appointment_status: str
    window_date: date
    window_start_local: time
    window_end_local: time
    source_ref: str


class DockAppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    stop_id: UUID
    appointment_code: str
    appointment_status: str
    window_date: date
    window_start_local: time
    window_end_local: time
    source_ref: str


def _as_row(row: DockAppointment) -> DockAppointmentResponse:
    return DockAppointmentResponse.model_validate(row)


@router.get("", response_model=list[DockAppointmentResponse])
async def list_dock_appointments(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DockAppointmentResponse]:
    rows = await DockAppointmentService(session).list_appointments()
    return [_as_row(row) for row in rows]


@router.post("", response_model=DockAppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_dock_appointment(
    body: DockAppointmentCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DockAppointmentResponse:
    order = await ShipmentService(session).get_shipment(body.shipment_id)
    halt = await StopService(session).get_stop(body.stop_id)
    require_stop_on_shipment(order.id, halt.shipment_id)
    place = await LocationService(session).get_location(halt.location_id)
    require_warehouse_location_kind(place.kind)
    row = await DockAppointmentService(session).record_appointment(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=order.id,
        stop_id=halt.id,
        appointment_code=body.appointment_code,
        appointment_status=body.appointment_status,
        window_date=body.window_date,
        window_start_local=body.window_start_local,
        window_end_local=body.window_end_local,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
