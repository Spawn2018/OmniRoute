from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_prospect import (
    require_board_id,
    require_outreach_code,
    require_party_id,
    require_prospect_source_ref,
)
from app.models.tender_prospect import TenderProspect
from app.repositories.tender_prospects.tender_prospect_repository import (
    TenderProspectRepository,
)


class TenderProspectService:
    def __init__(self, session: AsyncSession) -> None:
        self._prospects = TenderProspectRepository(session)

    async def list_prospects(self) -> list[TenderProspect]:
        return await self._prospects.fetch_prospects()

    async def persist_prospect(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        party_id: object,
        outreach_code: object,
        source_ref: object,
    ) -> TenderProspect:
        row = TenderProspect(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            party_id=require_party_id(party_id),
            outreach_code=require_outreach_code(outreach_code),
            source_ref=require_prospect_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._prospects.add(row)
