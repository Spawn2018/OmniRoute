import re

from app.domain.errors import InvalidWorkingCapitalMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"dso", "cash_at_risk", "aging", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://working-capital-mark/"
_REF_CAP = 256


def parse_working_capital_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidWorkingCapitalMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidWorkingCapitalMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidWorkingCapitalMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidWorkingCapitalMark(
            "rodzaj: dso, cash_at_risk, aging albo other",
        )
    if type(origin) is not str:
        raise InvalidWorkingCapitalMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidWorkingCapitalMark("obce wskazanie zapisu znacznika working capital")
    if len(pointer) > _REF_CAP:
        raise InvalidWorkingCapitalMark(
            "obce wskazanie zapisu znacznika working capital za długie",
        )
    return slug, token, pointer
