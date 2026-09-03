from collections.abc import Callable
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.inbound_message import (
    inbound_draft_status,
    require_body_text,
    require_external_id,
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

    async def get_message(self, message_id: UUID) -> InboundMessage:
        found = await self._messages.get(message_id)
        if found is None:
            raise ResourceNotFound(f"nieznana wiadomość: {message_id}")
        return found

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

    async def attach_party(self, message_id: UUID, party_id: UUID) -> InboundMessage:
        row = await self.get_message(message_id)
        row.party_id = party_id
        await self._messages.add(row)
        return row

    async def ingest_by_external_id(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        external_id: str,
        source_ref: str,
        from_address: str,
        subject: str,
        body_text: str,
        require_origin: Callable[[object], str],
    ) -> InboundMessage:
        token = require_external_id(external_id)
        found = await self._messages.get_by_external_id(token)
        if found is not None:
            return found
        row = InboundMessage(
            id=uuid4(),
            organization_id=organization_id,
            source_ref=require_origin(source_ref),
            from_address=require_from_address(from_address),
            subject=require_subject(subject),
            body_text=require_body_text(body_text),
            status=inbound_draft_status(),
            external_id=token,
            created_by=user_id,
        )
        return await self._messages.add(row)
