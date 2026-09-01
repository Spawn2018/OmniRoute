import re

from app.domain.errors import InvalidCommodityCode

_COMMODITY_CODE_PATTERN = re.compile(r"^[0-9]{4,10}$")


def normalize_commodity_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCommodityCode("kod towarowy musi być tekstem")
    token = raw.strip()
    if _COMMODITY_CODE_PATTERN.fullmatch(token) is None:
        raise InvalidCommodityCode("kod towarowy: 4–10 cyfr")
    return token


def normalize_commodity_aliases(raw: list[str]) -> list[str]:
    unique: list[str] = []
    for item in raw:
        token = normalize_commodity_code(item)
        if token not in unique:
            unique.append(token)
    return unique
