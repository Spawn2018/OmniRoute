import re

from app.domain.errors import InvalidImpactNodeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset(
    {"shipment", "inventory", "sku", "line", "order", "revenue", "margin", "cash", "other"},
)
_MANUAL = "tenant:manual"
_PREFIX = "fixture://impact-node-mark/"
_REF_CAP = 256


def parse_impact_node_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidImpactNodeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidImpactNodeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidImpactNodeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidImpactNodeMark(
            "rodzaj: shipment, inventory, sku, line, order, revenue, margin, cash albo other",
        )
    if type(origin) is not str:
        raise InvalidImpactNodeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidImpactNodeMark("obce wskazanie zapisu znacznika impact node")
    if len(pointer) > _REF_CAP:
        raise InvalidImpactNodeMark(
            "obce wskazanie zapisu znacznika impact node za długie",
        )
    return slug, token, pointer
