from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import bind_tenant, get_session
from app.core.session_token import SessionIdentity, decode_session_token
from app.domain.errors import PermissionDenied, Unauthenticated
from app.integrations.openfga.client import AuthzChecker, OpenFgaAuthz, build_openfga_client

_authz: AuthzChecker | None = None
_bearer = HTTPBearer(auto_error=False)


def set_authz_checker(checker: AuthzChecker | None) -> None:
    global _authz
    _authz = checker


async def get_authz() -> AuthzChecker:
    if _authz is not None:
        return _authz
    client = await build_openfga_client()
    return OpenFgaAuthz(client)


async def get_current_identity(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> SessionIdentity:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise Unauthenticated("Brak tokenu sesji")
    return decode_session_token(credentials.credentials)


async def tenant_session(
    identity: Annotated[SessionIdentity, Depends(get_current_identity)],
    session: AsyncSession = Depends(get_session),
) -> AsyncSession:
    await bind_tenant(session, identity.organization_id)
    return session


async def require_tenant_session(
    session: AsyncSession = Depends(tenant_session),
) -> AsyncSession:
    return session


def require_permission(relation: str, object_type: str) -> Callable[..., object]:
    async def _check(
        identity: Annotated[SessionIdentity, Depends(get_current_identity)],
        authz: Annotated[AuthzChecker, Depends(get_authz)],
    ) -> None:
        allowed = await authz.check(
            user_id=identity.user_id,
            relation=relation,
            object_type=object_type,
            object_id=identity.organization_id,
        )
        if not allowed:
            raise PermissionDenied(f"Brak uprawnienia {relation} na {object_type}")

    return _check
