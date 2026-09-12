from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.diversion_mark import parse_diversion_mark_row
from app.models.diversion_mark import DiversionMark
from app.repositories.diversion_marks.diversion_mark_repository import (
    DiversionMarkRepository,
)


class DiversionMarkService:
    """HITL katalog diversion — bez FK shipment i bez cargo_value."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = DiversionMarkRepository(session)

    async def list_marks(self) -> list[DiversionMark]:
        return await self._marks.list_marks()

    async def persist_diversion_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> DiversionMark:
        code, kind, pointer = parse_diversion_mark_row(
            mark_code,
            stance_kind,
            source_ref,
        )
        row = DiversionMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            stance_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
