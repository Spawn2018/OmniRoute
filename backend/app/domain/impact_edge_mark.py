import re

from app.domain.errors import InvalidImpactEdgeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset(
    {"shipment", "inventory", "sku", "line", "order", "revenue", "margin", "cash", "other"},
)
_MANUAL = "tenant:manual"
_PREFIX = "fixture://impact-edge-mark/"
_REF_CAP = 256
_KIND_HINT = "shipment, inventory, sku, line, order, revenue, margin, cash albo other"


def _parse_kind(kind: object, label: str) -> str:
    if type(kind) is not str:
        raise InvalidImpactEdgeMark(f"{label} musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidImpactEdgeMark(f"{label}: {_KIND_HINT}")
    return token


def parse_impact_edge_mark_row(
    code: object,
    from_kind: object,
    to_kind: object,
    origin: object,
) -> tuple[str, str, str, str]:
    if type(code) is not str:
        raise InvalidImpactEdgeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidImpactEdgeMark("oznaczenie: snake 2–32")
    start = _parse_kind(from_kind, "from_kind")
    end = _parse_kind(to_kind, "to_kind")
    if type(origin) is not str:
        raise InvalidImpactEdgeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidImpactEdgeMark("obce wskazanie zapisu znacznika impact edge")
    if len(pointer) > _REF_CAP:
        raise InvalidImpactEdgeMark(
            "obce wskazanie zapisu znacznika impact edge za długie",
        )
    return slug, start, end, pointer
