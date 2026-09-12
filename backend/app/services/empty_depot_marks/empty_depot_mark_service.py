from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.empty_depot_mark import parse_empty_depot_mark_row
from app.models.empty_depot_mark import EmptyDepotMark
from app.repositories.empty_depot_marks.empty_depot_mark_repository import (
    EmptyDepotMarkRepository,
)


class EmptyDepotMarkService:
    """HITL katalog empty/depot — bez depot live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = EmptyDepotMarkRepository(session)

    async def list_marks(self) -> list[EmptyDepotMark]:
        return await self._marks.list_marks()

    async def persist_empty_depot_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        depot_kind: object,
        source_ref: object,
    ) -> EmptyDepotMark:
        code, kind, pointer = parse_empty_depot_mark_row(
            mark_code,
            depot_kind,
            source_ref,
        )
        row = EmptyDepotMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            depot_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
