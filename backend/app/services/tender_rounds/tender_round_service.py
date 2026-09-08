from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_round import require_board_id, require_round_no, require_round_source_ref
from app.models.tender_round import TenderRound
from app.repositories.tender_rounds.tender_round_repository import TenderRoundRepository


class TenderRoundService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TenderRoundRepository(session)

    async def list_turns(self) -> list[TenderRound]:
        return await self._rows.fetch_rows()

    async def record_turn(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        round_no: object,
        source_ref: object,
    ) -> TenderRound:
        row = TenderRound(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            round_no=require_round_no(round_no),
            source_ref=require_round_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
