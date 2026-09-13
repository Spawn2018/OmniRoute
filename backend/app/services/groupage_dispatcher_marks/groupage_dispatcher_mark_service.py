from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.groupage_dispatcher_mark import parse_groupage_dispatcher_mark_row
from app.models.groupage_dispatcher_mark import GroupageDispatcherMark
from app.repositories.groupage_dispatcher_marks.groupage_dispatcher_mark_repository import (
    GroupageDispatcherMarkRepository,
)


class GroupageDispatcherMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = GroupageDispatcherMarkRepository(session)

    async def list_marks(self) -> list[GroupageDispatcherMark]:
        return await self._rows.list_marks()

    async def persist_groupage_dispatcher_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        dispatcher_kind: object,
        source_ref: object,
    ) -> GroupageDispatcherMark:
        code, kind, origin = parse_groupage_dispatcher_mark_row(
            mark_code,
            dispatcher_kind,
            source_ref,
        )
        row = GroupageDispatcherMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            dispatcher_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
