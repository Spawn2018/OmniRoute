import re

from app.domain.errors import InvalidSpendMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"invoice", "clause", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://spend-mark/"
_REF_CAP = 256


def parse_spend_mark_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSpendMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSpendMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSpendMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSpendMark("rodzaj: invoice, clause albo other")
    if type(origin) is not str:
        raise InvalidSpendMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSpendMark("obce wskazanie zapisu znacznika wycieku")
    if len(pointer) > _REF_CAP:
        raise InvalidSpendMark("obce wskazanie zapisu znacznika wycieku za długie")
    return slug, token, pointer
