from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.nac_mark import parse_nac_mark_row
from app.models.nac_mark import NacMark
from app.repositories.nac_marks.nac_mark_repository import NacMarkRepository


class NacMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = NacMarkRepository(session)

    async def list_marks(self) -> list[NacMark]:
        return await self._rows.list_marks()

    async def persist_nac_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        nac_kind: object,
        source_ref: object,
    ) -> NacMark:
        code, kind, origin = parse_nac_mark_row(
            mark_code,
            nac_kind,
            source_ref,
        )
        row = NacMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            nac_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
