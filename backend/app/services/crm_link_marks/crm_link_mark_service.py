from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.crm_link_mark import parse_crm_link_mark_row
from app.models.crm_link_mark import CrmLinkMark
from app.repositories.crm_link_marks.crm_link_mark_repository import (
    CrmLinkMarkRepository,
)


class CrmLinkMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CrmLinkMarkRepository(session)

    async def list_marks(self) -> list[CrmLinkMark]:
        return await self._rows.list_marks()

    async def persist_crm_link_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        link_kind: object,
        source_ref: object,
    ) -> CrmLinkMark:
        code, kind, origin = parse_crm_link_mark_row(
            mark_code,
            link_kind,
            source_ref,
        )
        row = CrmLinkMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            link_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
