from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article50_mark import Article50Mark


class Article50MarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[Article50Mark]:
        stmt = select(Article50Mark).order_by(
            Article50Mark.mark_code,
            Article50Mark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: Article50Mark) -> Article50Mark:
        self._session.add(row)
        await self._session.flush()
        return row
