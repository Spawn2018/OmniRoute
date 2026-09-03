from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.cargo_claims.cargo_claim_service import CargoClaimService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/cargo-claims", tags=["cargo-claims"])


class CargoClaimCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    claim_kind: str
    source_ref: str


class CargoClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    claim_kind: str
    source_ref: str


@router.get("", response_model=list[CargoClaimResponse])
async def list_cargo_claims(
    _authz: None = Depends(require_permission("can_manage_cargo_claims", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CargoClaimResponse]:
    rows = await CargoClaimService(session).list_claims()
    return [CargoClaimResponse.model_validate(row) for row in rows]


@router.post("", response_model=CargoClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_cargo_claim(
    body: CargoClaimCreate,
    _authz: None = Depends(require_permission("can_manage_cargo_claims", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CargoClaimResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await CargoClaimService(session).record_claim(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        claim_kind=body.claim_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return CargoClaimResponse.model_validate(row)
