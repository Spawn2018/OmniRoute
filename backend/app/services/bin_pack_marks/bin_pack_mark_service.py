from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.bin_pack_mark import parse_bin_pack_mark_row
from app.models.bin_pack_mark import BinPackMark
from app.repositories.bin_pack_marks.bin_pack_mark_repository import (
    BinPackMarkRepository,
)


class BinPackMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BinPackMarkRepository(session)

    async def list_marks(self) -> list[BinPackMark]:
        return await self._rows.list_marks()

    async def persist_bin_pack_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        pack_kind: object,
        source_ref: object,
    ) -> BinPackMark:
        code, kind, origin = parse_bin_pack_mark_row(
            mark_code,
            pack_kind,
            source_ref,
        )
        row = BinPackMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            pack_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
