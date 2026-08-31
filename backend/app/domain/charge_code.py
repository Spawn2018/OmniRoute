import re

from app.domain.errors import InvalidChargeCode

_CHARGE_CODE_PATTERN = re.compile(r"^[A-Z0-9_]{2,32}$")


def normalize_charge_code(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidChargeCode("kod opłaty musi być tekstem")
    token = raw.strip().upper()
    if _CHARGE_CODE_PATTERN.fullmatch(token) is None:
        raise InvalidChargeCode("kod opłaty: 2–32 znaki A-Z, 0-9, _")
    return token


def normalize_aliases(raw: list[str]) -> list[str]:
    unique: list[str] = []
    for item in raw:
        token = normalize_charge_code(item)
        if token not in unique:
            unique.append(token)
    return unique
