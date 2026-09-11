import re

from app.domain.errors import InvalidEdiMapMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"field_map", "segment", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://edi-map-mark/"
_REF_CAP = 256


def parse_edi_map_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidEdiMapMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidEdiMapMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidEdiMapMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidEdiMapMark(
            "rodzaj: field_map, segment albo other",
        )
    if type(origin) is not str:
        raise InvalidEdiMapMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidEdiMapMark("obce wskazanie zapisu znacznika mapy EDI")
    if len(pointer) > _REF_CAP:
        raise InvalidEdiMapMark(
            "obce wskazanie zapisu znacznika mapy EDI za długie",
        )
    return slug, token, pointer
