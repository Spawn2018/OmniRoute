from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.create_block_mark import CreateBlockMark


class CreateBlockMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CreateBlockMark]:
        packed = await self._session.scalars(
            select(CreateBlockMark).order_by(
                CreateBlockMark.mark_code,
                CreateBlockMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CreateBlockMark) -> CreateBlockMark:
        self._session.add(row)
        await self._session.flush()
        return row
