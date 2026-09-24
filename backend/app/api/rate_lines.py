from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.money import Money
from app.models.rate_line import RateLine
from app.services.rate_lines.rate_line_service import RateLineService

router = APIRouter(prefix="/rate-lines", tags=["rate-lines"])


class RateLineCreate(BaseModel):
    charge_code: str = Field(min_length=1, max_length=32)
    amount: str = Field(min_length=1, max_length=32)
    currency: str = Field(min_length=3, max_length=3)
    source_ref: str = Field(min_length=1, max_length=512)
    allotment_teu: str | None = Field(default=None, max_length=32)
    spot_or_contract: str | None = Field(default=None, max_length=16)
    index_id: str | None = Field(default=None, max_length=128)
    fuel_index_id: UUID | None = None


class RateLineSupersede(BaseModel):
    amount: str = Field(min_length=1, max_length=32)
    currency: str = Field(min_length=3, max_length=3)
    source_ref: str = Field(min_length=1, max_length=512)
    allotment_teu: str | None = Field(default=None, max_length=32)
    spot_or_contract: str | None = Field(default=None, max_length=16)
    index_id: str | None = Field(default=None, max_length=128)
    fuel_index_id: UUID | None = None


class RateLineResponse(BaseModel):
    id: UUID
    organization_id: UUID
    charge_code: str
    amount: str
    currency: str
    source_ref: str
    allotment_teu: str | None
    spot_or_contract: str | None
    index_id: str | None
    fuel_index_id: UUID | None
    superseded_by: UUID | None

    @classmethod
    def from_row(cls, row: RateLine) -> "RateLineResponse":
        money = Money.of(row.amount, row.currency)
        amount_text, currency = money.as_pair()
        teu_text = None if row.allotment_teu is None else format(row.allotment_teu, "f")
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            charge_code=row.charge_code,
            amount=amount_text,
            currency=currency,
            source_ref=row.source_ref,
            allotment_teu=teu_text,
            spot_or_contract=row.spot_or_contract,
            index_id=row.index_id,
            fuel_index_id=row.fuel_index_id,
            superseded_by=row.superseded_by,
        )


@router.get("", response_model=list[RateLineResponse])
async def list_rate_lines(
    _authz: None = Depends(require_permission("can_manage_rate_lines", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RateLineResponse]:
    service = RateLineService(session)
    rows = await service.list_rates()
    return [RateLineResponse.from_row(row) for row in rows]


@router.post("", response_model=RateLineResponse, status_code=status.HTTP_201_CREATED)
async def create_rate_line(
    body: RateLineCreate,
    _authz: None = Depends(require_permission("can_manage_rate_lines", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RateLineResponse:
    service = RateLineService(session)
    row = await service.create_buy_rate(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_code=body.charge_code,
        amount=body.amount,
        currency=body.currency,
        source_ref=body.source_ref,
        allotment_teu=body.allotment_teu,
        spot_or_contract=body.spot_or_contract,
        index_id=body.index_id,
        fuel_index_id=body.fuel_index_id,
    )
    await session.commit()
    return RateLineResponse.from_row(row)


@router.post(
    "/{rate_line_id}/supersede",
    response_model=RateLineResponse,
    status_code=status.HTTP_201_CREATED,
)
async def supersede_rate_line(
    rate_line_id: UUID,
    body: RateLineSupersede,
    _authz: None = Depends(require_permission("can_manage_rate_lines", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RateLineResponse:
    service = RateLineService(session)
    row = await service.supersede(
        rate_line_id=rate_line_id,
        user_id=identity.user_id,
        amount=body.amount,
        currency=body.currency,
        source_ref=body.source_ref,
        allotment_teu=body.allotment_teu,
        spot_or_contract=body.spot_or_contract,
        index_id=body.index_id,
        fuel_index_id=body.fuel_index_id,
    )
    await session.commit()
    return RateLineResponse.from_row(row)
