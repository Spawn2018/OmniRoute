from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.clause_notice import parse_clause_notice_row
from app.models.clause_notice import ClauseNotice
from app.repositories.clause_notices.clause_notice_repository import (
    ClauseNoticeRepository,
)


class ClauseNoticeService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ClauseNoticeRepository(session)

    async def list_notices(self) -> list[ClauseNotice]:
        return await self._rows.list_notices()

    async def persist_clause_notice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        notice_code: object,
        clause_label: object,
        source_ref: object,
    ) -> ClauseNotice:
        code, label, origin = parse_clause_notice_row(
            notice_code, clause_label, source_ref
        )
        row = ClauseNotice(
            id=uuid4(),
            organization_id=organization_id,
            notice_code=code,
            clause_label=label,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_notice(row)
