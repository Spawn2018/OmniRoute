from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.network_member import NetworkMember
from app.services.networks.network_service import NetworkService

router = APIRouter(prefix="/networks", tags=["networks"])


class NetworkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=128)
    aliases: list[str] = Field(default_factory=list)
    website: str | None = Field(default=None, max_length=256)
    region_scope: str | None = Field(default=None, max_length=64)
    is_global: bool = False


class NetworkMemberCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    member_code: str = Field(min_length=1, max_length=32)
    legal_name: str = Field(min_length=1, max_length=128)


class NetworkMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    network_id: UUID
    member_code: str
    legal_name: str
    source_ref: str

    @classmethod
    def from_row(cls, row: NetworkMember) -> "NetworkMemberResponse":
        return cls.model_validate(row)


class NetworkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    name: str
    aliases: list[str]
    website: str | None
    region_scope: str | None
    is_global: bool
    source_ref: str


@router.get("", response_model=list[NetworkResponse])
async def list_networks(
    _authz: None = Depends(require_permission("can_manage_networks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NetworkResponse]:
    service = NetworkService(session)
    rows = await service.list_networks()
    return [NetworkResponse.model_validate(row) for row in rows]


@router.get("/resolve", response_model=NetworkResponse)
async def resolve_network(
    token: str = Query(..., min_length=1, max_length=32),
    _authz: None = Depends(require_permission("can_manage_networks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> NetworkResponse:
    service = NetworkService(session)
    row = await service.resolve(token)
    return NetworkResponse.model_validate(row)


@router.post("", response_model=NetworkResponse, status_code=status.HTTP_201_CREATED)
async def create_network(
    body: NetworkCreate,
    _authz: None = Depends(require_permission("can_manage_networks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NetworkResponse:
    service = NetworkService(session)
    row = await service.create_network(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        code=body.code,
        name=body.name,
        aliases=body.aliases,
        website=body.website,
        region_scope=body.region_scope,
        is_global=body.is_global,
    )
    await session.commit()
    return NetworkResponse.model_validate(row)


@router.get("/{network_id}/members", response_model=list[NetworkMemberResponse])
async def list_network_members(
    network_id: UUID,
    _authz: None = Depends(require_permission("can_manage_networks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NetworkMemberResponse]:
    rows = await NetworkService(session).list_members(network_id)
    return [NetworkMemberResponse.from_row(row) for row in rows]


@router.post(
    "/{network_id}/members",
    response_model=NetworkMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_network_member(
    network_id: UUID,
    body: NetworkMemberCreate,
    _authz: None = Depends(require_permission("can_manage_networks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NetworkMemberResponse:
    row = await NetworkService(session).create_member(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        network_id=network_id,
        member_code=body.member_code,
        legal_name=body.legal_name,
    )
    await session.commit()
    return NetworkMemberResponse.from_row(row)
