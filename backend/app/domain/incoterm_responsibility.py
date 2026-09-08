from app.domain.errors import InvalidIncotermResponsibility

_INCOTERMS = frozenset(
    {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"},
)
_SIDES = frozenset({"import", "export"})
_CLEARANCE = frozenset(
    {"seller", "buyer", "omni_customs", "origin_agent", "client_customs"},
)
_BOOKERS = frozenset({"seller", "buyer"})
_SCOPES = frozenset(
    {"precarriage", "ocean", "oncarriage", "contact_exchange", "none"},
)
_MAX_REF = 256
_OMNI_SEED = "omni:incoterms2020:ops"
_FIXTURE = "fixture://incoterm-responsibility/"
_MANUAL = "tenant:manual"


def require_responsibility_incoterm(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidIncotermResponsibility("incoterm musi być tekstem")
    token = raw.strip().upper()
    if token not in _INCOTERMS:
        raise InvalidIncotermResponsibility("nieznany incoterm")
    return token


def require_responsibility_trade_side(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidIncotermResponsibility("trade_side musi być tekstem")
    token = raw.strip()
    if token not in _SIDES:
        raise InvalidIncotermResponsibility("nieznana strona handlu")
    return token


def require_clearance_role(raw: object, *, field: str) -> str:
    if type(raw) is not str:
        raise InvalidIncotermResponsibility(f"{field} musi być tekstem")
    token = raw.strip()
    if token not in _CLEARANCE:
        raise InvalidIncotermResponsibility("nieznana rola odprawy")
    return token


def require_main_carriage_booker(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidIncotermResponsibility("main_carriage_booker musi być tekstem")
    token = raw.strip()
    if token not in _BOOKERS:
        raise InvalidIncotermResponsibility("nieznany booker głównego przewozu")
    return token


def require_booking_scope(raw: object) -> list[str]:
    if type(raw) is not list:
        raise InvalidIncotermResponsibility("booking_scope musi być listą")
    if len(raw) == 0:
        raise InvalidIncotermResponsibility("booking_scope puste")
    tokens: list[str] = []
    for entry in raw:
        if type(entry) is not str:
            raise InvalidIncotermResponsibility("token zakresu musi być tekstem")
        token = entry.strip()
        if token not in _SCOPES:
            raise InvalidIncotermResponsibility("nieznany zakres bookingu")
        if token not in tokens:
            tokens.append(token)
    return tokens


def require_responsibility_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidIncotermResponsibility("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidIncotermResponsibility("wskazanie zapisu macierzy")
    if len(token) > _MAX_REF:
        raise InvalidIncotermResponsibility("wskazanie zapisu macierzy za długie")
    if token not in {_OMNI_SEED, _MANUAL} and not token.startswith(_FIXTURE):
        raise InvalidIncotermResponsibility("obce wskazanie zapisu macierzy")
    return token


def omni_ops_seed_pairs() -> tuple[dict[str, object], ...]:
    # Dane Omni (ops), nie cytat tabeli ICC.
    rules = (
        ("EXW", "buyer", "buyer", "buyer", ["none"]),
        ("FCA", "seller", "buyer", "buyer", ["precarriage"]),
        ("CPT", "seller", "buyer", "seller", ["ocean"]),
        ("CIP", "seller", "buyer", "seller", ["ocean"]),
        ("DAP", "seller", "buyer", "seller", ["ocean", "oncarriage"]),
        ("DPU", "seller", "buyer", "seller", ["ocean", "oncarriage"]),
        ("DDP", "seller", "seller", "seller", ["ocean", "oncarriage"]),
        ("FAS", "seller", "buyer", "buyer", ["ocean"]),
        ("FOB", "seller", "buyer", "buyer", ["ocean"]),
        ("CFR", "seller", "buyer", "seller", ["ocean"]),
        ("CIF", "seller", "buyer", "seller", ["ocean"]),
    )
    pairs: list[dict[str, object]] = []
    for code, export_role, import_role, booker, scope in rules:
        for side in ("import", "export"):
            pairs.append(
                {
                    "incoterm": code,
                    "trade_side": side,
                    "export_clearance_role": export_role,
                    "import_clearance_role": import_role,
                    "main_carriage_booker": booker,
                    "booking_scope": list(scope),
                    "source_ref": _OMNI_SEED,
                },
            )
    return tuple(pairs)
