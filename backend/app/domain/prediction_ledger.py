import re
from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidPredictionLedger

_KINDS = frozenset({"eta", "transit", "disrupt"})
_HORIZONS = frozenset({"h1h", "h6h", "h24h", "h7d"})
_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://prediction-ledger/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_prediction_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPredictionLedger("rodzaj musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidPredictionLedger("rodzaj: eta, transit albo disrupt")
    return token


def require_horizon_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPredictionLedger("horyzont musi być tekstem")
    token = raw.strip().lower()
    if token not in _HORIZONS:
        raise InvalidPredictionLedger("horyzont: h1h, h6h, h24h albo h7d")
    return token


def require_model_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPredictionLedger("model musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidPredictionLedger("model: snake 2–32")
    return token


def _nonneg_decimal(raw: object, label: str) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidPredictionLedger(f"{label} nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidPredictionLedger(f"{label} musi być liczbą dziesiętną")
    token = raw.strip() if isinstance(raw, str) else raw
    if token == "":
        raise InvalidPredictionLedger(f"{label}: brak metryki")
    try:
        parsed = token if isinstance(token, Decimal) else Decimal(str(token))
    except InvalidOperation as exc:
        raise InvalidPredictionLedger(f"{label} musi być liczbą dziesiętną") from exc
    if parsed < 0:
        raise InvalidPredictionLedger(f"{label}: ujemna")
    return parsed.quantize(_FOUR)


def require_crps(raw: object) -> Decimal:
    return _nonneg_decimal(raw, "crps")


def require_mae(raw: object) -> Decimal:
    return _nonneg_decimal(raw, "mae")


def require_interval_bound(raw: object) -> Decimal:
    return _nonneg_decimal(raw, "przedział")


def require_interval_order(low: Decimal, high: Decimal) -> None:
    if high < low:
        raise InvalidPredictionLedger("przedział: high poniżej low")


def require_ledger_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPredictionLedger("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidPredictionLedger("wskazanie zapisu ledgeru predykcji")
    if len(token) > _MAX_REF:
        raise InvalidPredictionLedger("wskazanie zapisu ledgeru predykcji za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidPredictionLedger("obce wskazanie zapisu ledgeru predykcji")
    return token
