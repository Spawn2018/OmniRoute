import re

from app.domain.errors import InvalidTrackingConsent

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"party", "driver", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://tracking-consent/"
_REF_CAP = 256


def parse_tracking_consent_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTrackingConsent("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidTrackingConsent("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidTrackingConsent("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidTrackingConsent("rodzaj: party, driver albo other")
    if type(origin) is not str:
        raise InvalidTrackingConsent("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidTrackingConsent("obce wskazanie zapisu zgody")
    if len(pointer) > _REF_CAP:
        raise InvalidTrackingConsent("obce wskazanie zapisu zgody za dlugie")
    return slug, token, pointer
