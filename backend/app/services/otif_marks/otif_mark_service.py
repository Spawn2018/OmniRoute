from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.otif_mark import parse_otif_mark_row
from app.models.otif_mark import OtifMark
from app.repositories.otif_marks.otif_mark_repository import OtifMarkRepository


class OtifMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OtifMarkRepository(session)

    async def list_marks(self) -> list[OtifMark]:
        return await self._rows.list_marks()

    async def persist_otif_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        scope_kind: object,
        source_ref: object,
    ) -> OtifMark:
        code, scope, origin = parse_otif_mark_row(mark_code, scope_kind, source_ref)
        row = OtifMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            scope_kind=scope,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
