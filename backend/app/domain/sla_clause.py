import re
from uuid import UUID

from app.domain.errors import InvalidSlaClause

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_METRICS = frozenset({"otif", "delay", "damage", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://sla-clause/"
_REF_CAP = 256
_MAX_LABEL = 128


def parse_sla_clause_row(
    *,
    customer_contract_id: object,
    clause_code: object,
    metric_kind: object,
    threshold_label: object,
    source_ref: object,
) -> tuple[UUID, str, str, str, str]:
    return (
        _require_contract(customer_contract_id),
        _require_code(clause_code),
        _require_metric(metric_kind),
        _require_threshold(threshold_label),
        _require_origin(source_ref),
    )


def _require_contract(raw: object) -> UUID:
    if type(raw) is UUID:
        return raw
    raise InvalidSlaClause("nieznana umowa")


def _require_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSlaClause("oznaczenie musi być tekstem")
    slug = raw.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSlaClause("oznaczenie: snake 2–32")
    return slug


def _require_metric(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSlaClause("metryka musi być tekstem")
    token = raw.strip().lower()
    if token not in _METRICS:
        raise InvalidSlaClause("metryka: otif, delay, damage albo other")
    return token


def _require_threshold(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSlaClause("prog musi być tekstem")
    label = raw.strip()
    if not label or len(label) > _MAX_LABEL:
        raise InvalidSlaClause("prog: tekst 1–128")
    return label


def _require_origin(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSlaClause("obce source_ref")
    pointer = raw.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSlaClause("obce wskazanie zapisu klauzuli SLA")
    if len(pointer) > _REF_CAP:
        raise InvalidSlaClause("obce wskazanie zapisu klauzuli SLA za długie")
    return pointer
