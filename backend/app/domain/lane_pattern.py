from app.domain.errors import InvalidLanePattern, InvalidUnlocode
from app.domain.port import normalize_unlocode

_MAX_REF = 256
_FIXTURE = "fixture://lane-pattern/"
_MANUAL = "tenant:manual"


def require_pattern_pair(origin_raw: object, dest_raw: object) -> tuple[str, str]:
    if type(origin_raw) is not str or type(dest_raw) is not str:
        raise InvalidLanePattern("wzorzec musi być parą kodów UN/LOCODE")
    try:
        origin = normalize_unlocode(origin_raw)
        dest = normalize_unlocode(dest_raw)
    except InvalidUnlocode as exc:
        raise InvalidLanePattern(f"wzorzec: {exc}") from exc
    if origin == dest:
        raise InvalidLanePattern("wzorzec nie może mieć tych samych końców")
    return origin, dest


def require_pattern_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidLanePattern("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidLanePattern("wskazanie zapisu wzorca korytarza")
    if len(token) > _MAX_REF:
        raise InvalidLanePattern("wskazanie zapisu wzorca korytarza za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidLanePattern("obce wskazanie zapisu wzorca korytarza")
    return token
