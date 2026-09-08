from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ocean_bill import OceanBill
from app.services.ocean_bills.ocean_bill_service import OceanBillService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/ocean-bills", tags=["ocean-bills"])

_PERM = "can_manage_ocean_bills"


class OceanBillCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    bill_no: str
    bill_kind: str
    source_ref: str


class OceanBillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    bill_no: str
    bill_kind: str
    source_ref: str


def _as_row(row: OceanBill) -> OceanBillResponse:
    return OceanBillResponse.model_validate(row)


@router.get("", response_model=list[OceanBillResponse])
async def list_ocean_bills(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OceanBillResponse]:
    rows = await OceanBillService(session).list_bills()
    return [_as_row(row) for row in rows]


@router.post("", response_model=OceanBillResponse, status_code=status.HTTP_201_CREATED)
async def create_ocean_bill(
    body: OceanBillCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OceanBillResponse:
    order = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await OceanBillService(session).record_bill(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=order.id,
        bill_no=body.bill_no,
        bill_kind=body.bill_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
