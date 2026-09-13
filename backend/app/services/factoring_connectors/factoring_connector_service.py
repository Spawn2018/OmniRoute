from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.factoring_connector import (
    require_connector_code,
    require_factoring_source_ref,
    require_system_kind,
)
from app.models.factoring_connector import FactoringConnector
from app.repositories.factoring_connectors.factoring_connector_repository import (
    FactoringConnectorRepository,
)


class FactoringConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FactoringConnectorRepository(session)

    async def list_rows(self) -> list[FactoringConnector]:
        return await self._rows.fetch_rows()

    async def persist_factoring_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> FactoringConnector:
        row = FactoringConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            system_kind=require_system_kind(system_kind),
            source_ref=require_factoring_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
