from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_win_loss import (
    require_board_id,
    require_outcome,
    require_reason_code,
    require_verdict_source_ref,
)
from app.models.tender_win_loss import TenderWinLoss
from app.repositories.tender_win_losses.tender_win_loss_repository import TenderWinLossRepository


class TenderWinLossService:
    def __init__(self, session: AsyncSession) -> None:
        self._verdicts = TenderWinLossRepository(session)

    async def list_verdicts(self) -> list[TenderWinLoss]:
        return await self._verdicts.fetch_verdicts()

    async def record_verdict(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        outcome: object,
        reason_code: object,
        source_ref: object,
    ) -> TenderWinLoss:
        row = TenderWinLoss(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            outcome=require_outcome(outcome),
            reason_code=require_reason_code(reason_code),
            source_ref=require_verdict_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._verdicts.add(row)
