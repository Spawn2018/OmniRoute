from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest

from app.core.config import Settings, settings
from app.core.session_token import decode_session_token, encode_session_token
from app.domain.errors import Unauthenticated


def _claims(*, expired: bool = False, **overrides: object) -> dict[str, object]:
    now = datetime.now(UTC)
    payload: dict[str, object] = {
        "sub": str(uuid4()),
        "org": str(uuid4()),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "jti": str(uuid4()),
        "ver": settings.jwt_token_version,
        "iat": now,
        "exp": now - timedelta(hours=1) if expired else now + timedelta(minutes=5),
    }
    payload.update(overrides)
    return payload


def test_hello_ttl_default_is_fifteen_minutes() -> None:
    assert Settings.model_fields["jwt_expire_minutes"].default == 15


def test_roundtrip_includes_jti_iss_aud_ver() -> None:
    token = encode_session_token(user_id=uuid4(), organization_id=uuid4())
    raw = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )
    assert raw["iss"] == "omniroute"
    assert raw["aud"] == "omniroute-api"
    assert raw["jti"]
    assert raw["ver"] == 1


def test_roundtrip_preserves_tenant_and_user() -> None:
    user_id = uuid4()
    organization_id = uuid4()
    token = encode_session_token(user_id=user_id, organization_id=organization_id)
    identity = decode_session_token(token)
    assert identity.user_id == user_id
    assert identity.organization_id == organization_id


def test_expired_token_is_rejected() -> None:
    token = jwt.encode(_claims(expired=True), settings.jwt_secret, algorithm="HS256")
    with pytest.raises(Unauthenticated, match="wygasł"):
        decode_session_token(token)


def test_foreign_signature_is_rejected() -> None:
    token = jwt.encode(
        _claims(),
        "different-secret-not-the-test-one!!",
        algorithm="HS256",
    )
    with pytest.raises(Unauthenticated, match="ważnego"):
        decode_session_token(token)


def test_wrong_issuer_is_rejected() -> None:
    token = jwt.encode(_claims(iss="other"), settings.jwt_secret, algorithm="HS256")
    with pytest.raises(Unauthenticated, match="ważnego"):
        decode_session_token(token)


def test_wrong_token_version_is_rejected() -> None:
    token = jwt.encode(_claims(ver=99), settings.jwt_secret, algorithm="HS256")
    with pytest.raises(Unauthenticated, match="ważnego"):
        decode_session_token(token)


def test_short_secret_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.core.config.settings.jwt_secret", "too-short")
    with pytest.raises(Unauthenticated, match="skonfigurowana"):
        encode_session_token(user_id=uuid4(), organization_id=uuid4())


def test_non_uuid_claims_are_rejected() -> None:
    token = jwt.encode(
        _claims(sub="not-a-uuid", org="also-not"),
        settings.jwt_secret,
        algorithm="HS256",
    )
    with pytest.raises(Unauthenticated, match="ważnego"):
        decode_session_token(token)
