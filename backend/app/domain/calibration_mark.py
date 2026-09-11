import re

from app.domain.errors import InvalidCalibrationMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ready", "pending"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://calibration-mark/"
_REF_CAP = 256


def parse_calibration_mark_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCalibrationMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCalibrationMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCalibrationMark("gotowość musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCalibrationMark("gotowość: ready albo pending")
    if type(origin) is not str:
        raise InvalidCalibrationMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCalibrationMark("obce wskazanie zapisu znacznika kalibracji")
    if len(pointer) > _REF_CAP:
        raise InvalidCalibrationMark("obce wskazanie zapisu znacznika kalibracji za długie")
    return slug, token, pointer
