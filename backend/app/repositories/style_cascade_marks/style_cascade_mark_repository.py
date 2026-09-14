from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.style_cascade_mark import StyleCascadeMark


class StyleCascadeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[StyleCascadeMark]:
        stmt = select(StyleCascadeMark).order_by(
            StyleCascadeMark.mark_code,
            StyleCascadeMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: StyleCascadeMark) -> StyleCascadeMark:
        self._session.add(row)
        await self._session.flush()
        return row
