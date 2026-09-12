from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.switch_bl_loi_mark import parse_switch_bl_loi_mark_row
from app.models.switch_bl_loi_mark import SwitchBlLoiMark
from app.repositories.switch_bl_loi_marks.switch_bl_loi_mark_repository import (
    SwitchBlLoiMarkRepository,
)


class SwitchBlLoiMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SwitchBlLoiMarkRepository(session)

    async def list_marks(self) -> list[SwitchBlLoiMark]:
        return await self._rows.list_marks()

    async def persist_switch_bl_loi_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        instrument_kind: object,
        source_ref: object,
    ) -> SwitchBlLoiMark:
        code, kind, origin = parse_switch_bl_loi_mark_row(
            mark_code,
            instrument_kind,
            source_ref,
        )
        row = SwitchBlLoiMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            instrument_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
