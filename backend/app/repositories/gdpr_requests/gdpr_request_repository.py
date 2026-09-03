from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gdpr_request import GdprRequest


class GdprRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[GdprRequest]:
        result = await self._session.scalars(
            select(GdprRequest).order_by(GdprRequest.created_at.desc()),
        )
        return list(result.all())

    async def get_by_id(self, request_id: UUID) -> GdprRequest | None:
        return await self._session.get(GdprRequest, request_id)

    async def add(self, row: GdprRequest) -> GdprRequest:
        self._session.add(row)
        await self._session.flush()
        return row
