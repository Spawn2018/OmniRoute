import re

from app.domain.errors import InvalidDataSource

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://data-source/"
_REF_CAP = 256


def _label(raw: object, *, field: str, lo: int, hi: int) -> str:
    if type(raw) is not str:
        raise InvalidDataSource(f"{field} musi byc tekstem")
    token = raw.strip()
    if not lo <= len(token) <= hi:
        raise InvalidDataSource(f"{field}: dlugosc {lo}–{hi}")
    return token


def parse_data_source_row(
    code: object,
    license_label: object,
    rights_scope: object,
    origin: object,
) -> tuple[str, str, str, str]:
    if type(code) is not str:
        raise InvalidDataSource("oznaczenie musi byc tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidDataSource("oznaczenie: snake 2–32")
    license_token = _label(license_label, field="licencja", lo=2, hi=64)
    rights_token = _label(rights_scope, field="zakres praw", lo=2, hi=128)
    if type(origin) is not str:
        raise InvalidDataSource("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidDataSource("obce wskazanie zapisu zrodla danych")
    if len(pointer) > _REF_CAP:
        raise InvalidDataSource("obce wskazanie zapisu zrodla danych za dlugie")
    return slug, license_token, rights_token, pointer
