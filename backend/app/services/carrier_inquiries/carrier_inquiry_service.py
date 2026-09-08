from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.carrier_inquiry import (
    carrier_inquiry_draft_status,
    carrier_inquiry_manual_source,
    require_answered_quote,
    require_inquiry_port_id,
    require_inquiry_status,
    require_member_batch,
    require_network_member_id,
)
from app.domain.errors import UnknownNetworkMember, UnknownPort
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
        status: object = None,
        origin_port_id: object = None,
        destination_port_id: object = None,
        quoted_amount: object = None,
        quoted_currency: object = None,
        quoted_transit_days: object = None,
    ) -> CarrierInquiry:
        token = require_inquiry_status(
            carrier_inquiry_draft_status() if status is None else status,
        )
        money, iso, days = require_answered_quote(
            status=token,
            quoted_amount=quoted_amount,
            quoted_currency=quoted_currency,
            quoted_transit_days=quoted_transit_days,
        )
        row = _new_inquiry(
            organization_id=organization_id,
            user_id=user_id,
            network_member_id=require_network_member_id(network_member_id),
            status=token,
            origin_port_id=require_inquiry_port_id(origin_port_id, field="origin_port_id"),
            destination_port_id=require_inquiry_port_id(
                destination_port_id,
                field="destination_port_id",
            ),
            quoted_amount=money,
            quoted_currency=iso,
            quoted_transit_days=days,
        )
        return await self._insert(row)

    async def record_batch(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        network_member_ids: object,
        status: object = None,
        origin_port_id: object = None,
        destination_port_id: object = None,
        quoted_amount: object = None,
        quoted_currency: object = None,
        quoted_transit_days: object = None,
    ) -> list[CarrierInquiry]:
        rows: list[CarrierInquiry] = []
        for member_id in require_member_batch(network_member_ids):
            rows.append(
                await self.record_inquiry(
                    organization_id=organization_id,
                    user_id=user_id,
                    network_member_id=member_id,
                    status=status,
                    origin_port_id=origin_port_id,
                    destination_port_id=destination_port_id,
                    quoted_amount=quoted_amount,
                    quoted_currency=quoted_currency,
                    quoted_transit_days=quoted_transit_days,
                ),
            )
        return rows

    async def _insert(self, row: CarrierInquiry) -> CarrierInquiry:
        try:
            return await self._inquiries.add(row)
        except IntegrityError as orig:
            detail = str(orig.orig) if orig.orig is not None else str(orig)
            if "fk_carrier_inquiry_network_member" in detail:
                raise UnknownNetworkMember("nieznany członek sieci") from orig
            if "fk_carrier_inquiry_origin_port" in detail:
                raise UnknownPort("nieznany port załadunku") from orig
            if "fk_carrier_inquiry_destination_port" in detail:
                raise UnknownPort("nieznany port wyładunku") from orig
            raise


def _new_inquiry(
    *,
    organization_id: UUID,
    user_id: UUID,
    network_member_id: UUID,
    status: str,
    origin_port_id: UUID | None,
    destination_port_id: UUID | None,
    quoted_amount: Decimal | None,
    quoted_currency: str | None,
    quoted_transit_days: int | None,
) -> CarrierInquiry:
    return CarrierInquiry(
        id=uuid4(),
        organization_id=organization_id,
        network_member_id=network_member_id,
        source_ref=carrier_inquiry_manual_source(),
        status=status,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        quoted_amount=quoted_amount,
        quoted_currency=quoted_currency,
        quoted_transit_days=quoted_transit_days,
        created_by=user_id,
    )
