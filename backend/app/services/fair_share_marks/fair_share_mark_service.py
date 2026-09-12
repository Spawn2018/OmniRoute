from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.fair_share_mark import parse_fair_share_mark_row
from app.models.fair_share_mark import FairShareMark
from app.repositories.fair_share_marks.fair_share_mark_repository import (
    FairShareMarkRepository,
)


class FairShareMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FairShareMarkRepository(session)

    async def list_marks(self) -> list[FairShareMark]:
        return await self._rows.list_marks()

    async def persist_fair_share_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        share_kind: object,
        source_ref: object,
    ) -> FairShareMark:
        code, kind, origin = parse_fair_share_mark_row(
            mark_code,
            share_kind,
            source_ref,
        )
        row = FairShareMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            share_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
