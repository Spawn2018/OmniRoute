from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.handover_sbar_mark import parse_handover_sbar_mark_row
from app.models.handover_sbar_mark import HandoverSbarMark
from app.repositories.handover_sbar_marks.handover_sbar_mark_repository import (
    HandoverSbarMarkRepository,
)


class HandoverSbarMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = HandoverSbarMarkRepository(session)

    async def list_marks(self) -> list[HandoverSbarMark]:
        return await self._rows.list_marks()

    async def persist_handover_sbar_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sbar_kind: object,
        source_ref: object,
    ) -> HandoverSbarMark:
        code, kind, origin = parse_handover_sbar_mark_row(
            mark_code,
            sbar_kind,
            source_ref,
        )
        row = HandoverSbarMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sbar_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
