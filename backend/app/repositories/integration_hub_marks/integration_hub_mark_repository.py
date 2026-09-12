from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.integration_hub_mark import IntegrationHubMark


class IntegrationHubMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[IntegrationHubMark]:
        packed = await self._session.scalars(
            select(IntegrationHubMark).order_by(
                IntegrationHubMark.mark_code,
                IntegrationHubMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: IntegrationHubMark) -> IntegrationHubMark:
        self._session.add(row)
        await self._session.flush()
        return row
