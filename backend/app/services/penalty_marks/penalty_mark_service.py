from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.penalty_mark import parse_penalty_mark_row
from app.models.penalty_mark import PenaltyMark
from app.repositories.penalty_marks.penalty_mark_repository import PenaltyMarkRepository


class PenaltyMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PenaltyMarkRepository(session)

    async def list_marks(self) -> list[PenaltyMark]:
        return await self._rows.list_marks()

    async def persist_penalty_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        breach_kind: object,
        source_ref: object,
    ) -> PenaltyMark:
        code, kind, origin = parse_penalty_mark_row(mark_code, breach_kind, source_ref)
        row = PenaltyMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            breach_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
