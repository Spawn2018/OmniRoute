from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.oog_permit_mark import parse_oog_permit_mark_row
from app.models.oog_permit_mark import OogPermitMark
from app.repositories.oog_permit_marks.oog_permit_mark_repository import (
    OogPermitMarkRepository,
)


class OogPermitMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OogPermitMarkRepository(session)

    async def list_marks(self) -> list[OogPermitMark]:
        return await self._rows.list_marks()

    async def persist_oog_permit_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        permit_kind: object,
        source_ref: object,
    ) -> OogPermitMark:
        code, kind, origin = parse_oog_permit_mark_row(
            mark_code,
            permit_kind,
            source_ref,
        )
        row = OogPermitMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            permit_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
