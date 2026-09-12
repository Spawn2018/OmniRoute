from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.eur1_atr_mark import parse_eur1_atr_mark_row
from app.models.eur1_atr_mark import Eur1AtrMark
from app.repositories.eur1_atr_marks.eur1_atr_mark_repository import (
    Eur1AtrMarkRepository,
)


class Eur1AtrMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = Eur1AtrMarkRepository(session)

    async def list_marks(self) -> list[Eur1AtrMark]:
        return await self._rows.list_marks()

    async def persist_eur1_atr_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        cert_kind: object,
        source_ref: object,
    ) -> Eur1AtrMark:
        code, kind, origin = parse_eur1_atr_mark_row(
            mark_code,
            cert_kind,
            source_ref,
        )
        row = Eur1AtrMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            cert_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
