from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.fuel_anomaly_mark import parse_fuel_anomaly_mark_row
from app.models.fuel_anomaly_mark import FuelAnomalyMark
from app.repositories.fuel_anomaly_marks.fuel_anomaly_mark_repository import (
    FuelAnomalyMarkRepository,
)


class FuelAnomalyMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FuelAnomalyMarkRepository(session)

    async def list_marks(self) -> list[FuelAnomalyMark]:
        return await self._rows.list_marks()

    async def persist_fuel_anomaly_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        anomaly_kind: object,
        source_ref: object,
    ) -> FuelAnomalyMark:
        code, kind, origin = parse_fuel_anomaly_mark_row(
            mark_code,
            anomaly_kind,
            source_ref,
        )
        row = FuelAnomalyMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            anomaly_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
