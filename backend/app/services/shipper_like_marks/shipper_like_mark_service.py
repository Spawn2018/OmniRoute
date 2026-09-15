from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipper_like_mark import parse_shipper_like_mark_row
from app.models.shipper_like_mark import ShipperLikeMark
from app.repositories.shipper_like_marks.shipper_like_mark_repository import (
    ShipperLikeMarkRepository,
)


class ShipperLikeMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipperLikeMarkRepository(session)

    async def list_marks(self) -> list[ShipperLikeMark]:
        return await self._rows.list_marks()

    async def persist_shipper_like_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        like_kind: object,
        source_ref: object,
    ) -> ShipperLikeMark:
        code, kind, origin = parse_shipper_like_mark_row(
            mark_code,
            like_kind,
            source_ref,
        )
        row = ShipperLikeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            like_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
