import re
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidDelayForecast

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://delay-forecast/"
_REF_CAP = 256
_HORIZON_MIN = 1
_HORIZON_MAX = 168


def parse_delay_forecast_row(
    code: object, horizon_hours: object, p_late: object, origin: object
) -> tuple[str, int, Decimal, str]:
    return (
        _require_code(code),
        _require_horizon(horizon_hours),
        _require_p_late(p_late),
        _require_origin(origin),
    )


def _require_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDelayForecast("oznaczenie musi być tekstem")
    slug = raw.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidDelayForecast("oznaczenie: snake 2–32")
    return slug


def _require_horizon(raw: object) -> int:
    if type(raw) is not int or isinstance(raw, bool):
        raise InvalidDelayForecast("horyzont musi być liczbą całkowitą")
    if raw < _HORIZON_MIN or raw > _HORIZON_MAX:
        raise InvalidDelayForecast("horyzont: 1–168 godzin")
    return raw


def _require_p_late(raw: object) -> Decimal:
    if type(raw) is Decimal:
        value = raw
    elif type(raw) is str:
        try:
            value = Decimal(raw.strip())
        except InvalidOperation as exc:
            raise InvalidDelayForecast("p_late: Decimal 0–1") from exc
    elif type(raw) is int and not isinstance(raw, bool):
        value = Decimal(raw)
    else:
        raise InvalidDelayForecast("p_late musi być Decimal")
    if value < 0 or value > 1:
        raise InvalidDelayForecast("p_late: Decimal 0–1")
    return value


def _require_origin(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDelayForecast("obce source_ref")
    pointer = raw.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidDelayForecast("obce wskazanie zapisu prognozy opóźnienia")
    if len(pointer) > _REF_CAP:
        raise InvalidDelayForecast("obce wskazanie zapisu prognozy opóźnienia za długie")
    return pointer
