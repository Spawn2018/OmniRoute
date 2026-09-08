from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_playbook import (
    require_board_id,
    require_claim_code,
    require_claim_text,
    require_play_source_ref,
)
from app.models.tender_playbook import TenderPlaybook
from app.repositories.tender_playbooks.tender_playbook_repository import TenderPlaybookRepository


class TenderPlaybookService:
    def __init__(self, session: AsyncSession) -> None:
        self._plays = TenderPlaybookRepository(session)

    async def list_plays(self) -> list[TenderPlaybook]:
        return await self._plays.fetch_plays()

    async def record_play(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        claim_code: object,
        claim_text: object,
        source_ref: object,
    ) -> TenderPlaybook:
        row = TenderPlaybook(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            claim_code=require_claim_code(claim_code),
            claim_text=require_claim_text(claim_text),
            source_ref=require_play_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._plays.add(row)
