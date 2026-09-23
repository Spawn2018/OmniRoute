from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.local_charge_warning_mark import LocalChargeWarningMark


class LocalChargeWarningMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[LocalChargeWarningMark]:
        result = await self._db.scalars(
            select(LocalChargeWarningMark).order_by(
                LocalChargeWarningMark.warning_kind.asc(),
                LocalChargeWarningMark.mark_code.asc(),
                LocalChargeWarningMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: LocalChargeWarningMark) -> LocalChargeWarningMark:
        self._db.add(row)
        await self._db.flush()
        return row
