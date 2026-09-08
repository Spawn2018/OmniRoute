from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipment_stakeholder import (
    require_stakeholder_party_id,
    require_stakeholder_role,
    require_stakeholder_shipment_id,
    require_stakeholder_source_ref,
)
from app.models.shipment_stakeholder import ShipmentStakeholder
from app.repositories.shipment_stakeholders.shipment_stakeholder_repository import (
    ShipmentStakeholderRepository,
)


class ShipmentStakeholderService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipmentStakeholderRepository(session)

    async def list_for_shipment(self, shipment_id: object) -> list[ShipmentStakeholder]:
        return await self._rows.list_current_for_shipment(
            require_stakeholder_shipment_id(shipment_id),
        )

    async def record_assignment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        party_id: object,
        role: object,
        source_ref: object,
    ) -> ShipmentStakeholder:
        order_id = require_stakeholder_shipment_id(shipment_id)
        counterpart = require_stakeholder_party_id(party_id)
        token = require_stakeholder_role(role)
        origin = require_stakeholder_source_ref(source_ref)
        current = await self._rows.find_current(order_id, token)
        if current is not None and current.party_id == counterpart and current.source_ref == origin:
            return current
        saved = await self._rows.add(
            ShipmentStakeholder(
                id=uuid4(),
                organization_id=organization_id,
                shipment_id=order_id,
                party_id=counterpart,
                role=token,
                source_ref=origin,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
