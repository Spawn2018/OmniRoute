import re

from app.domain.errors import InvalidCostAllocationMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"direct", "abc", "shared", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://cost-allocation-mark/"
_REF_CAP = 256


def parse_cost_allocation_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCostAllocationMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCostAllocationMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCostAllocationMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCostAllocationMark(
            "rodzaj: direct, abc, shared albo other",
        )
    if type(origin) is not str:
        raise InvalidCostAllocationMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCostAllocationMark("obce wskazanie zapisu znacznika cost allocation")
    if len(pointer) > _REF_CAP:
        raise InvalidCostAllocationMark(
            "obce wskazanie zapisu znacznika cost allocation za długie",
        )
    return slug, token, pointer
