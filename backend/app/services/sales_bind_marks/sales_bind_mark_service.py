from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sales_bind_mark import parse_sales_bind_mark_row
from app.models.sales_bind_mark import SalesBindMark
from app.repositories.sales_bind_marks.sales_bind_mark_repository import (
    SalesBindMarkRepository,
)


class SalesBindMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = SalesBindMarkRepository(session)

    async def list_marks(self) -> list[SalesBindMark]:
        return await self._repo.list_marks()

    async def persist_sales_bind_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bind_kind: object,
        source_ref: object,
    ) -> SalesBindMark:
        code, kind, origin = parse_sales_bind_mark_row(mark_code, bind_kind, source_ref)
        row = SalesBindMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bind_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._repo.add_mark(row)
