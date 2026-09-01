from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.port_surcharge import PortSurcharge
from app.services.port_surcharges.port_surcharge_service import PortSurchargeService

router = APIRouter(prefix="/port-surcharges", tags=["port-surcharges"])

_GEOGRAPHY = require_permission("can_manage_geography", "organization")


class PortSurchargeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    port_id: UUID
    code: str = Field(min_length=1, max_length=32)
    title: str = Field(min_length=1, max_length=128)
    applies_when: str = Field(min_length=1, max_length=512)
    amount: str = Field(min_length=1, max_length=32)
    currency: str = Field(min_length=3, max_length=3)


class PortSurchargeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    port_id: UUID
    code: str
    title: str
    applies_when: str
    amount: str
    currency: str
    source_ref: str

    @classmethod
    def from_row(cls, row: PortSurcharge) -> "PortSurchargeResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            port_id=row.port_id,
            code=row.code,
            title=row.title,
            applies_when=row.applies_when,
            amount=format(row.amount, "f"),
            currency=str(row.currency).strip(),
            source_ref=row.source_ref,
        )


@router.get("", response_model=list[PortSurchargeResponse])
async def list_port_surcharges(
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PortSurchargeResponse]:
    service = PortSurchargeService(session)
    rows = await service.list_surcharges()
    return [PortSurchargeResponse.from_row(row) for row in rows]


@router.get("/resolve", response_model=PortSurchargeResponse)
async def resolve_port_surcharge(
    port_id: UUID = Query(...),
    code: str = Query(..., min_length=1, max_length=32),
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> PortSurchargeResponse:
    service = PortSurchargeService(session)
    row = await service.resolve(port_id, code)
    return PortSurchargeResponse.from_row(row)


@router.post("", response_model=PortSurchargeResponse, status_code=status.HTTP_201_CREATED)
async def create_port_surcharge(
    body: PortSurchargeCreate,
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PortSurchargeResponse:
    service = PortSurchargeService(session)
    row = await service.create_surcharge(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        port_id=body.port_id,
        code=body.code,
        title=body.title,
        applies_when=body.applies_when,
        amount=body.amount,
        currency=body.currency,
    )
    await session.commit()
    return PortSurchargeResponse.from_row(row)
