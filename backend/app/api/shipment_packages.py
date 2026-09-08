from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.shipment_package import require_stop_on_shipment
from app.models.shipment_package import ShipmentPackage
from app.services.shipment_packages.shipment_package_service import ShipmentPackageService
from app.services.shipments.shipment_service import ShipmentService
from app.services.stops.stop_service import StopService

router = APIRouter(prefix="/shipment-packages", tags=["shipment-packages"])

_PERM = "can_manage_shipment_packages"


class ShipmentPackageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    stop_id: UUID
    package_code: str
    package_status: str
    scan_token: str
    source_ref: str


class ShipmentPackageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    stop_id: UUID
    package_code: str
    package_status: str
    scan_token: str
    source_ref: str


def _as_row(row: ShipmentPackage) -> ShipmentPackageResponse:
    return ShipmentPackageResponse.model_validate(row)


@router.get("", response_model=list[ShipmentPackageResponse])
async def list_shipment_packages(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentPackageResponse]:
    rows = await ShipmentPackageService(session).list_packages()
    return [_as_row(row) for row in rows]


@router.post("", response_model=ShipmentPackageResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment_package(
    body: ShipmentPackageCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentPackageResponse:
    order = await ShipmentService(session).get_shipment(body.shipment_id)
    halt = await StopService(session).get_stop(body.stop_id)
    require_stop_on_shipment(order.id, halt.shipment_id)
    row = await ShipmentPackageService(session).record_package(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=order.id,
        stop_id=halt.id,
        package_code=body.package_code,
        package_status=body.package_status,
        scan_token=body.scan_token,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
