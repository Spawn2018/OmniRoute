from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tracking_consent import parse_tracking_consent_row
from app.models.tracking_consent import TrackingConsent
from app.repositories.tracking_consents.tracking_consent_repository import (
    TrackingConsentRepository,
)


class TrackingConsentService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TrackingConsentRepository(session)

    async def list_consents(self) -> list[TrackingConsent]:
        return await self._rows.list_consents()

    async def persist_tracking_consent(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        consent_code: object,
        consent_kind: object,
        source_ref: object,
    ) -> TrackingConsent:
        code, kind, origin = parse_tracking_consent_row(
            consent_code,
            consent_kind,
            source_ref,
        )
        row = TrackingConsent(
            id=uuid4(),
            organization_id=organization_id,
            consent_code=code,
            consent_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_consent(row)
