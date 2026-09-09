from app.domain.errors import InvalidFreeTimeClock

_KINDS = frozenset({"demurrage", "detention", "mixed", "rollover"})
_MAX_DAYS = 3650
_MAX_REF = 256
_FIXTURE = "fixture://free-time-clock/"
_MANUAL = "tenant:manual"


def require_clock_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFreeTimeClock("rodzaj musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidFreeTimeClock("rodzaj: allowlista HITL")
    return token


def require_free_days(raw: object) -> int:
    if type(raw) is bool or type(raw) is not int:
        raise InvalidFreeTimeClock("dni muszą być liczbą całkowitą")
    if raw < 0:
        raise InvalidFreeTimeClock("dni: nieujemne")
    if raw > _MAX_DAYS:
        raise InvalidFreeTimeClock("dni: za dużo")
    return raw


def require_clock_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidFreeTimeClock("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidFreeTimeClock("wskazanie zapisu zegara D&D")
    if len(token) > _MAX_REF:
        raise InvalidFreeTimeClock("wskazanie zapisu zegara D&D za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidFreeTimeClock("obce wskazanie zapisu zegara D&D")
    return token
