from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.registry_poll_mark import parse_registry_poll_mark_row
from app.models.registry_poll_mark import RegistryPollMark
from app.repositories.registry_poll_marks.registry_poll_mark_repository import (
    RegistryPollMarkRepository,
)


class RegistryPollMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RegistryPollMarkRepository(session)

    async def list_marks(self) -> list[RegistryPollMark]:
        return await self._rows.list_marks()

    async def persist_registry_poll_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        poll_kind: object,
        source_ref: object,
    ) -> RegistryPollMark:
        code, kind, origin = parse_registry_poll_mark_row(
            mark_code,
            poll_kind,
            source_ref,
        )
        row = RegistryPollMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            poll_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
