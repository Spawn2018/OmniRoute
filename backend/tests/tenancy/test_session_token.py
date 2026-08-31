from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest

from app.core.config import settings
from app.core.session_token import decode_session_token, encode_session_token
from app.domain.errors import Unauthenticated


def test_roundtrip_preserves_tenant_and_user() -> None:
    user_id = uuid4()
    organization_id = uuid4()
    token = encode_session_token(user_id=user_id, organization_id=organization_id)
    identity = decode_session_token(token)
    assert identity.user_id == user_id
    assert identity.organization_id == organization_id


def test_expired_token_is_rejected() -> None:
    now = datetime.now(UTC)
    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "org": str(uuid4()),
            "iat": now - timedelta(hours=2),
            "exp": now - timedelta(hours=1),
        },
        settings.jwt_secret,
        algorithm="HS256",
    )
    with pytest.raises(Unauthenticated, match="wygasł"):
        decode_session_token(token)


def test_foreign_signature_is_rejected() -> None:
    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "org": str(uuid4()),
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "different-secret-not-the-test-one!!",
        algorithm="HS256",
    )
    with pytest.raises(Unauthenticated, match="ważnego"):
        decode_session_token(token)


def test_short_secret_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.core.config.settings.jwt_secret", "too-short")
    with pytest.raises(Unauthenticated, match="skonfigurowana"):
        encode_session_token(user_id=uuid4(), organization_id=uuid4())


def test_non_uuid_claims_are_rejected() -> None:
    token = jwt.encode(
        {
            "sub": "not-a-uuid",
            "org": "also-not",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        settings.jwt_secret,
        algorithm="HS256",
    )
    with pytest.raises(Unauthenticated, match="ważnego"):
        decode_session_token(token)
