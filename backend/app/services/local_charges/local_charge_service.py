from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.local_charge import (
    require_levy_amount,
    require_levy_carrier_label,
    require_levy_currency,
    require_levy_iso,
    require_levy_kind,
    require_levy_port,
    require_levy_service_label,
    require_levy_source_ref,
)
from app.models.local_charge import LocalCharge
from app.repositories.local_charges.local_charge_repository import LocalChargeRepository


class LocalChargeService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LocalChargeRepository(session)

    async def list_levies(self) -> list[LocalCharge]:
        return await self._rows.list_all()

    async def record_levy(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_kind: object,
        amount: object,
        currency: object,
        source_ref: object,
        port_unlocode: object = None,
        iso_size_type: object = None,
        carrier_label: object = None,
        service_label: object = None,
    ) -> LocalCharge:
        row = LocalCharge(
            id=uuid4(),
            organization_id=organization_id,
            charge_kind=require_levy_kind(charge_kind),
            amount=require_levy_amount(amount),
            currency=require_levy_currency(currency),
            port_unlocode=require_levy_port(port_unlocode),
            iso_size_type=require_levy_iso(iso_size_type),
            carrier_label=require_levy_carrier_label(carrier_label),
            service_label=require_levy_service_label(service_label),
            source_ref=require_levy_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
