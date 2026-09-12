from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.profit_center_mark import parse_profit_center_mark_row
from app.models.profit_center_mark import ProfitCenterMark
from app.repositories.profit_center_marks.profit_center_mark_repository import (
    ProfitCenterMarkRepository,
)


class ProfitCenterMarkService:
    """HITL katalog centrum zysku/kosztu/projektu — bez kolumny shipment i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = ProfitCenterMarkRepository(session)

    async def list_marks(self) -> list[ProfitCenterMark]:
        return await self._marks.list_marks()

    async def persist_profit_center_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        center_kind: object,
        source_ref: object,
    ) -> ProfitCenterMark:
        code, kind, pointer = parse_profit_center_mark_row(
            mark_code,
            center_kind,
            source_ref,
        )
        row = ProfitCenterMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            center_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
