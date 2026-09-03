from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.carrier_inquiry import (
    carrier_inquiry_draft_status,
    carrier_inquiry_manual_source,
    require_network_member_id,
)
from app.domain.errors import UnknownNetworkMember
from app.models.carrier_inquiry import CarrierInquiry
from app.repositories.carrier_inquiries.carrier_inquiry_repository import (
    CarrierInquiryRepository,
)


class CarrierInquiryService:
    def __init__(self, session: AsyncSession) -> None:
        self._inquiries = CarrierInquiryRepository(session)

    async def list_inquiries(self) -> list[CarrierInquiry]:
        return await self._inquiries.list_recent()

    async def record_inquiry(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        network_member_id: UUID,
    ) -> CarrierInquiry:
        row = CarrierInquiry(
            id=uuid4(),
            organization_id=organization_id,
            network_member_id=require_network_member_id(network_member_id),
            source_ref=carrier_inquiry_manual_source(),
            status=carrier_inquiry_draft_status(),
            created_by=user_id,
        )
        try:
            return await self._inquiries.add(row)
        except IntegrityError as orig:
            detail = str(orig.orig) if orig.orig is not None else str(orig)
            if "fk_carrier_inquiry_network_member" in detail:
                raise UnknownNetworkMember("nieznany członek sieci") from orig
            raise
