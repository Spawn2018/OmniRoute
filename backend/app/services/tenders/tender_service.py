from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender import (
    require_board_source_ref,
    require_buyer_id,
    require_deadline_at,
    require_incoterm,
    require_kind,
    require_named_place,
    require_side,
    require_status,
    require_trade_side,
)
from app.models.tender import Tender
from app.repositories.tenders.tender_repository import TenderRepository


class TenderService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TenderRepository(session)

    async def list_boards(self) -> list[Tender]:
        return await self._rows.list_all()

    async def record_board(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        side: object,
        kind: object,
        status: object,
        buyer_party_id: object,
        deadline_at: object,
        incoterm: object,
        trade_side: object,
        named_place: object,
        source_ref: object,
    ) -> Tender:
        token = require_incoterm(incoterm)
        row = Tender(
            id=uuid4(),
            organization_id=organization_id,
            side=require_side(side),
            kind=require_kind(kind),
            status=require_status(status),
            buyer_party_id=require_buyer_id(buyer_party_id),
            deadline_at=require_deadline_at(deadline_at),
            incoterm=token,
            trade_side=require_trade_side(trade_side),
            named_place=require_named_place(token, named_place),
            source_ref=require_board_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
