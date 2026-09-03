from uuid import UUID

from app.domain.errors import InvalidCostToServe

_MAX_REF = 256
_FIXTURE = "fixture://cost-to-serve/"
_MANUAL = "tenant:manual"


def require_cost_to_serve_sop_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCostToServe("customer_sop_id musi być UUID")
    return raw


def require_cost_to_serve_quotation_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCostToServe("quotation_id musi być UUID")
    return raw


def require_cost_to_serve_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCostToServe("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCostToServe("wskazanie zapisu kosztu obsługi")
    if len(token) > _MAX_REF:
        raise InvalidCostToServe("wskazanie zapisu kosztu obsługi za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCostToServe("obce wskazanie zapisu kosztu obsługi")
    return token
