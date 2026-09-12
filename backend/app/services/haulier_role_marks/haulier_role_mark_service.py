from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.haulier_role_mark import parse_haulier_role_mark_row
from app.models.haulier_role_mark import HaulierRoleMark
from app.repositories.haulier_role_marks.haulier_role_mark_repository import (
    HaulierRoleMarkRepository,
)


class HaulierRoleMarkService:
    """HITL katalog roli przewoznika — bez FK party na shipment i bez cargo_value."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = HaulierRoleMarkRepository(session)

    async def list_marks(self) -> list[HaulierRoleMark]:
        return await self._marks.list_marks()

    async def persist_haulier_role_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        role_kind: object,
        source_ref: object,
    ) -> HaulierRoleMark:
        code, kind, pointer = parse_haulier_role_mark_row(
            mark_code,
            role_kind,
            source_ref,
        )
        row = HaulierRoleMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            role_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
