import re
from datetime import date

from app.domain.charge_code import normalize_charge_code
from app.domain.errors import InvalidChargeCode, InvalidChargeTemplate

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://charge-template/"
_MANUAL = "tenant:manual"


def require_template_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidChargeTemplate("szablon musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidChargeTemplate("szablon: snake 2–32")
    return token


def require_member_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidChargeTemplate("kod opłaty musi być tekstem")
    try:
        return normalize_charge_code(raw)
    except InvalidChargeCode as exc:
        raise InvalidChargeTemplate(str(exc)) from exc


def _iso_day(raw: object, *, edge: str) -> date:
    if type(raw) is not str:
        raise InvalidChargeTemplate(f"ważność {edge} musi być datą")
    token = raw.strip()
    if token == "":
        raise InvalidChargeTemplate(f"ważność {edge} musi być datą")
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidChargeTemplate(f"ważność {edge} musi być datą ISO") from exc


def require_validity_window(valid_from: object, valid_until: object) -> tuple[date, date]:
    start = _iso_day(valid_from, edge="od")
    end = _iso_day(valid_until, edge="do")
    if end < start:
        raise InvalidChargeTemplate("ważność: do nie może być przed od")
    return start, end


def require_template_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidChargeTemplate("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidChargeTemplate("wskazanie zapisu szablonu opłat")
    if len(token) > _MAX_REF:
        raise InvalidChargeTemplate("wskazanie zapisu szablonu opłat za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidChargeTemplate("obce wskazanie zapisu szablonu opłat")
    return token
