from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.yard_mark import parse_yard_mark_row
from app.models.yard_mark import YardMark
from app.repositories.yard_marks.yard_mark_repository import YardMarkRepository


class YardMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = YardMarkRepository(session)

    async def list_marks(self) -> list[YardMark]:
        return await self._rows.list_marks()

    async def persist_yard_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        yard_kind: object,
        source_ref: object,
    ) -> YardMark:
        code, kind, origin = parse_yard_mark_row(
            mark_code,
            yard_kind,
            source_ref,
        )
        row = YardMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            yard_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
