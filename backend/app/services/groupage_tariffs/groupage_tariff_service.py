from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.groupage_tariff import (
    require_chargeable_weight,
    require_tariff_amount,
    require_tariff_code,
    require_tariff_currency,
    require_tariff_location_id,
    require_tariff_source_ref,
    require_tariff_volume_m3,
)
from app.models.groupage_tariff import GroupageTariff
from app.repositories.groupage_tariffs.groupage_tariff_repository import (
    GroupageTariffRepository,
)


class GroupageTariffService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = GroupageTariffRepository(session)

    async def list_tariffs(self) -> list[GroupageTariff]:
        return await self._rows.list_all()

    async def record_tariff(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        location_id: object,
        tariff_code: object,
        chargeable_weight: object,
        amount: object,
        currency: object,
        source_ref: object,
        volume_m3: object = None,
    ) -> GroupageTariff:
        row = GroupageTariff(
            id=uuid4(),
            organization_id=organization_id,
            location_id=require_tariff_location_id(location_id),
            tariff_code=require_tariff_code(tariff_code),
            chargeable_weight=require_chargeable_weight(chargeable_weight),
            amount=require_tariff_amount(amount),
            currency=require_tariff_currency(currency),
            source_ref=require_tariff_source_ref(source_ref),
            volume_m3=require_tariff_volume_m3(volume_m3),
            created_by=user_id,
        )
        return await self._rows.add(row)
