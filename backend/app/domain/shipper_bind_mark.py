import re

from app.domain.errors import InvalidShipperBindMark

_SHIPPER_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_SHIPPER_KINDS = frozenset({"tender", "party", "other"})
_SHIPPER_MANUAL = "tenant:manual"
_SHIPPER_FIXTURE = "fixture://shipper-bind-mark/"
_SHIPPER_REF_MAX = 256


def parse_shipper_bind_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidShipperBindMark("mark_code musi być tekstem")
    slug = code.strip()
    if _SHIPPER_CODE.fullmatch(slug) is None:
        raise InvalidShipperBindMark("mark_code: snake_case 2–32")
    if type(kind) is not str:
        raise InvalidShipperBindMark("bind_kind musi być tekstem")
    token = kind.strip().lower()
    if token not in _SHIPPER_KINDS:
        raise InvalidShipperBindMark("bind_kind: tender, party albo other")
    if type(origin) is not str:
        raise InvalidShipperBindMark("source_ref obce")
    pointer = origin.strip()
    if pointer != _SHIPPER_MANUAL and not pointer.startswith(_SHIPPER_FIXTURE):
        raise InvalidShipperBindMark("source_ref shipper_bind obce")
    if len(pointer) > _SHIPPER_REF_MAX:
        raise InvalidShipperBindMark("source_ref shipper_bind za długie")
    return slug, token, pointer
