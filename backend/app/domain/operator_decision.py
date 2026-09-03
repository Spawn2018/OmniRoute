from uuid import UUID

from app.domain.errors import InvalidOperatorDecision
from app.domain.rate_line import require_source_ref

_PENDING = "pending"
_INBOUND = "inbound_message"
_DECIDE = frozenset({"accepted", "rejected"})


def operator_decision_pending_status() -> str:
    return _PENDING


def require_decision_source_ref(raw: object) -> str:
    return require_source_ref(raw)


def require_subject_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOperatorDecision("subject_kind musi być tekstem")
    token = raw.strip()
    if token != _INBOUND:
        raise InvalidOperatorDecision("subject_kind: tylko inbound_message")
    return token


def require_subject_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidOperatorDecision("subject_id musi być UUID")
    return raw


def require_decide_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOperatorDecision("status decyzji musi być tekstem")
    token = raw.strip()
    if token not in _DECIDE:
        raise InvalidOperatorDecision("status: accepted albo rejected")
    return token


def require_pending_before_decide(current: str) -> str:
    if current != _PENDING:
        raise InvalidOperatorDecision("decyzja już zapisana")
    return current
