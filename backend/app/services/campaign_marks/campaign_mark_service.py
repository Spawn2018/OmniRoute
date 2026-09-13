from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.campaign_mark import parse_campaign_mark_row
from app.models.campaign_mark import CampaignMark
from app.repositories.campaign_marks.campaign_mark_repository import (
    CampaignMarkRepository,
)


class CampaignMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CampaignMarkRepository(session)

    async def list_marks(self) -> list[CampaignMark]:
        return await self._rows.list_marks()

    async def persist_campaign_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        campaign_kind: object,
        source_ref: object,
    ) -> CampaignMark:
        code, kind, origin = parse_campaign_mark_row(
            mark_code,
            campaign_kind,
            source_ref,
        )
        row = CampaignMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            campaign_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
