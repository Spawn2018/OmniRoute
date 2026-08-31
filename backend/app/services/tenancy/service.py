from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_user import AppUser
from app.repositories.tenancy.app_user_repository import AppUserRepository


class TenancyService:
    def __init__(self, session: AsyncSession) -> None:
        self._users = AppUserRepository(session)

    async def list_users(self) -> list[AppUser]:
        return await self._users.list_for_tenant()

    async def get_user(self, user_id: UUID) -> AppUser | None:
        return await self._users.get_by_id(user_id)
