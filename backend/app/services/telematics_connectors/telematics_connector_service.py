from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.telematics_connector import (
    require_connector_source_ref,
    require_observation_kind,
    require_provider_code,
)
from app.models.telematics_connector import TelematicsConnector
from app.repositories.telematics_connectors.telematics_connector_repository import (
    TelematicsConnectorRepository,
)


class TelematicsConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._marks = TelematicsConnectorRepository(session)

    async def list_marks(self) -> list[TelematicsConnector]:
        return await self._marks.fetch_marks()

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        observation_kind: object,
        provider_code: object,
        source_ref: object,
    ) -> TelematicsConnector:
        row = TelematicsConnector(
            id=uuid4(),
            organization_id=organization_id,
            observation_kind=require_observation_kind(observation_kind),
            provider_code=require_provider_code(provider_code),
            source_ref=require_connector_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._marks.add(row)
