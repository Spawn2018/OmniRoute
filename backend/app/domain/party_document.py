import re
from uuid import UUID

from app.domain.errors import InvalidPartyDocument

_KIND = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://party-document/"
_MANUAL = "tenant:manual"


def require_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidPartyDocument("party_id musi być UUID")
    return raw


def require_document_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPartyDocument("dokument musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _KIND.fullmatch(token) is None:
        raise InvalidPartyDocument("dokument: snake 2–32")
    return token


def require_party_document_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPartyDocument("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidPartyDocument("wskazanie zapisu dokumentu kontrahenta")
    if len(token) > _MAX_REF:
        raise InvalidPartyDocument("wskazanie zapisu dokumentu kontrahenta za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidPartyDocument("obce wskazanie zapisu dokumentu kontrahenta")
    return token
