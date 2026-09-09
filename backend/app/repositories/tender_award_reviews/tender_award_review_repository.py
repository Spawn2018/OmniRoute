from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_award_review import TenderAwardReview


class TenderAwardReviewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_reviews(self) -> list[TenderAwardReview]:
        packed = await self._session.scalars(
            select(TenderAwardReview).order_by(
                TenderAwardReview.created_at.desc(),
                TenderAwardReview.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: TenderAwardReview) -> TenderAwardReview:
        self._session.add(row)
        await self._session.flush()
        return row
