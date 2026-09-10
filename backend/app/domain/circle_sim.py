import re

from app.domain.errors import InvalidCircleSim, InvalidUnlocode
from app.domain.port import normalize_unlocode

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://circle-sim/"
_MANUAL = "tenant:manual"


def require_sim_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCircleSim("kolko musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidCircleSim("kolko: snake 2–32")
    return token


def _as_unlocode(raw: object, token: str) -> str:
    if type(raw) is not str:
        raise InvalidCircleSim(f"{token} musi być tekstem")
    try:
        return normalize_unlocode(raw)
    except InvalidUnlocode as exc:
        raise InvalidCircleSim(f"{token}: {exc}") from exc


def require_circle_pair(unload_raw: object, load_raw: object) -> tuple[str, str]:
    unload = _as_unlocode(unload_raw, "rozladunek")
    load = _as_unlocode(load_raw, "zaladunek")
    if unload == load:
        raise InvalidCircleSim("para nie może mieć tych samych końców")
    return unload, load


def require_circle_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCircleSim("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCircleSim("obce wskazanie zapisu kółka")
    if len(token) > _MAX_REF:
        raise InvalidCircleSim("obce wskazanie zapisu kółka za długie")
    return token
