import re
from datetime import datetime

from app.domain.errors import InvalidWeatherObservation

_CONDITIONS = frozenset({"clear", "rain", "snow", "wind", "fog", "ice", "other"})
_STATION = re.compile(r"^[A-Z]{2}[A-Z0-9]{3}$")
_MAX_REF = 256
_FIXTURE = "fixture://weather-observation/"
_MANUAL = "tenant:manual"
_PROVIDER = "hitl"


def require_condition_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidWeatherObservation("warunek musi być tekstem")
    token = raw.strip().lower()
    if token not in _CONDITIONS:
        raise InvalidWeatherObservation("warunek: allowlista HITL")
    return token


def require_station_unlocode(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidWeatherObservation("stacja musi być tekstem")
    token = raw.strip().upper()
    if _STATION.fullmatch(token) is None:
        raise InvalidWeatherObservation("stacja: UN/LOCODE")
    return token


def require_observed_at(raw: object) -> datetime:
    if type(raw) is not str:
        raise InvalidWeatherObservation("obserwacja musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidWeatherObservation("obserwacja: brak czasu")
    try:
        parsed = datetime.fromisoformat(token.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidWeatherObservation("obserwacja: ISO-8601") from exc
    if parsed.tzinfo is None:
        raise InvalidWeatherObservation("obserwacja: brak strefy")
    return parsed


def require_provider_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidWeatherObservation("dostawca musi być tekstem")
    token = raw.strip().lower()
    if token != _PROVIDER:
        raise InvalidWeatherObservation("dostawca: tylko hitl")
    return token


def require_weather_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidWeatherObservation("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidWeatherObservation("wskazanie zapisu pogody")
    if len(token) > _MAX_REF:
        raise InvalidWeatherObservation("wskazanie zapisu pogody za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidWeatherObservation("obce wskazanie zapisu pogody")
    return token
