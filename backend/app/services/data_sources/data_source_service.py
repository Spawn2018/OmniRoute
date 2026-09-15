from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.data_source import parse_data_source_row
from app.models.data_source import DataSource
from app.repositories.data_sources.data_source_repository import (
    DataSourceRepository,
)


class DataSourceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = DataSourceRepository(session)

    async def list_marks(self) -> list[DataSource]:
        return await self._rows.list_marks()

    async def persist_data_source(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_code: object,
        license_label: object,
        rights_scope: object,
        source_ref: object,
    ) -> DataSource:
        code, license_token, rights_token, origin = parse_data_source_row(
            source_code,
            license_label,
            rights_scope,
            source_ref,
        )
        row = DataSource(
            id=uuid4(),
            organization_id=organization_id,
            source_code=code,
            license_label=license_token,
            rights_scope=rights_token,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
