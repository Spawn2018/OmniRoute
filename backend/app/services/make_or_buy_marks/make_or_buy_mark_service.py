from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.make_or_buy_mark import parse_make_or_buy_mark_row
from app.models.make_or_buy_mark import MakeOrBuyMark
from app.repositories.make_or_buy_marks.make_or_buy_mark_repository import (
    MakeOrBuyMarkRepository,
)


class MakeOrBuyMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = MakeOrBuyMarkRepository(session)

    async def list_marks(self) -> list[MakeOrBuyMark]:
        return await self._rows.list_marks()

    async def persist_make_or_buy_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        buy_kind: object,
        source_ref: object,
    ) -> MakeOrBuyMark:
        code, kind, origin = parse_make_or_buy_mark_row(
            mark_code,
            buy_kind,
            source_ref,
        )
        row = MakeOrBuyMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            buy_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
