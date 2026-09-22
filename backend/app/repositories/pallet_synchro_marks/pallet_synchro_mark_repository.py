from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pallet_synchro_mark import PalletSynchroMark


class PalletSynchroMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[PalletSynchroMark]:
        result = await self._db.scalars(
            select(PalletSynchroMark).order_by(
                PalletSynchroMark.synchro_kind.asc(),
                PalletSynchroMark.mark_code.asc(),
                PalletSynchroMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: PalletSynchroMark) -> PalletSynchroMark:
        self._db.add(row)
        await self._db.flush()
        return row
