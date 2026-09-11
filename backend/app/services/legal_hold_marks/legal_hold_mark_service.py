from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.legal_hold_mark import parse_legal_hold_mark_row
from app.models.legal_hold_mark import LegalHoldMark
from app.repositories.legal_hold_marks.legal_hold_mark_repository import LegalHoldMarkRepository


class LegalHoldMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LegalHoldMarkRepository(session)

    async def list_marks(self) -> list[LegalHoldMark]:
        return await self._rows.list_marks()

    async def persist_legal_hold_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        hold_kind: object,
        source_ref: object,
    ) -> LegalHoldMark:
        code, kind, origin = parse_legal_hold_mark_row(
            mark_code,
            hold_kind,
            source_ref,
        )
        row = LegalHoldMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            hold_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
