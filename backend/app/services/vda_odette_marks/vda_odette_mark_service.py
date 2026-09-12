from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.vda_odette_mark import parse_vda_odette_mark_row
from app.models.vda_odette_mark import VdaOdetteMark
from app.repositories.vda_odette_marks.vda_odette_mark_repository import (
    VdaOdetteMarkRepository,
)


class VdaOdetteMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = VdaOdetteMarkRepository(session)

    async def list_marks(self) -> list[VdaOdetteMark]:
        return await self._rows.list_marks()

    async def persist_vda_odette_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        edi_kind: object,
        source_ref: object,
    ) -> VdaOdetteMark:
        code, kind, origin = parse_vda_odette_mark_row(
            mark_code,
            edi_kind,
            source_ref,
        )
        row = VdaOdetteMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            edi_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
