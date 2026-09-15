from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.kpi_definition_mark import parse_kpi_definition_mark_row
from app.models.kpi_definition_mark import KpiDefinitionMark
from app.repositories.kpi_definition_marks.kpi_definition_mark_repository import (
    KpiDefinitionMarkRepository,
)


class KpiDefinitionMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = KpiDefinitionMarkRepository(session)

    async def list_marks(self) -> list[KpiDefinitionMark]:
        return await self._rows.list_marks()

    async def persist_kpi_definition_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        kpi_kind: object,
        source_ref: object,
    ) -> KpiDefinitionMark:
        code, kind, origin = parse_kpi_definition_mark_row(
            mark_code,
            kpi_kind,
            source_ref,
        )
        row = KpiDefinitionMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            kpi_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
