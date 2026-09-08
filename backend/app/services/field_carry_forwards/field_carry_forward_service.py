from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.field_carry_forward import (
    require_carry_quotation_id,
    require_carry_shipment_id,
    require_field_map,
)
from app.models.field_carry_forward import FieldCarryForward
from app.repositories.field_carry_forwards.field_carry_forward_repository import (
    FieldCarryForwardRepository,
)


class FieldCarryForwardService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FieldCarryForwardRepository(session)

    async def list_for_shipment(self, shipment_id: UUID) -> list[FieldCarryForward]:
        return await self._rows.list_for_shipment(require_carry_shipment_id(shipment_id))

    async def record_fields(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        shipment_id: UUID,
        fields: object,
    ) -> list[FieldCarryForward]:
        quote = require_carry_quotation_id(quotation_id)
        shipment = require_carry_shipment_id(shipment_id)
        mapped = require_field_map(fields)
        recorded: list[FieldCarryForward] = []
        for key, value in mapped.items():
            recorded.append(
                await self._upsert_field(
                    organization_id=organization_id,
                    user_id=user_id,
                    quotation_id=quote,
                    shipment_id=shipment,
                    field_key=key,
                    field_value=value,
                ),
            )
        return recorded

    async def _upsert_field(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        shipment_id: UUID,
        field_key: str,
        field_value: str,
    ) -> FieldCarryForward:
        current = await self._rows.find_current(quotation_id, shipment_id, field_key)
        if current is not None and current.field_value == field_value:
            return current
        successor = FieldCarryForward(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=quotation_id,
            shipment_id=shipment_id,
            field_key=field_key,
            field_value=field_value,
            created_by=user_id,
        )
        saved = await self._rows.add(successor)
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
