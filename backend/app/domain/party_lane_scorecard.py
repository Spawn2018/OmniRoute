from decimal import Decimal
from uuid import UUID

from app.domain.errors import InvalidPartyScorecard
from app.domain.party_scorecard import optional_non_negative_int

_EMPTY = "brak historii na tym kierunku — karta globalna / sieć"


def require_lane_port_id(raw: object, field: str) -> UUID:
    if type(raw) is not UUID:
        raise InvalidPartyScorecard(f"{field} musi być UUID")
    return raw


def require_lane_window_days(raw: object) -> int:
    if raw is None:
        return 90
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise InvalidPartyScorecard("window_days musi być liczbą całkowitą")
    if raw < 1 or raw > 365:
        raise InvalidPartyScorecard("window_days: 1–365")
    return raw


def required_lane_count(raw: object, field: str) -> int:
    if raw is None:
        return 0
    value = optional_non_negative_int(raw, field)
    return 0 if value is None else value


def lane_scorecard_hint(
    *,
    sample_size: int,
    answered_inquiry_count: int,
    shipment_count: int,
    cheapest_count: int,
    median_response_hours: Decimal | None,
    window_days: int,
) -> str:
    if sample_size == 0:
        return _EMPTY
    hours = "brak mediany" if median_response_hours is None else f"{median_response_hours} h"
    return (
        f"okno {window_days} d · próba {sample_size} · odpowiedzi {answered_inquiry_count} · "
        f"zlecenia {shipment_count} · najtańszy {cheapest_count} · mediana {hours}"
    )
