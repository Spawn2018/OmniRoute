from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.postal_epo_mark import PostalEpoMark


class PostalEpoMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PostalEpoMark]:
        packed = await self._session.scalars(
            select(PostalEpoMark).order_by(PostalEpoMark.mark_code, PostalEpoMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: PostalEpoMark) -> PostalEpoMark:
        self._session.add(row)
        await self._session.flush()
        return row
