import re

from app.domain.errors import InvalidPhytoAtaMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"phyto", "ata", "plant", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://phyto-ata-mark/"
_REF_CAP = 256


def parse_phyto_ata_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPhytoAtaMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPhytoAtaMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPhytoAtaMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPhytoAtaMark(
            "rodzaj: phyto, ata, plant albo other",
        )
    if type(origin) is not str:
        raise InvalidPhytoAtaMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPhytoAtaMark("obce wskazanie zapisu znacznika phyto/ATA")
    if len(pointer) > _REF_CAP:
        raise InvalidPhytoAtaMark(
            "obce wskazanie zapisu znacznika phyto/ATA za długie",
        )
    return slug, token, pointer
