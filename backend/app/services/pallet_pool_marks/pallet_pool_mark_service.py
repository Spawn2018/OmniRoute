from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.pallet_pool_mark import parse_pallet_pool_mark_row
from app.models.pallet_pool_mark import PalletPoolMark
from app.repositories.pallet_pool_marks.pallet_pool_mark_repository import (
    PalletPoolMarkRepository,
)


class PalletPoolMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PalletPoolMarkRepository(session)

    async def list_marks(self) -> list[PalletPoolMark]:
        return await self._rows.list_marks()

    async def persist_pallet_pool_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        pool_kind: object,
        source_ref: object,
    ) -> PalletPoolMark:
        code, kind, origin = parse_pallet_pool_mark_row(
            mark_code,
            pool_kind,
            source_ref,
        )
        row = PalletPoolMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            pool_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
