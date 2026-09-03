from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cost_to_serve import (
    require_cost_to_serve_quotation_id,
    require_cost_to_serve_sop_id,
    require_cost_to_serve_source_ref,
)
from app.domain.errors import InvalidCostToServe
from app.models.cost_to_serve import CostToServe
from app.repositories.cost_to_serve.cost_to_serve_repository import CostToServeRepository


class CostToServeService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CostToServeRepository(session)

    async def list_rows(self) -> list[CostToServe]:
        return await self._rows.list_all()

    async def record_row(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        customer_sop_id: UUID,
        quotation_id: UUID,
        source_ref: str,
    ) -> CostToServe:
        row = CostToServe(
            id=uuid4(),
            organization_id=organization_id,
            customer_sop_id=require_cost_to_serve_sop_id(customer_sop_id),
            quotation_id=require_cost_to_serve_quotation_id(quotation_id),
            source_ref=require_cost_to_serve_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidCostToServe("para już zapisana") from orig
