from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.container import Container
from app.services.containers.container_service import ContainerService, _WriteBox
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
    superseded_by: UUID | None


def _as_response(row: Container) -> ContainerResponse:
    return ContainerResponse.model_validate(row)


def _write_from_body(body: ContainerCreate, shipment_id: UUID | None) -> _WriteBox:
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
    )


async def _bound_shipment(session: AsyncSession, shipment_id: UUID | None) -> UUID | None:
    if shipment_id is None:
        return None
    row = await ShipmentService(session).get_shipment(shipment_id)
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
    row = await ContainerService(session).record_container(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        write=_write_from_body(body, shipment_id),
    )
    await session.commit()
    return _as_response(row)
