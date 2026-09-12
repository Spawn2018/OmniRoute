from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.demo_wipe_mark import parse_demo_wipe_mark_row
from app.models.demo_wipe_mark import DemoWipeMark
from app.repositories.demo_wipe_marks.demo_wipe_mark_repository import (
    DemoWipeMarkRepository,
)


class DemoWipeMarkService:
    """HITL katalog wipe demo — bez live wipe i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = DemoWipeMarkRepository(session)

    async def list_marks(self) -> list[DemoWipeMark]:
        return await self._marks.list_marks()

    async def persist_demo_wipe_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        wipe_kind: object,
        source_ref: object,
    ) -> DemoWipeMark:
        code, kind, pointer = parse_demo_wipe_mark_row(
            mark_code,
            wipe_kind,
            source_ref,
        )
        row = DemoWipeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            wipe_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
