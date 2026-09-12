from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.rail_cim_mark import parse_rail_cim_mark_row
from app.models.rail_cim_mark import RailCimMark
from app.repositories.rail_cim_marks.rail_cim_mark_repository import RailCimMarkRepository


class RailCimMarkService:
    """HITL katalog rail CIM — bez rail live filing i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = RailCimMarkRepository(session)

    async def list_marks(self) -> list[RailCimMark]:
        return await self._marks.list_marks()

    async def persist_rail_cim_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        rail_kind: object,
        source_ref: object,
    ) -> RailCimMark:
        code, kind, pointer = parse_rail_cim_mark_row(mark_code, rail_kind, source_ref)
        row = RailCimMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            rail_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
