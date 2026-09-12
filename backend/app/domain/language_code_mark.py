import re

from app.domain.errors import InvalidLanguageCodeMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"pl", "en", "de", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://language-code-mark/"


def parse_language_code_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLanguageCodeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidLanguageCodeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLanguageCodeMark("rodzaj locale musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidLanguageCodeMark(
            "rodzaj locale: pl, en, de albo other",
        )
    if type(origin) is not str:
        raise InvalidLanguageCodeMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidLanguageCodeMark(
            "obce wskazanie zapisu znacznika kodu języka",
        )
    if len(pointer) > 256:
        raise InvalidLanguageCodeMark(
            "obce wskazanie zapisu znacznika kodu języka za długie",
        )
    return slug, token, pointer
