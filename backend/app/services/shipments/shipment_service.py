from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound, ShipmentConflict
from app.domain.shipment import (
    require_party_on_quotation,
    require_quotation_id,
    require_shipment_ref,
    require_shipment_source_ref,
    shipment_draft_status,
)
from app.models.shipment import Shipment
from app.repositories.shipments.shipment_repository import ShipmentRepository


class ShipmentService:
    def __init__(self, session: AsyncSession) -> None:
        self._shipments = ShipmentRepository(session)

    async def list_shipments(self) -> list[Shipment]:
        return await self._shipments.list_all()

    async def get_shipment(self, shipment_id: UUID) -> Shipment:
        found = await self._shipments.get(shipment_id)
        if found is None:
            raise ResourceNotFound("nieznane zlecenie")
        return found

    async def create_shipment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        party_id: UUID,
        source_ref: str,
        shipment_ref: object = None,
    ) -> Shipment:
        row = Shipment(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=require_quotation_id(quotation_id),
            party_id=require_party_on_quotation(party_id),
            source_ref=require_shipment_source_ref(source_ref),
            shipment_ref=require_shipment_ref(shipment_ref),
            status=shipment_draft_status(),
            created_by=user_id,
        )
        try:
            return await self._shipments.add(row)
        except IntegrityError as orig:
            detail = str(orig.orig) if orig.orig is not None else str(orig)
            if "uq_shipment_org_quotation" in detail:
                raise ShipmentConflict(
                    "to zlecenie już istnieje dla tej wyceny",
                ) from orig
            if "uq_shipment_org_shipment_ref" in detail:
                raise ShipmentConflict("ten numer zlecenia już istnieje") from orig
            raise
