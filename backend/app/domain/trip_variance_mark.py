import re

from app.domain.errors import InvalidTripVarianceMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"expected", "actual", "gap", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://trip-variance/"
_MAX_REF = 256


def parse_trip_variance_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTripVarianceMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidTripVarianceMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidTripVarianceMark("wariancja musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidTripVarianceMark(
            "wariancja: expected, actual, gap albo other",
        )
    if type(origin) is not str:
        raise InvalidTripVarianceMark("obce wskazanie wariancji przejazdu")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidTripVarianceMark("obce wskazanie wariancji przejazdu")
    if len(pointer) > _MAX_REF:
        raise InvalidTripVarianceMark("wskazanie wariancji przejazdu za długie")
    return slug, token, pointer
