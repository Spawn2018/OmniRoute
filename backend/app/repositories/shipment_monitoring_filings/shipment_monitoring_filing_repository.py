from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment_monitoring_filing import ShipmentMonitoringFiling


class ShipmentMonitoringFilingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ShipmentMonitoringFiling]:
        packed = await self._session.scalars(
            select(ShipmentMonitoringFiling).order_by(
                ShipmentMonitoringFiling.filing_code,
                ShipmentMonitoringFiling.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: ShipmentMonitoringFiling) -> ShipmentMonitoringFiling:
        self._session.add(row)
        await self._session.flush()
        return row
