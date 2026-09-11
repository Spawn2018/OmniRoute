from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.asn import Asn
from app.services.purchase_orders.asn_service import AsnService

router = APIRouter(prefix="/asns", tags=["asns"])

_PERM = "can_manage_purchase_orders"


class AsnCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    purchase_order_id: UUID
    asn_code: str
    plant_label: str | None = None
    carrier_label: str | None = None
    ship_ref_label: str | None = None
    source_ref: str


class AsnResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    purchase_order_id: UUID
    asn_code: str
    plant_label: str | None
    carrier_label: str | None
    ship_ref_label: str | None
    source_ref: str


def _notice(saved: Asn) -> AsnResponse:
    return AsnResponse(
        id=saved.id,
        organization_id=saved.organization_id,
        purchase_order_id=saved.purchase_order_id,
        asn_code=saved.asn_code,
        plant_label=saved.plant_label,
        carrier_label=saved.carrier_label,
        ship_ref_label=saved.ship_ref_label,
        source_ref=saved.source_ref,
    )


@router.get("", response_model=list[AsnResponse])
async def list_asns(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AsnResponse]:
    packed = await AsnService(session).list_notices()
    return [_notice(item) for item in packed]


@router.post("", response_model=AsnResponse, status_code=status.HTTP_201_CREATED)
async def create_asn(
    body: AsnCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AsnResponse:
    saved = await AsnService(session).persist_asn(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        purchase_order_id=body.purchase_order_id,
        asn_code=body.asn_code,
        plant_label=body.plant_label,
        carrier_label=body.carrier_label,
        ship_ref_label=body.ship_ref_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _notice(saved)
