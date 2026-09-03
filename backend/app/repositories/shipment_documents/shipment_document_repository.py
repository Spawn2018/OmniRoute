from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment_document import ShipmentDocument


class ShipmentDocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[ShipmentDocument]:
        result = await self._session.scalars(
            select(ShipmentDocument).order_by(ShipmentDocument.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: ShipmentDocument) -> ShipmentDocument:
        self._session.add(row)
        await self._session.flush()
        return row
