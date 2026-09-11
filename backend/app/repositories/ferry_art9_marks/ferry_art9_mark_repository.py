from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ferry_art9_mark import FerryArt9Mark


class FerryArt9MarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FerryArt9Mark]:
        packed = await self._session.scalars(
            select(FerryArt9Mark).order_by(
                FerryArt9Mark.mark_code,
                FerryArt9Mark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FerryArt9Mark) -> FerryArt9Mark:
        self._session.add(row)
        await self._session.flush()
        return row
