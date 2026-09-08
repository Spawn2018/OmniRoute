import re
from datetime import date

from app.domain.errors import InvalidOrganizationCalendar

_COUNTRY = re.compile(r"^[A-Z]{2}$")
_KINDS = frozenset({"holiday", "working"})
_MAX_REF = 256
_FIXTURE = "fixture://organization-calendar/"
_MANUAL = "tenant:manual"


def require_country_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOrganizationCalendar("country_code musi być tekstem")
    token = raw.strip().upper()
    if _COUNTRY.fullmatch(token) is None:
        raise InvalidOrganizationCalendar("nieznany kod kraju")
    return token


def require_calendar_day(raw: object) -> date:
    if type(raw) is date:
        return raw
    raise InvalidOrganizationCalendar("dzień kalendarza musi być datą")


def require_day_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOrganizationCalendar("day_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidOrganizationCalendar("nieznany rodzaj dnia")
    return token


def require_calendar_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOrganizationCalendar("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidOrganizationCalendar("wskazanie zapisu dnia")
    if len(token) > _MAX_REF:
        raise InvalidOrganizationCalendar("wskazanie zapisu dnia za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidOrganizationCalendar("obce wskazanie zapisu dnia")
    return token
