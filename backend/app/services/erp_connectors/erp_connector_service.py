from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.erp_connector import (
    require_connector_code,
    require_erp_source_ref,
    require_system_kind,
)
from app.models.erp_connector import ErpConnector
from app.repositories.erp_connectors.erp_connector_repository import ErpConnectorRepository


class ErpConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ErpConnectorRepository(session)

    async def list_rows(self) -> list[ErpConnector]:
        return await self._rows.fetch_rows()

    async def persist_erp_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> ErpConnector:
        row = ErpConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            system_kind=require_system_kind(system_kind),
            source_ref=require_erp_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
