from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tracking_consent import TrackingConsent


class TrackingConsentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_consents(self) -> list[TrackingConsent]:
        packed = await self._session.scalars(
            select(TrackingConsent).order_by(
                TrackingConsent.consent_code,
                TrackingConsent.id,
            ),
        )
        return list(packed.all())

    async def add_consent(self, row: TrackingConsent) -> TrackingConsent:
        self._session.add(row)
        await self._session.flush()
        return row
