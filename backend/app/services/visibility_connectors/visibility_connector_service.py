from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.visibility_connector import parse_visibility_row
from app.models.visibility_connector import VisibilityConnector
from app.repositories.visibility_connectors.visibility_connector_repository import (
    VisibilityConnectorRepository,
)


class VisibilityConnectorService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = VisibilityConnectorRepository(session)

    async def list_fixtures(self) -> list[VisibilityConnector]:
        return await self._rows.list_fixtures()

    async def persist_visibility_fixture(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        system_kind: object,
        source_ref: object,
    ) -> VisibilityConnector:
        code, kind, origin = parse_visibility_row(connector_code, system_kind, source_ref)
        row = VisibilityConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=code,
            system_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_fixture(row)
