from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.postal_dispatch_mark import PostalDispatchMark


class PostalDispatchMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PostalDispatchMark]:
        packed = await self._session.scalars(
            select(PostalDispatchMark).order_by(
                PostalDispatchMark.mark_code,
                PostalDispatchMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: PostalDispatchMark) -> PostalDispatchMark:
        self._session.add(row)
        await self._session.flush()
        return row
