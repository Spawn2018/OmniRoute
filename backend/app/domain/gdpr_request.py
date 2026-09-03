from uuid import UUID

from app.domain.errors import InvalidGdprRequest

_MAX_REF = 256
_FIXTURE = "fixture://gdpr-request/"
_MANUAL = "tenant:manual"
_KINDS = frozenset({"access", "erasure"})
ERASED_DISPLAY_NAME = "usunięte"


def require_gdpr_app_user_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidGdprRequest("app_user_id musi być UUID")
    return raw


def require_gdpr_request_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidGdprRequest("request_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidGdprRequest("nieznany rodzaj wniosku")
    return token


def require_gdpr_request_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidGdprRequest("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidGdprRequest("wskazanie zapisu wniosku")
    if len(token) > _MAX_REF:
        raise InvalidGdprRequest("wskazanie zapisu wniosku za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidGdprRequest("obce wskazanie zapisu wniosku")
    return token


def require_open_gdpr_request(raw: object) -> str:
    if raw != "open":
        raise InvalidGdprRequest("wniosek już wypełniony")
    return "open"


def erasure_mailbox(user_id: UUID) -> str:
    return f"erased.{user_id.hex}@erased.invalid"
