import re

from app.domain.errors import InvalidTelematicsDevice

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"tracker", "fault", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://telematics-device/"
_REF_CAP = 256


def parse_telematics_device_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTelematicsDevice("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidTelematicsDevice("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidTelematicsDevice("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidTelematicsDevice("rodzaj: tracker, fault albo other")
    if type(origin) is not str:
        raise InvalidTelematicsDevice("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidTelematicsDevice("obce wskazanie zapisu urzadzenia")
    if len(pointer) > _REF_CAP:
        raise InvalidTelematicsDevice("obce wskazanie zapisu urzadzenia za dlugie")
    return slug, token, pointer
