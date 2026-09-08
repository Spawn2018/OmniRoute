from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.pallet_balance import (
    require_balance_party_id,
    require_balance_source_ref,
    require_pallet_kind,
    require_unit_count,
)
from app.models.pallet_balance import PalletBalance
from app.repositories.pallet_balances.pallet_balance_repository import (
    PalletBalanceRepository,
)


class PalletBalanceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PalletBalanceRepository(session)

    async def list_balances(self) -> list[PalletBalance]:
        return await self._rows.list_all()

    async def record_balance(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: object,
        pallet_kind: object,
        unit_count: object,
        source_ref: object,
    ) -> PalletBalance:
        row = PalletBalance(
            id=uuid4(),
            organization_id=organization_id,
            party_id=require_balance_party_id(party_id),
            pallet_kind=require_pallet_kind(pallet_kind),
            unit_count=require_unit_count(unit_count),
            source_ref=require_balance_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
