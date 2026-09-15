import re

from app.domain.errors import InvalidShipperAwardMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"go", "hold", "no_award", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://shipper-award-mark/"
_LIMIT = 256


def parse_shipper_award_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidShipperAwardMark("kod award musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidShipperAwardMark("kod award: snake 2–32")
    if type(kind) is not str:
        raise InvalidShipperAwardMark("award_kind musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidShipperAwardMark("award_kind: go, hold, no_award albo other")
    if type(origin) is not str:
        raise InvalidShipperAwardMark("source_ref award obce")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_PREFIX):
        raise InvalidShipperAwardMark("source_ref award obce")
    if len(pointer) > _LIMIT:
        raise InvalidShipperAwardMark("source_ref award za długie")
    return slug, token, pointer
