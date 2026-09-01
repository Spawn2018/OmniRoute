import re
from enum import StrEnum

from app.domain.errors import (
    InvalidLocationData,
    InvalidPostalCode,
    InvalidPostalRange,
)

_POSTAL_PATTERN = re.compile(r"^[A-Z0-9]{2,10}$")
_ZONE_CODE_PATTERN = re.compile(r"^[A-Z0-9_]{2,32}$")
_POSTAL_SEPARATORS = str.maketrans("", "", " -")


class LocationKind(StrEnum):
    UNLOCODE = "unlocode"
    POSTAL_ZONE = "postal_zone"
    ADDRESS = "address"


def parse_location_kind(raw: str) -> LocationKind:
    if type(raw) is not str:
        raise InvalidLocationData("rodzaj lokalizacji musi być tekstem")
    try:
        return LocationKind(raw.strip().lower())
    except ValueError as exc:
        allowed = ", ".join(kind.value for kind in LocationKind)
        raise InvalidLocationData(f"rodzaj lokalizacji spoza zbioru: {allowed}") from exc


def normalize_zone_code(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidLocationData("kod strefy musi być tekstem")
    token = raw.strip().upper().replace(" ", "_")
    if _ZONE_CODE_PATTERN.fullmatch(token) is None:
        raise InvalidLocationData("kod strefy: 2-32 znaki A-Z, 0-9, _")
    return token


def normalize_location_name(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidLocationData("nazwa lokalizacji musi być tekstem")
    label = " ".join(raw.split())
    if label == "":
        raise InvalidLocationData("nazwa lokalizacji jest wymagana")
    return label


def normalize_postal_code(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidPostalCode("kod pocztowy musi być tekstem")
    token = raw.strip().upper().translate(_POSTAL_SEPARATORS)
    if _POSTAL_PATTERN.fullmatch(token) is None:
        raise InvalidPostalCode("kod pocztowy: 2-10 znaków A-Z i 0-9 po normalizacji")
    return token


def normalize_postal_bounds(raw_from: str, raw_to: str) -> tuple[str, str]:
    lower = normalize_postal_code(raw_from)
    upper = normalize_postal_code(raw_to)
    if len(lower) != len(upper):
        raise InvalidPostalRange("oba końce zakresu muszą mieć tę samą długość")
    # Porównanie kodów Unicode pokrywa się z kolacją "C" bazy, bo normalizacja
    # zostawia wyłącznie ASCII. Zakres liczy Postgres, tu jest tylko odrzut wejścia.
    if lower > upper:
        raise InvalidPostalRange(f"zakres odwrócony: {lower} po {upper}")
    return (lower, upper)
