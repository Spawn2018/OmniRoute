from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.phyto_ata_mark import parse_phyto_ata_mark_row
from app.models.phyto_ata_mark import PhytoAtaMark
from app.repositories.phyto_ata_marks.phyto_ata_mark_repository import (
    PhytoAtaMarkRepository,
)


class PhytoAtaMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PhytoAtaMarkRepository(session)

    async def list_marks(self) -> list[PhytoAtaMark]:
        return await self._rows.list_marks()

    async def persist_phyto_ata_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        permit_kind: object,
        source_ref: object,
    ) -> PhytoAtaMark:
        code, kind, origin = parse_phyto_ata_mark_row(
            mark_code,
            permit_kind,
            source_ref,
        )
        row = PhytoAtaMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            permit_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
