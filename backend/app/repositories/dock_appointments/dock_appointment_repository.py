from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dock_appointment import DockAppointment


class DockAppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[DockAppointment]:
        result = await self._session.scalars(
            select(DockAppointment).order_by(
                DockAppointment.created_at.desc(),
                DockAppointment.id,
            ),
        )
        return list(result.all())

    async def add(self, row: DockAppointment) -> DockAppointment:
        self._session.add(row)
        await self._session.flush()
        return row
