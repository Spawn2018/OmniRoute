from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.style_cascade_mark import parse_style_cascade_mark_row
from app.models.style_cascade_mark import StyleCascadeMark
from app.repositories.style_cascade_marks.style_cascade_mark_repository import (
    StyleCascadeMarkRepository,
)


class StyleCascadeMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = StyleCascadeMarkRepository(session)

    async def list_marks(self) -> list[StyleCascadeMark]:
        return await self._rows.list_marks()

    async def persist_style_cascade_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        cascade_kind: object,
        source_ref: object,
    ) -> StyleCascadeMark:
        code, kind, origin = parse_style_cascade_mark_row(
            mark_code,
            cascade_kind,
            source_ref,
        )
        row = StyleCascadeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            cascade_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
