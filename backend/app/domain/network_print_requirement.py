import re

from app.domain.errors import InvalidNetworkPrintRequirement

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://network-print-requirement/"
_REF_CAP = 256
_LABEL_CAP = 64


def parse_network_print_requirement_row(
    code: object,
    label: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidNetworkPrintRequirement("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidNetworkPrintRequirement("oznaczenie: snake 2–32")
    if type(label) is not str:
        raise InvalidNetworkPrintRequirement("etykieta sieci musi być tekstem")
    network = label.strip()
    if network == "" or len(network) > _LABEL_CAP:
        raise InvalidNetworkPrintRequirement("etykieta sieci: 1–64 znaków")
    if type(origin) is not str:
        raise InvalidNetworkPrintRequirement("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidNetworkPrintRequirement(
            "obce wskazanie zapisu wymogu wydruku sieci",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidNetworkPrintRequirement(
            "obce wskazanie zapisu wymogu wydruku sieci za długie",
        )
    return slug, network, pointer
