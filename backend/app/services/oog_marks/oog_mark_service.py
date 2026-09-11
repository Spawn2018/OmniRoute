from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.oog_mark import parse_oog_mark_row
from app.models.oog_mark import OogMark
from app.repositories.oog_marks.oog_mark_repository import OogMarkRepository


class OogMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OogMarkRepository(session)

    async def list_marks(self) -> list[OogMark]:
        return await self._rows.list_marks()

    async def persist_oog_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        escort_kind: object,
        source_ref: object,
    ) -> OogMark:
        code, kind, origin = parse_oog_mark_row(
            mark_code,
            escort_kind,
            source_ref,
        )
        row = OogMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            escort_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
