from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.database import bind_tenant
from app.core.session_token import decode_session_token
from app.domain.errors import Unauthenticated
from app.models.app_user import AppUser
from app.services.tenancy.session_service import SessionService


@pytest.mark.asyncio
async def test_issue_for_known_app_user() -> None:
    org_id = uuid4()
    user_id = uuid4()
    user = AppUser(
        id=user_id,
        organization_id=org_id,
        email="dev@local.test",
        display_name="Dev Local",
    )
    session = AsyncMock()
    session.get = AsyncMock(return_value=user)
    token = await SessionService(session).issue_for_app_user(org_id, user_id)
    identity = decode_session_token(token)
    assert identity.user_id == user_id
    assert identity.organization_id == org_id


@pytest.mark.asyncio
async def test_issue_rejects_missing_user() -> None:
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    with pytest.raises(Unauthenticated):
        await SessionService(session).issue_for_app_user(uuid4(), uuid4())


@pytest.mark.asyncio
async def test_issue_rejects_user_from_other_org() -> None:
    user = AppUser(
        id=uuid4(),
        organization_id=uuid4(),
        email="a@example.com",
        display_name="A",
    )
    session = AsyncMock()
    session.get = AsyncMock(return_value=user)
    with pytest.raises(Unauthenticated):
        await SessionService(session).issue_for_app_user(uuid4(), user.id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cannot_issue_token_for_foreign_tenant(session, two_tenants) -> None:
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_b.id)
    with pytest.raises(Unauthenticated):
        await SessionService(session).issue_for_app_user(org_b.id, user_a.id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_issue_token_for_tenant_member(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    token = await SessionService(session).issue_for_app_user(org_a.id, user_a.id)
    identity = decode_session_token(token)
    assert identity.user_id == user_a.id
    assert identity.organization_id == org_a.id
