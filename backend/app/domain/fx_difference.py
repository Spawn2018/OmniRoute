from uuid import UUID

from app.domain.errors import InvalidFxDifference

_MAX_REF = 256
_FIXTURE = "fixture://fx-difference/"
_MANUAL = "tenant:manual"


def require_fx_quotation_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidFxDifference("quotation_id musi być UUID")
    return raw


def require_fx_rate_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidFxDifference("nbp_rate_id musi być UUID")
    return raw


def require_fx_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFxDifference("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidFxDifference("wskazanie zapisu różnicy")
    if len(token) > _MAX_REF:
        raise InvalidFxDifference("wskazanie zapisu różnicy za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidFxDifference("obce wskazanie zapisu różnicy")
    return token
