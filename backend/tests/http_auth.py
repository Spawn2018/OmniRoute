from uuid import UUID, uuid4

from app.core.session_token import encode_session_token


def bearer_auth_headers(
    *,
    organization_id: UUID | None = None,
    user_id: UUID | None = None,
) -> dict[str, str]:
    token = encode_session_token(
        user_id=user_id or uuid4(),
        organization_id=organization_id or uuid4(),
    )
    return {"Authorization": f"Bearer {token}"}
