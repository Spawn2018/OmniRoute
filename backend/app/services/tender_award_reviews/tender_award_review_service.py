from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_award_review import (
    require_board_id,
    require_review_code,
    require_review_source_ref,
)
from app.models.tender_award_review import TenderAwardReview
from app.repositories.tender_award_reviews.tender_award_review_repository import (
    TenderAwardReviewRepository,
)


class TenderAwardReviewService:
    def __init__(self, session: AsyncSession) -> None:
        self._reviews = TenderAwardReviewRepository(session)

    async def list_reviews(self) -> list[TenderAwardReview]:
        return await self._reviews.fetch_reviews()

    async def persist_review(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        review_code: object,
        source_ref: object,
    ) -> TenderAwardReview:
        row = TenderAwardReview(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            review_code=require_review_code(review_code),
            source_ref=require_review_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._reviews.add(row)
