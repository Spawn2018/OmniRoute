from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.remediation_option import parse_remediation_option_row
from app.models.remediation_option import RemediationOption
from app.repositories.remediation_options.remediation_option_repository import (
    RemediationOptionRepository,
)


class RemediationOptionService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RemediationOptionRepository(session)

    async def list_options(self) -> list[RemediationOption]:
        return await self._rows.list_options()

    async def persist_remediation_option(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        option_code: object,
        option_kind: object,
        source_ref: object,
    ) -> RemediationOption:
        code, kind, origin = parse_remediation_option_row(
            option_code, option_kind, source_ref
        )
        row = RemediationOption(
            id=uuid4(),
            organization_id=organization_id,
            option_code=code,
            option_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_option(row)
