from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crm_lead import CrmLead


class CrmLeadRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_leads(self) -> list[CrmLead]:
        packed = await self._session.scalars(
            select(CrmLead).order_by(CrmLead.lead_code, CrmLead.id),
        )
        return list(packed.all())

    async def add_lead(self, row: CrmLead) -> CrmLead:
        self._session.add(row)
        await self._session.flush()
        return row
