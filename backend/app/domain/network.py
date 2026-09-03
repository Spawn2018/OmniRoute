import re

from app.domain.errors import InvalidNetworkCode

_NETWORK_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")


def normalize_network_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidNetworkCode("kod sieci musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _NETWORK_CODE_PATTERN.fullmatch(token) is None:
        raise InvalidNetworkCode("kod sieci: snake 2–32")
    return token


def normalize_network_aliases(raw: list[str]) -> list[str]:
    unique: list[str] = []
    for item in raw:
        token = normalize_network_code(item)
        if token not in unique:
            unique.append(token)
    return unique


def require_network_member_name(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidNetworkCode("nazwa członka musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidNetworkCode("nazwa członka jest wymagana")
    if len(token) > 128:
        raise InvalidNetworkCode("nazwa członka za długa")
    return token


def optional_network_text(raw: str | None, *, limit: int, field: str) -> str | None:
    if raw is None:
        return None
    token = raw.strip()
    if token == "":
        return None
    if len(token) > limit:
        raise InvalidNetworkCode(f"{field} za długie")
    return token
