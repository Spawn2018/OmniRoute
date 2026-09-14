import re

from app.domain.errors import InvalidWmsFlowMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"receipt", "location", "pick", "ship", "count", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://wms-flow/"
_REF_CAP = 256


def parse_wms_flow_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidWmsFlowMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidWmsFlowMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidWmsFlowMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidWmsFlowMark(
            "rodzaj: receipt, location, pick, ship, count albo other",
        )
    if type(origin) is not str:
        raise InvalidWmsFlowMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidWmsFlowMark("obce wskazanie zapisu WMS")
    if len(pointer) > _REF_CAP:
        raise InvalidWmsFlowMark("obce wskazanie zapisu WMS za dlugie")
    return slug, token, pointer
