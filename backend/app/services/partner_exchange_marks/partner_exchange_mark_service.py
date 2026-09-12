from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.partner_exchange_mark import parse_partner_exchange_mark_row
from app.models.partner_exchange_mark import PartnerExchangeMark
from app.repositories.partner_exchange_marks.partner_exchange_mark_repository import (
    PartnerExchangeMarkRepository,
)


class PartnerExchangeMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PartnerExchangeMarkRepository(session)

    async def list_marks(self) -> list[PartnerExchangeMark]:
        return await self._rows.list_marks()

    async def persist_partner_exchange_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        exchange_kind: object,
        source_ref: object,
    ) -> PartnerExchangeMark:
        code, kind, origin = parse_partner_exchange_mark_row(
            mark_code,
            exchange_kind,
            source_ref,
        )
        row = PartnerExchangeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            exchange_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
