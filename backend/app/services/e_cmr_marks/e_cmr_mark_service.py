from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.e_cmr_mark import parse_e_cmr_mark_row
from app.models.e_cmr_mark import ECmrMark
from app.repositories.e_cmr_marks.e_cmr_mark_repository import (
    ECmrMarkRepository,
)


class ECmrMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ECmrMarkRepository(session)

    async def list_marks(self) -> list[ECmrMark]:
        return await self._rows.list_marks()

    async def persist_e_cmr_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        cmr_kind: object,
        source_ref: object,
    ) -> ECmrMark:
        code, kind, origin = parse_e_cmr_mark_row(
            mark_code,
            cmr_kind,
            source_ref,
        )
        row = ECmrMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            cmr_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
