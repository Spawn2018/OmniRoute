import re

from app.domain.errors import InvalidShipmentMonitoringFiling

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"open", "filed", "closed", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://shipment-monitoring-filing/"
_REF_CAP = 256


def parse_shipment_monitoring_filing_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidShipmentMonitoringFiling("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidShipmentMonitoringFiling("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidShipmentMonitoringFiling("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidShipmentMonitoringFiling(
            "status: open, filed, closed albo other",
        )
    if type(origin) is not str:
        raise InvalidShipmentMonitoringFiling("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidShipmentMonitoringFiling("obce wskazanie zapisu znacznika zgloszenia SENT/BDO")
    if len(pointer) > _REF_CAP:
        raise InvalidShipmentMonitoringFiling(
            "obce wskazanie zapisu znacznika zgloszenia SENT/BDO za długie",
        )
    return slug, token, pointer
