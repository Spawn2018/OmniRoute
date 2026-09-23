import re

from app.domain.errors import InvalidLocalChargeMatchMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"match", "gap", "waive", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://local-charge-match/"
_MAX_REF = 256


def parse_local_charge_match_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLocalChargeMatchMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidLocalChargeMatchMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidLocalChargeMatchMark("dopasowanie musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidLocalChargeMatchMark(
            "dopasowanie: match, gap, waive albo other",
        )
    if type(origin) is not str:
        raise InvalidLocalChargeMatchMark("obce wskazanie dopasowania dopłaty lokalnej")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidLocalChargeMatchMark("obce wskazanie dopasowania dopłaty lokalnej")
    if len(pointer) > _MAX_REF:
        raise InvalidLocalChargeMatchMark("wskazanie dopasowania dopłaty lokalnej za długie")
    return slug, token, pointer
