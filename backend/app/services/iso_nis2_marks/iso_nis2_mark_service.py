from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.iso_nis2_mark import parse_iso_nis2_mark_row
from app.models.iso_nis2_mark import IsoNis2Mark
from app.repositories.iso_nis2_marks.iso_nis2_mark_repository import (
    IsoNis2MarkRepository,
)


class IsoNis2MarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = IsoNis2MarkRepository(session)

    async def list_marks(self) -> list[IsoNis2Mark]:
        return await self._rows.list_marks()

    async def persist_iso_nis2_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ops_kind: object,
        source_ref: object,
    ) -> IsoNis2Mark:
        code, kind, origin = parse_iso_nis2_mark_row(
            mark_code,
            ops_kind,
            source_ref,
        )
        row = IsoNis2Mark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ops_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
