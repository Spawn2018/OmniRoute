from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crm_opportunity import CrmOpportunity


class CrmOpportunityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_opportunities(self) -> list[CrmOpportunity]:
        packed = await self._session.scalars(
            select(CrmOpportunity).order_by(
                CrmOpportunity.opportunity_code,
                CrmOpportunity.id,
            ),
        )
        return list(packed.all())

    async def add_opportunity(self, row: CrmOpportunity) -> CrmOpportunity:
        self._session.add(row)
        await self._session.flush()
        return row
