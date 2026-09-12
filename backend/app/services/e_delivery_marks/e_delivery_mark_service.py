from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.e_delivery_mark import parse_e_delivery_mark_row
from app.models.e_delivery_mark import EDeliveryMark
from app.repositories.e_delivery_marks.e_delivery_mark_repository import (
    EDeliveryMarkRepository,
)


class EDeliveryMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = EDeliveryMarkRepository(session)

    async def list_marks(self) -> list[EDeliveryMark]:
        return await self._rows.list_marks()

    async def persist_e_delivery_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        delivery_kind: object,
        source_ref: object,
    ) -> EDeliveryMark:
        code, kind, origin = parse_e_delivery_mark_row(
            mark_code,
            delivery_kind,
            source_ref,
        )
        row = EDeliveryMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            delivery_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
