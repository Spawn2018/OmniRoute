import re

from app.domain.errors import InvalidMarginMatchMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"match", "hold", "waive", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://margin-match/"
_MAX_REF = 256


def parse_margin_match_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidMarginMatchMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidMarginMatchMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidMarginMatchMark("dopasowanie musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidMarginMatchMark(
            "dopasowanie: match, hold, waive albo other",
        )
    if type(origin) is not str:
        raise InvalidMarginMatchMark("obce wskazanie dopasowania podłogi")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidMarginMatchMark("obce wskazanie dopasowania podłogi")
    if len(pointer) > _MAX_REF:
        raise InvalidMarginMatchMark("wskazanie dopasowania podłogi za długie")
    return slug, token, pointer
