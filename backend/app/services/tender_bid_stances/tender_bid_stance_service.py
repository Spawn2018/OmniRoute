from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_bid_stance import (
    require_board_id,
    require_stance_code,
    require_stance_source_ref,
)
from app.models.tender_bid_stance import TenderBidStance
from app.repositories.tender_bid_stances.tender_bid_stance_repository import (
    TenderBidStanceRepository,
)


class TenderBidStanceService:
    def __init__(self, session: AsyncSession) -> None:
        self._stances = TenderBidStanceRepository(session)

    async def list_stances(self) -> list[TenderBidStance]:
        return await self._stances.fetch_stances()

    async def persist_stance(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        stance_code: object,
        source_ref: object,
    ) -> TenderBidStance:
        row = TenderBidStance(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            stance_code=require_stance_code(stance_code),
            source_ref=require_stance_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._stances.add(row)
