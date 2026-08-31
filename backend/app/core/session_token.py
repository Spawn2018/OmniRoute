from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

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
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
            "jti": str(uuid4()),
            "ver": settings.jwt_token_version,
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
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={"require": ["exp", "sub", "org", "iss", "aud", "jti", "ver"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise Unauthenticated("Token sesji wygasł") from exc
    except jwt.InvalidTokenError as exc:
        raise Unauthenticated("Brak ważnego tokenu sesji") from exc

    if not isinstance(raw, dict):
        raise Unauthenticated("Brak ważnego tokenu sesji")
    sub: object = raw.get("sub")
    org: object = raw.get("org")
    ver: object = raw.get("ver")
    jti: object = raw.get("jti")
    if not isinstance(sub, str) or not isinstance(org, str):
        raise Unauthenticated("Brak ważnego tokenu sesji")
    if not isinstance(jti, str) or jti == "":
        raise Unauthenticated("Brak ważnego tokenu sesji")
    if ver != settings.jwt_token_version:
        raise Unauthenticated("Brak ważnego tokenu sesji")
    try:
        return SessionIdentity(user_id=UUID(sub), organization_id=UUID(org))
    except ValueError as exc:
        raise Unauthenticated("Brak ważnego tokenu sesji") from exc
