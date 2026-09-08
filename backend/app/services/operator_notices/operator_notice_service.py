from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.operator_notice import (
    notice_after_read,
    operator_notice_manual_kind,
    operator_notice_unread_status,
    require_notice_body,
    require_notice_kind,
    require_notice_source_ref,
)
from app.models.operator_notice import OperatorNotice
from app.repositories.operator_notices.operator_notice_repository import (
    OperatorNoticeRepository,
)


class OperatorNoticeService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OperatorNoticeRepository(session)

    async def list_notices(self) -> list[OperatorNotice]:
        return await self._rows.list_all()

    async def get_notice(self, notice_id: UUID) -> OperatorNotice:
        found = await self._rows.get(notice_id)
        if found is None:
            raise ResourceNotFound(f"nieznane powiadomienie: {notice_id}")
        return found

    async def create_notice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        body: str,
        source_ref: str,
        kind: object = None,
    ) -> OperatorNotice:
        token = (
            operator_notice_manual_kind() if kind is None else require_notice_kind(kind)
        )
        row = OperatorNotice(
            id=uuid4(),
            organization_id=organization_id,
            kind=token,
            body=require_notice_body(body),
            status=operator_notice_unread_status(),
            source_ref=require_notice_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)

    async def mark_read(self, notice_id: UUID) -> OperatorNotice:
        row = await self.get_notice(notice_id)
        if row.status == notice_after_read(row.status) and row.read_at is not None:
            return row
        row.status = notice_after_read(row.status)
        row.read_at = datetime.now(UTC)
        return await self._rows.save(row)
