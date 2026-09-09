from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.rate_card import RateCard
from app.services.rate_cards.rate_card_service import RateCardService

router = APIRouter(prefix="/rate-cards", tags=["rate-cards"])

_PERM = "can_manage_rate_cards"


class RateCardCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    card_code: str
    applies_when: str
    amount: str
    currency: str
    source_ref: str


class RateCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    card_code: str
    applies_when: str
    amount: str
    currency: str
    source_ref: str


def _as_row(row: RateCard) -> RateCardResponse:
    return RateCardResponse(
        id=row.id,
        organization_id=row.organization_id,
        card_code=row.card_code,
        applies_when=row.applies_when,
        amount=format(row.amount, "f"),
        currency=str(row.currency).strip(),
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[RateCardResponse])
async def list_rate_cards(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RateCardResponse]:
    rows = await RateCardService(session).list_cards()
    return [_as_row(row) for row in rows]


@router.get("/matching", response_model=list[RateCardResponse])
async def equal_when_rate_cards(
    applies_when: str | None = Query(default=None),
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RateCardResponse]:
    rows = await RateCardService(session).cards_for_when(applies_when)
    return [_as_row(row) for row in rows]


@router.post("", response_model=RateCardResponse, status_code=status.HTTP_201_CREATED)
async def create_rate_card(
    body: RateCardCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RateCardResponse:
    row = await RateCardService(session).record_card(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        card_code=body.card_code,
        applies_when=body.applies_when,
        amount=body.amount,
        currency=body.currency,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
