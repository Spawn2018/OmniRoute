import re

from app.domain.errors import InvalidCostCategoryMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset(
    {"direct", "shared", "allocated", "overhead", "capital", "risk", "other"},
)
_MANUAL = "tenant:manual"
_PREFIX = "fixture://cost-category-mark/"
_REF_CAP = 256


def parse_cost_category_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCostCategoryMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCostCategoryMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCostCategoryMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCostCategoryMark(
            "rodzaj: direct, shared, allocated, overhead, capital, risk albo other",
        )
    if type(origin) is not str:
        raise InvalidCostCategoryMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCostCategoryMark("obce wskazanie zapisu znacznika cost category")
    if len(pointer) > _REF_CAP:
        raise InvalidCostCategoryMark(
            "obce wskazanie zapisu znacznika cost category za długie",
        )
    return slug, token, pointer
