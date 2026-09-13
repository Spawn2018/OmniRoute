from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.load_order_mark import parse_load_order_mark_row
from app.models.load_order_mark import LoadOrderMark
from app.repositories.load_order_marks.load_order_mark_repository import (
    LoadOrderMarkRepository,
)


class LoadOrderMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LoadOrderMarkRepository(session)

    async def list_marks(self) -> list[LoadOrderMark]:
        return await self._rows.list_marks()

    async def persist_load_order_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        order_kind: object,
        source_ref: object,
    ) -> LoadOrderMark:
        code, kind, origin = parse_load_order_mark_row(
            mark_code,
            order_kind,
            source_ref,
        )
        row = LoadOrderMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            order_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
