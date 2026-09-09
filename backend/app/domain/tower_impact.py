from app.domain.errors import InvalidTowerImpact

_STAGES = frozenset({"stock", "production", "sales", "ebitda"})
_PACTS = frozenset({"missing", "recorded"})
_MAX_REF = 256
_FIXTURE = "fixture://tower-impact/"
_MANUAL = "tenant:manual"
_GAP = "brak danych umowy"


def require_chain_stage(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTowerImpact("etap musi być tekstem")
    token = raw.strip().lower()
    if token not in _STAGES:
        raise InvalidTowerImpact("etap: allowlista HITL")
    return token


def require_contract_data_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTowerImpact("umowa musi być tekstem")
    token = raw.strip().lower()
    if token not in _PACTS:
        raise InvalidTowerImpact("umowa: allowlista HITL")
    return token


def require_impact_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTowerImpact("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTowerImpact("wskazanie zapisu skutku wieży")
    if len(token) > _MAX_REF:
        raise InvalidTowerImpact("wskazanie zapisu skutku wieży za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTowerImpact("obce wskazanie zapisu skutku wieży")
    return token


def contract_gap_label(status: str) -> str | None:
    if status == "missing":
        return _GAP
    return None
