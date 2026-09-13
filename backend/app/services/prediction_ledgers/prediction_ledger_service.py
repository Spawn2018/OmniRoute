from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.prediction_ledger import (
    require_horizon_code,
    require_interval_bound,
    require_interval_order,
    require_ledger_source_ref,
    require_model_code,
    require_prediction_kind,
)
from app.models.prediction_ledger import PredictionLedger
from app.repositories.prediction_ledgers.prediction_ledger_repository import (
    PredictionLedgerRepository,
)


class PredictionLedgerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PredictionLedgerRepository(session)

    async def list_rows(self) -> list[PredictionLedger]:
        return await self._rows.fetch_rows()

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        prediction_kind: object,
        horizon_code: object,
        interval_low: object,
        interval_high: object,
        model_code: object,
        source_ref: object,
    ) -> PredictionLedger:
        low = require_interval_bound(interval_low)
        high = require_interval_bound(interval_high)
        require_interval_order(low, high)
        row = PredictionLedger(
            id=uuid4(),
            organization_id=organization_id,
            prediction_kind=require_prediction_kind(prediction_kind),
            horizon_code=require_horizon_code(horizon_code),
            interval_low=low,
            interval_high=high,
            crps=None,
            mae=None,
            model_code=require_model_code(model_code),
            source_ref=require_ledger_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
