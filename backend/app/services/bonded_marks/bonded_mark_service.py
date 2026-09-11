from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.bonded_mark import parse_bonded_mark_row
from app.models.bonded_mark import BondedMark
from app.repositories.bonded_marks.bonded_mark_repository import BondedMarkRepository


class BondedMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BondedMarkRepository(session)

    async def list_marks(self) -> list[BondedMark]:
        return await self._rows.list_marks()

    async def persist_bonded_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bond_kind: object,
        source_ref: object,
    ) -> BondedMark:
        code, kind, origin = parse_bonded_mark_row(
            mark_code,
            bond_kind,
            source_ref,
        )
        row = BondedMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bond_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
