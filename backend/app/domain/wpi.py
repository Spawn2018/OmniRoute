from decimal import Decimal, InvalidOperation

from app.domain.errors import InvalidWpiData

HARBOR_SIZES = (
    "Very Small",
    "Small",
    "Medium",
    "Large",
)
HARBOR_TYPES = (
    "Coastal Natural",
    "Coastal Breakwater",
    "Coastal Tide Gate",
    "River Natural",
    "River Basin",
    "River Tide Gate",
    "Lake or Canal",
    "Open Roadstead",
    "Typhoon Harbor",
)
SHELTERS = ("Excellent", "Good", "Fair", "Poor", "None")


def sql_in_list(values: tuple[str, ...]) -> str:
    quoted = ", ".join(f"'{item}'" for item in values)
    return quoted


def parse_optional_label(raw: str, *, allowed: tuple[str, ...], field: str) -> str | None:
    token = raw.strip()
    if token == "":
        return None
    if token not in allowed:
        raise InvalidWpiData(f"{field} spoza słownika NGA: {token}")
    return token


def parse_optional_wpi_number(raw: str) -> int | None:
    token = raw.strip()
    if token == "":
        return None
    try:
        number = int(token)
    except ValueError as exc:
        raise InvalidWpiData(f"numer WPI musi być całkowity: {token}") from exc
    if number <= 0:
        raise InvalidWpiData(f"numer WPI musi być dodatni: {token}")
    return number


def parse_optional_depth_m(raw: str, *, field: str) -> Decimal | None:
    token = raw.strip()
    if token == "":
        return None
    try:
        depth = Decimal(token)
    except InvalidOperation as exc:
        raise InvalidWpiData(f"{field} musi być liczbą metrów: {token}") from exc
    if depth < 0:
        raise InvalidWpiData(f"{field} nie może być ujemna")
    return depth
