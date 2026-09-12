from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.slot_guarantee_mark import parse_slot_guarantee_mark_row
from app.models.slot_guarantee_mark import SlotGuaranteeMark
from app.repositories.slot_guarantee_marks.slot_guarantee_mark_repository import (
    SlotGuaranteeMarkRepository,
)


class SlotGuaranteeMarkService:
    """HITL katalog stance slotu — bez live T8 i bez confirmed z formularza."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = SlotGuaranteeMarkRepository(session)

    async def list_marks(self) -> list[SlotGuaranteeMark]:
        return await self._marks.list_marks()

    async def persist_slot_guarantee_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> SlotGuaranteeMark:
        code, kind, pointer = parse_slot_guarantee_mark_row(
            mark_code,
            stance_kind,
            source_ref,
        )
        row = SlotGuaranteeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            stance_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
