from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.commodity_codes.commodity_code_service import CommodityCodeService

router = APIRouter(prefix="/commodity-codes", tags=["commodity-codes"])


class CommodityCodeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=1, max_length=128)
    aliases: list[str] = Field(default_factory=list)


class CommodityCodeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    name: str
    aliases: list[str]
    source_ref: str


@router.get("", response_model=list[CommodityCodeResponse])
async def list_commodity_codes(
    _authz: None = Depends(require_permission("can_manage_commodity_codes", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CommodityCodeResponse]:
    service = CommodityCodeService(session)
    rows = await service.list_codes()
    return [CommodityCodeResponse.model_validate(row) for row in rows]


@router.get("/resolve", response_model=CommodityCodeResponse)
async def resolve_commodity_code(
    token: str = Query(..., min_length=1, max_length=10),
    _authz: None = Depends(require_permission("can_manage_commodity_codes", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> CommodityCodeResponse:
    service = CommodityCodeService(session)
    row = await service.resolve(token)
    return CommodityCodeResponse.model_validate(row)


@router.post("", response_model=CommodityCodeResponse, status_code=status.HTTP_201_CREATED)
async def create_commodity_code(
    body: CommodityCodeCreate,
    _authz: None = Depends(require_permission("can_manage_commodity_codes", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CommodityCodeResponse:
    service = CommodityCodeService(session)
    row = await service.create_code(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        code=body.code,
        name=body.name,
        aliases=body.aliases,
    )
    await session.commit()
    return CommodityCodeResponse.model_validate(row)
