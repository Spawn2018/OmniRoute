import re
from uuid import UUID

from app.domain.errors import InvalidAsn

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://asn/"
_REF_CAP = 256
_MAX_LABEL = 128


def parse_asn_row(
    *,
    purchase_order_id: object,
    asn_code: object,
    plant_label: object,
    carrier_label: object,
    ship_ref_label: object,
    source_ref: object,
) -> tuple[UUID, str, str | None, str | None, str | None, str]:
    return (
        _require_header(purchase_order_id),
        _require_asn_code(asn_code),
        _optional_label(plant_label, "zakład"),
        _optional_label(carrier_label, "przewoźnik"),
        _optional_label(ship_ref_label, "referencja"),
        _require_origin(source_ref),
    )


def _require_header(raw: object) -> UUID:
    if type(raw) is UUID:
        return raw
    raise InvalidAsn("nieznane zamówienie")


def _require_asn_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidAsn("awizo musi być tekstem")
    slug = raw.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidAsn("awizo: snake 2–32")
    return slug


def _optional_label(raw: object, token: str) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidAsn(f"{token} musi być tekstem")
    label = raw.strip()
    if not label:
        return None
    if len(label) > _MAX_LABEL:
        raise InvalidAsn(f"{token}: tekst 1–128")
    return label


def _require_origin(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidAsn("obce source_ref")
    pointer = raw.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known or len(pointer) > _REF_CAP:
        raise InvalidAsn("obce wskazanie zapisu awiza wysyłki")
    return pointer
