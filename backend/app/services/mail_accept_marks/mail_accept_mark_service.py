from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.mail_accept_mark import parse_mail_accept_mark_row
from app.models.mail_accept_mark import MailAcceptMark
from app.repositories.mail_accept_marks.mail_accept_mark_repository import (
    MailAcceptMarkRepository,
)


class MailAcceptMarkService:
    """HITL katalog Terms AI — bez terms live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = MailAcceptMarkRepository(session)

    async def list_marks(self) -> list[MailAcceptMark]:
        return await self._marks.list_marks()

    async def persist_mail_accept_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        accept_kind: object,
        source_ref: object,
    ) -> MailAcceptMark:
        code, kind, pointer = parse_mail_accept_mark_row(
            mark_code,
            accept_kind,
            source_ref,
        )
        row = MailAcceptMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            accept_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
