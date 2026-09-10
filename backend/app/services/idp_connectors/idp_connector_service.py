from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.idp_connector import (
    require_connector_code,
    require_idp_source_ref,
    require_provider_code,
    require_public_domain,
)
from app.models.idp_connector import IdpConnector
from app.repositories.idp_connectors.idp_connector_repository import IdpConnectorRepository


class IdpConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = IdpConnectorRepository(session)

    async def list_rows(self) -> list[IdpConnector]:
        return await self._rows.fetch_rows()

    async def persist_idp_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        provider_code: object,
        source_ref: object,
        public_domain: object = None,
    ) -> IdpConnector:
        row = IdpConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            provider_code=require_provider_code(provider_code),
            public_domain=require_public_domain(public_domain),
            source_ref=require_idp_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
