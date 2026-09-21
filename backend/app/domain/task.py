import re

from app.domain.errors import InvalidTask

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_STATUSES = frozenset({"open", "done", "skipped", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://task/"
_REF_CAP = 256


def require_task_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTask("zadanie musi być tekstem")
    slug = raw.strip().lower().replace("-", "_")
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidTask("zadanie: snake 2–32")
    return slug


def require_task_template_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTask("szablon musi być tekstem")
    slug = raw.strip().lower().replace("-", "_")
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidTask("szablon: snake 2–32")
    return slug


def require_task_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTask("status musi być tekstem")
    token = raw.strip().lower()
    if token not in _STATUSES:
        raise InvalidTask("status: open, done, skipped albo other")
    return token


def require_task_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTask("obce source_ref")
    pointer = raw.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidTask("obce wskazanie zapisu zadania")
    if len(pointer) > _REF_CAP:
        raise InvalidTask("obce wskazanie zapisu zadania za długie")
    return pointer


def parse_task_row(
    code: object,
    template: object,
    status: object,
    origin: object,
) -> tuple[str, str, str, str]:
    return (
        require_task_code(code),
        require_task_template_code(template),
        require_task_status(status),
        require_task_source_ref(origin),
    )
