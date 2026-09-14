from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.style_fidelity_mark import StyleFidelityMark


class StyleFidelityMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[StyleFidelityMark]:
        stmt = select(StyleFidelityMark).order_by(
            StyleFidelityMark.mark_code,
            StyleFidelityMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: StyleFidelityMark) -> StyleFidelityMark:
        self._session.add(row)
        await self._session.flush()
        return row
