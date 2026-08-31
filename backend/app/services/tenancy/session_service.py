from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session_token import encode_session_token
from app.domain.errors import Unauthenticated
from app.repositories.tenancy.app_user_repository import AppUserRepository


class SessionService:
    def __init__(self, session: AsyncSession) -> None:
        self._users = AppUserRepository(session)

    async def issue_for_app_user(self, organization_id: UUID, user_id: UUID) -> str:
        user = await self._users.get_by_id(user_id)
        if user is None or user.organization_id != organization_id:
            raise Unauthenticated("Nieznany użytkownik sesji")
        return encode_session_token(user_id=user.id, organization_id=user.organization_id)
