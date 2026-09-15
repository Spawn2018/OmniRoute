from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipper_award_mark import parse_shipper_award_mark_row
from app.models.shipper_award_mark import ShipperAwardMark
from app.repositories.shipper_award_marks.shipper_award_mark_repository import (
    ShipperAwardMarkRepository,
)


class ShipperAwardMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ShipperAwardMarkRepository(session)

    async def list_marks(self) -> list[ShipperAwardMark]:
        return await self._repo.list_marks()

    async def persist_shipper_award_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        award_kind: object,
        source_ref: object,
    ) -> ShipperAwardMark:
        code, kind, origin = parse_shipper_award_mark_row(
            mark_code,
            award_kind,
            source_ref,
        )
        return await self._repo.add_mark(
            ShipperAwardMark(
                id=uuid4(),
                organization_id=organization_id,
                mark_code=code,
                award_kind=kind,
                source_ref=origin,
                created_by=user_id,
            ),
        )
