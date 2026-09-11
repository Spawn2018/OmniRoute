from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.routing_guide_gate import (
    assert_asn_labels_on_routing_guide,
    assert_asn_on_routing_guide,
)
from app.domain.shipment import require_party_on_quotation
from app.services.quotations.quotation_service import QuotationService
from app.services.routing_guide_enforcements.routing_guide_enforcement_service import (
    RoutingGuideEnforcementService,
)
from app.services.routing_guide_matches.routing_guide_match_service import (
    RoutingGuideMatchService,
)
from app.services.routing_guides.routing_guide_service import RoutingGuideService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/shipments", tags=["shipments"])


class ShipmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    source_ref: str
    shipment_ref: str | None = None
    parent_shipment_id: UUID | None = None
    relation_kind: str | None = None
    guide_code: str | None = None
    plant_label: str | None = None
    carrier_label: str | None = None


class ShipmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    quotation_id: UUID
    party_id: UUID
    source_ref: str
    shipment_ref: str | None
    parent_shipment_id: UUID | None
    relation_kind: str | None
    guide_code: str | None
    plant_label: str | None
    carrier_label: str | None
    status: str


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


@router.get("", response_model=list[ShipmentResponse])
async def list_shipments(
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentResponse]:
    rows = await ShipmentService(session).list_shipments()
    return [ShipmentResponse.model_validate(row) for row in rows]


@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    body: ShipmentCreate,
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentResponse:
    await _enforce_guide_if_blocking(
        session,
        guide_code=body.guide_code,
        plant_label=body.plant_label,
        carrier_label=body.carrier_label,
    )
    quote = await QuotationService(session).get_quotation(body.quotation_id)
    row = await ShipmentService(session).create_shipment(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=quote.id,
        party_id=require_party_on_quotation(quote.party_id),
        source_ref=body.source_ref,
        shipment_ref=body.shipment_ref,
        parent_shipment_id=body.parent_shipment_id,
        relation_kind=body.relation_kind,
        guide_code=body.guide_code,
        plant_label=body.plant_label,
        carrier_label=body.carrier_label,
    )
    await session.commit()
    return ShipmentResponse.model_validate(row)
