from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.field_confidence_mark import parse_field_confidence_mark_row
from app.models.field_confidence_mark import FieldConfidenceMark
from app.repositories.field_confidence_marks.field_confidence_mark_repository import (
    FieldConfidenceMarkRepository,
)


class FieldConfidenceMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FieldConfidenceMarkRepository(session)

    async def list_marks(self) -> list[FieldConfidenceMark]:
        return await self._rows.list_marks()

    async def persist_field_confidence_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        band_kind: object,
        source_ref: object,
    ) -> FieldConfidenceMark:
        code, kind, origin = parse_field_confidence_mark_row(
            mark_code,
            band_kind,
            source_ref,
        )
        row = FieldConfidenceMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            band_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
