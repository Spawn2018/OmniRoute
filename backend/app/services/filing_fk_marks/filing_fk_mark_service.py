from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.filing_fk_mark import parse_filing_fk_mark_row
from app.models.filing_fk_mark import FilingFkMark
from app.repositories.filing_fk_marks import FilingFkMarkRepository


class FilingFkMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FilingFkMarkRepository(session)

    async def list_marks(self) -> list[FilingFkMark]:
        return await self._rows.list_marks()

    async def persist_filing_fk_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        fk_kind: object,
        source_ref: object,
    ) -> FilingFkMark:
        code, kind, origin = parse_filing_fk_mark_row(
            mark_code,
            fk_kind,
            source_ref,
        )
        row = FilingFkMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            fk_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
