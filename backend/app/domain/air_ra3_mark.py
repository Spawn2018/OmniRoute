import re

from app.domain.errors import InvalidAirRa3Mark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_AIR_KINDS = frozenset({"ra3", "lithium", "known_consignor", "other"})
_TENANT_MANUAL = "tenant:manual"
_PREFIX = "fixture://air-ra3-mark/"
_REF_CAP = 256


def parse_air_ra3_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidAirRa3Mark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidAirRa3Mark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidAirRa3Mark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _AIR_KINDS:
        raise InvalidAirRa3Mark("rodzaj: ra3, lithium, known_consignor albo other")
    if type(origin) is not str:
        raise InvalidAirRa3Mark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _TENANT_MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidAirRa3Mark("obce wskazanie zapisu znacznika air RA3")
    if len(pointer) > _REF_CAP:
        raise InvalidAirRa3Mark("obce wskazanie zapisu znacznika air RA3 za długie")
    return slug, token, pointer
