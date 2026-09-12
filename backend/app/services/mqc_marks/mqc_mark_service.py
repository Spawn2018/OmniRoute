from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.mqc_mark import parse_mqc_mark_row
from app.models.mqc_mark import MqcMark
from app.repositories.mqc_marks.mqc_mark_repository import (
    MqcMarkRepository,
)


class MqcMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = MqcMarkRepository(session)

    async def list_marks(self) -> list[MqcMark]:
        return await self._rows.list_marks()

    async def persist_mqc_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        mqc_kind: object,
        source_ref: object,
    ) -> MqcMark:
        code, kind, origin = parse_mqc_mark_row(
            mark_code,
            mqc_kind,
            source_ref,
        )
        row = MqcMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            mqc_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
