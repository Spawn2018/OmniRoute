from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.impact_node_mark import parse_impact_node_mark_row
from app.models.impact_node_mark import ImpactNodeMark
from app.repositories.impact_node_marks.impact_node_mark_repository import (
    ImpactNodeMarkRepository,
)


class ImpactNodeMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ImpactNodeMarkRepository(session)

    async def list_marks(self) -> list[ImpactNodeMark]:
        return await self._rows.list_marks()

    async def persist_impact_node_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        node_kind: object,
        source_ref: object,
    ) -> ImpactNodeMark:
        code, kind, origin = parse_impact_node_mark_row(
            mark_code,
            node_kind,
            source_ref,
        )
        row = ImpactNodeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            node_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
