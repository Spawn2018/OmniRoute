from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidMailDraft, ResourceNotFound
from app.domain.mail_draft import (
    mail_draft_extract_kind,
    mail_draft_sent_status,
    mail_draft_status,
    require_mail_draft_body,
    require_mail_draft_source_ref,
    require_mail_draft_subject_id,
    require_mail_draft_subject_ids,
    require_mail_draft_subject_kind,
    require_mail_draft_to_address,
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
        subject_kind: object = None,
    ) -> MailDraft:
        kind = mail_draft_extract_kind() if subject_kind is None else subject_kind
        row = MailDraft(
            id=uuid4(),
            organization_id=organization_id,
            subject_kind=require_mail_draft_subject_kind(kind),
            subject_id=require_mail_draft_subject_id(subject_id),
            body=require_mail_draft_body(body),
            status=mail_draft_status(),
            source_ref=require_mail_draft_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)

    async def create_batch(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_ids: object,
        body: str,
        source_ref: str,
        subject_kind: object,
    ) -> list[MailDraft]:
        kind = require_mail_draft_subject_kind(subject_kind)
        token_body = require_mail_draft_body(body)
        token_ref = require_mail_draft_source_ref(source_ref)
        rows = [
            MailDraft(
                id=uuid4(),
                organization_id=organization_id,
                subject_kind=kind,
                subject_id=subject_id,
                body=token_body,
                status=mail_draft_status(),
                source_ref=token_ref,
                created_by=user_id,
            )
            for subject_id in require_mail_draft_subject_ids(subject_ids)
        ]
        return await self._rows.add_many(rows)

    async def mark_sent(self, draft_id: UUID, to_address: str) -> MailDraft:
        row = await self.get_draft(draft_id)
        if row.status == mail_draft_sent_status():
            raise InvalidMailDraft("szkic już wysłany")
        row.to_address = require_mail_draft_to_address(to_address)
        row.status = mail_draft_sent_status()
        return await self._rows.add(row)
