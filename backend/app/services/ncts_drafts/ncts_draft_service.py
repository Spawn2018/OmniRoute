from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ncts_draft import parse_ncts_draft_row
from app.models.ncts_draft import NctsDraft
from app.repositories.ncts_drafts.ncts_draft_repository import NctsDraftRepository


class NctsDraftService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = NctsDraftRepository(session)

    async def list_drafts(self) -> list[NctsDraft]:
        return await self._rows.list_drafts()

    async def persist_ncts_draft(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        draft_code: object,
        transit_kind: object,
        source_ref: object,
    ) -> NctsDraft:
        code, kind, origin = parse_ncts_draft_row(
            draft_code,
            transit_kind,
            source_ref,
        )
        row = NctsDraft(
            id=uuid4(),
            organization_id=organization_id,
            draft_code=code,
            transit_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_draft(row)
