from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.edi_message import (
    require_edi_kind,
    require_edi_shipment_id,
    require_edi_source_ref,
)
from app.models.edi_message import EdiMessage
from app.repositories.edi_messages.edi_message_repository import EdiMessageRepository


class EdiMessageService:
    def __init__(self, session: AsyncSession) -> None:
        self._messages = EdiMessageRepository(session)

    async def list_messages(self) -> list[EdiMessage]:
        return await self._messages.list_all()

    async def record_message(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        message_kind: str,
        source_ref: str,
    ) -> EdiMessage:
        row = EdiMessage(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_edi_shipment_id(shipment_id),
            message_kind=require_edi_kind(message_kind),
            source_ref=require_edi_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._messages.add(row)
