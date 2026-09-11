import re

from app.domain.errors import InvalidAeoDossierMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"aeo", "authorised", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://aeo-dossier-mark/"
_REF_CAP = 256


def parse_aeo_dossier_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidAeoDossierMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidAeoDossierMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidAeoDossierMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidAeoDossierMark(
            "rodzaj: aeo, authorised albo other",
        )
    if type(origin) is not str:
        raise InvalidAeoDossierMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidAeoDossierMark("obce wskazanie zapisu znacznika dossier AEO")
    if len(pointer) > _REF_CAP:
        raise InvalidAeoDossierMark(
            "obce wskazanie zapisu znacznika dossier AEO za długie",
        )
    return slug, token, pointer
