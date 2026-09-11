from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.delay_forecast import DelayForecast


class DelayForecastRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_forecasts(self) -> list[DelayForecast]:
        packed = await self._session.scalars(
            select(DelayForecast).order_by(DelayForecast.forecast_code, DelayForecast.id),
        )
        return list(packed.all())

    async def add_forecast(self, row: DelayForecast) -> DelayForecast:
        self._session.add(row)
        await self._session.flush()
        return row
