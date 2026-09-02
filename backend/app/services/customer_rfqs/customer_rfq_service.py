from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer_rfq import (
    customer_rfq_draft_status,
    require_inbound_message_id,
    require_rfq_source_ref,
)
from app.domain.errors import CustomerRfqConflict
from app.models.customer_rfq import CustomerRfq
from app.repositories.customer_rfqs.customer_rfq_repository import CustomerRfqRepository


class CustomerRfqService:
    def __init__(self, session: AsyncSession) -> None:
        self._rfqs = CustomerRfqRepository(session)

    async def list_rfqs(self) -> list[CustomerRfq]:
        return await self._rfqs.list_all()

    async def create_rfq(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        inbound_message_id: UUID,
        source_ref: str,
        party_id: UUID | None,
    ) -> CustomerRfq:
        row = CustomerRfq(
            id=uuid4(),
            organization_id=organization_id,
            inbound_message_id=require_inbound_message_id(inbound_message_id),
            source_ref=require_rfq_source_ref(source_ref),
            status=customer_rfq_draft_status(),
            party_id=party_id,
            created_by=user_id,
        )
        try:
            return await self._rfqs.add(row)
        except IntegrityError as orig:
            detail = str(orig.orig) if orig.orig is not None else str(orig)
            if "uq_customer_rfq_org_message" in detail:
                raise CustomerRfqConflict(
                    "to zapytanie już istnieje dla tej wiadomości",
                ) from orig
            raise
