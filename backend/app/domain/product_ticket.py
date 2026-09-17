import re

from app.domain.errors import InvalidProductTicket

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"report", "triage", "owner_ok", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://product-ticket/"
_REF_CAP = 256
_TITLE_CAP = 200
_BODY_CAP = 2000


def _snake_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidProductTicket("oznaczenie musi być tekstem")
    slug = raw.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidProductTicket("oznaczenie: snake 2–32")
    return slug


def _title(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidProductTicket("tytuł musi być tekstem")
    heading = raw.strip()
    if not heading:
        raise InvalidProductTicket("tytuł nie może być pusty")
    if len(heading) > _TITLE_CAP:
        raise InvalidProductTicket("tytuł za długi")
    return heading


def _body(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidProductTicket("treść musi być tekstem")
    text = raw.strip()
    if not text:
        raise InvalidProductTicket("treść nie może być pusta")
    if len(text) > _BODY_CAP:
        raise InvalidProductTicket("treść za długa")
    return text


def _kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidProductTicket("rodzaj musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidProductTicket(
            "rodzaj: report, triage, owner_ok albo other",
        )
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidProductTicket("obce source_ref")
    pointer = raw.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidProductTicket("obce wskazanie zapisu ticketu produktu")
    if len(pointer) > _REF_CAP:
        raise InvalidProductTicket("obce wskazanie zapisu ticketu produktu za długie")
    return pointer


def parse_product_ticket_row(
    code: object,
    title: object,
    body: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str, str, str]:
    return (
        _snake_code(code),
        _title(title),
        _body(body),
        _kind(kind),
        _source_ref(origin),
    )
