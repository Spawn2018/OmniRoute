from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.api.shipments import ShipmentResponse
from app.core.session_token import SessionIdentity
from app.domain.routing_guide_gate import (
    assert_asn_labels_on_routing_guide,
    assert_asn_on_routing_guide,
)
from app.domain.shipment import require_party_on_quotation
from app.models.asn import Asn
from app.services.purchase_orders.asn_service import AsnService
from app.services.quotations.quotation_service import QuotationService
from app.services.routing_guide_enforcements.routing_guide_enforcement_service import (
    RoutingGuideEnforcementService,
)
from app.services.routing_guide_matches.routing_guide_match_service import (
    RoutingGuideMatchService,
)
from app.services.routing_guides.routing_guide_service import RoutingGuideService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/asns", tags=["asns"])

_PERM = "can_manage_purchase_orders"


class AsnCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    purchase_order_id: UUID
    asn_code: str
    plant_label: str | None = None
    carrier_label: str | None = None
    ship_ref_label: str | None = None
    guide_code: str | None = None
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
    guide_code: str | None
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
        guide_code=saved.guide_code,
        source_ref=saved.source_ref,
    )


async def _enforce_guide_if_blocking(
    session: AsyncSession,
    *,
    guide_code: str | None,
    plant_label: str | None,
    carrier_label: str | None,
) -> None:
    kinds = {
        row.enforcement_kind
        for row in await RoutingGuideEnforcementService(session).list_marks()
    }
    guides = await RoutingGuideService(session).list_guides()
    codes = {row.guide_code for row in guides}
    token = guide_code.strip() if type(guide_code) is str else guide_code
    if type(token) is str and not token:
        token = None
    assert_asn_on_routing_guide(
        guide_code=token,
        enforcement_kinds=kinds,
        known_guide_codes=codes,
    )
    match_kinds = {
        row.match_kind
        for row in await RoutingGuideMatchService(session).list_marks()
    }
    assert_asn_labels_on_routing_guide(
        guide_code=token,
        enforcement_kinds=kinds,
        match_kinds=match_kinds,
        plant_label=plant_label,
        carrier_label=carrier_label,
        guide_lane_by_code={row.guide_code: row.lane_label for row in guides},
        guide_mode_by_code={row.guide_code: row.mode_label for row in guides},
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
    await _enforce_guide_if_blocking(
        session,
        guide_code=body.guide_code,
        plant_label=body.plant_label,
        carrier_label=body.carrier_label,
    )
    saved = await AsnService(session).persist_asn(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        purchase_order_id=body.purchase_order_id,
        asn_code=body.asn_code,
        plant_label=body.plant_label,
        carrier_label=body.carrier_label,
        ship_ref_label=body.ship_ref_label,
        guide_code=body.guide_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _notice(saved)


class AsnPromote(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    source_ref: str = "tenant:manual"


@router.post(
    "/{asn_id}/promote",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def promote_asn_to_shipment(
    asn_id: UUID,
    body: AsnPromote,
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentResponse:
    notice = await AsnService(session).get_notice(asn_id)
    await _enforce_guide_if_blocking(
        session,
        guide_code=notice.guide_code,
        plant_label=notice.plant_label,
        carrier_label=notice.carrier_label,
    )
    quote = await QuotationService(session).get_quotation(body.quotation_id)
    row = await ShipmentService(session).create_shipment(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=quote.id,
        party_id=require_party_on_quotation(quote.party_id),
        source_ref=body.source_ref,
        guide_code=notice.guide_code,
        plant_label=notice.plant_label,
        carrier_label=notice.carrier_label,
        asn_id=notice.id,
    )
    await session.commit()
    return ShipmentResponse.model_validate(row)
