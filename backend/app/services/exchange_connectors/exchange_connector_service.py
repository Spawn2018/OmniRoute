from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exchange_connector import (
    require_connector_code,
    require_exchange_source_ref,
    require_system_kind,
)
from app.models.exchange_connector import ExchangeConnector
from app.repositories.exchange_connectors.exchange_connector_repository import (
    ExchangeConnectorRepository,
)


class ExchangeConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ExchangeConnectorRepository(session)

    async def list_rows(self) -> list[ExchangeConnector]:
        return await self._rows.fetch_rows()

    async def persist_exchange_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> ExchangeConnector:
        row = ExchangeConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            system_kind=require_system_kind(system_kind),
            source_ref=require_exchange_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
