from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.offboarding_mark import parse_offboarding_mark_row
from app.models.offboarding_mark import OffboardingMark
from app.repositories.offboarding_marks.offboarding_mark_repository import (
    OffboardingMarkRepository,
)


class OffboardingMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OffboardingMarkRepository(session)

    async def list_marks(self) -> list[OffboardingMark]:
        return await self._rows.list_marks()

    async def persist_offboarding_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        offboard_kind: object,
        source_ref: object,
    ) -> OffboardingMark:
        code, kind, origin = parse_offboarding_mark_row(
            mark_code,
            offboard_kind,
            source_ref,
        )
        row = OffboardingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            offboard_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
