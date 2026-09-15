from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.field_confidence_mark import FieldConfidenceMark


class FieldConfidenceMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FieldConfidenceMark]:
        stmt = select(FieldConfidenceMark).order_by(
            FieldConfidenceMark.mark_code,
            FieldConfidenceMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: FieldConfidenceMark) -> FieldConfidenceMark:
        self._session.add(row)
        await self._session.flush()
        return row
