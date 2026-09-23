from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.margin_match_mark import MarginMatchMark


class MarginMatchMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[MarginMatchMark]:
        result = await self._db.scalars(
            select(MarginMatchMark).order_by(
                MarginMatchMark.match_kind.asc(),
                MarginMatchMark.mark_code.asc(),
                MarginMatchMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: MarginMatchMark) -> MarginMatchMark:
        self._db.add(row)
        await self._db.flush()
        return row
