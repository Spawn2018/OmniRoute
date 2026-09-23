import re

from app.domain.errors import InvalidLocalChargeBindMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"charge", "quote", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://local-charge-bind/"
_MAX_REF = 256


def parse_local_charge_bind_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLocalChargeBindMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidLocalChargeBindMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidLocalChargeBindMark("wiązanie musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidLocalChargeBindMark(
            "wiązanie: charge, quote albo other",
        )
    if type(origin) is not str:
        raise InvalidLocalChargeBindMark("obce wskazanie wiązania dopłaty lokalnej")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidLocalChargeBindMark("obce wskazanie wiązania dopłaty lokalnej")
    if len(pointer) > _MAX_REF:
        raise InvalidLocalChargeBindMark("wskazanie wiązania dopłaty lokalnej za długie")
    return slug, token, pointer
