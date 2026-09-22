from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidOceanBill, ResourceNotFound
from app.domain.ocean_bill import (
    optional_bill_no,
    require_bill_kind,
    require_bill_number_prefix,
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

    async def get_bill(self, bill_id: UUID) -> OceanBill:
        found = await self._rows.get(bill_id)
        if found is None:
            raise ResourceNotFound(f"nieznany konosament: {bill_id}")
        return found

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
            bill_no=optional_bill_no(bill_no),
            bill_kind=require_bill_kind(bill_kind),
            source_ref=require_bill_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)

    async def issue_hbl(self, *, bill_id: UUID, prefix: str | None) -> OceanBill:
        token = require_bill_number_prefix(prefix)
        current = await self.get_bill(bill_id)
        if current.bill_kind != "hbl":
            raise InvalidOceanBill("nadanie HBL tylko dla bill_kind hbl")
        if current.bill_no is not None:
            return current
        issued = await self._rows.issue_hbl(bill_id=bill_id, prefix=token)
        if issued is None:
            again = await self.get_bill(bill_id)
            if again.bill_no is not None:
                return again
            raise InvalidOceanBill("nie udało się nadać numeru HBL")
        return issued

    async def issue_mbl(self, *, bill_id: UUID, prefix: str | None) -> OceanBill:
        token = require_bill_number_prefix(prefix)
        current = await self.get_bill(bill_id)
        if current.bill_kind != "mbl":
            raise InvalidOceanBill("nadanie MBL tylko dla bill_kind mbl")
        if current.bill_no is not None:
            return current
        issued = await self._rows.issue_mbl(bill_id=bill_id, prefix=token)
        if issued is None:
            again = await self.get_bill(bill_id)
            if again.bill_no is not None:
                return again
            raise InvalidOceanBill("nie udało się nadać numeru MBL")
        return issued
