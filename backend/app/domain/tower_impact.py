from app.domain.errors import InvalidTowerImpact

_STAGES = ("stock", "production", "sales", "ebitda")
_PACTS = ("missing", "recorded")
_FIXTURE = "fixture://tower-impact/"
_MANUAL = "tenant:manual"
_GAP = "brak danych umowy"


def require_chain_stage(raw: object) -> str:
    match raw:
        case str() as text:
            token = text.strip().lower()
            if token in _STAGES:
                return token
            raise InvalidTowerImpact("etap: allowlista HITL")
        case _:
            raise InvalidTowerImpact("etap musi być tekstem")


def require_contract_data_status(raw: object) -> str:
    match raw:
        case str() as text:
            token = text.strip().lower()
            if token in _PACTS:
                return token
            raise InvalidTowerImpact("umowa: allowlista HITL")
        case _:
            raise InvalidTowerImpact("umowa musi być tekstem")


def require_impact_source_ref(raw: object) -> str:
    match raw:
        case str() as text:
            token = text.strip()
            if token == _MANUAL or token.startswith(_FIXTURE):
                if len(token) <= 256:
                    return token
                raise InvalidTowerImpact("wskazanie zapisu skutku wieży za długie")
            if token == "":
                raise InvalidTowerImpact("wskazanie zapisu skutku wieży")
            raise InvalidTowerImpact("obce wskazanie zapisu skutku wieży")
        case _:
            raise InvalidTowerImpact("source_ref musi być tekstem")


def contract_gap_label(status: str) -> str | None:
    return _GAP if status == "missing" else None
