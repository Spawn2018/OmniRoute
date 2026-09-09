from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.dangerous_goods.dangerous_good_service import DangerousGoodService

router = APIRouter(prefix="/dangerous-goods", tags=["dangerous-goods"])


class DangerousGoodCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    un_number: str = Field(min_length=1, max_length=6)
    imdg_class: str = Field(min_length=1, max_length=3)
    adr_tunnel_code: str = Field(min_length=1, max_length=1)
    segregation_group: str = Field(min_length=1, max_length=8)
    name: str = Field(min_length=1, max_length=128)
    aliases: list[str] = Field(default_factory=list)


class DangerousGoodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    un_number: str
    imdg_class: str
    adr_tunnel_code: str
    segregation_group: str
    name: str
    aliases: list[str]
    source_ref: str


@router.get("", response_model=list[DangerousGoodResponse])
async def list_dangerous_goods(
    _authz: None = Depends(require_permission("can_manage_dangerous_goods", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DangerousGoodResponse]:
    service = DangerousGoodService(session)
    rows = await service.list_goods()
    return [DangerousGoodResponse.model_validate(row) for row in rows]


@router.get("/resolve", response_model=DangerousGoodResponse)
async def resolve_dangerous_good(
    token: str = Query(..., min_length=1, max_length=6),
    _authz: None = Depends(require_permission("can_manage_dangerous_goods", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> DangerousGoodResponse:
    service = DangerousGoodService(session)
    row = await service.resolve(token)
    return DangerousGoodResponse.model_validate(row)


@router.post("", response_model=DangerousGoodResponse, status_code=status.HTTP_201_CREATED)
async def create_dangerous_good(
    body: DangerousGoodCreate,
    _authz: None = Depends(require_permission("can_manage_dangerous_goods", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DangerousGoodResponse:
    service = DangerousGoodService(session)
    row = await service.create_good(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        un_number=body.un_number,
        imdg_class=body.imdg_class,
        name=body.name,
        aliases=body.aliases,
        adr_tunnel_code=body.adr_tunnel_code,
        segregation_group=body.segregation_group,
    )
    await session.commit()
    return DangerousGoodResponse.model_validate(row)
