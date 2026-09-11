from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.filing_scheme_mark import parse_filing_scheme_mark_row
from app.models.filing_scheme_mark import FilingSchemeMark
from app.repositories.filing_scheme_marks.filing_scheme_mark_repository import (
    FilingSchemeMarkRepository,
)


class FilingSchemeMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FilingSchemeMarkRepository(session)

    async def list_marks(self) -> list[FilingSchemeMark]:
        return await self._rows.list_marks()

    async def persist_filing_scheme_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        scheme_kind: object,
        source_ref: object,
    ) -> FilingSchemeMark:
        code, kind, origin = parse_filing_scheme_mark_row(
            mark_code,
            scheme_kind,
            source_ref,
        )
        row = FilingSchemeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            scheme_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
