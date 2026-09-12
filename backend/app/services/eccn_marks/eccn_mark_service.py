from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.eccn_mark import parse_eccn_mark_row
from app.models.eccn_mark import EccnMark
from app.repositories.eccn_marks.eccn_mark_repository import (
    EccnMarkRepository,
)


class EccnMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = EccnMarkRepository(session)

    async def list_marks(self) -> list[EccnMark]:
        return await self._rows.list_marks()

    async def persist_eccn_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        control_kind: object,
        source_ref: object,
    ) -> EccnMark:
        code, kind, origin = parse_eccn_mark_row(
            mark_code,
            control_kind,
            source_ref,
        )
        row = EccnMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            control_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
