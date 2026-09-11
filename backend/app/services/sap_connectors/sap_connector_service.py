from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sap_connector import (
    require_connector_code,
    require_sap_source_ref,
    require_system_kind,
)
from app.models.sap_connector import SapConnector
from app.repositories.sap_connectors.sap_connector_repository import SapConnectorRepository


class SapConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SapConnectorRepository(session)

    async def list_connectors(self) -> list[SapConnector]:
        return await self._rows.list_connectors()

    async def persist_sap_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> SapConnector:
        row = SapConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            system_kind=require_system_kind(system_kind),
            source_ref=require_sap_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add_connector(row)
