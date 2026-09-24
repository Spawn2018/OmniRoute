import re

from app.domain.errors import InvalidChargeCode

_CHARGE_CODE_PATTERN = re.compile(r"^[A-Z0-9_]{2,32}$")
_OMNI_EXP1_SEED = "omni:charge-code:exp1"


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


def omni_exp1_seed_codes() -> tuple[tuple[str, str], ...]:
    # Dane Omni EXP1 — nie CHECK allowlisty; operator może dodać inne kody.
    return (
        ("WAITING", "Waiting time"),
        ("NO_SHOW", "No-show"),
        ("DIVERSION", "Diversion"),
        ("STAMP", "Stamp fee"),
    )


def omni_exp1_source_ref() -> str:
    return _OMNI_EXP1_SEED
