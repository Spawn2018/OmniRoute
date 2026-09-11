from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.calibration_mark import parse_calibration_mark_row
from app.models.calibration_mark import CalibrationMark
from app.repositories.calibration_marks.calibration_mark_repository import (
    CalibrationMarkRepository,
)


class CalibrationMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CalibrationMarkRepository(session)

    async def list_marks(self) -> list[CalibrationMark]:
        return await self._rows.list_marks()

    async def persist_calibration_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sample_ready: object,
        source_ref: object,
    ) -> CalibrationMark:
        code, ready, origin = parse_calibration_mark_row(
            mark_code, sample_ready, source_ref
        )
        row = CalibrationMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sample_ready=ready,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
