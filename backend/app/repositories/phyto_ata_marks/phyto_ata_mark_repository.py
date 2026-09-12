from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.phyto_ata_mark import PhytoAtaMark


class PhytoAtaMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PhytoAtaMark]:
        packed = await self._session.scalars(
            select(PhytoAtaMark).order_by(
                PhytoAtaMark.mark_code,
                PhytoAtaMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: PhytoAtaMark) -> PhytoAtaMark:
        self._session.add(row)
        await self._session.flush()
        return row
