import re

from app.domain.errors import InvalidAisImportMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ais", "aes", "intrastat", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://ais-import-mark/"
_REF_CAP = 256


def parse_ais_import_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidAisImportMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidAisImportMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidAisImportMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidAisImportMark(
            "rodzaj: ais, aes, intrastat albo other",
        )
    if type(origin) is not str:
        raise InvalidAisImportMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidAisImportMark(
            "obce wskazanie zapisu znacznika AIS/AES/Intrastat",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidAisImportMark(
            "obce wskazanie zapisu znacznika AIS/AES/Intrastat za długie",
        )
    return slug, token, pointer
