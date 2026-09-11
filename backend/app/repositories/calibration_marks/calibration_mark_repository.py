from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calibration_mark import CalibrationMark


class CalibrationMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CalibrationMark]:
        packed = await self._session.scalars(
            select(CalibrationMark).order_by(
                CalibrationMark.mark_code,
                CalibrationMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CalibrationMark) -> CalibrationMark:
        self._session.add(row)
        await self._session.flush()
        return row
