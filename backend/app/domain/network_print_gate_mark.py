import re

from app.domain.errors import InvalidNetworkPrintGateMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"block_409", "warn_only", "record_only", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://network-print-gate/"
_MAX_REF = 256


def parse_network_print_gate_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidNetworkPrintGateMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidNetworkPrintGateMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidNetworkPrintGateMark("gate musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidNetworkPrintGateMark(
            "gate: block_409, warn_only, record_only albo other",
        )
    if type(origin) is not str:
        raise InvalidNetworkPrintGateMark("obce wskazanie bramy wydruku sieci")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidNetworkPrintGateMark("obce wskazanie bramy wydruku sieci")
    if len(pointer) > _MAX_REF:
        raise InvalidNetworkPrintGateMark("wskazanie bramy wydruku sieci za długie")
    return slug, token, pointer
