from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_carbon_mark import (
    require_board_id,
    require_carbon_source_ref,
    require_mark_code,
)
from app.models.tender_carbon_mark import TenderCarbonMark
from app.repositories.tender_carbon_marks.tender_carbon_mark_repository import (
    TenderCarbonMarkRepository,
)


class TenderCarbonMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._marks = TenderCarbonMarkRepository(session)

    async def list_marks(self) -> list[TenderCarbonMark]:
        return await self._marks.fetch_marks()

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        mark_code: object,
        source_ref: object,
    ) -> TenderCarbonMark:
        row = TenderCarbonMark(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            mark_code=require_mark_code(mark_code),
            source_ref=require_carbon_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._marks.add(row)
