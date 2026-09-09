from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_ted_notice import (
    require_board_id,
    require_notice_number,
    require_ted_source_ref,
)
from app.models.tender_ted_notice import TenderTedNotice
from app.repositories.tender_ted_notices.tender_ted_notice_repository import (
    TenderTedNoticeRepository,
)


class TenderTedNoticeService:
    def __init__(self, session: AsyncSession) -> None:
        self._notices = TenderTedNoticeRepository(session)

    async def list_notices(self) -> list[TenderTedNotice]:
        return await self._notices.fetch_notices()

    async def persist_notice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        notice_number: object,
        source_ref: object,
    ) -> TenderTedNotice:
        row = TenderTedNotice(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            notice_number=require_notice_number(notice_number),
            source_ref=require_ted_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._notices.add(row)
