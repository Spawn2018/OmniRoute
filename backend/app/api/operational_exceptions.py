from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.operational_exceptions.operational_exception_service import (
    OperationalExceptionService,
)
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/operational-exceptions", tags=["operational-exceptions"])


class OperationalExceptionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    exception_kind: str
    source_ref: str


class OperationalExceptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    exception_kind: str
    source_ref: str


@router.get("", response_model=list[OperationalExceptionResponse])
async def list_operational_exceptions(
    _authz: None = Depends(require_permission("can_manage_exceptions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OperationalExceptionResponse]:
    rows = await OperationalExceptionService(session).list_exceptions()
    return [OperationalExceptionResponse.model_validate(row) for row in rows]


@router.post(
    "",
    response_model=OperationalExceptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_operational_exception(
    body: OperationalExceptionCreate,
    _authz: None = Depends(require_permission("can_manage_exceptions", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OperationalExceptionResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await OperationalExceptionService(session).record_exception(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        exception_kind=body.exception_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return OperationalExceptionResponse.model_validate(row)
