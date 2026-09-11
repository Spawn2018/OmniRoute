import re

from app.domain.errors import InvalidFuelAnomalyMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"card", "tank", "spike", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://fuel-anomaly-mark/"
_REF_CAP = 256


def parse_fuel_anomaly_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFuelAnomalyMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidFuelAnomalyMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFuelAnomalyMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFuelAnomalyMark(
            "rodzaj: card, tank, spike albo other",
        )
    if type(origin) is not str:
        raise InvalidFuelAnomalyMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidFuelAnomalyMark("obce wskazanie zapisu znacznika fuel anomaly")
    if len(pointer) > _REF_CAP:
        raise InvalidFuelAnomalyMark(
            "obce wskazanie zapisu znacznika fuel anomaly za długie",
        )
    return slug, token, pointer
