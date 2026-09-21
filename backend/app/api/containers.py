from datetime import date, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.container import Container
from app.services.containers.container_service import ContainerService, _WriteBox
from app.services.parties.party_service import PartyService
from app.services.shipment_legs.shipment_leg_service import ShipmentLegService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/containers", tags=["containers"])

_SHIP = "can_manage_shipments"


class ContainerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    container_no: str
    iso_size_type: str
    shipment_id: UUID | None = None
    source_ref: str
    seal_no_1: str | None = None
    seal_no_2: str | None = None
    seal_no_3: str | None = None
    vessel_name: str | None = None
    voyage_no: str | None = None
    remarks: str | None = None
    cargo_description: str | None = None
    packaging_code: str | None = None
    grade: object | None = None
    ref_1: str | None = None
    ref_2: str | None = None
    ref_3: str | None = None
    ref_4: str | None = None
    ref_5: str | None = None
    reefer: object = False
    pickup_terminal: str | None = None
    return_terminal: str | None = None
    bl_kind: str | None = None
    free_time_origin_h: object | None = None
    free_time_dest_h: object | None = None
    demurrage_free_days: object | None = None
    detention_free_days: object | None = None
    mixed_dd_days: object | None = None
    si_cutoff_at: object | None = None
    ams_cutoff_at: object | None = None
    cy_cutoff_at: object | None = None
    cfs_cutoff_at: object | None = None
    vgm_kg: object | None = None
    tare_kg: object | None = None
    pin_code: object | None = None
    payload_kg: object | None = None
    teu: object | None = None
    quantity: object | None = None
    weight_kg: object | None = None
    volume_m3: object | None = None
    pickup_date: object | None = None
    return_date: object | None = None
    gate_in_date: object | None = None
    delivery_date: object | None = None
    unload_date: object | None = None
    temp_min: object | None = None
    temp_max: object | None = None
    needs_external_power: object = False
    vgm_method: object | None = None
    vgm_cutoff_at: object | None = None
    last_survey_at: object | None = None
    booking_no: object | None = None
    carrier_party_id: UUID | None = None
    container_release_party_id: UUID | None = None
    shipment_leg_id: UUID | None = None


class ContainerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    container_no: str
    iso_size_type: str
    shipment_id: UUID | None
    source_ref: str
    seal_no_1: str | None
    seal_no_2: str | None
    seal_no_3: str | None
    vessel_name: str | None
    voyage_no: str | None
    remarks: str | None
    cargo_description: str | None
    packaging_code: str | None
    grade: str | None
    ref_1: str | None
    ref_2: str | None
    ref_3: str | None
    ref_4: str | None
    ref_5: str | None
    reefer: bool
    pickup_terminal: str | None
    return_terminal: str | None
    bl_kind: str | None
    free_time_origin_h: int | None
    free_time_dest_h: int | None
    demurrage_free_days: int | None
    detention_free_days: int | None
    mixed_dd_days: int | None
    si_cutoff_at: datetime | None
    ams_cutoff_at: datetime | None
    cy_cutoff_at: datetime | None
    cfs_cutoff_at: datetime | None
    vgm_kg: str | None
    tare_kg: str | None
    pin_code: str | None
    payload_kg: str | None
    teu: str | None
    quantity: int | None
    weight_kg: str | None
    volume_m3: str | None
    pickup_date: date | None
    return_date: date | None
    gate_in_date: date | None
    delivery_date: date | None
    unload_date: date | None
    temp_min: str | None
    temp_max: str | None
    needs_external_power: bool
    vgm_method: str | None
    vgm_cutoff_at: datetime | None
    last_survey_at: datetime | None
    booking_no: str | None
    carrier_party_id: UUID | None
    container_release_party_id: UUID | None
    shipment_leg_id: UUID | None
    superseded_by: UUID | None


def _as_response(row: Container) -> ContainerResponse:
    dumped = {name: getattr(row, name) for name in ContainerResponse.model_fields}
    dumped["vgm_kg"] = None if row.vgm_kg is None else format(row.vgm_kg, "f")
    dumped["tare_kg"] = None if row.tare_kg is None else format(row.tare_kg, "f")
    dumped["payload_kg"] = None if row.payload_kg is None else format(row.payload_kg, "f")
    dumped["teu"] = None if row.teu is None else format(row.teu, "f")
    dumped["weight_kg"] = None if row.weight_kg is None else format(row.weight_kg, "f")
    dumped["volume_m3"] = None if row.volume_m3 is None else format(row.volume_m3, "f")
    dumped["temp_min"] = None if row.temp_min is None else format(row.temp_min, "f")
    dumped["temp_max"] = None if row.temp_max is None else format(row.temp_max, "f")
    return ContainerResponse.model_validate(dumped)


def _write_from_body(
    body: ContainerCreate,
    shipment_id: UUID | None,
    carrier_id: UUID | None,
    release_id: UUID | None,
    leg_id: UUID | None,
) -> _WriteBox:
    return _WriteBox(
        body.container_no,
        body.iso_size_type,
        shipment_id,
        body.source_ref,
        body.seal_no_1,
        body.seal_no_2,
        body.seal_no_3,
        body.vessel_name,
        body.voyage_no,
        body.remarks,
        body.cargo_description,
        body.packaging_code, body.grade,
        body.ref_1,
        body.ref_2,
        body.ref_3,
        body.ref_4,
        body.ref_5,
        body.reefer,
        body.pickup_terminal,
        body.return_terminal,
        body.bl_kind,
        body.free_time_origin_h, body.free_time_dest_h,
        body.demurrage_free_days, body.detention_free_days, body.mixed_dd_days,
        body.si_cutoff_at, body.ams_cutoff_at, body.cy_cutoff_at, body.cfs_cutoff_at,
        body.vgm_kg, body.vgm_method, body.vgm_cutoff_at, body.last_survey_at,
        body.booking_no,
        carrier_id, release_id, leg_id,
        body.tare_kg, body.pin_code, body.payload_kg, body.teu, body.quantity,
        body.weight_kg, body.volume_m3, body.pickup_date, body.return_date,
        body.gate_in_date, body.delivery_date, body.unload_date,
        body.temp_min, body.temp_max, body.needs_external_power,
    )


async def _bound_shipment(session: AsyncSession, shipment_id: UUID | None) -> UUID | None:
    if shipment_id is None:
        return None
    row = await ShipmentService(session).get_shipment(shipment_id)
    return row.id


async def _bound_carrier(session: AsyncSession, carrier_id: UUID | None) -> UUID | None:
    if carrier_id is None:
        return None
    row = await PartyService(session).get_party(carrier_id)
    return row.id


async def _bound_release(session: AsyncSession, release_id: UUID | None) -> UUID | None:
    if release_id is None:
        return None
    row = await PartyService(session).get_party(release_id)
    return row.id


async def _bound_leg(session: AsyncSession, leg_id: UUID | None) -> UUID | None:
    if leg_id is None:
        return None
    row = await ShipmentLegService(session).get_leg(leg_id)
    return row.id


@router.get("", response_model=list[ContainerResponse])
async def list_containers(
    iso_size_type: str | None = Query(default=None),
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ContainerResponse]:
    size_type = None if iso_size_type is None or iso_size_type.strip() == "" else iso_size_type
    rows = await ContainerService(session).list_containers(iso_size_type=size_type)
    return [_as_response(row) for row in rows]


@router.post("", response_model=ContainerResponse, status_code=status.HTTP_201_CREATED)
async def create_container(
    body: ContainerCreate,
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ContainerResponse:
    shipment_id = await _bound_shipment(session, body.shipment_id)
    carrier_id = await _bound_carrier(session, body.carrier_party_id)
    release_id = await _bound_release(session, body.container_release_party_id)
    leg_id = await _bound_leg(session, body.shipment_leg_id)
    row = await ContainerService(session).record_container(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        write=_write_from_body(body, shipment_id, carrier_id, release_id, leg_id),
    )
    await session.commit()
    return _as_response(row)
