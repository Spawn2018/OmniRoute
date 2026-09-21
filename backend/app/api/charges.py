from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.charge import margin
from app.domain.errors import (
    InvalidOperatorDecision,
    MarginFloorBreach,
    OperatorDecisionConflict,
)
from app.domain.margin_floor import parse_optional_floor_lane, require_margin_above_floor
from app.domain.money import Money
from app.models.charge import Charge
from app.models.margin_floor import MarginFloor
from app.models.operator_decision import OperatorDecision
from app.repositories.margin_floors.margin_floor_repository import MarginFloorRepository
from app.services.charges.charge_service import ChargeService
from app.services.operator_decisions.operator_decision_service import (
    OperatorDecisionService,
)

router = APIRouter(prefix="/charges", tags=["charges"])

_FLOOR_KIND = "margin_floor"


class ChargeCreate(BaseModel):
    charge_code: str = Field(min_length=1, max_length=32)
    buy_amount: str = Field(min_length=1, max_length=32)
    buy_currency: str = Field(min_length=3, max_length=3)
    sell_amount: str = Field(min_length=1, max_length=32)
    sell_currency: str = Field(min_length=3, max_length=3)
    rate_line_id: UUID | None = None
    shipment_id: UUID | None = None
    source_ref: str = Field(min_length=1, max_length=512)
    # 539.0: tylko lookup margin_floor — nie kolumny na charge
    origin_unlocode: str | None = Field(default=None, max_length=5)
    destination_unlocode: str | None = Field(default=None, max_length=5)
    # 544.0: accepted operator_decision (margin_floor) — override podłogi
    floor_decision_id: UUID | None = None


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
    shipment_id: UUID | None
    source_ref: str | None

    @classmethod
    def from_row(cls, row: Charge) -> "ChargeResponse":
        buy = Money.of(row.buy_amount, row.buy_currency)
        sell = Money.of(row.sell_amount, row.sell_currency)
        return cls._packed(row, buy, sell, margin(buy, sell))

    @classmethod
    def from_sql_gap(cls, row: Charge, sql_gap: Decimal) -> "ChargeResponse":
        buy = Money.of(row.buy_amount, row.buy_currency)
        sell = Money.of(row.sell_amount, row.sell_currency)
        return cls._packed(row, buy, sell, Money.of(sql_gap, row.buy_currency))

    @classmethod
    def _packed(
        cls,
        row: Charge,
        buy: Money,
        sell: Money,
        gap: Money,
    ) -> "ChargeResponse":
        buy_text, buy_ccy = buy.as_pair()
        sell_text, sell_ccy = sell.as_pair()
        margin_text, margin_ccy = gap.as_pair()
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
            shipment_id=row.shipment_id,
            source_ref=row.source_ref,
        )


async def _accepted_floor_override(
    decisions: OperatorDecisionService,
    *,
    decision_id: UUID,
    floor_id: UUID,
) -> None:
    row = await decisions.get_decision(decision_id)
    if (
        row.subject_kind != _FLOOR_KIND
        or row.subject_id != floor_id
        or row.status != "accepted"
    ):
        raise InvalidOperatorDecision(
            "floor_decision_id musi być accepted dla tej podłogi marży",
        )


async def _pending_for_floor_breach(
    decisions: OperatorDecisionService,
    *,
    organization_id: UUID,
    user_id: UUID,
    floor_id: UUID,
    source_ref: str,
) -> OperatorDecision:
    try:
        return await decisions.create_decision(
            organization_id=organization_id,
            user_id=user_id,
            subject_kind=_FLOOR_KIND,
            subject_id=floor_id,
            source_ref=source_ref,
        )
    except OperatorDecisionConflict:
        existing = await decisions.get_pending(_FLOOR_KIND, floor_id)
        if existing is None:
            raise
        return existing


async def _enforce_margin_floor(
    session: AsyncSession,
    identity: SessionIdentity,
    body: ChargeCreate,
    floor: MarginFloor,
    gap: Money,
) -> None:
    try:
        require_margin_above_floor(
            margin_amount=gap.amount,
            margin_currency=gap.currency.code,
            floor_amount=floor.floor_amount,
            floor_currency=floor.floor_currency,
        )
    except MarginFloorBreach as breach:
        decisions = OperatorDecisionService(session)
        if body.floor_decision_id is not None:
            await _accepted_floor_override(
                decisions,
                decision_id=body.floor_decision_id,
                floor_id=floor.id,
            )
            return
        pending = await _pending_for_floor_breach(
            decisions,
            organization_id=identity.organization_id,
            user_id=identity.user_id,
            floor_id=floor.id,
            source_ref=body.source_ref,
        )
        raise MarginFloorBreach(str(breach), decision_id=pending.id) from breach


@router.get("", response_model=list[ChargeResponse])
async def list_charges(
    _authz: None = Depends(require_permission("can_manage_charges", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ChargeResponse]:
    service = ChargeService(session)
    pairs = await service.list_charges()
    return [ChargeResponse.from_sql_gap(row, gap) for row, gap in pairs]


@router.post("", response_model=ChargeResponse, status_code=status.HTTP_201_CREATED)
async def create_charge(
    body: ChargeCreate,
    _authz: None = Depends(require_permission("can_manage_charges", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ChargeResponse:
    lane = parse_optional_floor_lane(body.origin_unlocode, body.destination_unlocode)
    if lane is not None:
        buy = Money.of(body.buy_amount, body.buy_currency)
        sell = Money.of(body.sell_amount, body.sell_currency)
        gap = margin(buy, sell)
        floor = await MarginFloorRepository(session).find_for_lane(
            origin_unlocode=lane[0],
            destination_unlocode=lane[1],
            floor_currency=gap.currency.code,
        )
        if floor is not None:
            await _enforce_margin_floor(session, identity, body, floor, gap)
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
        source_ref=body.source_ref,
        shipment_id=body.shipment_id,
    )
    await session.commit()
    return ChargeResponse.from_row(row)
