from datetime import date
from uuid import UUID

from app.domain.errors import InvalidResource
from app.domain.resource import require_resource_source_ref

_KINDS = frozenset({"licence", "insurance", "other"})


def require_document_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidResource("rodzaj dokumentu")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidResource("rodzaj dokumentu")
    return token


def require_valid_until(raw: object) -> date:
    if type(raw) is not str:
        raise InvalidResource("ważność")
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise InvalidResource("ważność") from exc


def require_fleet_resource_id(raw: object) -> UUID:
    if isinstance(raw, UUID):
        return raw
    if type(raw) is not str:
        raise InvalidResource("zasób")
    try:
        return UUID(raw)
    except ValueError as exc:
        raise InvalidResource("zasób") from exc


def parse_resource_document(
    resource_id: object,
    document_kind: object,
    valid_until: object,
    source_ref: object,
) -> tuple[UUID, str, date, str]:
    return (
        require_fleet_resource_id(resource_id),
        require_document_kind(document_kind),
        require_valid_until(valid_until),
        require_resource_source_ref(source_ref),
    )
