import re

from app.domain.errors import InvalidRegistryPollMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ceidg", "krs", "vies", "whitelist", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://registry-poll-mark/"
_REF_CAP = 256


def parse_registry_poll_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRegistryPollMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRegistryPollMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRegistryPollMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRegistryPollMark(
            "rodzaj: ceidg, krs, vies, whitelist albo other",
        )
    if type(origin) is not str:
        raise InvalidRegistryPollMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRegistryPollMark("obce wskazanie zapisu znacznika poll rejestru")
    if len(pointer) > _REF_CAP:
        raise InvalidRegistryPollMark(
            "obce wskazanie zapisu znacznika poll rejestru za długie",
        )
    return slug, token, pointer
