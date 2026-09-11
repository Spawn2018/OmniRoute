import re
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidPoLine

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://po-line/"
_REF_CAP = 256
_MAX_SKU = 64
_MAX_UOM = 16
_MAX_LABEL = 128
_FOUR = Decimal("0.0001")


def parse_po_line_row(
    *,
    purchase_order_id: object,
    line_code: object,
    sku_code: object,
    qty: object,
    uom_code: object,
    plant_label: object,
    batch_label: object,
    serial_label: object,
    coo_label: object,
    source_ref: object,
) -> tuple[UUID, str, str, Decimal, str, str | None, str | None, str | None, str | None, str]:
    return (
        _require_header(purchase_order_id),
        _require_line_code(line_code),
        _require_sku(sku_code),
        _require_qty(qty),
        _require_uom(uom_code),
        _optional_label(plant_label, "zakład"),
        _optional_label(batch_label, "partia"),
        _optional_label(serial_label, "seria"),
        _optional_label(coo_label, "kraj"),
        _require_origin(source_ref),
    )


def _require_header(raw: object) -> UUID:
    if type(raw) is UUID:
        return raw
    raise InvalidPoLine("nieznane zamówienie")


def _require_line_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPoLine("linia musi być tekstem")
    slug = raw.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPoLine("linia: snake 2–32")
    return slug


def _require_sku(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPoLine("sku musi być tekstem")
    token = raw.strip()
    if not token or len(token) > _MAX_SKU:
        raise InvalidPoLine("sku: tekst 1–64")
    return token


def _require_qty(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidPoLine("ilość nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidPoLine("ilość musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidPoLine("ilość musi być liczbą dziesiętną") from exc
    if parsed < 0:
        raise InvalidPoLine("ilość nie może być ujemne")
    return parsed.quantize(_FOUR)


def _require_uom(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPoLine("jm musi być tekstem")
    token = raw.strip()
    if not token or len(token) > _MAX_UOM:
        raise InvalidPoLine("jm: tekst 1–16")
    return token


def _optional_label(raw: object, token: str) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidPoLine(f"{token} musi być tekstem")
    label = raw.strip()
    if not label:
        return None
    if len(label) > _MAX_LABEL:
        raise InvalidPoLine(f"{token}: tekst 1–128")
    return label


def _require_origin(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPoLine("obce source_ref")
    pointer = raw.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known or len(pointer) > _REF_CAP:
        raise InvalidPoLine("obce wskazanie zapisu linii zamówienia")
    return pointer
