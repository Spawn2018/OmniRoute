import re

from app.domain.errors import InvalidLocalChargeWarningMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"warn", "hold", "waived", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://local-charge-warning/"
_MAX_REF = 256


def parse_local_charge_warning_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLocalChargeWarningMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidLocalChargeWarningMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidLocalChargeWarningMark("ostrzezenie musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidLocalChargeWarningMark(
            "ostrzezenie: warn, hold, waived albo other",
        )
    if type(origin) is not str:
        raise InvalidLocalChargeWarningMark("obce wskazanie ostrzeżenia dopłaty")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidLocalChargeWarningMark("obce wskazanie ostrzeżenia dopłaty")
    if len(pointer) > _MAX_REF:
        raise InvalidLocalChargeWarningMark("wskazanie ostrzeżenia dopłaty za długie")
    return slug, token, pointer
