from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.fuel_card_mark import parse_fuel_card_mark_row
from app.models.fuel_card_mark import FuelCardMark
from app.repositories.fuel_card_marks.fuel_card_mark_repository import (
    FuelCardMarkRepository,
)


class FuelCardMarkService:
    """HITL katalog karty paliwowej — bez live API i bez litrów."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = FuelCardMarkRepository(session)

    async def list_marks(self) -> list[FuelCardMark]:
        return await self._marks.list_marks()

    async def persist_fuel_card_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        card_kind: object,
        source_ref: object,
    ) -> FuelCardMark:
        code, kind, pointer = parse_fuel_card_mark_row(
            mark_code,
            card_kind,
            source_ref,
        )
        row = FuelCardMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            card_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
