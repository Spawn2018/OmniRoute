from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.rail_uic_mark import parse_rail_uic_mark_row
from app.models.rail_uic_mark import RailUicMark
from app.repositories.rail_uic_marks.rail_uic_mark_repository import (
    RailUicMarkRepository,
)


class RailUicMarkService:
    """HITL katalog UIC/CIM/SMGS — bez live rail API i bez km."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = RailUicMarkRepository(session)

    async def list_marks(self) -> list[RailUicMark]:
        return await self._marks.list_marks()

    async def persist_rail_uic_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        rail_kind: object,
        source_ref: object,
    ) -> RailUicMark:
        code, kind, pointer = parse_rail_uic_mark_row(
            mark_code,
            rail_kind,
            source_ref,
        )
        row = RailUicMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            rail_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
