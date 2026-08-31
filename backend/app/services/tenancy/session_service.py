from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import bind_tenant
from app.core.password_hash import dummy_password_hash, verify_password
from app.core.refresh_secret import hash_refresh_secret
from app.core.session_token import encode_session_token
from app.domain.errors import Unauthenticated
from app.models.app_user import AppUser
from app.models.refresh_token import RefreshToken
from app.repositories.tenancy.app_user_repository import AppUserRepository
from app.repositories.tenancy.refresh_token_repository import RefreshTokenRepository

_LOGIN_FAIL = "Nieprawidłowy email lub hasło"


@dataclass(frozen=True)
class IssuedSession:
    access_token: str
    refresh_token: str


async def _bind_login_email(session: AsyncSession, email: str) -> None:
    await session.execute(
        text("SELECT set_config('app.login_email', :email, true)"),
        {"email": email},
    )


async def _bind_refresh_hash(session: AsyncSession, token_hash: str) -> None:
    await session.execute(
        text("SELECT set_config('app.refresh_hash', :token_hash, true)"),
        {"token_hash": token_hash},
    )


class SessionService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = AppUserRepository(session)
        self._refresh = RefreshTokenRepository(session)

    async def issue_for_app_user(self, organization_id: UUID, user_id: UUID) -> str:
        user = await self._users.get_by_id(user_id)
        if user is None or user.organization_id != organization_id:
            raise Unauthenticated("Nieznany użytkownik sesji")
        return encode_session_token(user_id=user.id, organization_id=user.organization_id)

    async def issue_for_credentials(self, email: str, password: str) -> IssuedSession:
        user = await self._user_for_email_password(email, password)
        await bind_tenant(self._session, user.organization_id)
        return await self._issue_pair(user_id=user.id, organization_id=user.organization_id)

    async def rotate_refresh(self, refresh_secret: str) -> IssuedSession:
        row = await self._active_refresh(refresh_secret)
        if row.expires_at <= datetime.now(UTC):
            raise Unauthenticated(_LOGIN_FAIL)
        await bind_tenant(self._session, row.organization_id)
        await self._refresh.revoke(row)
        return await self._issue_pair(user_id=row.user_id, organization_id=row.organization_id)

    async def _user_for_email_password(self, email: str, password: str) -> AppUser:
        await _bind_login_email(self._session, email)
        user = await self._users.get_by_email(email)
        await _bind_login_email(self._session, "")
        if user is None or user.password_hash is None:
            verify_password(password_hash=dummy_password_hash(), password=password)
            raise Unauthenticated(_LOGIN_FAIL)
        if not verify_password(password_hash=user.password_hash, password=password):
            raise Unauthenticated(_LOGIN_FAIL)
        return user

    async def _active_refresh(self, refresh_secret: str) -> RefreshToken:
        token_hash = hash_refresh_secret(refresh_secret)
        await _bind_refresh_hash(self._session, token_hash)
        row = await self._refresh.get_by_token_hash(token_hash)
        await _bind_refresh_hash(self._session, "")
        if row is None:
            raise Unauthenticated(_LOGIN_FAIL)
        return row

    async def _issue_pair(self, *, user_id: UUID, organization_id: UUID) -> IssuedSession:
        secret = token_urlsafe(32)
        expires = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_expire_days)
        await self._refresh.add(
            RefreshToken(
                id=uuid4(),
                organization_id=organization_id,
                user_id=user_id,
                token_hash=hash_refresh_secret(secret),
                expires_at=expires,
                created_by=user_id,
            ),
        )
        access = encode_session_token(user_id=user_id, organization_id=organization_id)
        return IssuedSession(access_token=access, refresh_token=secret)
