from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_decline_reason import parse_tender_decline_reason_row
from app.models.tender_decline_reason import TenderDeclineReason
from app.repositories.tender_decline_reasons.tender_decline_reason_repository import (
    TenderDeclineReasonRepository,
)


class TenderDeclineReasonService:
    """HITL zapis powodu decline — bez auto-award i bez RFP scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = TenderDeclineReasonRepository(session)

    async def list_marks(self) -> list[TenderDeclineReason]:
        return await self._repo.list_marks()

    async def persist_tender_decline_reason(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        decline_kind: object,
        source_ref: object,
    ) -> TenderDeclineReason:
        code, kind, pointer = parse_tender_decline_reason_row(
            mark_code,
            decline_kind,
            source_ref,
        )
        entity = TenderDeclineReason(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            decline_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._repo.add_mark(entity)
