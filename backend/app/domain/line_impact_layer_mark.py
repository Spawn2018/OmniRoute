import re

from app.domain.errors import InvalidLineImpactLayerMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"scored", "forecast", "actual", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://line-impact-layer/"
_REF_CAP = 256


def parse_line_impact_layer_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLineImpactLayerMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidLineImpactLayerMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLineImpactLayerMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidLineImpactLayerMark(
            "rodzaj: scored, forecast, actual albo other",
        )
    if type(origin) is not str:
        raise InvalidLineImpactLayerMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidLineImpactLayerMark(
            "obce wskazanie zapisu warstwy wpływu na linię",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidLineImpactLayerMark(
            "obce wskazanie zapisu warstwy wpływu na linię za dlugie",
        )
    return slug, token, pointer
