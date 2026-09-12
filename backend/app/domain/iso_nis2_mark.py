import re

from app.domain.errors import InvalidIsoNis2Mark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"iso", "nis2", "policy", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://iso-nis2-mark/"
_REF_CAP = 256


def parse_iso_nis2_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidIsoNis2Mark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidIsoNis2Mark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidIsoNis2Mark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidIsoNis2Mark(
            "rodzaj: iso, nis2, policy albo other",
        )
    if type(origin) is not str:
        raise InvalidIsoNis2Mark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidIsoNis2Mark("obce wskazanie zapisu znacznika ISO/NIS2 ops")
    if len(pointer) > _REF_CAP:
        raise InvalidIsoNis2Mark(
            "obce wskazanie zapisu znacznika ISO/NIS2 ops za długie",
        )
    return slug, token, pointer
