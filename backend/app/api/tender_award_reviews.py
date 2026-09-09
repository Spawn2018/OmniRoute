from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_award_review import TenderAwardReview
from app.services.tender_award_reviews.tender_award_review_service import (
    TenderAwardReviewService,
)
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-award-reviews", tags=["tender-award-reviews"])

_PERM = "can_manage_tender_award_reviews"


class TenderAwardReviewCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    review_code: str
    source_ref: str


class TenderAwardReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    review_code: str
    source_ref: str


def _as_row(row: TenderAwardReview) -> TenderAwardReviewResponse:
    return TenderAwardReviewResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        review_code=row.review_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderAwardReviewResponse])
async def list_tender_award_reviews(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderAwardReviewResponse]:
    rows = await TenderAwardReviewService(session).list_reviews()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TenderAwardReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tender_award_review(
    body: TenderAwardReviewCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderAwardReviewResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderAwardReviewService(session).persist_review(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        review_code=body.review_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
