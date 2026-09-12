from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.language_code_mark import parse_language_code_mark_row
from app.models.language_code_mark import LanguageCodeMark
from app.repositories.language_code_marks.language_code_mark_repository import (
    LanguageCodeMarkRepository,
)


class LanguageCodeMarkService:
    """HITL katalog kodu języka — bez kolumny shipment i bez preferred_language party."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = LanguageCodeMarkRepository(session)

    async def list_marks(self) -> list[LanguageCodeMark]:
        return await self._marks.list_marks()

    async def persist_language_code_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        locale_kind: object,
        source_ref: object,
    ) -> LanguageCodeMark:
        code, kind, pointer = parse_language_code_mark_row(
            mark_code,
            locale_kind,
            source_ref,
        )
        row = LanguageCodeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            locale_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
