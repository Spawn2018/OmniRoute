from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidShipmentLeg
from app.domain.shipment_leg import (
    require_leg_kind,
    require_leg_location_id,
    require_leg_shipment_id,
    require_leg_source_ref,
)
from app.models.shipment_leg import ShipmentLeg
from app.repositories.shipment_legs.shipment_leg_repository import ShipmentLegRepository


class ShipmentLegService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipmentLegRepository(session)

    async def list_legs(self) -> list[ShipmentLeg]:
        return await self._rows.list_all()

    async def record_leg(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        origin_location_id: UUID,
        destination_location_id: UUID,
        source_ref: str,
        leg_kind: str = "road",
    ) -> ShipmentLeg:
        row = ShipmentLeg(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_leg_shipment_id(shipment_id),
            origin_location_id=require_leg_location_id(
                origin_location_id, field="origin_location_id",
            ),
            destination_location_id=require_leg_location_id(
                destination_location_id, field="destination_location_id",
            ),
            leg_kind=require_leg_kind(leg_kind),
            source_ref=require_leg_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidShipmentLeg("odcinek tego rodzaju już zapisany") from orig
