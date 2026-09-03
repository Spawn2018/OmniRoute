from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.errors import InvalidShipmentLeg
from app.domain.shipment_leg import (
    require_china_rail_country,
    require_distinct_ends,
    require_leg_kind,
    require_rail_location_kind,
    require_rail_port_flag,
    require_road_location_kind,
)
from app.models.location import Location
from app.models.port import Port
from app.services.geography.location_service import LocationService
from app.services.geography.port_service import PortService
from app.services.shipment_legs.shipment_leg_service import ShipmentLegService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/shipment-legs", tags=["shipment-legs"])


class ShipmentLegCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    origin_location_id: UUID
    destination_location_id: UUID
    source_ref: str
    leg_kind: str = "road"


class ShipmentLegResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    origin_location_id: UUID
    destination_location_id: UUID
    leg_kind: str
    source_ref: str


@router.get("", response_model=list[ShipmentLegResponse])
async def list_shipment_legs(
    _authz: None = Depends(require_permission("can_manage_shipment_legs", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentLegResponse]:
    rows = await ShipmentLegService(session).list_legs()
    return [ShipmentLegResponse.model_validate(row) for row in rows]


@router.post("", response_model=ShipmentLegResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment_leg(
    body: ShipmentLegCreate,
    _authz: None = Depends(require_permission("can_manage_shipment_legs", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentLegResponse:
    kind = require_leg_kind(body.leg_kind)
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    origin, destination = await _ends_for_kind(
        session, kind, body.origin_location_id, body.destination_location_id,
    )
    row = await ShipmentLegService(session).record_leg(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        origin_location_id=origin.id,
        destination_location_id=destination.id,
        source_ref=body.source_ref,
        leg_kind=kind,
    )
    await session.commit()
    return ShipmentLegResponse.model_validate(row)


async def _ends_for_kind(
    session: AsyncSession,
    kind: str,
    origin_id: UUID,
    destination_id: UUID,
) -> tuple[Location, Location]:
    if kind == "china_rail":
        return await _china_rail_ends(session, origin_id, destination_id)
    if kind == "rail":
        return await _rail_ends(session, origin_id, destination_id)
    return await _land_ends(session, origin_id, destination_id)


async def _land_ends(
    session: AsyncSession,
    origin_id: UUID,
    destination_id: UUID,
) -> tuple[Location, Location]:
    catalog = LocationService(session)
    origin = await catalog.get_location(origin_id)
    destination = await catalog.get_location(destination_id)
    require_road_location_kind(origin.kind)
    require_road_location_kind(destination.kind)
    require_distinct_ends(origin.id, destination.id)
    return origin, destination


async def _unlocode_ends(
    session: AsyncSession,
    origin_id: UUID,
    destination_id: UUID,
) -> tuple[Location, Location]:
    catalog = LocationService(session)
    origin = await catalog.get_location(origin_id)
    destination = await catalog.get_location(destination_id)
    require_rail_location_kind(origin.kind)
    require_rail_location_kind(destination.kind)
    require_distinct_ends(origin.id, destination.id)
    return origin, destination


async def _rail_ends(
    session: AsyncSession,
    origin_id: UUID,
    destination_id: UUID,
) -> tuple[Location, Location]:
    origin, destination = await _unlocode_ends(session, origin_id, destination_id)
    await _require_rail_ports(session, origin, destination)
    return origin, destination


async def _china_rail_ends(
    session: AsyncSession,
    origin_id: UUID,
    destination_id: UUID,
) -> tuple[Location, Location]:
    origin, destination = await _unlocode_ends(session, origin_id, destination_id)
    start, end = await _require_rail_ports(session, origin, destination)
    require_china_rail_country(start.country_code)
    require_china_rail_country(end.country_code)
    return origin, destination


async def _require_rail_ports(
    session: AsyncSession,
    origin: Location,
    destination: Location,
) -> tuple[Port, Port]:
    if origin.port_id is None or destination.port_id is None:
        raise InvalidShipmentLeg("lokalizacja UN/LOCODE bez portu")
    ports = PortService(session)
    start = await ports.get_port(origin.port_id)
    end = await ports.get_port(destination.port_id)
    require_rail_port_flag(start.function_flags)
    require_rail_port_flag(end.function_flags)
    return start, end
