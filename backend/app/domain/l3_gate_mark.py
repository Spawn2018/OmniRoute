import re

from app.domain.errors import InvalidL3GateMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"sot", "owner", "exception", "rollback", "blast", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://l3-gate/"
_REF_CAP = 256


def parse_l3_gate_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidL3GateMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidL3GateMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidL3GateMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidL3GateMark(
            "rodzaj: sot, owner, exception, rollback, blast albo other",
        )
    if type(origin) is not str:
        raise InvalidL3GateMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidL3GateMark(
            "obce wskazanie zapisu checklisty bramy L3",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidL3GateMark(
            "obce wskazanie zapisu checklisty bramy L3 za dlugie",
        )
    return slug, token, pointer
