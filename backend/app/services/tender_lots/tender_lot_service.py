from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.tender_lot import require_lot_code, require_lot_source_ref, require_tender_id
from app.models.tender_lot import TenderLot
from app.repositories.tender_lots.tender_lot_repository import TenderLotRepository


class TenderLotService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TenderLotRepository(session)

    async def list_lots(self) -> list[TenderLot]:
        return await self._rows.list_all()

    async def get_lot(self, lot_id: UUID) -> TenderLot:
        found = await self._rows.get(lot_id)
        if found is None:
            raise ResourceNotFound("nieznana partia")
        return found

    async def record_lot(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        lot_code: object,
        source_ref: object,
    ) -> TenderLot:
        row = TenderLot(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_tender_id(tender_id),
            lot_code=require_lot_code(lot_code),
            source_ref=require_lot_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
