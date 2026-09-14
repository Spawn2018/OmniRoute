from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quality_descent_mark import QualityDescentMark


class QualityDescentMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[QualityDescentMark]:
        stmt = select(QualityDescentMark).order_by(
            QualityDescentMark.mark_code,
            QualityDescentMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: QualityDescentMark) -> QualityDescentMark:
        self._session.add(row)
        await self._session.flush()
        return row
