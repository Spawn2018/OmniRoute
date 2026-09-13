from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.crm_opportunity import parse_crm_opportunity_row
from app.models.crm_opportunity import CrmOpportunity
from app.repositories.crm_opportunities.crm_opportunity_repository import (
    CrmOpportunityRepository,
)


class CrmOpportunityService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CrmOpportunityRepository(session)

    async def list_opportunities(self) -> list[CrmOpportunity]:
        return await self._rows.list_opportunities()

    async def persist_crm_opportunity(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        opportunity_code: object,
        stage_kind: object,
        source_ref: object,
    ) -> CrmOpportunity:
        code, kind, origin = parse_crm_opportunity_row(
            opportunity_code,
            stage_kind,
            source_ref,
        )
        row = CrmOpportunity(
            id=uuid4(),
            organization_id=organization_id,
            opportunity_code=code,
            stage_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_opportunity(row)
