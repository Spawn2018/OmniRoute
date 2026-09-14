from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.style_fidelity_mark import parse_style_fidelity_mark_row
from app.models.style_fidelity_mark import StyleFidelityMark
from app.repositories.style_fidelity_marks.style_fidelity_mark_repository import (
    StyleFidelityMarkRepository,
)


class StyleFidelityMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = StyleFidelityMarkRepository(session)

    async def list_marks(self) -> list[StyleFidelityMark]:
        return await self._rows.list_marks()

    async def persist_style_fidelity_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        fidelity_kind: object,
        source_ref: object,
    ) -> StyleFidelityMark:
        code, kind, origin = parse_style_fidelity_mark_row(
            mark_code,
            fidelity_kind,
            source_ref,
        )
        row = StyleFidelityMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            fidelity_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
