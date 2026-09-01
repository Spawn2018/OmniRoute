from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.geography.location_service import LocationService

router = APIRouter(prefix="/locations", tags=["locations"])

_GEOGRAPHY = require_permission("can_manage_geography", "organization")


class ZoneCreate(BaseModel):
    code: str = Field(min_length=2, max_length=32)
    name: str = Field(min_length=1, max_length=128)


class ZoneMemberCreate(BaseModel):
    country_code: str = Field(min_length=2, max_length=2)
    postal_from: str = Field(min_length=2, max_length=16)
    postal_to: str = Field(min_length=2, max_length=16)


class LocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    kind: str
    name: str
    code: str | None
    port_id: UUID | None
    country_code: str | None
    city: str | None
    address_line: str | None
    postal_code: str | None
    lat: Decimal | None
    lng: Decimal | None
    source_ref: str


class ZoneMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    zone_location_id: UUID
    country_code: str
    postal_from: str
    postal_to: str
    source_ref: str


@router.get("", response_model=list[LocationResponse])
async def list_locations(
    kind: str | None = Query(default=None, max_length=16),
    search: str | None = Query(default=None, max_length=128),
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LocationResponse]:
    rows = await LocationService(session).list_locations(kind=kind, search=search)
    return [LocationResponse.model_validate(row) for row in rows]


@router.get("/resolve", response_model=LocationResponse)
async def resolve_postal_code(
    country_code: str = Query(..., min_length=2, max_length=2),
    postal_code: str = Query(..., min_length=2, max_length=16),
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> LocationResponse:
    row = await LocationService(session).resolve_postal(
        country_code=country_code,
        postal_code=postal_code,
    )
    return LocationResponse.model_validate(row)


@router.post("", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_zone(
    body: ZoneCreate,
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LocationResponse:
    row = await LocationService(session).create_zone(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        code=body.code,
        name=body.name,
    )
    await session.commit()
    return LocationResponse.model_validate(row)


@router.get("/{zone_id}/members", response_model=list[ZoneMemberResponse])
async def list_zone_members(
    zone_id: UUID,
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ZoneMemberResponse]:
    rows = await LocationService(session).list_zone_members(zone_id)
    return [ZoneMemberResponse.model_validate(row) for row in rows]


@router.post(
    "/{zone_id}/members",
    response_model=ZoneMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_zone_member(
    zone_id: UUID,
    body: ZoneMemberCreate,
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ZoneMemberResponse:
    row = await LocationService(session).add_zone_member(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        zone_id=zone_id,
        country_code=body.country_code,
        postal_from=body.postal_from,
        postal_to=body.postal_to,
    )
    await session.commit()
    return ZoneMemberResponse.model_validate(row)
