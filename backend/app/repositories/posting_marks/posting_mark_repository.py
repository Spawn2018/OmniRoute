from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.posting_mark import PostingMark


def _posting_catalog_query() -> Select[tuple[PostingMark]]:
    return select(PostingMark).order_by(
        PostingMark.mark_code.asc(),
        PostingMark.created_at.desc(),
    )


class PostingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PostingMark]:
        loaded = await self._session.scalars(_posting_catalog_query())
        batch: Sequence[PostingMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: PostingMark) -> PostingMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
