import re

from app.domain.errors import InvalidPoFinancingMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"po", "release", "advance", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://po-financing/"
_REF_CAP = 256


def parse_po_financing_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPoFinancingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPoFinancingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPoFinancingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPoFinancingMark("rodzaj: po, release, advance albo other")
    if type(origin) is not str:
        raise InvalidPoFinancingMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPoFinancingMark("obce wskazanie zapisu PO Financing")
    if len(pointer) > _REF_CAP:
        raise InvalidPoFinancingMark("obce wskazanie zapisu PO Financing za dlugie")
    return slug, token, pointer
