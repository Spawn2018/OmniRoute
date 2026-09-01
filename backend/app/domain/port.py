import re
from collections.abc import Sequence
from decimal import Decimal
from typing import Protocol

from app.domain.errors import (
    AmbiguousPortToken,
    InvalidPortData,
    InvalidPortToken,
    InvalidUnlocode,
    UnknownPort,
)

_UNLOCODE_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{3}$")
_COUNTRY_PATTERN = re.compile(r"^[A-Z]{2}$")
_POSITION_PATTERN = re.compile(r"^(\d{2})(\d{2})([NS]) (\d{3})(\d{2})([EW])$")

# Klasyfikator UN/LOCODE ma osiem pozycji; M-05 modeluje cztery z nich.
_FUNCTION_POSITIONS = ((0, "port"), (1, "rail"), (3, "airport"), (5, "icd"))
_MINUTES_IN_DEGREE = Decimal(60)
_POSITION_SCALE = Decimal("0.000001")


class ResolvablePort(Protocol):
    @property
    def unlocode(self) -> str: ...

    @property
    def is_official(self) -> bool: ...


def normalize_unlocode(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidUnlocode("kod UN/LOCODE musi być tekstem")
    token = raw.replace(" ", "").upper()
    if _UNLOCODE_PATTERN.fullmatch(token) is None:
        raise InvalidUnlocode("kod UN/LOCODE: 5 znaków — kraj i miejsce")
    return token


def normalize_country_code(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidPortData("kod kraju musi być tekstem")
    token = raw.strip().upper()
    if _COUNTRY_PATTERN.fullmatch(token) is None:
        raise InvalidPortData("kod kraju: dwie litery ISO 3166-1 alfa-2")
    return token


def normalize_port_token(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidPortToken("token portu musi być tekstem")
    token = " ".join(raw.split()).upper()
    if token == "":
        raise InvalidPortToken("pusty token portu")
    return token


def normalize_port_aliases(raw: Sequence[str]) -> list[str]:
    unique: list[str] = []
    for item in raw:
        token = normalize_port_token(item)
        if token not in unique:
            unique.append(token)
    return unique


def decode_function_flags(classifier: str) -> list[str]:
    if type(classifier) is not str or len(classifier) != 8:
        raise InvalidPortData("klasyfikator funkcji UN/LOCODE ma 8 pozycji")
    return [name for position, name in _FUNCTION_POSITIONS if classifier[position].isdigit()]


def parse_coordinates(raw: str) -> tuple[Decimal | None, Decimal | None]:
    if type(raw) is not str:
        raise InvalidPortData("współrzędne muszą być tekstem")
    position = raw.strip()
    if position == "":
        return (None, None)
    match = _POSITION_PATTERN.fullmatch(position)
    if match is None:
        raise InvalidPortData("współrzędne UN/LOCODE w formacie DDMMN DDDMME")
    latitude = _from_sexagesimal(match.group(1), match.group(2), match.group(3) == "S")
    longitude = _from_sexagesimal(match.group(4), match.group(5), match.group(6) == "W")
    return (latitude, longitude)


def select_resolved_port[PortT: ResolvablePort](token: str, candidates: Sequence[PortT]) -> PortT:
    if not candidates:
        raise UnknownPort(f"nieznany port: {token}")

    by_code = [row for row in candidates if row.unlocode == token.replace(" ", "")]
    if len(by_code) == 1:
        return by_code[0]

    preferred = [row for row in candidates if row.is_official] or list(candidates)
    if len(preferred) > 1:
        codes = ", ".join(sorted(row.unlocode for row in preferred))
        raise AmbiguousPortToken(f"token {token} wskazuje na wiele portów: {codes}")
    return preferred[0]


def _from_sexagesimal(degrees: str, minutes: str, negative: bool) -> Decimal:
    value = (Decimal(degrees) + Decimal(minutes) / _MINUTES_IN_DEGREE).quantize(_POSITION_SCALE)
    return -value if negative else value
