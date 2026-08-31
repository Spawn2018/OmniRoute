from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import bind_tenant, get_session


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
