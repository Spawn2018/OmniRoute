from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.bid_decision_mark import parse_bid_decision_mark_row
from app.models.bid_decision_mark import BidDecisionMark
from app.repositories.bid_decision_marks.bid_decision_mark_repository import (
    BidDecisionMarkRepository,
)


class BidDecisionMarkService:
    """HITL katalog bid decision — bez kolumny quotation i bez auto-award."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = BidDecisionMarkRepository(session)

    async def list_marks(self) -> list[BidDecisionMark]:
        return await self._marks.list_marks()

    async def persist_bid_decision_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        decision_kind: object,
        source_ref: object,
    ) -> BidDecisionMark:
        code, kind, pointer = parse_bid_decision_mark_row(
            mark_code,
            decision_kind,
            source_ref,
        )
        row = BidDecisionMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            decision_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
