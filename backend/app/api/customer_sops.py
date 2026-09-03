from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.customer_sop import CustomerSop
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/customer-sops", tags=["customer-sops"])

_PARTIES = require_permission("can_manage_parties", "organization")


class CustomerSopCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    code: str = Field(min_length=1, max_length=32)
    title: str = Field(min_length=1, max_length=128)
    body: str = Field(min_length=1, max_length=8000)
    blocks_auto: bool = True


class CustomerSopAutoBlock(BaseModel):
    party_id: UUID
    blocks_auto: bool


class CustomerSopResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    code: str
    title: str
    body: str
    status: str
    approved_at: datetime | None
    blocks_auto: bool
    source_ref: str

    @classmethod
    def from_row(cls, row: CustomerSop) -> "CustomerSopResponse":
        return cls.model_validate(row)


@router.get("", response_model=list[CustomerSopResponse])
async def list_customer_sops(
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CustomerSopResponse]:
    service = PartyService(session)
    rows = await service.list_sops()
    return [CustomerSopResponse.from_row(row) for row in rows]


@router.get("/resolve", response_model=CustomerSopResponse)
async def resolve_customer_sop(
    party_id: UUID = Query(...),
    code: str = Query(..., min_length=1, max_length=32),
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> CustomerSopResponse:
    service = PartyService(session)
    row = await service.resolve_sop(party_id, code)
    return CustomerSopResponse.from_row(row)


@router.post("", response_model=CustomerSopResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_sop(
    body: CustomerSopCreate,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CustomerSopResponse:
    service = PartyService(session)
    row = await service.create_sop(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=body.party_id,
        code=body.code,
        title=body.title,
        body=body.body,
        blocks_auto=body.blocks_auto,
    )
    await session.commit()
    return CustomerSopResponse.from_row(row)


@router.get("/auto-block", response_model=CustomerSopAutoBlock)
async def customer_sop_auto_block(
    party_id: UUID = Query(...),
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> CustomerSopAutoBlock:
    blocked = await PartyService(session).party_blocks_auto(party_id)
    return CustomerSopAutoBlock(party_id=party_id, blocks_auto=blocked)


@router.post("/{sop_id}/approve", response_model=CustomerSopResponse)
async def approve_customer_sop(
    sop_id: UUID,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> CustomerSopResponse:
    service = PartyService(session)
    row = await service.approve_sop(sop_id)
    await session.commit()
    return CustomerSopResponse.from_row(row)
