from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.bookkeeping import (
    require_bookkeeping_charge_id,
    require_bookkeeping_invoice_id,
    require_bookkeeping_source_ref,
)
from app.domain.errors import InvalidBookkeeping
from app.models.bookkeeping import Bookkeeping
from app.repositories.bookkeeping.bookkeeping_repository import BookkeepingRepository


class BookkeepingService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BookkeepingRepository(session)

    async def list_entries(self) -> list[Bookkeeping]:
        return await self._rows.list_all()

    async def record_entry(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_id: UUID,
        sales_invoice_id: UUID,
        source_ref: str,
    ) -> Bookkeeping:
        row = Bookkeeping(
            id=uuid4(),
            organization_id=organization_id,
            charge_id=require_bookkeeping_charge_id(charge_id),
            sales_invoice_id=require_bookkeeping_invoice_id(sales_invoice_id),
            source_ref=require_bookkeeping_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidBookkeeping("para już zapisana") from orig
