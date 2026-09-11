from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.spend_mark import parse_spend_mark_row
from app.models.spend_mark import SpendMark
from app.repositories.spend_marks.spend_mark_repository import SpendMarkRepository


class SpendMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SpendMarkRepository(session)

    async def list_marks(self) -> list[SpendMark]:
        return await self._rows.list_marks()

    async def persist_spend_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        leakage_kind: object,
        source_ref: object,
    ) -> SpendMark:
        code, kind, origin = parse_spend_mark_row(mark_code, leakage_kind, source_ref)
        row = SpendMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            leakage_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
