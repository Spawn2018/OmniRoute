import re

from app.domain.errors import InvalidFieldConfidenceMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"green", "yellow", "orange", "hold", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://field-confidence/"
_REF_CAP = 256


def parse_field_confidence_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFieldConfidenceMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidFieldConfidenceMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFieldConfidenceMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFieldConfidenceMark(
            "rodzaj: green, yellow, orange, hold albo other",
        )
    if type(origin) is not str:
        raise InvalidFieldConfidenceMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidFieldConfidenceMark(
            "obce wskazanie zapisu pasma pewnosci per pole",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidFieldConfidenceMark(
            "obce wskazanie zapisu pasma pewnosci per pole za dlugie",
        )
    return slug, token, pointer
