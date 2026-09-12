from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.peppol_mark import parse_peppol_mark_row
from app.models.peppol_mark import PeppolMark
from app.repositories.peppol_marks.peppol_mark_repository import (
    PeppolMarkRepository,
)


class PeppolMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PeppolMarkRepository(session)

    async def list_marks(self) -> list[PeppolMark]:
        return await self._rows.list_marks()

    async def persist_peppol_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        peppol_kind: object,
        source_ref: object,
    ) -> PeppolMark:
        code, kind, origin = parse_peppol_mark_row(
            mark_code,
            peppol_kind,
            source_ref,
        )
        row = PeppolMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            peppol_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
