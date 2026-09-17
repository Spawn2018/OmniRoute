from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipment_monitoring_filing import ShipmentMonitoringFiling
from app.services.shipment_monitoring_filings.shipment_monitoring_filing_service import (
    ShipmentMonitoringFilingService,
)

router = APIRouter(prefix="/shipment-monitoring-filings", tags=["shipment-monitoring-filings"])

_PERM = "can_manage_shipment_monitoring_filings"


class ShipmentMonitoringFilingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filing_code: str
    status_kind: str
    source_ref: str


class ShipmentMonitoringFilingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    filing_code: str
    status_kind: str
    source_ref: str


def _row(saved: ShipmentMonitoringFiling) -> ShipmentMonitoringFilingResponse:
    return ShipmentMonitoringFilingResponse.model_validate(saved)


@router.get("", response_model=list[ShipmentMonitoringFilingResponse])
async def list_shipment_monitoring_filings(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentMonitoringFilingResponse]:
    packed = await ShipmentMonitoringFilingService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ShipmentMonitoringFilingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shipment_monitoring_filing(
    body: ShipmentMonitoringFilingCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentMonitoringFilingResponse:
    saved = await ShipmentMonitoringFilingService(session).persist_shipment_monitoring_filing(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        filing_code=body.filing_code,
        status_kind=body.status_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
