from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidShipmentLeg, ResourceNotFound
from app.domain.shipment_leg import (
    require_air_waybill_kind,
    require_air_waybill_no,
    require_leg_kind,
    require_leg_location_id,
    require_leg_shipment_id,
    require_leg_source_ref,
    require_mawb_iata_check,
    require_waybill_number_prefix,
)
from app.models.shipment_leg import ShipmentLeg
from app.repositories.shipment_legs.shipment_leg_repository import ShipmentLegRepository


class ShipmentLegService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipmentLegRepository(session)

    async def list_legs(self) -> list[ShipmentLeg]:
        return await self._rows.list_all()

    async def get_leg(self, leg_id: UUID) -> ShipmentLeg:
        found = await self._rows.get(leg_id)
        if found is None:
            raise ResourceNotFound(f"nieznany odcinek: {leg_id}")
        return found

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
        hawb_no: object = None,
        mawb_no: object = None,
    ) -> ShipmentLeg:
        kind = require_leg_kind(leg_kind)
        house = require_air_waybill_no(hawb_no)
        master = require_mawb_iata_check(require_air_waybill_no(mawb_no))
        require_air_waybill_kind(kind, house, master)
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
            leg_kind=kind,
            hawb_no=house,
            mawb_no=master,
            source_ref=require_leg_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidShipmentLeg("odcinek tego rodzaju już zapisany") from orig

    async def issue_hawb(self, *, leg_id: UUID, prefix: str | None) -> ShipmentLeg:
        token = require_waybill_number_prefix(prefix)
        current = await self.get_leg(leg_id)
        if current.leg_kind != "air":
            raise InvalidShipmentLeg("list lotniczy tylko na odcinku air")
        if current.hawb_no is not None:
            return current
        issued = await self._rows.issue_hawb(leg_id=leg_id, prefix=token)
        if issued is None:
            again = await self.get_leg(leg_id)
            if again.hawb_no is not None:
                return again
            raise InvalidShipmentLeg("nie udało się nadać numeru HAWB")
        return issued

    async def issue_mawb(self, *, leg_id: UUID, prefix: str | None) -> ShipmentLeg:
        token = require_waybill_number_prefix(prefix)
        current = await self.get_leg(leg_id)
        if current.leg_kind != "air":
            raise InvalidShipmentLeg("list lotniczy tylko na odcinku air")
        if current.mawb_no is not None:
            return current
        issued = await self._rows.issue_mawb(leg_id=leg_id, prefix=token)
        if issued is None:
            again = await self.get_leg(leg_id)
            if again.mawb_no is not None:
                return again
            raise InvalidShipmentLeg("nie udało się nadać numeru MAWB")
        return issued
