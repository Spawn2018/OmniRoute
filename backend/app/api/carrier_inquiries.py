from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.carrier_inquiries.carrier_inquiry_service import CarrierInquiryService

router = APIRouter(prefix="/carrier-inquiries", tags=["carrier-inquiries"])


class CarrierInquiryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    network_member_id: UUID


class CarrierInquiryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    network_member_id: UUID
    source_ref: str
    status: str


@router.get("", response_model=list[CarrierInquiryResponse])
async def list_carrier_inquiries(
    _authz: None = Depends(require_permission("can_manage_networks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CarrierInquiryResponse]:
    rows = await CarrierInquiryService(session).list_inquiries()
    return [CarrierInquiryResponse.model_validate(row) for row in rows]


@router.post("", response_model=CarrierInquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_carrier_inquiry(
    body: CarrierInquiryCreate,
    _authz: None = Depends(require_permission("can_manage_networks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CarrierInquiryResponse:
    row = await CarrierInquiryService(session).record_inquiry(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        network_member_id=body.network_member_id,
    )
    await session.commit()
    return CarrierInquiryResponse.model_validate(row)
