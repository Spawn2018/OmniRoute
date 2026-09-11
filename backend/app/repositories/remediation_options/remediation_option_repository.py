from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.remediation_option import RemediationOption


class RemediationOptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_options(self) -> list[RemediationOption]:
        packed = await self._session.scalars(
            select(RemediationOption).order_by(
                RemediationOption.option_code,
                RemediationOption.id,
            ),
        )
        return list(packed.all())

    async def add_option(self, row: RemediationOption) -> RemediationOption:
        self._session.add(row)
        await self._session.flush()
        return row
