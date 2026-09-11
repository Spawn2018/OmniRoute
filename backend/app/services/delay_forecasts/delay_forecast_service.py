from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.delay_forecast import parse_delay_forecast_row
from app.models.delay_forecast import DelayForecast
from app.repositories.delay_forecasts.delay_forecast_repository import DelayForecastRepository


class DelayForecastService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = DelayForecastRepository(session)

    async def list_forecasts(self) -> list[DelayForecast]:
        return await self._rows.list_forecasts()

    async def persist_delay_forecast(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        forecast_code: object,
        horizon_hours: object,
        p_late: object,
        source_ref: object,
    ) -> DelayForecast:
        code, horizon, chance, origin = parse_delay_forecast_row(
            forecast_code, horizon_hours, p_late, source_ref
        )
        row = DelayForecast(
            id=uuid4(),
            organization_id=organization_id,
            forecast_code=code,
            horizon_hours=horizon,
            p_late=chance,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_forecast(row)
