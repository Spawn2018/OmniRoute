import re
from datetime import date
from uuid import UUID

from app.domain.errors import InvalidShipment

_DRAFT = "draft"
_MAX_REF = 256
_FIXTURE = "fixture://shipment/"
_MANUAL = "tenant:manual"
_FIXTURE_NUM = "fixture://shipment-ref/"
_OMNI_NUM = "omni://shipment/"
_OMNI_TAIL = re.compile(r"^[a-z0-9][a-z0-9._-]{1,62}$")


def shipment_draft_status() -> str:
    return _DRAFT


def require_quotation_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipment("quotation_id musi być UUID")
    return raw


def require_party_on_quotation(raw: UUID | None) -> UUID:
    if raw is None:
        raise InvalidShipment("wycena bez kontrahenta")
    return raw


def require_shipment_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipment("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidShipment("wskazanie zapisu zlecenia")
    if len(token) > _MAX_REF:
        raise InvalidShipment("wskazanie zapisu zlecenia za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidShipment("obce wskazanie zapisu zlecenia")
    return token


def require_shipment_ref(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidShipment("numer musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_REF:
        raise InvalidShipment("numer zlecenia za długi")
    if token.startswith(_FIXTURE_NUM):
        rest = token.removeprefix(_FIXTURE_NUM)
        if rest == "":
            raise InvalidShipment("numer: allowlista HITL")
        return token
    if token.startswith(_OMNI_NUM):
        rest = token.removeprefix(_OMNI_NUM)
        if _OMNI_TAIL.fullmatch(rest) is None:
            raise InvalidShipment("numer: allowlista HITL")
        return token
    raise InvalidShipment("obce wskazanie numeru zlecenia")


def require_is_waste(raw: object) -> bool:
    if raw is None:
        return False
    if type(raw) is not bool:
        raise InvalidShipment("is_waste musi być true albo false")
    return raw


_PARENT_KINDS = frozenset({"drayage", "oncarriage", "leg_subcontract", "other"})
_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_LABEL = 128


def require_optional_label(raw: object, token: str) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidShipment(f"{token} musi być tekstem")
    label = raw.strip()
    if label == "":
        return None
    if len(label) > _MAX_LABEL:
        raise InvalidShipment(f"{token} za długi")
    return label


def require_guide_code(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidShipment("przewodnik musi być tekstem")
    slug = raw.strip()
    if not slug:
        return None
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidShipment("przewodnik: snake 2–32")
    return slug


def require_parent_shipment_id(raw: object) -> UUID | None:
    if raw is None:
        return None
    if type(raw) is not UUID:
        raise InvalidShipment("główne zlecenie musi być UUID")
    return raw


def require_relation_kind(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidShipment("rodzaj musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if token not in _PARENT_KINDS:
        raise InvalidShipment("rodzaj relacji spoza zbioru")
    return token


def require_parent_pair(
    parent_id: UUID | None,
    relation_kind: str | None,
    *,
    child_id: UUID,
) -> None:
    if parent_id is None and relation_kind is None:
        return
    if parent_id is None:
        raise InvalidShipment("główne zlecenie wymagane przy rodzaju relacji")
    if relation_kind is None:
        raise InvalidShipment("rodzaj relacji wymagany przy zleceniu głównym")
    if parent_id == child_id:
        raise InvalidShipment("główne zlecenie nie może być tym samym wierszem")


def require_shipment_anchor_date(raw: object) -> date | None:
    if raw is None:
        return None
    if type(raw) is date:
        return raw
    if type(raw) is not str:
        raise InvalidShipment("data")
    token = raw.strip()
    if token == "":
        return None
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidShipment("data") from exc
