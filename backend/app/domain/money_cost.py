from uuid import UUID

from app.domain.errors import InvalidMoneyCost

_MAX_REF = 256
_FIXTURE = "fixture://money-cost/"
_MANUAL = "tenant:manual"


def require_cost_payment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidMoneyCost("bank_payment_id musi być UUID")
    return raw


def require_cost_rate_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidMoneyCost("nbp_rate_id musi być UUID")
    return raw


def require_cost_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMoneyCost("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidMoneyCost("wskazanie zapisu kosztu")
    if len(token) > _MAX_REF:
        raise InvalidMoneyCost("wskazanie zapisu kosztu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidMoneyCost("obce wskazanie zapisu kosztu")
    return token
