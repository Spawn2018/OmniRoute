from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from app.core.config import settings
from app.domain.errors import Unauthenticated

_JWT_ALG = "HS256"
_MIN_SECRET_LEN = 32


@dataclass(frozen=True)
class SessionIdentity:
    user_id: UUID
    organization_id: UUID


def _secret() -> str:
    secret = settings.jwt_secret
    if len(secret) < _MIN_SECRET_LEN:
        raise Unauthenticated("Sesja nie jest skonfigurowana")
    return secret


def encode_session_token(*, user_id: UUID, organization_id: UUID) -> str:
    now = datetime.now(UTC)
    return jwt.encode(
        {
            "sub": str(user_id),
            "org": str(organization_id),
            "iat": now,
            "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
        },
        _secret(),
        algorithm=_JWT_ALG,
    )


def decode_session_token(token: str) -> SessionIdentity:
    try:
        raw: object = jwt.decode(
            token,
            _secret(),
            algorithms=[_JWT_ALG],
            options={"require": ["exp", "sub", "org"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise Unauthenticated("Token sesji wygasł") from exc
    except jwt.InvalidTokenError as exc:
        raise Unauthenticated("Brak ważnego tokenu sesji") from exc

    if not isinstance(raw, dict):
        raise Unauthenticated("Brak ważnego tokenu sesji")
    sub: object = raw.get("sub")
    org: object = raw.get("org")
    if not isinstance(sub, str) or not isinstance(org, str):
        raise Unauthenticated("Brak ważnego tokenu sesji")
    try:
        return SessionIdentity(user_id=UUID(sub), organization_id=UUID(org))
    except ValueError as exc:
        raise Unauthenticated("Brak ważnego tokenu sesji") from exc
