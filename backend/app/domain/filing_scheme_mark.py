import re

from app.domain.errors import InvalidFilingSchemeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ics2", "cbam", "eudr", "efti", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://filing-scheme-mark/"
_REF_CAP = 256


def parse_filing_scheme_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFilingSchemeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidFilingSchemeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFilingSchemeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFilingSchemeMark(
            "rodzaj: ics2, cbam, eudr, efti albo other",
        )
    if type(origin) is not str:
        raise InvalidFilingSchemeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidFilingSchemeMark("obce wskazanie zapisu znacznika schematu składania")
    if len(pointer) > _REF_CAP:
        raise InvalidFilingSchemeMark(
            "obce wskazanie zapisu znacznika schematu składania za długie",
        )
    return slug, token, pointer
