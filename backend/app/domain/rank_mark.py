from app.domain.errors import InvalidRankMark

_KINDS = frozenset({"price", "transit", "reliability", "carbon", "other"})
_FIXTURE = "fixture://rank-mark/"
_MANUAL = "tenant:manual"


def require_rank_kind(raw: object) -> str:
    if not isinstance(raw, str):
        raise InvalidRankMark("ranking musi być tekstem")
    token = raw.strip().lower()
    if token in _KINDS:
        return token
    raise InvalidRankMark("ranking: allowlista HITL")


def require_rank_source_ref(raw: object) -> str:
    if not isinstance(raw, str):
        raise InvalidRankMark("source_ref musi być tekstem")
    origin = raw.strip()
    allowed = origin == _MANUAL or origin.startswith(_FIXTURE)
    if not allowed:
        if origin == "":
            raise InvalidRankMark("wskazanie zapisu osi rankingu")
        raise InvalidRankMark("obce wskazanie zapisu osi rankingu")
    if len(origin) > 256:
        raise InvalidRankMark("wskazanie zapisu osi rankingu za długie")
    return origin
