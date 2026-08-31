from collections.abc import Callable
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import bind_tenant, get_session
from app.domain.errors import PermissionDenied
from app.integrations.openfga.client import AuthzChecker, OpenFgaAuthz, build_openfga_client

_authz: AuthzChecker | None = None


def set_authz_checker(checker: AuthzChecker | None) -> None:
    global _authz
    _authz = checker


async def get_authz() -> AuthzChecker:
    if _authz is not None:
        return _authz
    client = await build_openfga_client()
    return OpenFgaAuthz(client)


async def tenant_session(
    x_organization_id: UUID = Header(..., alias="X-Organization-Id"),
    session: AsyncSession = Depends(get_session),
) -> AsyncSession:
    await bind_tenant(session, x_organization_id)
    return session


async def require_tenant_session(
    session: AsyncSession = Depends(tenant_session),
) -> AsyncSession:
    return session


def require_permission(relation: str, object_type: str) -> Callable[..., object]:
    async def _check(
        x_organization_id: Annotated[UUID, Header(alias="X-Organization-Id")],
        x_user_id: Annotated[UUID, Header(alias="X-User-Id")],
        authz: Annotated[AuthzChecker, Depends(get_authz)],
    ) -> None:
        allowed = await authz.check(
            user_id=x_user_id,
            relation=relation,
            object_type=object_type,
            object_id=x_organization_id,
        )
        if not allowed:
            raise PermissionDenied(f"Brak uprawnienia {relation} na {object_type}")

    return _check
