from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidPartyScorecard

_QUANT = Decimal("0.0001")


def _as_decimal(raw: object, message: str) -> Decimal:
    if isinstance(raw, bool) or not isinstance(raw, int | str | Decimal):
        raise InvalidPartyScorecard(message)
    if type(raw) is str and raw.strip() == "":
        raise InvalidPartyScorecard(message)
    try:
        value = Decimal(str(raw).strip()) if type(raw) is str else Decimal(raw)
    except InvalidOperation as exc:
        raise InvalidPartyScorecard(message) from exc
    return value


def optional_unit_interval(raw: object, field: str) -> Decimal | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    value = _as_decimal(raw, f"{field} musi być liczbą dziesiętną")
    if value < 0 or value > 1:
        raise InvalidPartyScorecard(f"{field} musi być w zakresie 0–1")
    return value.quantize(_QUANT)


def optional_non_negative_hours(raw: object) -> Decimal | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    value = _as_decimal(raw, "mediana czasu musi być liczbą dziesiętną")
    if value < 0:
        raise InvalidPartyScorecard("mediana czasu nie może być ujemna")
    return value.quantize(_QUANT)


def optional_non_negative_int(raw: object, field: str) -> int | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise InvalidPartyScorecard(f"{field} musi być liczbą całkowitą")
    if raw < 0:
        raise InvalidPartyScorecard(f"{field} nie może być ujemne")
    return raw


def required_sample_size(raw: object) -> int:
    if raw is None:
        return 0
    value = optional_non_negative_int(raw, "sample_size")
    if value is None:
        return 0
    return value


def required_window_days(raw: object) -> int:
    if raw is None:
        return 90
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise InvalidPartyScorecard("window_days musi być liczbą całkowitą")
    if raw <= 0:
        raise InvalidPartyScorecard("window_days musi być dodatnie")
    return raw
