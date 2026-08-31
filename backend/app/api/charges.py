from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.charge import margin
from app.domain.money import Money
from app.models.charge import Charge
from app.services.charges.charge_service import ChargeService

router = APIRouter(prefix="/charges", tags=["charges"])


class ChargeCreate(BaseModel):
    charge_code: str = Field(min_length=1, max_length=32)
    buy_amount: str = Field(min_length=1, max_length=32)
    buy_currency: str = Field(min_length=3, max_length=3)
    sell_amount: str = Field(min_length=1, max_length=32)
    sell_currency: str = Field(min_length=3, max_length=3)
    rate_line_id: UUID | None = None


class ChargeResponse(BaseModel):
    id: UUID
    organization_id: UUID
    charge_code: str
    buy_amount: str
    buy_currency: str
    sell_amount: str
    sell_currency: str
    margin_amount: str
    margin_currency: str
    rate_line_id: UUID | None

    @classmethod
    def from_row(cls, row: Charge) -> "ChargeResponse":
        buy = Money.of(row.buy_amount, row.buy_currency)
        sell = Money.of(row.sell_amount, row.sell_currency)
        computed = margin(buy, sell)
        buy_text, buy_ccy = buy.as_pair()
        sell_text, sell_ccy = sell.as_pair()
        margin_text, margin_ccy = computed.as_pair()
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            charge_code=row.charge_code,
            buy_amount=buy_text,
            buy_currency=buy_ccy,
            sell_amount=sell_text,
            sell_currency=sell_ccy,
            margin_amount=margin_text,
            margin_currency=margin_ccy,
            rate_line_id=row.rate_line_id,
        )


@router.get("", response_model=list[ChargeResponse])
async def list_charges(
    _authz: None = Depends(require_permission("can_manage_charges", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ChargeResponse]:
    service = ChargeService(session)
    rows = await service.list_charges()
    return [ChargeResponse.from_row(row) for row in rows]


@router.post("", response_model=ChargeResponse, status_code=status.HTTP_201_CREATED)
async def create_charge(
    body: ChargeCreate,
    _authz: None = Depends(require_permission("can_manage_charges", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ChargeResponse:
    service = ChargeService(session)
    row = await service.create_charge(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_code=body.charge_code,
        buy_amount=body.buy_amount,
        buy_currency=body.buy_currency,
        sell_amount=body.sell_amount,
        sell_currency=body.sell_currency,
        rate_line_id=body.rate_line_id,
    )
    await session.commit()
    return ChargeResponse.from_row(row)
