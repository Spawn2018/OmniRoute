from app.domain.errors import InvalidResource

_KINDS = frozenset({"vehicle", "driver", "trailer"})
_MAX_NAME = 64
_MAX_REG = 32
_MAX_REF = 256
_FIXTURE = "fixture://resource/"
_MANUAL = "tenant:manual"


def require_resource_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidResource("resource_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidResource("nieznany rodzaj zasobu")
    return token


def require_display_name(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidResource("display_name musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidResource("nazwa zasobu")
    if len(token) > _MAX_NAME:
        raise InvalidResource("nazwa zasobu za długa")
    return token


def require_registration_no(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidResource("registration_no musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_REG:
        raise InvalidResource("numer rejestracyjny za długi")
    return token


def require_resource_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidResource("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidResource("wskazanie zapisu zasobu")
    if len(token) > _MAX_REF:
        raise InvalidResource("wskazanie zapisu zasobu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidResource("obce wskazanie zapisu zasobu")
    return token
