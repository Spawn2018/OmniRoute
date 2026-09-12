from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.general_average_mark import parse_general_average_mark_row
from app.models.general_average_mark import GeneralAverageMark
from app.repositories.general_average_marks.general_average_mark_repository import (
    GeneralAverageMarkRepository,
)


class GeneralAverageMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = GeneralAverageMarkRepository(session)

    async def list_marks(self) -> list[GeneralAverageMark]:
        return await self._rows.list_marks()

    async def persist_general_average_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        average_kind: object,
        source_ref: object,
    ) -> GeneralAverageMark:
        code, kind, origin = parse_general_average_mark_row(
            mark_code,
            average_kind,
            source_ref,
        )
        row = GeneralAverageMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            average_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
