from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.credit_review import CreditReview
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/credit-reviews", tags=["credit-reviews"])

_PARTIES = require_permission("can_manage_parties", "organization")


class CreditReviewCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    review_date: date
    decision: str = Field(min_length=2, max_length=8)
    note: str | None = Field(default=None, max_length=512)


class CreditReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    review_date: date
    decision: str
    note: str | None
    source_ref: str

    @classmethod
    def from_row(cls, row: CreditReview) -> "CreditReviewResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            party_id=row.party_id,
            review_date=row.review_date,
            decision=row.decision,
            note=row.note,
            source_ref=row.source_ref,
        )


@router.get("", response_model=list[CreditReviewResponse])
async def list_credit_reviews(
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CreditReviewResponse]:
    service = PartyService(session)
    rows = await service.list_reviews()
    return [CreditReviewResponse.from_row(row) for row in rows]


@router.get("/resolve", response_model=CreditReviewResponse)
async def resolve_credit_review(
    party_id: UUID = Query(...),
    on_date: date = Query(...),
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> CreditReviewResponse:
    service = PartyService(session)
    row = await service.resolve_review(party_id=party_id, on_date=on_date)
    return CreditReviewResponse.from_row(row)


@router.post("", response_model=CreditReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_credit_review(
    body: CreditReviewCreate,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CreditReviewResponse:
    service = PartyService(session)
    row = await service.create_review(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=body.party_id,
        review_date=body.review_date,
        decision=body.decision,
        note=body.note,
    )
    await session.commit()
    return CreditReviewResponse.from_row(row)
