from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chassis_mark import parse_chassis_mark_row
from app.models.chassis_mark import ChassisMark
from app.repositories.chassis_marks.chassis_mark_repository import (
    ChassisMarkRepository,
)


class ChassisMarkService:
    """HITL katalog chassis/trailer — bez live pool i bez TEU."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = ChassisMarkRepository(session)

    async def list_marks(self) -> list[ChassisMark]:
        return await self._marks.list_marks()

    async def persist_chassis_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        chassis_kind: object,
        source_ref: object,
    ) -> ChassisMark:
        code, kind, pointer = parse_chassis_mark_row(
            mark_code,
            chassis_kind,
            source_ref,
        )
        row = ChassisMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            chassis_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
