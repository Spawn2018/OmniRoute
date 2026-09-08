from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking_instruction import BookingInstruction


class BookingInstructionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current_for_shipment(
        self,
        shipment_id: UUID,
    ) -> list[BookingInstruction]:
        result = await self._session.scalars(
            select(BookingInstruction)
            .where(
                BookingInstruction.shipment_id == shipment_id,
                BookingInstruction.superseded_by.is_(None),
            )
            .order_by(
                BookingInstruction.booking_scope,
                BookingInstruction.target_role,
                BookingInstruction.id,
            ),
        )
        return list(result.all())

    async def find_current(
        self,
        shipment_id: UUID,
        booking_scope: str,
        target_role: str,
    ) -> BookingInstruction | None:
        result = await self._session.scalars(
            select(BookingInstruction).where(
                BookingInstruction.shipment_id == shipment_id,
                BookingInstruction.booking_scope == booking_scope,
                BookingInstruction.target_role == target_role,
                BookingInstruction.superseded_by.is_(None),
            ),
        )
        found = list(result.all())
        return found[0] if found else None

    async def add(self, row: BookingInstruction) -> BookingInstruction:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(
        self,
        current: BookingInstruction,
        successor_id: UUID,
    ) -> BookingInstruction:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
