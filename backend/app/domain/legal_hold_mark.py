import re

from app.domain.errors import InvalidLegalHoldMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"retention", "legal_hold", "eidas"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://legal-hold-mark/"
_REF_CAP = 256


def parse_legal_hold_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLegalHoldMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidLegalHoldMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLegalHoldMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidLegalHoldMark(
            "rodzaj: retention, legal_hold albo eidas",
        )
    if type(origin) is not str:
        raise InvalidLegalHoldMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidLegalHoldMark("obce wskazanie zapisu znacznika legal hold")
    if len(pointer) > _REF_CAP:
        raise InvalidLegalHoldMark("obce wskazanie zapisu znacznika legal hold za długie")
    return slug, token, pointer
