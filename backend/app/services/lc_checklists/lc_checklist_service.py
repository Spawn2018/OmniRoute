from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.lc_checklist import parse_lc_checklist_row
from app.models.lc_checklist import LcChecklist
from app.repositories.lc_checklists.lc_checklist_repository import LcChecklistRepository


class LcChecklistService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LcChecklistRepository(session)

    async def list_checklists(self) -> list[LcChecklist]:
        return await self._rows.list_checklists()

    async def persist_lc_checklist(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        checklist_code: object,
        status_kind: object,
        source_ref: object,
    ) -> LcChecklist:
        code, kind, origin = parse_lc_checklist_row(
            checklist_code,
            status_kind,
            source_ref,
        )
        row = LcChecklist(
            id=uuid4(),
            organization_id=organization_id,
            checklist_code=code,
            status_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_checklist(row)
