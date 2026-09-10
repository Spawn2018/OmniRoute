import re

from app.domain.errors import InvalidTaskTemplate

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_WHEN = 512
_MAX_REF = 256
_FIXTURE = "fixture://task-template/"
_MANUAL = "tenant:manual"


def require_task_template_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTaskTemplate("szablon musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTaskTemplate("szablon: snake 2–32")
    return token


def require_task_applies_when(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTaskTemplate("warunek musi być tekstem")
    note = raw.strip()
    if note == "":
        raise InvalidTaskTemplate("warunek jest wymagany")
    if len(note) > _MAX_WHEN:
        raise InvalidTaskTemplate("warunek za długi")
    return note


def require_task_template_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTaskTemplate("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTaskTemplate("wskazanie zapisu szablonu zadania")
    if len(token) > _MAX_REF:
        raise InvalidTaskTemplate("wskazanie zapisu szablonu zadania za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTaskTemplate("obce wskazanie zapisu szablonu zadania")
    return token
