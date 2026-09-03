from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidMoneyCost
from app.domain.money_cost import (
    require_cost_payment_id,
    require_cost_rate_id,
    require_cost_source_ref,
)
from app.models.money_cost import MoneyCost
from app.repositories.money_costs.money_cost_repository import MoneyCostRepository


class MoneyCostService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = MoneyCostRepository(session)

    async def list_costs(self) -> list[MoneyCost]:
        return await self._rows.list_all()

    async def record_cost(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        bank_payment_id: UUID,
        nbp_rate_id: UUID,
        source_ref: str,
    ) -> MoneyCost:
        row = MoneyCost(
            id=uuid4(),
            organization_id=organization_id,
            bank_payment_id=require_cost_payment_id(bank_payment_id),
            nbp_rate_id=require_cost_rate_id(nbp_rate_id),
            source_ref=require_cost_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidMoneyCost("para już zapisana") from orig
