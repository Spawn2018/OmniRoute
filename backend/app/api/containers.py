from datetime import datetime
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
    si_cutoff_at: object | None = None
    ams_cutoff_at: object | None = None
    cy_cutoff_at: object | None = None
    cfs_cutoff_at: object | None = None
    vgm_kg: object | None = None
    vgm_method: object | None = None
    vgm_cutoff_at: object | None = None
    last_survey_at: object | None = None
    booking_no: object | None = None
    carrier_party_id: UUID | None = None
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
    si_cutoff_at: datetime | None
    ams_cutoff_at: datetime | None
    cy_cutoff_at: datetime | None
    cfs_cutoff_at: datetime | None
    vgm_kg: str | None
    vgm_method: str | None
    vgm_cutoff_at: datetime | None
    last_survey_at: datetime | None
    booking_no: str | None
    carrier_party_id: UUID | None
    shipment_leg_id: UUID | None
    superseded_by: UUID | None


def _as_response(row: Container) -> ContainerResponse:
    dumped = {name: getattr(row, name) for name in ContainerResponse.model_fields}
    dumped["vgm_kg"] = None if row.vgm_kg is None else format(row.vgm_kg, "f")
    return ContainerResponse.model_validate(dumped)


def _write_from_body(
    body: ContainerCreate, shipment_id: UUID | None, carrier_id: UUID | None, leg_id: UUID | None,
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
        body.packaging_code,
        body.ref_1,
        body.ref_2,
        body.ref_3,
        body.ref_4,
        body.ref_5,
        body.reefer,
        body.pickup_terminal,
        body.return_terminal,
        body.bl_kind,
        body.free_time_origin_h,
        body.free_time_dest_h,
        body.demurrage_free_days,
        body.si_cutoff_at,
        body.ams_cutoff_at,
        body.cy_cutoff_at,
        body.cfs_cutoff_at,
        body.vgm_kg,
        body.vgm_method,
        body.vgm_cutoff_at,
        body.last_survey_at,
        body.booking_no,
        carrier_id,
        leg_id,
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
    leg_id = await _bound_leg(session, body.shipment_leg_id)
    row = await ContainerService(session).record_container(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        write=_write_from_body(body, shipment_id, carrier_id, leg_id),
    )
    await session.commit()
    return _as_response(row)
