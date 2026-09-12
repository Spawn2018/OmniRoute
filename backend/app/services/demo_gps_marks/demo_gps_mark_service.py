from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.demo_gps_mark import parse_demo_gps_mark_row
from app.models.demo_gps_mark import DemoGpsMark
from app.repositories.demo_gps_marks.demo_gps_mark_repository import (
    DemoGpsMarkRepository,
)


class DemoGpsMarkService:
    """HITL katalog demo GPS — bez live poll i bez lat/lng."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = DemoGpsMarkRepository(session)

    async def list_marks(self) -> list[DemoGpsMark]:
        return await self._marks.list_marks()

    async def persist_demo_gps_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        demo_kind: object,
        source_ref: object,
    ) -> DemoGpsMark:
        code, kind, pointer = parse_demo_gps_mark_row(
            mark_code,
            demo_kind,
            source_ref,
        )
        row = DemoGpsMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            demo_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
