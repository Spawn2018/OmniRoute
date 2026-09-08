from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ocean_bill import (
    require_bill_kind,
    require_bill_no,
    require_bill_shipment_id,
    require_bill_source_ref,
)
from app.models.ocean_bill import OceanBill
from app.repositories.ocean_bills.ocean_bill_repository import OceanBillRepository


class OceanBillService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OceanBillRepository(session)

    async def list_bills(self) -> list[OceanBill]:
        return await self._rows.list_all()

    async def record_bill(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        bill_no: object,
        bill_kind: object,
        source_ref: object,
    ) -> OceanBill:
        row = OceanBill(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_bill_shipment_id(shipment_id),
            bill_no=require_bill_no(bill_no),
            bill_kind=require_bill_kind(bill_kind),
            source_ref=require_bill_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
