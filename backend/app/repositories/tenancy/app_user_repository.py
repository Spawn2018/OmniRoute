from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_user import AppUser


class AppUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_tenant(self) -> list[AppUser]:
        result = await self._session.scalars(select(AppUser).order_by(AppUser.email))
        return list(result.all())

    async def get_by_id(self, user_id: UUID) -> AppUser | None:
        return await self._session.get(AppUser, user_id)
