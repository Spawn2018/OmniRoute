from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.capa_mark import parse_capa_mark_row
from app.models.capa_mark import CapaMark
from app.repositories.capa_marks.capa_mark_repository import CapaMarkRepository


class CapaMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CapaMarkRepository(session)

    async def list_marks(self) -> list[CapaMark]:
        return await self._rows.list_marks()

    async def persist_capa_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        mark_kind: object,
        source_ref: object,
    ) -> CapaMark:
        code, kind, origin = parse_capa_mark_row(mark_code, mark_kind, source_ref)
        row = CapaMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            mark_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
