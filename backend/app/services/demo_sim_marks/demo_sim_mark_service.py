from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.demo_sim_mark import parse_demo_sim_mark_row
from app.models.demo_sim_mark import DemoSimMark
from app.repositories.demo_sim_marks.demo_sim_mark_repository import (
    DemoSimMarkRepository,
)


class DemoSimMarkService:
    """HITL katalog demo sim — bez live floty i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = DemoSimMarkRepository(session)

    async def list_marks(self) -> list[DemoSimMark]:
        return await self._marks.list_marks()

    async def persist_demo_sim_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sim_kind: object,
        source_ref: object,
    ) -> DemoSimMark:
        code, kind, pointer = parse_demo_sim_mark_row(
            mark_code,
            sim_kind,
            source_ref,
        )
        row = DemoSimMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sim_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
