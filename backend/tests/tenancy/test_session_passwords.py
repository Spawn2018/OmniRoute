from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from app.api.session import SessionTokenRequest
from app.core.database import get_session
from app.core.password_hash import hash_password
from app.main import app
from app.models.app_user import AppUser
from app.models.refresh_token import RefreshToken
from app.repositories.tenancy.app_user_repository import AppUserRepository
from app.repositories.tenancy.refresh_token_repository import RefreshTokenRepository

_EMAIL = "a@example.com"
_PASSWORD = "correct-horse-battery"
_PASSWORD_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"


@pytest.fixture(autouse=True)
def _in_memory_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    user = AppUser(
        id=uuid4(),
        organization_id=uuid4(),
        email=_EMAIL,
        display_name="A",
        password_hash=hash_password(_PASSWORD),
    )
    stored: dict[str, RefreshToken] = {}

    async def get_by_email(_self: AppUserRepository, email: str) -> AppUser | None:
        if email == user.email:
            return user
        return None

    async def get_by_token_hash(
        _self: RefreshTokenRepository, token_hash: str
    ) -> RefreshToken | None:
        row = stored.get(token_hash)
        if row is None or row.revoked_at is not None:
            return None
        return row

    async def add(_self: RefreshTokenRepository, token: RefreshToken) -> RefreshToken:
        stored[token.token_hash] = token
        return token

    async def revoke(_self: RefreshTokenRepository, token: RefreshToken) -> None:
        token.revoked_at = datetime.now(UTC)

    monkeypatch.setattr(AppUserRepository, "get_by_email", get_by_email)
    monkeypatch.setattr(RefreshTokenRepository, "get_by_token_hash", get_by_token_hash)
    monkeypatch.setattr(RefreshTokenRepository, "add", add)
    monkeypatch.setattr(RefreshTokenRepository, "revoke", revoke)

    fake_session = AsyncMock()
    fake_session.execute = AsyncMock()

    async def override_session() -> object:
        yield fake_session

    app.dependency_overrides[get_session] = override_session
    yield
    app.dependency_overrides.pop(get_session, None)


def test_session_token_issues_access_and_refresh_for_email_and_password() -> None:
    response = TestClient(app).post(
        "/api/v1/session/token",
        json={"email": _EMAIL, "password": _PASSWORD},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    assert "password" not in body
    assert "password_hash" not in body


def test_session_token_request_is_email_and_password_not_user_ids() -> None:
    assert set(SessionTokenRequest.model_fields) == {"email", "password"}


def test_app_user_stores_password_hash_not_plaintext_password() -> None:
    assert "password_hash" in AppUser.__table__.columns
    assert "password" not in AppUser.__table__.columns


def test_session_refresh_rejects_a_reused_refresh_token() -> None:
    client = TestClient(app)
    login = client.post(
        "/api/v1/session/token",
        json={"email": _EMAIL, "password": _PASSWORD},
    )
    assert login.status_code == 201
    first_refresh = login.json()["refresh_token"]
    rotated = client.post(
        "/api/v1/session/refresh",
        json={"refresh_token": first_refresh},
    )
    assert rotated.status_code == 200
    assert rotated.json()["refresh_token"] != first_refresh
    reused = client.post(
        "/api/v1/session/refresh",
        json={"refresh_token": first_refresh},
    )
    assert reused.status_code == 401


@given(st.text(alphabet=_PASSWORD_ALPHABET, min_size=8, max_size=64))
@settings(max_examples=15, deadline=None)
def test_a_password_other_than_the_stored_one_does_not_issue_tokens(candidate: str) -> None:
    assume(candidate != _PASSWORD)
    response = TestClient(app).post(
        "/api/v1/session/token",
        json={"email": _EMAIL, "password": candidate},
    )
    assert response.status_code == 401
    assert "access_token" not in response.json()
