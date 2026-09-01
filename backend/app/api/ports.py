from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.geography.port_service import PortService

router = APIRouter(prefix="/ports", tags=["ports"])

_GEOGRAPHY = require_permission("can_manage_geography", "organization")


class PortCreate(BaseModel):
    unlocode: str = Field(min_length=5, max_length=8)
    name: str = Field(min_length=1, max_length=128)
    country_code: str = Field(min_length=2, max_length=2)
    lat: Decimal | None = None
    lng: Decimal | None = None
    is_seaport: bool = True
    function_flags: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)


class PortResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    unlocode: str
    name: str
    country_code: str
    lat: Decimal | None
    lng: Decimal | None
    is_seaport: bool
    function_flags: list[str]
    aliases: list[str]
    is_official: bool
    source_ref: str
    wpi_number: int | None = None
    harbor_size: str | None = None
    harbor_type: str | None = None
    shelter: str | None = None
    channel_depth_m: Decimal | None = None
    cargo_pier_depth_m: Decimal | None = None
    wpi_source_ref: str | None = None


@router.get("", response_model=list[PortResponse])
async def list_ports(
    search: str | None = Query(default=None, max_length=128),
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PortResponse]:
    rows = await PortService(session).list_ports(search)
    return [PortResponse.model_validate(row) for row in rows]


@router.get("/resolve", response_model=PortResponse)
async def resolve_port(
    token: str = Query(..., min_length=1, max_length=128),
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> PortResponse:
    row = await PortService(session).resolve(token)
    return PortResponse.model_validate(row)


@router.post("", response_model=PortResponse, status_code=status.HTTP_201_CREATED)
async def create_port(
    body: PortCreate,
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PortResponse:
    row = await PortService(session).create_manual_port(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        unlocode=body.unlocode,
        name=body.name,
        country_code=body.country_code,
        lat=body.lat,
        lng=body.lng,
        is_seaport=body.is_seaport,
        function_flags=body.function_flags,
        aliases=body.aliases,
    )
    await session.commit()
    return PortResponse.model_validate(row)
