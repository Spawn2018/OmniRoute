from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.abandoned_rto_mark import parse_abandoned_rto_mark_row
from app.models.abandoned_rto_mark import AbandonedRtoMark
from app.repositories.abandoned_rto_marks.abandoned_rto_mark_repository import (
    AbandonedRtoMarkRepository,
)


class AbandonedRtoMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = AbandonedRtoMarkRepository(session)

    async def list_marks(self) -> list[AbandonedRtoMark]:
        return await self._rows.list_marks()

    async def persist_abandoned_rto_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        fate_kind: object,
        source_ref: object,
    ) -> AbandonedRtoMark:
        code, kind, origin = parse_abandoned_rto_mark_row(
            mark_code,
            fate_kind,
            source_ref,
        )
        row = AbandonedRtoMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            fate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
