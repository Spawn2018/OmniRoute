from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.monitoring_scheme import require_scheme_code, require_scheme_source_ref
from app.models.monitoring_scheme import MonitoringScheme
from app.repositories.monitoring_schemes.monitoring_scheme_repository import (
    MonitoringSchemeRepository,
)


class MonitoringSchemeService:
    def __init__(self, session: AsyncSession) -> None:
        self._schemes = MonitoringSchemeRepository(session)

    async def list_schemes(self) -> list[MonitoringScheme]:
        return await self._schemes.fetch_schemes()

    async def persist_scheme(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        scheme_code: object,
        source_ref: object,
    ) -> MonitoringScheme:
        row = MonitoringScheme(
            id=uuid4(),
            organization_id=organization_id,
            scheme_code=require_scheme_code(scheme_code),
            source_ref=require_scheme_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._schemes.add(row)
