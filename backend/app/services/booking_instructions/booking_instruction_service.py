from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.booking_instruction import (
    require_booking_scope_token,
    require_instruction_shipment_id,
    require_instruction_source_ref,
    require_instruction_status,
    require_instruction_target_role,
)
from app.models.booking_instruction import BookingInstruction
from app.repositories.booking_instructions.booking_instruction_repository import (
    BookingInstructionRepository,
)


class BookingInstructionService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BookingInstructionRepository(session)

    async def list_for_shipment(self, shipment_id: object) -> list[BookingInstruction]:
        return await self._rows.list_current_for_shipment(
            require_instruction_shipment_id(shipment_id),
        )

    async def record_instruction(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        booking_scope: object,
        target_role: object,
        status: object,
        source_ref: object,
    ) -> BookingInstruction:
        order_id = require_instruction_shipment_id(shipment_id)
        scope = require_booking_scope_token(booking_scope)
        role = require_instruction_target_role(target_role)
        state = require_instruction_status(status)
        origin = require_instruction_source_ref(source_ref)
        current = await self._rows.find_current(order_id, scope, role)
        if current is not None and current.status == state and current.source_ref == origin:
            return current
        saved = await self._rows.add(
            BookingInstruction(
                id=uuid4(),
                organization_id=organization_id,
                shipment_id=order_id,
                booking_scope=scope,
                target_role=role,
                status=state,
                source_ref=origin,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
