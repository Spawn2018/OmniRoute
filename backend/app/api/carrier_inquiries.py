from datetime import date
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.carrier_inquiry import InquiryMemberRank
from app.models.carrier_inquiry import CarrierInquiry
from app.services.carrier_inquiries.carrier_inquiry_service import CarrierInquiryService
from app.services.entity_events.entity_event_service import EntityEventService

router = APIRouter(prefix="/carrier-inquiries", tags=["carrier-inquiries"])

_AUTHZ = require_permission("can_manage_networks", "organization")


class CarrierInquiryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    network_member_id: UUID
    status: str | None = None
    origin_port_id: UUID | None = None
    destination_port_id: UUID | None = None
    quoted_amount: str | None = None
    quoted_currency: str | None = None
    quoted_transit_days: int | None = None
    no_reply_after: date | None = None


class CarrierInquiryBatchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    network_member_ids: list[UUID]
    status: str | None = None
    origin_port_id: UUID | None = None
    destination_port_id: UUID | None = None
    quoted_amount: str | None = None
    quoted_currency: str | None = None
    quoted_transit_days: int | None = None
    no_reply_after: date | None = None


class CarrierInquiryDatePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    no_reply_after: date | None = None


class InquiryMemberRankResponse(BaseModel):
    network_member_id: UUID
    answered_count: int

    @classmethod
    def from_row(cls, row: InquiryMemberRank) -> "InquiryMemberRankResponse":
        return cls(
            network_member_id=row.network_member_id,
            answered_count=row.answered_count,
        )


class CarrierInquiryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    network_member_id: UUID
    source_ref: str
    status: str
    origin_port_id: UUID | None
    destination_port_id: UUID | None
    quoted_amount: str | None
    quoted_currency: str | None
    quoted_transit_days: int | None
    no_reply_after: date | None

    @classmethod
    def from_row(cls, row: CarrierInquiry) -> "CarrierInquiryResponse":
        money = row.quoted_amount
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            network_member_id=row.network_member_id,
            source_ref=row.source_ref,
            status=row.status,
            origin_port_id=row.origin_port_id,
            destination_port_id=row.destination_port_id,
            quoted_amount=format(money, "f") if isinstance(money, Decimal) else None,
            quoted_currency=row.quoted_currency,
            quoted_transit_days=row.quoted_transit_days,
            no_reply_after=row.no_reply_after,
        )


async def _append_queued_event(
    session: AsyncSession,
    identity: SessionIdentity,
    row: CarrierInquiry,
) -> None:
    if row.status != "queued":
        return
    await EntityEventService(session).create_event(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_kind="carrier_inquiry",
        subject_id=row.id,
        event_kind="inquiry_queued",
        source_ref=row.source_ref,
        occurred_at=None,
    )


@router.get("", response_model=list[CarrierInquiryResponse])
async def list_carrier_inquiries(
    silent: str | None = Query(default=None),
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CarrierInquiryResponse]:
    rows = await CarrierInquiryService(session).list_inquiries(silent=silent)
    return [CarrierInquiryResponse.from_row(row) for row in rows]


@router.get("/ranking", response_model=list[InquiryMemberRankResponse])
async def list_carrier_inquiry_ranking(
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InquiryMemberRankResponse]:
    rows = await CarrierInquiryService(session).list_member_ranks()
    return [InquiryMemberRankResponse.from_row(row) for row in rows]


@router.post("", response_model=CarrierInquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_carrier_inquiry(
    body: CarrierInquiryCreate,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CarrierInquiryResponse:
    row = await CarrierInquiryService(session).record_inquiry(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        network_member_id=body.network_member_id,
        status=body.status,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        quoted_amount=body.quoted_amount,
        quoted_currency=body.quoted_currency,
        quoted_transit_days=body.quoted_transit_days,
        no_reply_after=body.no_reply_after,
    )
    await _append_queued_event(session, identity, row)
    await session.commit()
    return CarrierInquiryResponse.from_row(row)


@router.patch("/{inquiry_id}", response_model=CarrierInquiryResponse)
async def patch_carrier_inquiry_silence(
    inquiry_id: UUID,
    body: CarrierInquiryDatePatch,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> CarrierInquiryResponse:
    row = await CarrierInquiryService(session).set_no_reply_after(
        inquiry_id,
        body.no_reply_after,
    )
    await session.commit()
    return CarrierInquiryResponse.from_row(row)


@router.post(
    "/batch",
    response_model=list[CarrierInquiryResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_carrier_inquiry_batch(
    body: CarrierInquiryBatchCreate,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> list[CarrierInquiryResponse]:
    rows = await CarrierInquiryService(session).record_batch(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        network_member_ids=body.network_member_ids,
        status=body.status,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        quoted_amount=body.quoted_amount,
        quoted_currency=body.quoted_currency,
        quoted_transit_days=body.quoted_transit_days,
        no_reply_after=body.no_reply_after,
    )
    await session.commit()
    return [CarrierInquiryResponse.from_row(row) for row in rows]
