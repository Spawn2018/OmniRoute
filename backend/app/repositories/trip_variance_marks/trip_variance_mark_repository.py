from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip_variance_mark import TripVarianceMark


class TripVarianceMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[TripVarianceMark]:
        result = await self._db.scalars(
            select(TripVarianceMark).order_by(
                TripVarianceMark.variance_kind.asc(),
                TripVarianceMark.mark_code.asc(),
                TripVarianceMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: TripVarianceMark) -> TripVarianceMark:
        self._db.add(row)
        await self._db.flush()
        return row
