from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.filing_bind_mark import parse_filing_bind_mark_row
from app.models.filing_bind_mark import FilingBindMark
from app.repositories.filing_bind_marks import FilingBindMarkRepository


class FilingBindMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FilingBindMarkRepository(session)

    async def list_marks(self) -> list[FilingBindMark]:
        return await self._rows.list_marks()

    async def persist_filing_bind_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bind_kind: object,
        source_ref: object,
    ) -> FilingBindMark:
        code, kind, origin = parse_filing_bind_mark_row(mark_code, bind_kind, source_ref)
        row = FilingBindMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bind_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
