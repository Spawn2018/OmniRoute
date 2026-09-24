import re

from app.domain.errors import InvalidDangerousGood, InvalidImdgClass

_UN_NUMBER_PATTERN = re.compile(r"^[0-9]{4}$")
_IMDG_CLASSES = frozenset(
    {
        "1",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.5",
        "1.6",
        "2.1",
        "2.2",
        "2.3",
        "3",
        "4.1",
        "4.2",
        "4.3",
        "5.1",
        "5.2",
        "6.1",
        "6.2",
        "7",
        "8",
        "9",
    },
)
_TUNNELS = frozenset({"A", "B", "C", "D", "E"})
_GROUPS = frozenset({"none", *(f"sg{n}" for n in range(1, 19))})
_PACKING = frozenset({"I", "II", "III"})


def normalize_un_number(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDangerousGood("numer UN musi być tekstem")
    token = raw.strip().upper()
    if token.startswith("UN"):
        token = token[2:].strip()
    if _UN_NUMBER_PATTERN.fullmatch(token) is None:
        raise InvalidDangerousGood("numer UN: 4 cyfry")
    return token


def normalize_imdg_class(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidImdgClass("klasa IMDG musi być tekstem")
    token = raw.strip()
    if token not in _IMDG_CLASSES:
        raise InvalidImdgClass("klasa IMDG spoza allowlisty")
    return token


def normalize_un_aliases(raw: list[str]) -> list[str]:
    unique: list[str] = []
    for item in raw:
        token = normalize_un_number(item)
        if token not in unique:
            unique.append(token)
    return unique


def normalize_adr_tunnel_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDangerousGood("tunel musi być tekstem")
    token = raw.strip().upper()
    if token not in _TUNNELS:
        raise InvalidDangerousGood("nieznany kod tunelu ADR")
    return token


def normalize_segregation_group(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDangerousGood("segregacja musi być tekstem")
    token = raw.strip().lower()
    if token not in _GROUPS:
        raise InvalidDangerousGood("segregacja: nieznana grupa")
    return token


def normalize_packing_group(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDangerousGood("pakowanie musi być tekstem")
    token = raw.strip().upper()
    if token not in _PACKING:
        raise InvalidDangerousGood("pakowanie: nieznana grupa")
    return token


def require_marine_pollutant(raw: object) -> bool:
    if type(raw) is not bool:
        raise InvalidDangerousGood("zanieczyszczenie morza musi być true albo false")
    return raw


def require_limited_quantity(raw: object) -> bool:
    if type(raw) is not bool:
        raise InvalidDangerousGood("limited quantity musi być true albo false")
    return raw
