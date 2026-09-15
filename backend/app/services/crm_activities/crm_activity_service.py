from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.crm_activity import parse_crm_activity_row
from app.models.crm_activity import CrmActivity
from app.repositories.crm_activities.crm_activity_repository import (
    CrmActivityRepository,
)


class CrmActivityService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CrmActivityRepository(session)

    async def list_activities(self) -> list[CrmActivity]:
        return await self._rows.list_activities()

    async def persist_crm_activity(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        activity_code: object,
        activity_kind: object,
        source_ref: object,
    ) -> CrmActivity:
        code, kind, origin = parse_crm_activity_row(
            activity_code,
            activity_kind,
            source_ref,
        )
        row = CrmActivity(
            id=uuid4(),
            organization_id=organization_id,
            activity_code=code,
            activity_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_activity(row)
