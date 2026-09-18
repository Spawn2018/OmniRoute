import re

from app.domain.errors import InvalidFilingBindMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"shipment", "scheme", "both", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://filing-bind-mark/"
_REF_CAP = 256


def parse_filing_bind_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFilingBindMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidFilingBindMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFilingBindMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFilingBindMark(
            "wiązanie: shipment, scheme, both albo other",
        )
    if type(origin) is not str:
        raise InvalidFilingBindMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidFilingBindMark(
            "obce wskazanie zapisu znacznika wiązania zgłoszenia",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidFilingBindMark(
            "obce wskazanie zapisu znacznika wiązania zgłoszenia za długie",
        )
    return slug, token, pointer
