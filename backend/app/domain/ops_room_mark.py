import re

from app.domain.errors import InvalidOpsRoomMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"shift", "board", "escalation", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://ops-room-mark/"
_REF_CAP = 256


def parse_ops_room_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidOpsRoomMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidOpsRoomMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidOpsRoomMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidOpsRoomMark(
            "rodzaj: shift, board, escalation albo other",
        )
    if type(origin) is not str:
        raise InvalidOpsRoomMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidOpsRoomMark(
            "obce wskazanie zapisu warstwy sali operacyjnej",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidOpsRoomMark(
            "obce wskazanie zapisu warstwy sali operacyjnej za dlugie",
        )
    return slug, token, pointer
