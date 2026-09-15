from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.allocation_key import AllocationKeyDraft, parse_allocation_key_row
from app.models.allocation_key import AllocationKey
from app.repositories.allocation_keys.allocation_key_repository import (
    AllocationKeyRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: AllocationKeyDraft,
) -> AllocationKey:
    return AllocationKey(
        id=uuid4(),
        organization_id=organization_id,
        key_code=draft.key_code,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class AllocationKeyService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = AllocationKeyRepository(session)

    async def list_rows(self) -> list[AllocationKey]:
        return await self._rows.list_rows()

    async def persist_key(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        key_code: object,
        source_ref: object,
    ) -> AllocationKey:
        draft = parse_allocation_key_row(key_code, source_ref)
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
