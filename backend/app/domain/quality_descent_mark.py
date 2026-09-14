import re

from app.domain.errors import InvalidQualityDescentMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"mae", "crps", "brier", "manual", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://quality-descent/"
_REF_CAP = 256


def parse_quality_descent_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidQualityDescentMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidQualityDescentMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidQualityDescentMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidQualityDescentMark(
            "rodzaj: mae, crps, brier, manual albo other",
        )
    if type(origin) is not str:
        raise InvalidQualityDescentMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidQualityDescentMark(
            "obce wskazanie zapisu powodu zejscia jakosci",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidQualityDescentMark(
            "obce wskazanie zapisu powodu zejscia jakosci za dlugie",
        )
    return slug, token, pointer
