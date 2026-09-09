from uuid import UUID

from app.domain.errors import InvalidKreptdLicence

_MAX_REF = 256
_MAX_LICENCE = 64
_MIN_LICENCE = 8
_FIXTURE = "fixture://kreptd-licence/"
_MANUAL = "tenant:manual"


def require_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidKreptdLicence("party_id musi być UUID")
    return raw


def require_licence_no(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidKreptdLicence("licencja musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) < _MIN_LICENCE or len(token) > _MAX_LICENCE:
        raise InvalidKreptdLicence("licencja KREPTD: 8–64 znaki")
    if "://" in token:
        raise InvalidKreptdLicence("licencja KREPTD nie jest URL")
    if not any(ch.isdigit() for ch in token):
        raise InvalidKreptdLicence("licencja KREPTD bez numeru")
    return token


def require_kreptd_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidKreptdLicence("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidKreptdLicence("wskazanie zapisu licencji KREPTD")
    if len(token) > _MAX_REF:
        raise InvalidKreptdLicence("wskazanie zapisu licencji KREPTD za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidKreptdLicence("obce wskazanie zapisu licencji KREPTD")
    return token
