from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.mail_draft import (
    mail_draft_extract_kind,
    mail_draft_status,
    require_mail_draft_body,
    require_mail_draft_source_ref,
    require_mail_draft_subject_id,
)
from app.models.mail_draft import MailDraft
from app.repositories.mail_drafts.mail_draft_repository import MailDraftRepository


class MailDraftService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = MailDraftRepository(session)

    async def list_drafts(self) -> list[MailDraft]:
        return await self._rows.list_all()

    async def get_draft(self, draft_id: UUID) -> MailDraft:
        found = await self._rows.get(draft_id)
        if found is None:
            raise ResourceNotFound(f"nieznany szkic maila: {draft_id}")
        return found

    async def create_draft(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_id: UUID,
        body: str,
        source_ref: str,
    ) -> MailDraft:
        row = MailDraft(
            id=uuid4(),
            organization_id=organization_id,
            subject_kind=mail_draft_extract_kind(),
            subject_id=require_mail_draft_subject_id(subject_id),
            body=require_mail_draft_body(body),
            status=mail_draft_status(),
            source_ref=require_mail_draft_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
