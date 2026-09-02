from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.inbound_message import (
    inbound_draft_status,
    require_body_text,
    require_from_address,
    require_inbound_source_ref,
    require_subject,
)
from app.models.inbound_message import InboundMessage
from app.repositories.inbound_messages.inbound_message_repository import (
    InboundMessageRepository,
)


class InboundMessageService:
    def __init__(self, session: AsyncSession) -> None:
        self._messages = InboundMessageRepository(session)

    async def list_messages(self) -> list[InboundMessage]:
        return await self._messages.list_all()

    async def create_message(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_ref: str,
        from_address: str,
        subject: str,
        body_text: str,
    ) -> InboundMessage:
        row = InboundMessage(
            id=uuid4(),
            organization_id=organization_id,
            source_ref=require_inbound_source_ref(source_ref),
            from_address=require_from_address(from_address),
            subject=require_subject(subject),
            body_text=require_body_text(body_text),
            status=inbound_draft_status(),
            created_by=user_id,
        )
        return await self._messages.add(row)
