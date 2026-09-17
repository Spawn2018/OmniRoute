from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipment_monitoring_filing import parse_shipment_monitoring_filing_row
from app.models.shipment_monitoring_filing import ShipmentMonitoringFiling
from app.repositories.shipment_monitoring_filings.shipment_monitoring_filing_repository import (
    ShipmentMonitoringFilingRepository,
)


class ShipmentMonitoringFilingService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipmentMonitoringFilingRepository(session)

    async def list_marks(self) -> list[ShipmentMonitoringFiling]:
        return await self._rows.list_marks()

    async def persist_shipment_monitoring_filing(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        filing_code: object,
        status_kind: object,
        source_ref: object,
    ) -> ShipmentMonitoringFiling:
        code, kind, origin = parse_shipment_monitoring_filing_row(
            filing_code,
            status_kind,
            source_ref,
        )
        row = ShipmentMonitoringFiling(
            id=uuid4(),
            organization_id=organization_id,
            filing_code=code,
            status_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
