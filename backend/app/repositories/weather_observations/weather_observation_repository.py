from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.weather_observation import WeatherObservation


class WeatherObservationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_marks(self) -> list[WeatherObservation]:
        packed = await self._session.scalars(
            select(WeatherObservation).order_by(
                WeatherObservation.created_at.desc(),
                WeatherObservation.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: WeatherObservation) -> WeatherObservation:
        self._session.add(row)
        await self._session.flush()
        return row
