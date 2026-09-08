from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dock_appointment import (
    require_appointment_code,
    require_appointment_status,
    require_appointment_uuid,
    require_dock_source_ref,
    require_dock_window,
    require_window_date,
)
from app.models.dock_appointment import DockAppointment
from app.repositories.dock_appointments.dock_appointment_repository import (
    DockAppointmentRepository,
)


class DockAppointmentService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = DockAppointmentRepository(session)

    async def list_appointments(self) -> list[DockAppointment]:
        return await self._rows.list_all()

    async def record_appointment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        stop_id: object,
        appointment_code: object,
        appointment_status: object,
        window_date: object,
        window_start_local: object,
        window_end_local: object,
        source_ref: object,
    ) -> DockAppointment:
        open_at, close_at = require_dock_window(window_start_local, window_end_local)
        row = DockAppointment(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_appointment_uuid(shipment_id, field="shipment_id"),
            stop_id=require_appointment_uuid(stop_id, field="stop_id"),
            appointment_code=require_appointment_code(appointment_code),
            appointment_status=require_appointment_status(appointment_status),
            window_date=require_window_date(window_date),
            window_start_local=open_at,
            window_end_local=close_at,
            source_ref=require_dock_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
