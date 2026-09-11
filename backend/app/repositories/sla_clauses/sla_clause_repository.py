from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer_contract import CustomerContract
from app.models.sla_clause import SlaClause


class SlaClauseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_clauses(self) -> list[SlaClause]:
        packed = await self._session.scalars(
            select(SlaClause).order_by(SlaClause.clause_code, SlaClause.id),
        )
        return list(packed.all())

    async def get_contract(self, contract_id: UUID) -> CustomerContract | None:
        packed = await self._session.scalars(
            select(CustomerContract).where(CustomerContract.id == contract_id),
        )
        return packed.first()

    async def add_clause(self, row: SlaClause) -> SlaClause:
        self._session.add(row)
        await self._session.flush()
        return row
