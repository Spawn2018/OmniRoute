from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipper_round_mark import parse_shipper_round_mark_row
from app.models.shipper_round_mark import ShipperRoundMark
from app.repositories.shipper_round_marks.shipper_round_mark_repository import (
    ShipperRoundMarkRepository,
)


class ShipperRoundMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipperRoundMarkRepository(session)

    async def list_marks(self) -> list[ShipperRoundMark]:
        return await self._rows.list_marks()

    async def persist_shipper_round_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        round_kind: object,
        source_ref: object,
    ) -> ShipperRoundMark:
        code, kind, origin = parse_shipper_round_mark_row(
            mark_code,
            round_kind,
            source_ref,
        )
        row = ShipperRoundMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            round_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
