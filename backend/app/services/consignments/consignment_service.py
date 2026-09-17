from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.consignment import (
    require_consignment_ref,
    require_consignment_shipment_id,
    require_consignment_source_ref,
    require_consignment_stop_id,
)
from app.domain.errors import ResourceNotFound
from app.models.consignment import Consignment
from app.repositories.consignments.consignment_repository import ConsignmentRepository


class ConsignmentService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ConsignmentRepository(session)

    async def list_parcels(self) -> list[Consignment]:
        return await self._rows.list_all()

    async def get_parcel(self, consignment_id: UUID) -> Consignment:
        row = await self._rows.get_by_id(consignment_id)
        if row is None:
            raise ResourceNotFound("nieznana przesyłka")
        return row

    async def record_parcel(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        consignment_ref: object,
        source_ref: object,
        stop_id: object | None = None,
    ) -> Consignment:
        halt: UUID | None = None
        if stop_id is not None:
            halt = require_consignment_stop_id(stop_id)
        row = Consignment(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_consignment_shipment_id(shipment_id),
            stop_id=halt,
            consignment_ref=require_consignment_ref(consignment_ref),
            source_ref=require_consignment_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
