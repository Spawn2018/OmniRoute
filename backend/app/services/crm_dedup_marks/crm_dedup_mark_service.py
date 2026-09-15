from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.crm_dedup_mark import parse_crm_dedup_mark_row
from app.models.crm_dedup_mark import CrmDedupMark
from app.repositories.crm_dedup_marks.crm_dedup_mark_repository import (
    CrmDedupMarkRepository,
)


class CrmDedupMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CrmDedupMarkRepository(session)

    async def list_marks(self) -> list[CrmDedupMark]:
        return await self._rows.list_marks()

    async def persist_crm_dedup_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        dedup_kind: object,
        source_ref: object,
    ) -> CrmDedupMark:
        code, kind, origin = parse_crm_dedup_mark_row(
            mark_code,
            dedup_kind,
            source_ref,
        )
        row = CrmDedupMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            dedup_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
