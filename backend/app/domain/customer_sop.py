import re

from app.domain.errors import InvalidCustomerSop

_SOP_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_BODY_MAX = 8000
_TITLE_MAX = 128


def normalize_sop_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCustomerSop("kod SOP musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _SOP_CODE_PATTERN.fullmatch(token) is None:
        raise InvalidCustomerSop("kod SOP: snake 2–32")
    return token


def normalize_sop_title(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCustomerSop("tytuł SOP musi być tekstem")
    title = " ".join(raw.split())
    if title == "":
        raise InvalidCustomerSop("tytuł SOP jest wymagany")
    if len(title) > _TITLE_MAX:
        raise InvalidCustomerSop("tytuł SOP za długi")
    return title


def normalize_sop_body(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCustomerSop("treść SOP musi być tekstem")
    body = raw.strip()
    if body == "":
        raise InvalidCustomerSop("treść SOP jest wymagana")
    if len(body) > _BODY_MAX:
        raise InvalidCustomerSop("treść SOP za długa")
    return body
