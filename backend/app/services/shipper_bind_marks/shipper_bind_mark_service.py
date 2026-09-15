from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipper_bind_mark import parse_shipper_bind_mark_row
from app.models.shipper_bind_mark import ShipperBindMark
from app.repositories.shipper_bind_marks.shipper_bind_mark_repository import (
    ShipperBindMarkRepository,
)


class ShipperBindMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._desk = ShipperBindMarkRepository(session)

    async def list_marks(self) -> list[ShipperBindMark]:
        return await self._desk.list_marks()

    async def persist_shipper_bind_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bind_kind: object,
        source_ref: object,
    ) -> ShipperBindMark:
        code, kind, origin = parse_shipper_bind_mark_row(mark_code, bind_kind, source_ref)
        entry = ShipperBindMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bind_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._desk.add_mark(entry)
