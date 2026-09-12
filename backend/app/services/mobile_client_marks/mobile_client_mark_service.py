from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.mobile_client_mark import parse_mobile_client_mark_row
from app.models.mobile_client_mark import MobileClientMark
from app.repositories.mobile_client_marks.mobile_client_mark_repository import (
    MobileClientMarkRepository,
)


class MobileClientMarkService:
    """HITL katalog klienta mobilnego — bez Expo/EAS i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = MobileClientMarkRepository(session)

    async def list_marks(self) -> list[MobileClientMark]:
        return await self._marks.list_marks()

    async def persist_mobile_client_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        client_kind: object,
        source_ref: object,
    ) -> MobileClientMark:
        code, kind, pointer = parse_mobile_client_mark_row(
            mark_code,
            client_kind,
            source_ref,
        )
        row = MobileClientMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            client_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
