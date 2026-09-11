from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sanctions_mark import parse_sanctions_mark_row
from app.models.sanctions_mark import SanctionsMark
from app.repositories.sanctions_marks.sanctions_mark_repository import (
    SanctionsMarkRepository,
)


class SanctionsMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SanctionsMarkRepository(session)

    async def list_marks(self) -> list[SanctionsMark]:
        return await self._rows.list_marks()

    async def persist_sanctions_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        list_kind: object,
        source_ref: object,
    ) -> SanctionsMark:
        code, kind, origin = parse_sanctions_mark_row(
            mark_code,
            list_kind,
            source_ref,
        )
        row = SanctionsMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            list_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
