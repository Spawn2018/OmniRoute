from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.automation_bias_mark import parse_automation_bias_mark_row
from app.models.automation_bias_mark import AutomationBiasMark
from app.repositories.automation_bias_marks.automation_bias_mark_repository import (
    AutomationBiasMarkRepository,
)


class AutomationBiasMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = AutomationBiasMarkRepository(session)

    async def list_marks(self) -> list[AutomationBiasMark]:
        return await self._rows.list_marks()

    async def persist_automation_bias_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bias_kind: object,
        source_ref: object,
    ) -> AutomationBiasMark:
        code, kind, origin = parse_automation_bias_mark_row(
            mark_code,
            bias_kind,
            source_ref,
        )
        row = AutomationBiasMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bias_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
