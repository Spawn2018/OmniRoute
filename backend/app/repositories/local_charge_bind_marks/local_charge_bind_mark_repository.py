from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.local_charge_bind_mark import LocalChargeBindMark


class LocalChargeBindMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[LocalChargeBindMark]:
        result = await self._db.scalars(
            select(LocalChargeBindMark).order_by(
                LocalChargeBindMark.bind_kind.asc(),
                LocalChargeBindMark.mark_code.asc(),
                LocalChargeBindMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: LocalChargeBindMark) -> LocalChargeBindMark:
        self._db.add(row)
        await self._db.flush()
        return row
