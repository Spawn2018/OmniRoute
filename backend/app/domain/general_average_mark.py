import re

from app.domain.errors import InvalidGeneralAverageMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ga", "contribution", "sacrifice", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://general-average-mark/"
_REF_CAP = 256


def parse_general_average_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidGeneralAverageMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidGeneralAverageMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidGeneralAverageMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidGeneralAverageMark(
            "rodzaj: ga, contribution, sacrifice albo other",
        )
    if type(origin) is not str:
        raise InvalidGeneralAverageMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidGeneralAverageMark("obce wskazanie zapisu znacznika general average")
    if len(pointer) > _REF_CAP:
        raise InvalidGeneralAverageMark(
            "obce wskazanie zapisu znacznika general average za długie",
        )
    return slug, token, pointer
